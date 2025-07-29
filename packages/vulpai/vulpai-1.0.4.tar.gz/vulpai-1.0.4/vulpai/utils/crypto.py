"""Utilitários de criptografia e hashing"""

import hashlib
import uuid
from pathlib import Path
from typing import Union


def calculate_hash(file_path: Union[str, Path], algorithm: str = 'sha256') -> str:
    """
    Calcula hash de um arquivo
    
    Args:
        file_path: Caminho do arquivo
        algorithm: Algoritmo de hash (sha256, md5, sha1)
        
    Returns:
        str: Hash hexadecimal
    """
    file_path = Path(file_path)
    
    if algorithm == 'sha256':
        hasher = hashlib.sha256()
    elif algorithm == 'md5':
        hasher = hashlib.md5()
    elif algorithm == 'sha1':
        hasher = hashlib.sha1()
    else:
        raise ValueError(f"Algoritmo não suportado: {algorithm}")
    
    # Ler arquivo em chunks para arquivos grandes
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    
    return hasher.hexdigest()


def generate_id() -> str:
    """
    Gera ID único
    
    Returns:
        str: UUID v4
    """
    return str(uuid.uuid4())


def hash_string(text: str, algorithm: str = 'sha256') -> str:
    """
    Calcula hash de uma string
    
    Args:
        text: Texto para hash
        algorithm: Algoritmo de hash
        
    Returns:
        str: Hash hexadecimal
    """
    if algorithm == 'sha256':
        hasher = hashlib.sha256()
    elif algorithm == 'md5':
        hasher = hashlib.md5()
    elif algorithm == 'sha1':
        hasher = hashlib.sha1()
    else:
        raise ValueError(f"Algoritmo não suportado: {algorithm}")
    
    hasher.update(text.encode('utf-8'))
    return hasher.hexdigest()


def verify_file_integrity(file_path: Union[str, Path], expected_hash: str, algorithm: str = 'sha256') -> bool:
    """
    Verifica integridade de um arquivo comparando hashes
    
    Args:
        file_path: Caminho do arquivo
        expected_hash: Hash esperado
        algorithm: Algoritmo de hash
        
    Returns:
        bool: True se o hash corresponde
    """
    actual_hash = calculate_hash(file_path, algorithm)
    return actual_hash == expected_hash