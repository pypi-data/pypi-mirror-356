"""Utilitários para compressão de arquivos"""

import gzip
import zipfile
import tarfile
from pathlib import Path
from typing import Union, List
import logging

logger = logging.getLogger(__name__)


def compress_file(
    file_path: Union[str, Path],
    output_path: Union[str, Path] = None,
    compression_type: str = 'gzip'
) -> Path:
    """
    Comprime um arquivo
    
    Args:
        file_path: Arquivo para comprimir
        output_path: Caminho de saída (opcional)
        compression_type: Tipo de compressão ('gzip', 'zip', 'tar.gz')
        
    Returns:
        Path: Caminho do arquivo comprimido
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    
    # Determinar caminho de saída
    if output_path is None:
        if compression_type == 'gzip':
            output_path = file_path.with_suffix(file_path.suffix + '.gz')
        elif compression_type == 'zip':
            output_path = file_path.with_suffix('.zip')
        elif compression_type == 'tar.gz':
            output_path = file_path.with_suffix('.tar.gz')
        else:
            raise ValueError(f"Tipo de compressão não suportado: {compression_type}")
    else:
        output_path = Path(output_path)
    
    # Comprimir
    if compression_type == 'gzip':
        with open(file_path, 'rb') as f_in:
            with gzip.open(output_path, 'wb') as f_out:
                f_out.write(f_in.read())
    
    elif compression_type == 'zip':
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(file_path, file_path.name)
    
    elif compression_type == 'tar.gz':
        with tarfile.open(output_path, 'w:gz') as tar:
            tar.add(file_path, arcname=file_path.name)
    
    logger.info(f"Arquivo comprimido: {output_path}")
    return output_path


def decompress_file(
    compressed_path: Union[str, Path],
    output_dir: Union[str, Path] = None
) -> Path:
    """
    Descomprime um arquivo
    
    Args:
        compressed_path: Arquivo comprimido
        output_dir: Diretório de saída (opcional)
        
    Returns:
        Path: Caminho do arquivo/diretório descomprimido
    """
    compressed_path = Path(compressed_path)
    
    if not compressed_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {compressed_path}")
    
    # Determinar diretório de saída
    if output_dir is None:
        output_dir = compressed_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Detectar tipo e descomprimir
    if compressed_path.suffix == '.gz':
        output_path = output_dir / compressed_path.stem
        with gzip.open(compressed_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                f_out.write(f_in.read())
        return output_path
    
    elif compressed_path.suffix == '.zip':
        with zipfile.ZipFile(compressed_path, 'r') as zf:
            zf.extractall(output_dir)
        return output_dir
    
    elif compressed_path.name.endswith('.tar.gz'):
        with tarfile.open(compressed_path, 'r:gz') as tar:
            tar.extractall(output_dir)
        return output_dir
    
    else:
        raise ValueError(f"Formato de compressão não suportado: {compressed_path.suffix}")


def get_compressed_size(file_path: Union[str, Path]) -> int:
    """
    Estima tamanho após compressão
    
    Args:
        file_path: Arquivo para estimar
        
    Returns:
        int: Tamanho estimado em bytes
    """
    file_path = Path(file_path)
    original_size = file_path.stat().st_size
    
    # Estimativa baseada em tipo de arquivo
    extension = file_path.suffix.lower()
    
    # Arquivos já comprimidos
    if extension in ['.zip', '.gz', '.bz2', '.xz', '.7z']:
        return original_size
    
    # Modelos binários (geralmente comprimem bem)
    if extension in ['.pkl', '.pickle', '.joblib', '.pt', '.pth']:
        return int(original_size * 0.6)
    
    # Dados estruturados
    if extension in ['.csv', '.json', '.xml']:
        return int(original_size * 0.3)
    
    # Padrão
    return int(original_size * 0.5)