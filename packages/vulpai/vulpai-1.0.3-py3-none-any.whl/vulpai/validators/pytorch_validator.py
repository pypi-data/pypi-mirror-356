"""Validador para modelos PyTorch"""

from pathlib import Path
from typing import Dict, Any, Union
import logging

from .base import BaseValidator

logger = logging.getLogger(__name__)


class PyTorchValidator(BaseValidator):
    """Validador para modelos PyTorch"""
    
    def can_validate(self, file_path: Union[str, Path]) -> bool:
        """Verifica se é um modelo PyTorch"""
        file_path = Path(file_path)
        
        # Verificar extensão
        if file_path.suffix.lower() not in ['.pt', '.pth']:
            return False
        
        try:
            import torch
            # Tentar carregar apenas metadados
            checkpoint = torch.load(file_path, map_location='cpu', weights_only=False)
            return True
        except Exception:
            return False
    
    def extract_metadata(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Extrai metadados do modelo PyTorch"""
        file_path = Path(file_path)
        
        try:
            import torch
            
            # Carregar checkpoint
            checkpoint = torch.load(file_path, map_location='cpu', weights_only=False)
            
            metadata = {
                'pytorch_version': torch.__version__,
                'checkpoint_type': self._detect_checkpoint_type(checkpoint)
            }
            
            # Se for state_dict
            if isinstance(checkpoint, dict):
                if 'model_state_dict' in checkpoint:
                    metadata['has_model_state'] = True
                    metadata['n_parameters'] = len(checkpoint['model_state_dict'])
                
                if 'optimizer_state_dict' in checkpoint:
                    metadata['has_optimizer_state'] = True
                
                if 'epoch' in checkpoint:
                    metadata['epoch'] = checkpoint['epoch']
                
                if 'loss' in checkpoint:
                    metadata['loss'] = checkpoint['loss']
                
                # Outras chaves úteis
                useful_keys = ['accuracy', 'best_accuracy', 'config', 'args']
                for key in useful_keys:
                    if key in checkpoint:
                        metadata[key] = checkpoint[key]
            
            # Se for modelo completo
            elif hasattr(checkpoint, 'state_dict'):
                metadata['model_class'] = type(checkpoint).__name__
                metadata['n_parameters'] = sum(
                    p.numel() for p in checkpoint.parameters()
                )
            
            return metadata
            
        except Exception as e:
            logger.error(f"Erro ao extrair metadados: {e}")
            return {'error': str(e)}
    
    def validate_structure(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Valida estrutura do modelo PyTorch"""
        file_path = Path(file_path)
        
        try:
            import torch
            
            checkpoint = torch.load(file_path, map_location='cpu', weights_only=False)
            
            validation = {
                'valid': True,
                'file_type': 'pytorch_checkpoint'
            }
            
            if isinstance(checkpoint, dict):
                validation['is_state_dict'] = True
                validation['keys'] = list(checkpoint.keys())
            elif hasattr(checkpoint, 'forward'):
                validation['is_complete_model'] = True
                validation['has_forward'] = True
            
            return validation
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    def get_framework_name(self) -> str:
        return "PyTorch"
    
    def _detect_checkpoint_type(self, checkpoint) -> str:
        """Detecta tipo de checkpoint"""
        if isinstance(checkpoint, dict):
            if 'model_state_dict' in checkpoint:
                return 'training_checkpoint'
            elif any(key.endswith('.weight') or key.endswith('.bias') for key in checkpoint.keys()):
                return 'state_dict'
            else:
                return 'custom_dict'
        else:
            return 'complete_model'