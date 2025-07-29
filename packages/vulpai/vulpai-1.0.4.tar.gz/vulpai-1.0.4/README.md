# VulpAI Python Client

<div align="center">
  <img src="raposa.svg" alt="VulpAI Logo" width="128">
  
  **Cliente Python oficial para o sistema VulpAI de validação automatizada de modelos de IA**
</div>

## Instalação

```bash
pip install vulpai
```

Para instalar com suporte a frameworks específicos:

```bash
# Scikit-learn
pip install vulpai[sklearn]

# PyTorch
pip install vulpai[pytorch]

# TensorFlow
pip install vulpai[tensorflow]

# Todos os frameworks
pip install vulpai[all]
```

## Início Rápido

```python
from vulpai import VulpAIClient

# Criar cliente
client = VulpAIClient(api_token="seu-token-aqui")

# Upload de modelo
artifact = client.upload_model(
    model_path="modelo.pkl",
    name="Meu Modelo",
    description="Modelo de classificação",
    tags=["producao", "v1.0"]
)

# Iniciar validação
validation_id = client.start_validation(artifact_id=artifact.id)

# Verificar resultados
result = client.get_validation_result(validation_id)
print(f"Acurácia: {result.metrics['accuracy']}")
```

## Funcionalidades Principais

### 💰 Gestão de Créditos
- Consultar saldo e uso de créditos
- Estimar custos antes do upload
- Histórico detalhado de consumo

### 📤 Upload de Artefatos
- Suporte para modelos e datasets
- Versionamento automático
- Validação local antes do envio
- Progress tracking para arquivos grandes

### ✅ Validação de Modelos
- Validação automatizada com Claude API
- Múltiplos níveis: Basic, Standard, Advanced
- Métricas customizáveis
- Geração de relatórios e visualizações

### =à Frameworks Suportados
- Scikit-learn (.pkl, .joblib)
- PyTorch (.pt, .pth)
- TensorFlow/Keras (.h5, .pb)
- XGBoost (.xgb)
- ONNX (.onnx)
- Formatos customizados

## Exemplos

### Upload com Progresso

```python
from vulpai.utils.progress import ConsoleProgress

progress = ConsoleProgress("Enviando modelo")
artifact = client.upload_model(
    model_path="modelo_grande.pkl",
    name="Modelo Grande",
    progress_callback=progress
)
```

### Validação Avançada

```python
from vulpai import ValidationConfig, ValidationLevel

config = ValidationConfig(
    validation_level=ValidationLevel.ADVANCED,
    cross_validation_folds=5,
    metrics=["accuracy", "precision", "recall", "f1", "roc_auc"],
    generate_visualizations=True
)

validation_id = client.start_validation(
    artifact_id=artifact.id,
    validation_config=config
)
```

### Versionamento de Modelos

```python
# Criar nova versão
new_version = client.create_model_version(
    original_artifact_id=artifact.id,
    model_path="modelo_v2.pkl",
    version_notes="Melhorias de performance"
)

# Listar versões
versions = client.get_artifact_versions(artifact.id)
```

## Configuração

### Variáveis de Ambiente

```bash
export VULPAI_API_TOKEN="seu-token"
export VULPAI_BASE_URL="https://api.vulpai.com"  # Opcional
```

### Configuração Programática

```python
from vulpai.config import VulpAIConfig

config = VulpAIConfig(
    api_token="seu-token",
    base_url="https://api.vulpai.com",
    timeout=300,
    max_retries=3
)

client = VulpAIClient.from_config(config)
```

## Documentação Completa

Para documentação detalhada, visite: [https://docs.vulpai.com](https://docs.vulpai.com)

## Contribuindo

Contribuições são bem-vindas! Por favor, veja nosso [guia de contribuição](CONTRIBUTING.md).

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.