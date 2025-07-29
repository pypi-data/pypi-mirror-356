"""Utilitários para extração de metadados"""

import os
import mimetypes
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Union
import magic


def extract_file_metadata(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Extrai metadados de um arquivo
    
    Args:
        file_path: Caminho do arquivo
        
    Returns:
        Dict com metadados do arquivo
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    
    stat = file_path.stat()
    
    metadata = {
        'name': file_path.name,
        'path': str(file_path.absolute()),
        'size_bytes': stat.st_size,
        'size_mb': stat.st_size / (1024 * 1024),
        'extension': file_path.suffix.lower(),
        'created_at': datetime.fromtimestamp(stat.st_ctime).isoformat(),
        'modified_at': datetime.fromtimestamp(stat.st_mtime).isoformat(),
        'accessed_at': datetime.fromtimestamp(stat.st_atime).isoformat(),
    }
    
    # Tipo MIME
    mime_type, _ = mimetypes.guess_type(str(file_path))
    metadata['mime_type'] = mime_type
    
    # Detecção mais precisa com python-magic
    try:
        file_magic = magic.from_file(str(file_path), mime=True)
        metadata['magic_mime_type'] = file_magic
        
        file_description = magic.from_file(str(file_path))
        metadata['file_description'] = file_description
    except Exception:
        # Se python-magic não estiver disponível
        pass
    
    # Permissões
    metadata['permissions'] = {
        'readable': os.access(file_path, os.R_OK),
        'writable': os.access(file_path, os.W_OK),
        'executable': os.access(file_path, os.X_OK)
    }
    
    return metadata


def get_model_framework(file_path: Union[str, Path]) -> str:
    """
    Tenta identificar o framework do modelo pelo arquivo
    
    Args:
        file_path: Caminho do arquivo
        
    Returns:
        str: Nome do framework ou 'unknown'
    """
    file_path = Path(file_path)
    extension = file_path.suffix.lower()
    
    # Mapeamento de extensões para frameworks
    extension_map = {
        '.pkl': 'scikit-learn',
        '.pickle': 'scikit-learn',
        '.joblib': 'scikit-learn',
        '.pt': 'pytorch',
        '.pth': 'pytorch',
        '.h5': 'tensorflow',
        '.hdf5': 'tensorflow',
        '.pb': 'tensorflow',
        '.onnx': 'onnx',
        '.pmml': 'pmml',
        '.xgb': 'xgboost',
        '.lgb': 'lightgbm',
        '.cbm': 'catboost'
    }
    
    return extension_map.get(extension, 'unknown')