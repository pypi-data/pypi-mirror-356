from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
import uuid


class ArtifactType(Enum):
    """Tipos de artefatos suportados"""
    MODEL = "model"
    DATASET = "dataset"
    CONFIGURATION = "configuration"


class ArtifactStatus(Enum):
    """Status dos artefatos"""
    UPLOADING = "uploading"
    PROCESSING = "processing"
    READY = "ready"
    ERROR = "error"
    DELETED = "deleted"


@dataclass
class Artifact:
    """Representa um artefato no sistema VulpAI"""
    
    id: str
    name: str
    artifact_type: ArtifactType
    status: ArtifactStatus
    created_at: datetime
    updated_at: datetime
    user_id: str
    size_bytes: int
    file_hash: str
    
    # Campos opcionais
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    version: int = 1
    parent_id: Optional[str] = None  # Para versionamento
    version_notes: Optional[str] = None
    
    # URLs para download
    download_url: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Artifact':
        """Cria instância a partir de dicionário"""
        return cls(
            id=data['id'],
            name=data['name'],
            artifact_type=ArtifactType(data['artifact_type']),
            status=ArtifactStatus(data['status']),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            user_id=data['user_id'],
            size_bytes=data['size_bytes'],
            file_hash=data['file_hash'],
            description=data.get('description'),
            tags=data.get('tags', []),
            metadata=data.get('metadata', {}),
            version=data.get('version', 1),
            parent_id=data.get('parent_id'),
            version_notes=data.get('version_notes'),
            download_url=data.get('download_url')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'artifact_type': self.artifact_type.value,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'user_id': self.user_id,
            'size_bytes': self.size_bytes,
            'file_hash': self.file_hash,
            'description': self.description,
            'tags': self.tags,
            'metadata': self.metadata,
            'version': self.version,
            'parent_id': self.parent_id,
            'version_notes': self.version_notes,
            'download_url': self.download_url
        }
    
    @property
    def size_mb(self) -> float:
        """Tamanho em MB"""
        return self.size_bytes / (1024 * 1024)
    
    @property
    def is_versioned(self) -> bool:
        """Verifica se é uma versão de outro artefato"""
        return self.parent_id is not None
    
    def __str__(self) -> str:
        return f"Artifact(id={self.id}, name={self.name}, type={self.artifact_type.value})"