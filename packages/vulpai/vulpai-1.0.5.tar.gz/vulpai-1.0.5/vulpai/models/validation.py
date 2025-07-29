from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any


class ValidationStatus(Enum):
    """Status de uma validação"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ValidationLevel(Enum):
    """Níveis de validação disponíveis"""
    BASIC = "basic"
    STANDARD = "standard"
    ADVANCED = "advanced"
    CUSTOM = "custom"


@dataclass
class ValidationConfig:
    """Configuração para validação de modelos"""
    
    validation_level: ValidationLevel = ValidationLevel.STANDARD
    test_split: float = 0.2
    cross_validation_folds: Optional[int] = None
    metrics: List[str] = field(default_factory=lambda: ['accuracy', 'precision', 'recall', 'f1'])
    custom_tests: Optional[Dict[str, Any]] = None
    dataset_id: Optional[str] = None
    max_runtime_minutes: int = 60
    generate_explanations: bool = True
    generate_visualizations: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'validation_level': self.validation_level.value,
            'test_split': self.test_split,
            'cross_validation_folds': self.cross_validation_folds,
            'metrics': self.metrics,
            'custom_tests': self.custom_tests,
            'dataset_id': self.dataset_id,
            'max_runtime_minutes': self.max_runtime_minutes,
            'generate_explanations': self.generate_explanations,
            'generate_visualizations': self.generate_visualizations
        }


@dataclass
class ValidationResult:
    """Resultado de uma validação"""
    
    validation_id: str
    artifact_id: str
    status: ValidationStatus
    started_at: datetime
    completed_at: Optional[datetime]
    duration_seconds: Optional[int]
    
    # Resultados da validação
    metrics: Dict[str, float] = field(default_factory=dict)
    test_results: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    issues: List[Dict[str, Any]] = field(default_factory=list)
    
    # Arquivos gerados
    report_url: Optional[str] = None
    visualization_urls: List[str] = field(default_factory=list)
    
    # Metadados
    validation_config: Optional[ValidationConfig] = None
    claude_analysis: Optional[Dict[str, Any]] = None
    credits_used: float = 0.0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ValidationResult':
        validation_config = None
        if data.get('validation_config'):
            validation_config = ValidationConfig(**data['validation_config'])
            
        return cls(
            validation_id=data['validation_id'],
            artifact_id=data['artifact_id'],
            status=ValidationStatus(data['status']),
            started_at=datetime.fromisoformat(data['started_at']),
            completed_at=datetime.fromisoformat(data['completed_at']) if data.get('completed_at') else None,
            duration_seconds=data.get('duration_seconds'),
            metrics=data.get('metrics', {}),
            test_results=data.get('test_results', {}),
            recommendations=data.get('recommendations', []),
            issues=data.get('issues', []),
            report_url=data.get('report_url'),
            visualization_urls=data.get('visualization_urls', []),
            validation_config=validation_config,
            claude_analysis=data.get('claude_analysis'),
            credits_used=data.get('credits_used', 0.0)
        )
    
    @property
    def is_successful(self) -> bool:
        """Verifica se a validação foi bem-sucedida"""
        return self.status == ValidationStatus.COMPLETED
    
    @property
    def has_issues(self) -> bool:
        """Verifica se foram encontrados problemas"""
        return len(self.issues) > 0