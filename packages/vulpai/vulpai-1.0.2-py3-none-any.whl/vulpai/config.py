"""Configurações do VulpAI"""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class VulpAIConfig:
    """Configurações globais do cliente VulpAI"""
    
    api_token: str
    base_url: str = "https://api.vulpai.com"
    timeout: int = 300
    max_retries: int = 3
    verify_ssl: bool = True
    
    # Limites de upload
    max_file_size_mb: int = 5000  # 5GB
    chunk_size_mb: int = 10
    
    # Configurações de validação
    default_validation_level: str = "standard"
    auto_retry_validation: bool = True
    
    # Cache
    enable_cache: bool = True
    cache_ttl_seconds: int = 3600
    
    @classmethod
    def from_env(cls) -> 'VulpAIConfig':
        """Cria configuração a partir de variáveis de ambiente"""
        api_token = os.getenv('VULPAI_API_TOKEN')
        if not api_token:
            raise ValueError("VULPAI_API_TOKEN não definido")
        
        return cls(
            api_token=api_token,
            base_url=os.getenv('VULPAI_BASE_URL', cls.base_url),
            timeout=int(os.getenv('VULPAI_TIMEOUT', str(cls.timeout))),
            max_retries=int(os.getenv('VULPAI_MAX_RETRIES', str(cls.max_retries))),
            verify_ssl=os.getenv('VULPAI_VERIFY_SSL', 'true').lower() == 'true'
        )
    
    @property
    def chunk_size_bytes(self) -> int:
        """Tamanho do chunk em bytes"""
        return self.chunk_size_mb * 1024 * 1024
    
    @property
    def max_file_size_bytes(self) -> int:
        """Tamanho máximo de arquivo em bytes"""
        return self.max_file_size_mb * 1024 * 1024