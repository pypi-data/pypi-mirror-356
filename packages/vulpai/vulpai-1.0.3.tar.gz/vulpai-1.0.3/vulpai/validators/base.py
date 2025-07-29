"""Base class para validadores de modelos"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Union, Optional
import logging

logger = logging.getLogger(__name__)


class BaseValidator(ABC):
    """Classe base para validação de modelos"""
    
    @abstractmethod
    def can_validate(self, file_path: Union[str, Path]) -> bool:
        """Verifica se pode validar este tipo de arquivo"""
        pass
    
    @abstractmethod
    def extract_metadata(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Extrai metadados do modelo"""
        pass
    
    @abstractmethod
    def validate_structure(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Valida estrutura do modelo"""
        pass
    
    def get_model_info(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Obtém informações completas do modelo
        
        Returns:
            Dict com informações do modelo
        """
        file_path = Path(file_path)
        
        info = {
            'file_name': file_path.name,
            'file_size': file_path.stat().st_size,
            'framework': self.get_framework_name()
        }
        
        # Adicionar metadados
        try:
            metadata = self.extract_metadata(file_path)
            info['metadata'] = metadata
        except Exception as e:
            logger.warning(f"Não foi possível extrair metadados: {e}")
            info['metadata'] = {}
        
        # Validar estrutura
        try:
            validation = self.validate_structure(file_path)
            info['validation'] = validation
        except Exception as e:
            logger.warning(f"Não foi possível validar estrutura: {e}")
            info['validation'] = {'valid': False, 'error': str(e)}
        
        return info
    
    @abstractmethod
    def get_framework_name(self) -> str:
        """Retorna nome do framework"""
        pass


def get_validator(file_path: Union[str, Path]) -> BaseValidator:
    """
    Retorna o validador apropriado para o arquivo
    
    Args:
        file_path: Caminho do arquivo
        
    Returns:
        BaseValidator: Validador apropriado
    """
    from .sklearn_validator import SklearnValidator
    from .pytorch_validator import PyTorchValidator
    from .tensorflow_validator import TensorFlowValidator
    from .custom_validator import CustomValidator
    
    validators = [
        SklearnValidator(),
        PyTorchValidator(),
        TensorFlowValidator(),
    ]
    
    for validator in validators:
        if validator.can_validate(file_path):
            return validator
    
    # Fallback para validador customizado
    return CustomValidator()