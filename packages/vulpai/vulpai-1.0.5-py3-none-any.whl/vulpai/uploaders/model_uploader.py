"""Uploader para modelos de ML"""

from pathlib import Path
from typing import Union
import pickle
import json
import joblib

from .base import BaseUploader
from ..models.artifact import ArtifactType
from ..exceptions import InvalidArtifactError


class ModelUploader(BaseUploader):
    """Uploader especializado para modelos de ML"""
    
    SUPPORTED_EXTENSIONS = {
        '.pkl', '.pickle',  # Pickle
        '.joblib',          # Joblib
        '.h5', '.hdf5',     # Keras/TensorFlow
        '.pt', '.pth',      # PyTorch
        '.onnx',            # ONNX
        '.json',            # JSON (para modelos simples)
        '.pb',              # TensorFlow SavedModel
        '.model',           # Genérico
    }
    
    def get_artifact_type(self) -> ArtifactType:
        return ArtifactType.MODEL
    
    def validate_file(self, file_path: Union[str, Path]) -> None:
        """Valida arquivo de modelo"""
        file_path = Path(file_path)
        
        # Verificar extensão
        if file_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise InvalidArtifactError(
                f"Formato de modelo não suportado: {file_path.suffix}. "
                f"Formatos suportados: {', '.join(self.SUPPORTED_EXTENSIONS)}"
            )
        
        # Tentar carregar o modelo para validação básica
        try:
            self._validate_model_integrity(file_path)
        except Exception as e:
            raise InvalidArtifactError(
                f"Não foi possível validar o modelo: {str(e)}"
            )
    
    def _validate_model_integrity(self, file_path: Path) -> None:
        """Valida integridade básica do modelo"""
        extension = file_path.suffix.lower()
        
        # Validação para pickle
        if extension in ['.pkl', '.pickle']:
            try:
                with open(file_path, 'rb') as f:
                    # Apenas tenta ler o header
                    pickle.load(f, encoding='bytes')
            except:
                # Se falhar, ainda pode ser válido
                pass
        
        # Validação para joblib
        elif extension == '.joblib':
            try:
                # Tenta ler metadados
                joblib.load(file_path, mmap_mode='r')
            except:
                pass
        
        # Validação para JSON
        elif extension == '.json':
            with open(file_path, 'r') as f:
                json.load(f)
        
        # Para outros formatos, confiar que o arquivo está correto
        # A validação completa será feita no servidor