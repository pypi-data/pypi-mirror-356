"""
VulpAI - Sistema de Validação de Modelos de IA
"""

__version__ = "1.0.3"
__author__ = "VulpAI Team"

from .client import VulpAIClient
from .models.artifact import Artifact, ArtifactType, ArtifactStatus
from .models.validation import ValidationConfig, ValidationResult
from .models.credit import CreditInfo, CreditUsage
from .exceptions import (
    VulpAIError,
    AuthenticationError,
    InsufficientCreditsError,
    ValidationError,
    UploadError
)

__all__ = [
    "VulpAIClient",
    "Artifact",
    "ArtifactType", 
    "ArtifactStatus",
    "ValidationConfig",
    "ValidationResult",
    "CreditInfo",
    "CreditUsage",
    "VulpAIError",
    "AuthenticationError",
    "InsufficientCreditsError",
    "ValidationError",
    "UploadError"
]