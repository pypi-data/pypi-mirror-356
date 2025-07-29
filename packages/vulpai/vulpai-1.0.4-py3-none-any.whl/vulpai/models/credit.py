from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional


@dataclass
class CreditInfo:
    """Informações sobre créditos do usuário"""
    
    total_credits: float
    used_credits: float
    available_credits: float
    monthly_limit: Optional[float]
    billing_cycle_start: datetime
    billing_cycle_end: datetime
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CreditInfo':
        return cls(
            total_credits=data['total_credits'],
            used_credits=data['used_credits'],
            available_credits=data['available_credits'],
            monthly_limit=data.get('monthly_limit'),
            billing_cycle_start=datetime.fromisoformat(data['billing_cycle_start']),
            billing_cycle_end=datetime.fromisoformat(data['billing_cycle_end'])
        )
    
    @property
    def usage_percentage(self) -> float:
        """Percentual de uso dos créditos"""
        if self.total_credits == 0:
            return 0.0
        return (self.used_credits / self.total_credits) * 100


@dataclass
class CreditUsage:
    """Registro de uso de créditos"""
    
    id: str
    amount: float
    operation_type: str  # 'validation', 'upload', 'consultation'
    artifact_id: Optional[str]
    validation_id: Optional[str]
    description: str
    created_at: datetime
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CreditUsage':
        return cls(
            id=data['id'],
            amount=data['amount'],
            operation_type=data['operation_type'],
            artifact_id=data.get('artifact_id'),
            validation_id=data.get('validation_id'),
            description=data['description'],
            created_at=datetime.fromisoformat(data['created_at'])
        )