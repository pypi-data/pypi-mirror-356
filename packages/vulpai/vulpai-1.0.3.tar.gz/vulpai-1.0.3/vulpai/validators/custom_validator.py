"""Validador customizado para outros tipos de modelos"""

from pathlib import Path
from typing import Dict, Any, Union
import json
import logging

from .base import BaseValidator

logger = logging.getLogger(__name__)


class CustomValidator(BaseValidator):
    """Validador genérico para modelos customizados"""
    
    def can_validate(self, file_path: Union[str, Path]) -> bool:
        """Sempre pode validar (fallback)"""
        return True
    
    def extract_metadata(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Extrai metadados básicos do arquivo"""
        file_path = Path(file_path)
        
        metadata = {
            'file_extension': file_path.suffix,
            'file_size_bytes': file_path.stat().st_size,
            'file_size_mb': file_path.stat().st_size / (1024 * 1024)
        }
        
        # Tentar ler como JSON
        if file_path.suffix.lower() == '.json':
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        metadata['json_keys'] = list(data.keys())
                        metadata['json_type'] = 'object'
                    elif isinstance(data, list):
                        metadata['json_type'] = 'array'
                        metadata['json_length'] = len(data)
            except Exception as e:
                logger.warning(f"Não foi possível ler JSON: {e}")
        
        # Verificar se é ONNX
        elif file_path.suffix.lower() == '.onnx':
            metadata['format'] = 'ONNX'
            metadata['framework'] = 'ONNX Runtime'
        
        return metadata
    
    def validate_structure(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Validação básica de estrutura"""
        file_path = Path(file_path)
        
        validation = {
            'valid': True,
            'file_exists': file_path.exists(),
            'is_file': file_path.is_file(),
            'readable': file_path.exists() and file_path.is_file()
        }
        
        # Validação específica para ONNX
        if file_path.suffix.lower() == '.onnx':
            try:
                import onnx
                model = onnx.load(str(file_path))
                onnx.checker.check_model(model)
                validation['onnx_valid'] = True
            except Exception as e:
                validation['onnx_valid'] = False
                validation['onnx_error'] = str(e)
        
        return validation
    
    def get_framework_name(self) -> str:
        return "Custom/Unknown"