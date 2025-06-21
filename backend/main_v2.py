from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, validator
from web3 import Web3
import json
import os
from dotenv import load_dotenv
import numpy as np
from scipy.stats import beta
import secrets
import hashlib
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
from contextlib import asynccontextmanager

# Импортируем наши модули
from zk_system import zk_system, ZKProof
from bayesian_analyzer import bayesian_analyzer, SuspiciousEvent

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

# Инициализация безопасности
security = HTTPBearer()

class ConfigSettings:
    """Настройки конфигурации"""
    WEB3_PROVIDER_URI = os.getenv("WEB3_PROVIDER_URI", "http://localhost:8545")
    CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
    ADMIN_ADDRESS = os.getenv("ADMIN_ADDRESS")
    SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))
    MAX_BETS_PER_HOUR = int(os.getenv("MAX_BETS_PER_HOUR", "50"))
    MIN_BET_AMOUNT = float(os.getenv("MIN_BET_AMOUNT", "0.001"))
    MAX_BET_AMOUNT = float(os.getenv("MAX_BET_AMOUNT", "10.0"))

config = ConfigSettings()

# Инициализация Web3
try:
    w3 = Web3(Web3.HTTPProvider(config.WEB3_PROVIDER_URI))
    if not w3.is_connected():
        logger.error("Failed to connect to Web3 provider")
        raise Exception("Web3 connection failed")
except Exception as e:
    logger.error(f"Web3 initialization error: {e}")
    w3 = None

# Загрузка контракта
if w3 and config.CONTRACT_ADDRESS:
    try:
        with open("../contracts/ZKRouletteV2.json") as f:
            contract_json = json.load(f)
        CONTRACT_ABI = contract_json["abi"]
        contract = w3.eth.contract(address=config.CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    except Exception as e:
        logger.error(f"Contract loading error: {e}")
        contract = None
else:
    contract = None

# Хранилище для rate limiting и сессий
player_sessions: Dict[str, Dict[str, Any]] = {}
rate_limits: Dict[str, List[datetime]] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    logger.info("🚀 Запуск ZK-Roulette API...")
    
    # Инициализация фоновых задач
    cleanup_task = asyncio.create_task(periodic_cleanup())
    
    yield
    
    # Очистка при выключении
    cleanup_task.cancel()
    logger.info("🛑 Остановка ZK-Roulette API...")

app = FastAPI(
    title="ZK-Roulette API v2",
    description="Продвинутая блокчейн рулетка с Zero-Knowledge Proof и байесовской аналитикой",
    version="2.0.0",
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============== МОДЕЛИ ДАННЫХ ===============

class PlayerAuthRequest(BaseModel):
    wallet_address: str = Field(..., regex=r"^0x[a-fA-F0-9]{40}$")
    signature: str = Field(..., min_length=132, max_length=132)
    message: str

class BetRequest(BaseModel):
    number: int = Field(..., ge=0, le=36, description="Номер от 0 до 36")
    amount: float = Field(..., gt=0, description="Размер ставки в ETH")
    player_address: str = Field(..., regex=r"^0x[a-fA-F0-9]{40}$")
    
    @validator('amount')
    def validate_amount(cls, v):
        if v < config.MIN_BET_AMOUNT:
            raise ValueError(f'Минимальная ставка: {config.MIN_BET_AMOUNT} ETH')
        if v > config.MAX_BET_AMOUNT:
            raise ValueError(f'Максимальная ставка: {config.MAX_BET_AMOUNT} ETH')
        return v

class ZKProofResponse(BaseModel):
    zk_proof: Dict[str, Any]
    transaction_data: Dict[str, Any]
    session_id: str

class BayesianStatsResponse(BaseModel):
    number: int
    probability: float
    confidence: float
    confidence_interval_95: List[float]
    confidence_interval_99: List[float]
    total_observations: int
    deviation_score: float

class PlayerRiskResponse(BaseModel):
    risk_level: str
    risk_score: float
    total_bets: int
    win_rate: float
    suspicious_events_count: int
    recommendation: str
    is_blacklisted: bool

class AnalyticsResponse(BaseModel):
    total_players: int
    total_spins: int
    house_edge_actual: float
    high_risk_players: int
    recent_suspicious_events: int
    top_numbers: List[Dict[str, Any]]
    system_health: Dict[str, Any]

# =============== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===============

async def check_rate_limit(player_address: str) -> bool:
    """Проверка rate limiting"""
    now = datetime.now()
    hour_ago = now - timedelta(hours=1)
    
    if player_address not in rate_limits:
        rate_limits[player_address] = []
    
    # Удаляем старые записи
    rate_limits[player_address] = [
        timestamp for timestamp in rate_limits[player_address]
        if timestamp > hour_ago
    ]
    
    # Проверяем лимит
    if len(rate_limits[player_address]) >= config.MAX_BETS_PER_HOUR:
        return False
    
    rate_limits[player_address].append(now)
    return True

def verify_player_signature(address: str, signature: str, message: str) -> bool:
    """Верификация подписи игрока"""
    try:
        # Восстанавливаем адрес из подписи
        message_hash = hashlib.sha3_256(message.encode()).digest()
        recovered_address = w3.eth.account.recover_message(
            message_hash, signature=signature
        )
        return recovered_address.lower() == address.lower()
    except Exception as e:
        logger.error(f"Signature verification error: {e}")
        return False

async def get_player_session(player_address: str) -> Dict[str, Any]:
    """Получение или создание сессии игрока"""
    if player_address not in player_sessions:
        player_sessions[player_address] = {
            'created_at': datetime.now(),
            'last_activity': datetime.now(),
            'bets_count': 0,
            'session_id': secrets.token_hex(16)
        }
    
    player_sessions[player_address]['last_activity'] = datetime.now()
    return player_sessions[player_address]

async def periodic_cleanup():
    """Периодическая очистка устаревших данных"""
    while True:
        try:
            # Очистка устаревших ZK commitments
            expired_count = zk_system.cleanup_expired_commitments(600)  # 10 минут
            if expired_count > 0:
                logger.info(f"Очищено {expired_count} устаревших ZK commitments")
            
            # Очистка старых сессий (старше 24 часов)
            now = datetime.now()
            old_sessions = [
                addr for addr, session in player_sessions.items()
                if now - session['last_activity'] > timedelta(hours=24)
            ]
            
            for addr in old_sessions:
                del player_sessions[addr]
            
            if old_sessions:
                logger.info(f"Очищено {len(old_sessions)} старых сессий")
            
            await asyncio.sleep(300)  # Каждые 5 минут
            
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
            await asyncio.sleep(60)

# =============== ЭНДПОИНТЫ API ===============

@app.post("/auth/player", response_model=Dict[str, str])
async def authenticate_player(auth_request: PlayerAuthRequest):
    """
    Аутентификация игрока через подпись кошелька
    """
    try:
        # Проверяем подпись
        if not verify_player_signature(
            auth_request.wallet_address,
            auth_request.signature,
            auth_request.message
        ):
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        # Создаем сессию
        session = await get_player_session(auth_request.wallet_address)
        
        return {
            "status": "authenticated",
            "session_id": session['session_id'],
            "player_address": auth_request.wallet_address
        }
        
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(status_code=500, detail="Authentication failed")

@app.post("/bet/prepare", response_model=ZKProofResponse)
async def prepare_bet(bet_request: BetRequest):
    """
    Подготовка ставки с генерацией ZK доказательства
    """
    try:
        # Проверка rate limiting
        if not await check_rate_limit(bet_request.player_address):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        # Проверка блокировки игрока
        player_stats = bayesian_analyzer.player_profiles.get(bet_request.player_address)
        if player_stats and player_stats.risk_score > 0.8:
            raise HTTPException(status_code=403, detail="Player temporarily suspended")
        
        # Генерация ZK commitment
        nonce, commitment_hash, secret_key = zk_system.generate_player_commitment(
            bet_request.player_address,
            bet_request.number
        )
        
        # Генерация ZK доказательства
        zk_proof = zk_system.generate_zk_proof(
            bet_request.player_address,
            commitment_hash,
            secret_key
        )
        
        # Подготовка транзакции
        if not contract:
            # Фиктивная транзакция для тестирования
            txn = {
                'to': '0x' + '0' * 40,
                'value': int(bet_request.amount * 10**18),
                'gas': 300000,
                'gasPrice': 20000000000,
                'nonce': 0,
                'data': '0x' + bet_request.number.to_bytes(32, byteorder='big').hex()
            }
        else:
            nonce_tx = w3.eth.get_transaction_count(bet_request.player_address)
            
            # Конвертируем ZK proof в формат для смарт-контракта
            merkle_proof_bytes = [bytes.fromhex(proof[2:]) if proof.startswith('0x') else bytes.fromhex(proof) 
                                 for proof in zk_proof.merkle_proof]
            
            txn = contract.functions.placeBet(
                bet_request.number,
                bytes.fromhex(zk_proof.commitment[2:] if zk_proof.commitment.startswith('0x') 
                             else zk_proof.commitment),
                merkle_proof_bytes,
                bytes.fromhex(zk_proof.merkle_root[2:] if zk_proof.merkle_root.startswith('0x') 
                             else zk_proof.merkle_root)
            ).build_transaction({
                'from': bet_request.player_address,
                'value': w3.to_wei(bet_request.amount, 'ether'),
                'gas': 300000,
                'gasPrice': w3.eth.gas_price,
                'nonce': nonce_tx,
            })
        
        # Получаем сессию игрока
        session = await get_player_session(bet_request.player_address)
        session['bets_count'] += 1
        
        return ZKProofResponse(
            zk_proof={
                'commitment': zk_proof.commitment,
                'challenge': zk_proof.challenge,
                'response': zk_proof.response,
                'merkle_proof': zk_proof.merkle_proof,
                'merkle_root': zk_proof.merkle_root,
                'timestamp': zk_proof.timestamp
            },
            transaction_data=txn,
            session_id=session['session_id']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Bet preparation error: {e}")
        raise HTTPException(status_code=500, detail="Bet preparation failed")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "web3_connected": w3.is_connected() if w3 else False,
        "contract_loaded": contract is not None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main_v2:app",
        host="localhost",
        port=8000,
        reload=True,
        log_level="info"
    ) 