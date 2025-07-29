"""Uploader para datasets"""

from pathlib import Path
from typing import Union
import pandas as pd

from .base import BaseUploader
from ..models.artifact import ArtifactType
from ..exceptions import InvalidArtifactError


class DatasetUploader(BaseUploader):
    """Uploader especializado para datasets"""
    
    SUPPORTED_EXTENSIONS = {
        '.csv', '.tsv',           # Delimitados
        '.parquet',               # Parquet
        '.json', '.jsonl',        # JSON
        '.xlsx', '.xls',          # Excel
        '.feather',               # Feather
        '.h5', '.hdf5',           # HDF5
        '.pkl', '.pickle',        # Pickle (DataFrames)
        '.zip',                   # Arquivos comprimidos
    }
    
    def get_artifact_type(self) -> ArtifactType:
        return ArtifactType.DATASET
    
    def validate_file(self, file_path: Union[str, Path]) -> None:
        """Valida arquivo de dataset"""
        file_path = Path(file_path)
        
        # Verificar extensão
        if file_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise InvalidArtifactError(
                f"Formato de dataset não suportado: {file_path.suffix}. "
                f"Formatos suportados: {', '.join(self.SUPPORTED_EXTENSIONS)}"
            )
        
        # Validação básica de integridade
        try:
            self._validate_dataset_integrity(file_path)
        except Exception as e:
            raise InvalidArtifactError(
                f"Não foi possível validar o dataset: {str(e)}"
            )
    
    def _validate_dataset_integrity(self, file_path: Path) -> None:
        """Valida integridade básica do dataset"""
        extension = file_path.suffix.lower()
        
        # Para CSV, tentar ler apenas o header
        if extension in ['.csv', '.tsv']:
            delimiter = '\t' if extension == '.tsv' else ','
            pd.read_csv(file_path, nrows=0, delimiter=delimiter)
        
        # Para Parquet
        elif extension == '.parquet':
            pd.read_parquet(file_path, engine='pyarrow', columns=[])
        
        # Para Excel
        elif extension in ['.xlsx', '.xls']:
            pd.read_excel(file_path, nrows=0)
        
        # Para JSON/JSONL
        elif extension in ['.json', '.jsonl']:
            if extension == '.jsonl':
                pd.read_json(file_path, lines=True, nrows=1)
            else:
                pd.read_json(file_path, nrows=1)
        
        # Para outros formatos, confiar na extensão