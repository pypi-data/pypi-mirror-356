"""Definição de endpoints da API VulpAI"""


class Endpoints:
    """Endpoints da API VulpAI"""
    
    # Base
    HEALTH = "/health"
    
    # Autenticação
    AUTH_TOKEN = "/auth/token"
    AUTH_REFRESH = "/auth/refresh"
    
    # Créditos
    CREDITS_INFO = "/credits/info"
    CREDITS_USAGE = "/credits/usage"
    CREDITS_PURCHASE = "/credits/purchase"
    
    # Artefatos
    ARTIFACTS = "/artifacts"
    ARTIFACT_DETAIL = "/artifacts/{artifact_id}"
    ARTIFACT_VERSIONS = "/artifacts/{artifact_id}/versions"
    ARTIFACT_UPLOAD = "/artifacts/upload"
    ARTIFACT_DOWNLOAD = "/artifacts/{artifact_id}/download"
    
    # Validações
    VALIDATIONS = "/validations"
    VALIDATION_DETAIL = "/validations/{validation_id}"
    VALIDATION_STATUS = "/validations/{validation_id}/status"
    VALIDATION_RESULT = "/validations/{validation_id}/result"
    VALIDATION_ESTIMATE = "/validations/estimate"
    VALIDATION_CANCEL = "/validations/{validation_id}/cancel"
    
    # Relatórios
    REPORTS = "/reports"
    REPORT_DOWNLOAD = "/reports/{report_id}/download"
    
    # Webhooks
    WEBHOOKS = "/webhooks"
    WEBHOOK_DETAIL = "/webhooks/{webhook_id}"