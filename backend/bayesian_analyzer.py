# blockchain_roulette/backend/bayesian_analyzer.py
# Байесовский анализатор для детекции махинаций в рулетке

import numpy as np
from scipy.stats import beta
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class SuspiciousEvent:
    player_address: str
    event_type: str
    severity: float
    description: str
    probability_score: float
    timestamp: datetime


@dataclass 
class PlayerProfile:
    address: str
    total_bets: int
    wins: int
    total_amount: float
    profit_loss: float
    risk_score: float
    win_rate: float
    is_blacklisted: bool
    last_activity: datetime
    bet_patterns: Dict[str, Any]


class BayesianAnalyzer:
    def __init__(self):
        # Байесовские параметры для каждого числа (0-36)
        self.alpha_params = {i: 1.0 for i in range(37)}  # Успехи + 1
        self.beta_params = {i: 36.0 for i in range(37)}  # Неудачи + 36
        
        # Профили игроков
        self.player_profiles: Dict[str, PlayerProfile] = {}
        
        # Подозрительные события
        self.suspicious_events: List[SuspiciousEvent] = []
        
        # Статистика чисел
        self.number_frequencies: Dict[int, int] = {i: 0 for i in range(37)}
        
        # Настройки детекции
        self.suspicious_threshold = 0.8
        self.blacklist_threshold = 0.9
    
    def get_bayesian_probability_distribution(self, number: int) -> Dict[str, float]:
        """Получает байесовское распределение вероятности для числа"""
        if not 0 <= number <= 36:
            raise ValueError("Number must be between 0 and 36")
        
        alpha = self.alpha_params[number]
        beta_param = self.beta_params[number]
        
        # Создаем Beta-распределение
        distribution = beta(alpha, beta_param)
        
        mean = distribution.mean()
        var = distribution.var()
        
        # Доверительные интервалы
        ci_95 = distribution.interval(0.95)
        ci_99 = distribution.interval(0.99)
        
        return {
            'mean': mean,
            'variance': var,
            'alpha': alpha,
            'beta': beta_param,
            'observations': alpha + beta_param - 37,
            'ci_95_lower': ci_95[0],
            'ci_95_upper': ci_95[1],
            'ci_99_lower': ci_99[0],
            'ci_99_upper': ci_99[1]
        }
    
    def update_player_stats(self, player_address: str, bet_data: Dict[str, Any]):
        """Обновляет статистику игрока"""
        if player_address not in self.player_profiles:
            self.player_profiles[player_address] = PlayerProfile(
                address=player_address,
                total_bets=0,
                wins=0,
                total_amount=0.0,
                profit_loss=0.0,
                risk_score=0.0,
                win_rate=0.0,
                is_blacklisted=False,
                last_activity=datetime.now(),
                bet_patterns={}
            )
        
        profile = self.player_profiles[player_address]
        profile.total_bets += 1
        profile.total_amount += bet_data.get('amount', 0)
        profile.last_activity = datetime.now()
        
        # Проверяем выигрыш
        if bet_data.get('won', False):
            profile.wins += 1
            payout = bet_data.get('payout', 0)
            profile.profit_loss += payout - bet_data.get('amount', 0)
        else:
            profile.profit_loss -= bet_data.get('amount', 0)
        
        # Обновляем процент побед
        profile.win_rate = profile.wins / profile.total_bets if profile.total_bets > 0 else 0
        profile.risk_score = profile.win_rate * 2  # Упрощенный расчет риска
    
    def get_player_risk_assessment(self, player_address: str) -> Dict[str, Any]:
        """Получает оценку риска для игрока"""
        if player_address not in self.player_profiles:
            return {"error": "Player not found"}
        
        profile = self.player_profiles[player_address]
        
        # Определяем уровень риска
        if profile.risk_score < 0.3:
            risk_level = "LOW"
            recommendation = "Игрок не представляет риска"
        elif profile.risk_score < 0.6:
            risk_level = "MEDIUM"
            recommendation = "Рекомендуется наблюдение"
        else:
            risk_level = "HIGH"
            recommendation = "Требуется пристальное внимание"
        
        return {
            "player_profile": {
                "risk_score": profile.risk_score,
                "total_bets": profile.total_bets,
                "win_rate": profile.win_rate,
                "is_blacklisted": profile.is_blacklisted
            },
            "risk_level": risk_level,
            "recommendation": recommendation,
            "total_suspicious_events": 0,
            "recent_events": []
        }
    
    def export_analytics_report(self) -> Dict[str, Any]:
        """Экспортирует аналитический отчет"""
        return {
            "summary": {
                "total_players": len(self.player_profiles),
                "total_spins": sum(self.number_frequencies.values()),
                "high_risk_players": 0,
                "suspicious_events_24h": 0
            }
        }


# Глобальный экземпляр анализатора
bayesian_analyzer = BayesianAnalyzer() 