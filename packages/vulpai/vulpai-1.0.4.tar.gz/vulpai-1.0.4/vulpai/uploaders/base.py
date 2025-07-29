"""Base class para uploaders"""

import os
import hashlib
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
import logging

from ..api.client import APIClient
from ..models.artifact import Artifact, ArtifactType
from ..exceptions import UploadError, InvalidArtifactError
from ..utils.progress import ProgressCallback

logger = logging.getLogger(__name__)


class BaseUploader(ABC):
    """Classe base para upload de artefatos"""
    
    MAX_FILE_SIZE = 5 * 1024 * 1024 * 1024  # 5GB
    CHUNK_SIZE = 10 * 1024 * 1024  # 10MB
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
    
    @abstractmethod
    def get_artifact_type(self) -> ArtifactType:
        """Retorna o tipo de artefato suportado"""
        pass
    
    @abstractmethod
    def validate_file(self, file_path: Union[str, Path]) -> None:
        """Valida o arquivo antes do upload"""
        pass
    
    def upload(
        self,
        file_path: Union[str, Path],
        name: str,
        description: Optional[str] = None,
        tags: List[str] = None,
        metadata: Dict[str, Any] = None,
        progress_callback: Optional[ProgressCallback] = None
    ) -> Artifact:
        """
        Faz upload de um artefato
        
        Args:
            file_path: Caminho do arquivo
            name: Nome do artefato
            description: Descrição
            tags: Tags para categorização
            metadata: Metadados adicionais
            progress_callback: Callback de progresso
            
        Returns:
            Artifact: Artefato criado
        """
        file_path = Path(file_path)
        
        # Validações básicas
        self._validate_basic(file_path)
        
        # Validação específica do tipo
        self.validate_file(file_path)
        
        # Calcular hash do arquivo
        file_hash = self._calculate_file_hash(file_path)
        
        # Preparar metadados
        upload_metadata = {
            "file_name": file_path.name,
            "file_size": file_path.stat().st_size,
            "file_hash": file_hash,
            "artifact_type": self.get_artifact_type().value,
            **(metadata or {})
        }
        
        # Dados do formulário
        form_data = {
            "name": name,
            "description": description,
            "tags": json.dumps(tags or []),
            "metadata": json.dumps(upload_metadata, default=str, allow_nan=False)
        }
        
        try:
            # Upload do arquivo
            response = self.api_client.upload_file(
                endpoint="/artifacts/upload",
                file_path=str(file_path),
                data=form_data,
                progress_callback=progress_callback
            )
            
            # Retornar artefato criado
            return Artifact.from_dict(response['artifact'])
            
        except Exception as e:
            logger.error(f"Erro no upload: {e}")
            raise UploadError(f"Falha no upload do arquivo: {str(e)}")
    
    def create_version(
        self,
        original_artifact_id: str,
        file_path: Union[str, Path],
        version_notes: Optional[str] = None,
        progress_callback: Optional[ProgressCallback] = None
    ) -> Artifact:
        """
        Cria nova versão de um artefato existente
        """
        file_path = Path(file_path)
        
        # Obter artefato original
        original = self.api_client.get(f"/artifacts/{original_artifact_id}")
        
        # Upload como nova versão
        return self.upload(
            file_path=file_path,
            name=original['name'],
            description=original.get('description'),
            tags=original.get('tags', []),
            metadata={
                **original.get('metadata', {}),
                'parent_id': original_artifact_id,
                'version_notes': version_notes
            },
            progress_callback=progress_callback
        )
    
    def _validate_basic(self, file_path: Path) -> None:
        """Validações básicas do arquivo"""
        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        if not file_path.is_file():
            raise InvalidArtifactError(f"Caminho não é um arquivo: {file_path}")
        
        file_size = file_path.stat().st_size
        if file_size > self.MAX_FILE_SIZE:
            raise InvalidArtifactError(
                f"Arquivo muito grande: {file_size / (1024**3):.2f}GB. "
                f"Máximo permitido: {self.MAX_FILE_SIZE / (1024**3):.2f}GB"
            )
        
        if file_size == 0:
            raise InvalidArtifactError("Arquivo vazio")
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calcula hash SHA256 do arquivo"""
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        
        return sha256_hash.hexdigest()