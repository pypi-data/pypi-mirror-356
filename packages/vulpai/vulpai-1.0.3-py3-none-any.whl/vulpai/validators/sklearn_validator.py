"""Validador para modelos Scikit-learn"""

from pathlib import Path
from typing import Dict, Any, Union
import pickle
import joblib
import logging

from .base import BaseValidator

logger = logging.getLogger(__name__)


class SklearnValidator(BaseValidator):
    """Validador para modelos Scikit-learn"""
    
    def can_validate(self, file_path: Union[str, Path]) -> bool:
        """Verifica se é um modelo sklearn"""
        file_path = Path(file_path)
        
        # Verificar extensão
        if file_path.suffix.lower() not in ['.pkl', '.pickle', '.joblib']:
            return False
        
        # Tentar carregar e verificar se é sklearn
        try:
            if file_path.suffix.lower() == '.joblib':
                model = joblib.load(file_path, mmap_mode='r')
            else:
                with open(file_path, 'rb') as f:
                    model = pickle.load(f)
            
            # Verificar se é modelo sklearn
            model_module = getattr(model, '__module__', '')
            return 'sklearn' in model_module or 'scikit' in model_module
            
        except Exception:
            return False
    
    def extract_metadata(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Extrai metadados do modelo sklearn"""
        file_path = Path(file_path)
        
        try:
            # Carregar modelo
            if file_path.suffix.lower() == '.joblib':
                model = joblib.load(file_path)
            else:
                with open(file_path, 'rb') as f:
                    model = pickle.load(f)
            
            metadata = {
                'model_type': type(model).__name__,
                'module': getattr(model, '__module__', 'unknown'),
                'sklearn_version': self._get_sklearn_version(model)
            }
            
            # Extrair parâmetros do modelo
            if hasattr(model, 'get_params'):
                metadata['parameters'] = model.get_params()
            
            # Para pipelines
            if hasattr(model, 'steps'):
                metadata['pipeline_steps'] = [
                    (name, type(estimator).__name__) 
                    for name, estimator in model.steps
                ]
            
            # Features
            if hasattr(model, 'n_features_in_'):
                metadata['n_features'] = model.n_features_in_
            
            if hasattr(model, 'feature_names_in_'):
                metadata['feature_names'] = list(model.feature_names_in_)
            
            # Classes (para classificadores)
            if hasattr(model, 'classes_'):
                metadata['classes'] = list(model.classes_)
                metadata['n_classes'] = len(model.classes_)
            
            return metadata
            
        except Exception as e:
            logger.error(f"Erro ao extrair metadados: {e}")
            return {'error': str(e)}
    
    def validate_structure(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Valida estrutura do modelo sklearn"""
        file_path = Path(file_path)
        
        try:
            # Carregar modelo
            if file_path.suffix.lower() == '.joblib':
                model = joblib.load(file_path)
            else:
                with open(file_path, 'rb') as f:
                    model = pickle.load(f)
            
            validation = {
                'valid': True,
                'is_fitted': self._check_is_fitted(model),
                'has_predict': hasattr(model, 'predict'),
                'has_predict_proba': hasattr(model, 'predict_proba'),
                'has_transform': hasattr(model, 'transform')
            }
            
            # Verificações adicionais
            if hasattr(model, 'steps'):  # Pipeline
                validation['is_pipeline'] = True
                validation['n_steps'] = len(model.steps)
            
            return validation
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    def get_framework_name(self) -> str:
        return "scikit-learn"
    
    def _get_sklearn_version(self, model) -> str:
        """Tenta obter versão do sklearn"""
        try:
            import sklearn
            return sklearn.__version__
        except:
            return "unknown"
    
    def _check_is_fitted(self, model) -> bool:
        """Verifica se o modelo está treinado"""
        try:
            # Verificar atributos comuns de modelos treinados
            fitted_attrs = [
                'coef_', 'intercept_', 'support_vectors_',
                'tree_', 'components_', 'cluster_centers_'
            ]
            
            for attr in fitted_attrs:
                if hasattr(model, attr):
                    return True
            
            # Para pipelines
            if hasattr(model, 'steps'):
                return all(
                    self._check_is_fitted(estimator) 
                    for _, estimator in model.steps
                )
            
            return False
            
        except:
            return False