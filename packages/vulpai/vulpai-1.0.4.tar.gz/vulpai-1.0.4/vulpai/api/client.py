"""Cliente HTTP para comunicação com a API VulpAI"""

import json
import logging
from typing import Dict, Any, Optional, Union
from urllib.parse import urljoin
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from ..exceptions import (
    APIError, AuthenticationError, VulpAIError
)
from .auth import AuthManager
from .endpoints import Endpoints

logger = logging.getLogger(__name__)


class APIClient:
    """Cliente HTTP para a API VulpAI"""
    
    def __init__(
        self,
        api_token: str,
        base_url: str = "https://api.vulpai.com",
        timeout: int = 300,
        max_retries: int = 3,
        verify_ssl: bool = False
    ):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        # Configurar autenticação
        self.auth_manager = AuthManager(api_token)
        
        # Configurar sessão com retry
        self.session = self._create_session(max_retries)
    
    def _create_session(self, max_retries: int) -> requests.Session:
        """Cria sessão com configuração de retry"""
        session = requests.Session()
        
        # Configurar retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _get_headers(self) -> Dict[str, str]:
        """Obtém headers padrão para requisições"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "VulpAI-Python-Client/1.0.0"
        }
        
        # Adicionar headers de autenticação
        headers.update(self.auth_manager.get_headers())
        
        return headers
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Faz uma requisição HTTP"""
        url = urljoin(self.base_url, endpoint)
        
        # Configurar headers
        headers = kwargs.pop('headers', {})
        headers.update(self._get_headers())
        
        # Configurar timeout
        kwargs.setdefault('timeout', self.timeout)
        kwargs.setdefault('verify', self.verify_ssl)
        
        try:
            logger.debug(f"{method} {url}")
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                **kwargs
            )
            
            # Verificar autenticação
            if response.status_code == 401:
                raise AuthenticationError("Token de API inválido ou expirado")
            
            # Verificar outros erros HTTP
            if response.status_code >= 400:
                self._handle_error_response(response)
            
            # Retornar resposta JSON
            if response.content:
                return response.json()
            return {}
            
        except requests.exceptions.Timeout:
            raise APIError(f"Timeout ao acessar {url}")
        except requests.exceptions.ConnectionError:
            raise APIError(f"Erro de conexão ao acessar {url}")
        except json.JSONDecodeError:
            raise APIError(f"Resposta inválida da API: {response.text}")
        except requests.exceptions.RequestException as e:
            raise APIError(f"Erro na requisição: {str(e)}")
    
    def _handle_error_response(self, response: requests.Response):
        """Trata respostas de erro da API"""
        try:
            error_data = response.json()
            error_message = error_data.get('error', 'Erro desconhecido')
            error_code = error_data.get('error_code')
        except:
            error_message = f"Erro HTTP {response.status_code}"
            error_code = None
        
        raise APIError(
            message=error_message,
            status_code=response.status_code,
            response_body=error_data if 'error_data' in locals() else None
        )
    
    # Métodos HTTP
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Requisição GET"""
        return self._make_request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Requisição POST"""
        return self._make_request('POST', endpoint, json=json, **kwargs)
    
    def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Requisição PUT"""
        return self._make_request('PUT', endpoint, json=json, **kwargs)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Requisição DELETE"""
        return self._make_request('DELETE', endpoint)
    
    def upload_file(
        self,
        endpoint: str,
        file_path: str,
        file_field: str = 'file',
        data: Optional[Dict[str, Any]] = None,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """Upload de arquivo com progresso opcional"""
        import os
        from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
        
        file_size = os.path.getsize(file_path)
        
        with open(file_path, 'rb') as f:
            # Preparar dados do formulário
            fields = data or {}
            fields[file_field] = (os.path.basename(file_path), f, 'application/octet-stream')
            
            # Criar encoder
            encoder = MultipartEncoder(fields=fields)
            
            # Adicionar monitor de progresso se callback fornecido
            if progress_callback:
                def callback(monitor):
                    progress_callback(monitor.bytes_read, file_size)
                
                monitor = MultipartEncoderMonitor(encoder, callback)
                data_to_send = monitor
            else:
                data_to_send = encoder
            
            # Fazer upload
            headers = self._get_headers()
            headers['Content-Type'] = encoder.content_type
            
            return self._make_request(
                'POST',
                endpoint,
                data=data_to_send,
                headers=headers
            )