"""Exceções customizadas do VulpAI"""


class VulpAIError(Exception):
    """Exceção base para todos os erros do VulpAI"""
    pass


class AuthenticationError(VulpAIError):
    """Erro de autenticação com a API"""
    pass


class InsufficientCreditsError(VulpAIError):
    """Erro quando não há créditos suficientes"""
    
    def __init__(self, message: str, required_credits: float = None, available_credits: float = None):
        super().__init__(message)
        self.required_credits = required_credits
        self.available_credits = available_credits


class ValidationError(VulpAIError):
    """Erro durante processo de validação"""
    pass


class UploadError(VulpAIError):
    """Erro durante upload de artefatos"""
    pass


class APIError(VulpAIError):
    """Erro genérico de comunicação com a API"""
    
    def __init__(self, message: str, status_code: int = None, response_body: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class ConfigurationError(VulpAIError):
    """Erro de configuração"""
    pass


class ArtifactNotFoundError(VulpAIError):
    """Artefato não encontrado"""
    pass


class InvalidArtifactError(VulpAIError):
    """Artefato inválido ou corrompido"""
    pass