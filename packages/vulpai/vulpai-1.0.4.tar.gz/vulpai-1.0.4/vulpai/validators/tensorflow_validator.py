"""Validador para modelos TensorFlow/Keras"""

from pathlib import Path
from typing import Dict, Any, Union
import logging

from .base import BaseValidator

logger = logging.getLogger(__name__)


class TensorFlowValidator(BaseValidator):
    """Validador para modelos TensorFlow/Keras"""
    
    def can_validate(self, file_path: Union[str, Path]) -> bool:
        """Verifica se é um modelo TensorFlow/Keras"""
        file_path = Path(file_path)
        
        # Verificar extensão
        if file_path.suffix.lower() in ['.h5', '.hdf5']:
            return True
        
        # Verificar se é SavedModel (diretório)
        if file_path.is_dir():
            return (file_path / 'saved_model.pb').exists()
        
        return file_path.suffix.lower() == '.pb'
    
    def extract_metadata(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Extrai metadados do modelo TensorFlow/Keras"""
        file_path = Path(file_path)
        
        try:
            import tensorflow as tf
            
            metadata = {
                'tensorflow_version': tf.__version__,
                'keras_version': tf.keras.__version__
            }
            
            # H5/HDF5 (Keras)
            if file_path.suffix.lower() in ['.h5', '.hdf5']:
                model = tf.keras.models.load_model(file_path, compile=False)
                metadata.update(self._extract_keras_metadata(model))
            
            # SavedModel
            elif file_path.is_dir() or file_path.suffix.lower() == '.pb':
                model = tf.saved_model.load(str(file_path))
                metadata['format'] = 'saved_model'
                metadata['signatures'] = list(model.signatures.keys()) if hasattr(model, 'signatures') else []
            
            return metadata
            
        except Exception as e:
            logger.error(f"Erro ao extrair metadados: {e}")
            return {'error': str(e)}
    
    def validate_structure(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Valida estrutura do modelo TensorFlow/Keras"""
        file_path = Path(file_path)
        
        try:
            import tensorflow as tf
            
            validation = {
                'valid': True,
                'file_type': 'tensorflow_model'
            }
            
            # H5/HDF5
            if file_path.suffix.lower() in ['.h5', '.hdf5']:
                try:
                    model = tf.keras.models.load_model(file_path, compile=False)
                    validation['format'] = 'keras_h5'
                    validation['is_sequential'] = isinstance(model, tf.keras.Sequential)
                    validation['n_layers'] = len(model.layers)
                except:
                    validation['valid'] = False
            
            # SavedModel
            elif file_path.is_dir():
                validation['format'] = 'saved_model'
                validation['has_pb'] = (file_path / 'saved_model.pb').exists()
                validation['has_variables'] = (file_path / 'variables').exists()
            
            return validation
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    def get_framework_name(self) -> str:
        return "TensorFlow"
    
    def _extract_keras_metadata(self, model) -> Dict[str, Any]:
        """Extrai metadados específicos do Keras"""
        metadata = {
            'model_name': model.name,
            'n_layers': len(model.layers),
            'n_parameters': model.count_params(),
            'input_shape': str(model.input_shape) if hasattr(model, 'input_shape') else None,
            'output_shape': str(model.output_shape) if hasattr(model, 'output_shape') else None
        }
        
        # Configuração do modelo
        if hasattr(model, 'optimizer') and model.optimizer:
            metadata['optimizer'] = type(model.optimizer).__name__
        
        if hasattr(model, 'loss'):
            metadata['loss'] = str(model.loss)
        
        # Tipos de camadas
        layer_types = {}
        for layer in model.layers:
            layer_type = type(layer).__name__
            layer_types[layer_type] = layer_types.get(layer_type, 0) + 1
        metadata['layer_types'] = layer_types
        
        return metadata