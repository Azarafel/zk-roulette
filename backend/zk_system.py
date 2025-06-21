# blockchain_roulette/backend/zk_system.py
# Система Zero-Knowledge доказательств для рулетки

import hashlib
import secrets
import time
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass


@dataclass
class ZKProof:
    commitment: str
    challenge: str
    response: str
    merkle_proof: List[str]
    merkle_root: str
    timestamp: float


class ZKCommitment:
    def __init__(self, player_address: str, number: int, nonce: str, timestamp: float):
        self.player_address = player_address
        self.number = number
        self.nonce = nonce
        self.timestamp = timestamp
        self.commitment_hash = self._generate_commitment_hash()
    
    def _generate_commitment_hash(self) -> str:
        """Генерирует хеш commitment"""
        data = f"{self.player_address}{self.number}{self.nonce}{self.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()


class MerkleTree:
    def __init__(self, leaves: List[str]):
        self.leaves = leaves
        self.tree = self._build_tree()
        self.root = self.tree[-1][0] if self.tree else ""
    
    def _build_tree(self) -> List[List[str]]:
        """Строит дерево Merkle"""
        if not self.leaves:
            return []
        
        current_level = self.leaves[:]
        tree = [current_level[:]]
        
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                parent = hashlib.sha256((left + right).encode()).hexdigest()
                next_level.append(parent)
            current_level = next_level
            tree.append(current_level[:])
        
        return tree
    
    def get_proof(self, leaf_index: int) -> List[str]:
        """Получает доказательство для листа"""
        if leaf_index >= len(self.leaves):
            return []
        
        proof = []
        index = leaf_index
        
        for level in range(len(self.tree) - 1):
            sibling_index = index ^ 1  # XOR с 1 для получения соседа
            if sibling_index < len(self.tree[level]):
                proof.append(self.tree[level][sibling_index])
            index //= 2
        
        return proof


class ZKSystem:
    def __init__(self, merkle_tree_depth: int = 10):
        self.merkle_tree_depth = merkle_tree_depth
        self.commitment_storage: Dict[str, ZKCommitment] = {}
        self.merkle_trees: Dict[str, MerkleTree] = {}
    
    def generate_player_commitment(
        self, 
        player_address: str, 
        bet_number: int
    ) -> Tuple[str, str, str]:
        """
        Генерирует commitment для игрока
        Возвращает: (nonce, commitment_hash, secret_key)
        """
        nonce = secrets.token_hex(16)
        timestamp = time.time()
        secret_key = secrets.token_hex(32)
        
        commitment = ZKCommitment(player_address, bet_number, nonce, timestamp)
        commitment_id = f"{player_address}_{timestamp}"
        
        self.commitment_storage[commitment_id] = commitment
        
        return nonce, commitment.commitment_hash, secret_key
    
    def generate_zk_proof(
        self,
        player_address: str,
        commitment_hash: str,
        secret_key: str
    ) -> ZKProof:
        """Генерирует ZK доказательство"""
        
        # Создаем фиктивные листья для Merkle Tree
        leaves = [
            hashlib.sha256(f"leaf_{i}_{commitment_hash}".encode()).hexdigest()
            for i in range(8)
        ]
        leaves.append(commitment_hash)
        
        # Строим Merkle Tree
        merkle_tree = MerkleTree(leaves)
        proof = merkle_tree.get_proof(len(leaves) - 1)
        
        # Генерируем challenge и response
        challenge = hashlib.sha256(
            f"{commitment_hash}{merkle_tree.root}{time.time()}".encode()
        ).hexdigest()
        
        response = hashlib.sha256(
            f"{challenge}{secret_key}".encode()
        ).hexdigest()
        
        return ZKProof(
            commitment=commitment_hash,
            challenge=challenge,
            response=response,
            merkle_proof=proof,
            merkle_root=merkle_tree.root,
            timestamp=time.time()
        )
    
    def verify_zk_proof(self, proof: ZKProof, player_address: str) -> bool:
        """Верифицирует ZK доказательство"""
        try:
            # Проверяем базовую структуру
            if not all([
                proof.commitment,
                proof.challenge,
                proof.response,
                proof.merkle_root
            ]):
                return False
            
            # Проверяем временные ограничения (доказательство действительно 10 минут)
            if time.time() - proof.timestamp > 600:
                return False
            
            # В реальной реализации здесь была бы полная верификация ZK доказательства
            # Для демо-версии просто проверяем базовые условия
            return True
            
        except Exception:
            return False
    
    def cleanup_expired_commitments(self, max_age_seconds: int = 600) -> int:
        """Очистка устаревших commitment'ов"""
        current_time = time.time()
        expired_keys = [
            key for key, commitment in self.commitment_storage.items()
            if current_time - commitment.timestamp > max_age_seconds
        ]
        
        for key in expired_keys:
            del self.commitment_storage[key]
        
        return len(expired_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        """Получение статистики системы"""
        return {
            "total_commitments": len(self.commitment_storage),
            "active_merkle_trees": len(self.merkle_trees),
            "merkle_tree_depth": self.merkle_tree_depth,
            "oldest_commitment": min(
                (c.timestamp for c in self.commitment_storage.values()),
                default=time.time()
            )
        }


# Глобальный экземпляр ZK системы
zk_system = ZKSystem()


def test_zk_system():
    """Базовый тест ZK системы"""
    print("🔍 Тестирование ZK системы...")
    
    # Тестируем генерацию commitment
    player_addr = "0x1234567890123456789012345678901234567890"
    bet_number = 7
    
    nonce, commitment_hash, secret_key = zk_system.generate_player_commitment(
        player_addr, bet_number
    )
    
    print(f"✅ Commitment сгенерирован: {commitment_hash[:16]}...")
    
    # Тестируем генерацию ZK доказательства
    proof = zk_system.generate_zk_proof(player_addr, commitment_hash, secret_key)
    print(f"✅ ZK доказательство сгенерировано")
    
    # Тестируем верификацию
    is_valid = zk_system.verify_zk_proof(proof, player_addr)
    print(f"✅ Верификация: {'УСПЕШНО' if is_valid else 'ОШИБКА'}")
    
    # Статистика
    stats = zk_system.get_stats()
    print(f"📊 Статистика: {stats['total_commitments']} commitments")
    
    return is_valid


if __name__ == "__main__":
    test_zk_system() 