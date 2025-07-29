import os
import uuid
from typing import Optional, List, Dict, Any, Union
from pathlib import Path
import logging

from .api.client import APIClient
from .models.artifact import Artifact, ArtifactType
from .models.validation import ValidationConfig, ValidationResult
from .models.credit import CreditInfo, CreditUsage
from .uploaders.model_uploader import ModelUploader
from .uploaders.dataset_uploader import DatasetUploader
from .validators.base import get_validator
from .exceptions import AuthenticationError, InsufficientCreditsError
from .utils.progress import ProgressCallback

logger = logging.getLogger(__name__)


class VulpAIClient:
    """
    Cliente principal para interação com a API VulpAI
    """
    
    def __init__(
        self,
        api_token: str,
        base_url: str = "https://api.vulpai.com",
        timeout: int = 300,
        max_retries: int = 3
    ):
        """
        Inicializa o cliente VulpAI
        
        Args:
            api_token: Token de autenticação
            base_url: URL base da API
            timeout: Timeout em segundos
            max_retries: Número máximo de tentativas
        """
        self.api_token = api_token
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        
        self._api_client = APIClient(
            api_token=api_token,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries
        )
        
        # Configuração de logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Configura logging para a biblioteca"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    # === GESTÃO DE CRÉDITOS ===
    
    def get_credit_info(self) -> CreditInfo:
        """
        Obtém informações sobre créditos do usuário
        
        Returns:
            CreditInfo: Informações de créditos
        """
        response = self._api_client.get("/credits/info")
        return CreditInfo.from_dict(response)
    
    def get_credit_usage(
        self, 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[CreditUsage]:
        """
        Obtém histórico de uso de créditos
        
        Args:
            start_date: Data início (YYYY-MM-DD)
            end_date: Data fim (YYYY-MM-DD)
            
        Returns:
            List[CreditUsage]: Lista de usos de créditos
        """
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
            
        response = self._api_client.get("/credits/usage", params=params)
        return [CreditUsage.from_dict(usage) for usage in response['usage']]
    
    def estimate_validation_cost(
        self,
        artifact_path: Union[str, Path],
        validation_config: Optional[ValidationConfig] = None
    ) -> Dict[str, Any]:
        """
        Estima o custo de validação de um artefato
        
        Args:
            artifact_path: Caminho para o artefato
            validation_config: Configuração de validação
            
        Returns:
            Dict com estimativa de custos
        """
        # Análise local do modelo para estimativa
        validator = get_validator(artifact_path)
        metadata = validator.extract_metadata(artifact_path)
        
        payload = {
            "artifact_metadata": metadata,
            "validation_config": validation_config.to_dict() if validation_config else None
        }
        
        response = self._api_client.post("/validations/estimate", json=payload)
        return response
    
    # === GESTÃO DE ARTEFATOS ===
    
    def upload_model(
        self,
        model_path: Union[str, Path],
        name: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        progress_callback: Optional[ProgressCallback] = None,
        check_credits: bool = True
    ) -> Artifact:
        """
        Faz upload de um modelo
        
        Args:
            model_path: Caminho para o modelo
            name: Nome do artefato
            description: Descrição opcional
            tags: Tags para categorização
            metadata: Metadados adicionais
            progress_callback: Callback para progresso
            check_credits: Verificar créditos antes do upload
            
        Returns:
            Artifact: Artefato criado
        """
        if check_credits:
            self._check_sufficient_credits(model_path)
        
        uploader = ModelUploader(self._api_client)
        
        artifact = uploader.upload(
            file_path=model_path,
            name=name,
            description=description,
            tags=tags or [],
            metadata=metadata or {},
            progress_callback=progress_callback
        )
        
        logger.info(f"Modelo '{name}' enviado com sucesso. ID: {artifact.id}")
        return artifact
    
    def upload_dataset(
        self,
        dataset_path: Union[str, Path],
        name: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        progress_callback: Optional[ProgressCallback] = None
    ) -> Artifact:
        """
        Faz upload de um dataset
        """
        uploader = DatasetUploader(self._api_client)
        
        artifact = uploader.upload(
            file_path=dataset_path,
            name=name,
            description=description,
            tags=tags or [],
            metadata=metadata or {},
            progress_callback=progress_callback
        )
        
        logger.info(f"Dataset '{name}' enviado com sucesso. ID: {artifact.id}")
        return artifact
    
    def create_model_version(
        self,
        original_artifact_id: str,
        model_path: Union[str, Path],
        version_notes: Optional[str] = None,
        progress_callback: Optional[ProgressCallback] = None
    ) -> Artifact:
        """
        Cria uma nova versão de um modelo existente
        
        Args:
            original_artifact_id: ID do artefato original
            model_path: Caminho para a nova versão
            version_notes: Notas da versão
            progress_callback: Callback para progresso
            
        Returns:
            Artifact: Nova versão criada
        """
        uploader = ModelUploader(self._api_client)
        
        artifact = uploader.create_version(
            original_artifact_id=original_artifact_id,
            file_path=model_path,
            version_notes=version_notes,
            progress_callback=progress_callback
        )
        
        logger.info(f"Nova versão criada. ID: {artifact.id}")
        return artifact
    
    def list_artifacts(
        self,
        artifact_type: Optional[ArtifactType] = None,
        tags: Optional[List[str]] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Artifact]:
        """
        Lista artefatos do usuário
        
        Args:
            artifact_type: Filtrar por tipo
            tags: Filtrar por tags
            limit: Limite de resultados
            offset: Offset para paginação
            
        Returns:
            List[Artifact]: Lista de artefatos
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if artifact_type:
            params["type"] = artifact_type.value
        if tags:
            params["tags"] = ",".join(tags)
        
        response = self._api_client.get("/artifacts", params=params)
        return [Artifact.from_dict(item) for item in response['artifacts']]
    
    def get_artifact(self, artifact_id: str) -> Artifact:
        """
        Obtém detalhes de um artefato específico
        
        Args:
            artifact_id: ID do artefato
            
        Returns:
            Artifact: Detalhes do artefato
        """
        response = self._api_client.get(f"/artifacts/{artifact_id}")
        return Artifact.from_dict(response)
    
    def get_artifact_versions(self, artifact_id: str) -> List[Artifact]:
        """
        Obtém todas as versões de um artefato
        
        Args:
            artifact_id: ID do artefato
            
        Returns:
            List[Artifact]: Lista de versões
        """
        response = self._api_client.get(f"/artifacts/{artifact_id}/versions")
        return [Artifact.from_dict(item) for item in response['versions']]
    
    def delete_artifact(self, artifact_id: str) -> bool:
        """
        Exclui um artefato
        
        Args:
            artifact_id: ID do artefato
            
        Returns:
            bool: Sucesso da operação
        """
        try:
            self._api_client.delete(f"/artifacts/{artifact_id}")
            logger.info(f"Artefato {artifact_id} excluído com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao excluir artefato {artifact_id}: {e}")
            return False
    
    # === VALIDAÇÕES ===
    
    def start_validation(
        self,
        artifact_id: str,
        validation_config: Optional[ValidationConfig] = None,
        dataset_id: Optional[str] = None
    ) -> str:
        """
        Inicia uma validação
        
        Args:
            artifact_id: ID do artefato a validar
            validation_config: Configuração da validação
            dataset_id: ID do dataset para validação
            
        Returns:
            str: ID da validação
        """
        payload = {
            "artifact_id": artifact_id,
            "validation_config": validation_config.to_dict() if validation_config else None,
            "dataset_id": dataset_id
        }
        
        response = self._api_client.post("/validations", json=payload)
        validation_id = response['validation_id']
        
        logger.info(f"Validação iniciada. ID: {validation_id}")
        return validation_id
    
    def get_validation_status(self, validation_id: str) -> Dict[str, Any]:
        """
        Obtém status de uma validação
        
        Args:
            validation_id: ID da validação
            
        Returns:
            Dict: Status da validação
        """
        response = self._api_client.get(f"/validations/{validation_id}/status")
        return response
    
    def get_validation_result(self, validation_id: str) -> ValidationResult:
        """
        Obtém resultado de uma validação
        
        Args:
            validation_id: ID da validação
            
        Returns:
            ValidationResult: Resultado da validação
        """
        response = self._api_client.get(f"/validations/{validation_id}/result")
        return ValidationResult.from_dict(response)
    
    def list_validations(
        self,
        artifact_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Lista validações do usuário
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if artifact_id:
            params["artifact_id"] = artifact_id
        if status:
            params["status"] = status
        
        response = self._api_client.get("/validations", params=params)
        return response['validations']
    
    # === MÉTODOS AUXILIARES ===
    
    def _check_sufficient_credits(self, model_path: Union[str, Path]) -> None:
        """
        Verifica se há créditos suficientes para a operação
        """
        try:
            estimate = self.estimate_validation_cost(model_path)
            credit_info = self.get_credit_info()
            
            estimated_cost = estimate.get('estimated_cost', 0)
            
            if credit_info.available_credits < estimated_cost:
                raise InsufficientCreditsError(
                    f"Créditos insuficientes. Necessário: {estimated_cost}, "
                    f"Disponível: {credit_info.available_credits}"
                )
        except Exception as e:
            logger.warning(f"Não foi possível verificar créditos: {e}")
    
    def health_check(self) -> Dict[str, Any]:
        """
        Verifica status da API
        
        Returns:
            Dict: Status da API
        """
        response = self._api_client.get("/health")
        return response
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        # Cleanup se necessário
        pass