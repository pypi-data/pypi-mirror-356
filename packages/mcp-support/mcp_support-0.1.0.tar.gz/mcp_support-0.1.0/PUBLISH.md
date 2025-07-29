# 📦 Publicar en PyPI - MCP Job Analyzer Support

## Requisitos Previos
1. Cuenta en [PyPI](https://pypi.org/account/register/)
2. Cuenta en [TestPyPI](https://test.pypi.org/account/register/) (para pruebas - opcional)
3. [UV](https://docs.astral.sh/uv/) instalado

## Pasos para Publicar

### 1. Sincronizar dependencias (incluye build y twine)
```bash
uv sync
```

### 2. Construir el paquete
```bash
uv run python -m build
```

### 3. Verificar el paquete
```bash
uv run python -m twine check dist/*
```

### 4. (Opcional) Publicar en TestPyPI
```bash
uv run python -m twine upload --repository testpypi dist/*
```

Luego probar la instalación:
```bash
pip install --index-url https://test.pypi.org/simple/ mcp-support
```

### 5. Publicar en PyPI oficial
```bash
uv run python -m twine upload dist/*
```

## Uso para los Usuarios

### Opción 1: Con uvx (Recomendado) - Sin instalación
Los usuarios solo necesitan tener `uv` instalado:

```json
{
  "mcpServers": {
    "JobAnalyzerSupport": {
      "command": "uvx",
      "args": [
        "--from", "mcp-support", "server",
        "--log-group-name", "tu-log-group-name",
        "--aws-access-key-id", "tu-access-key-id",
        "--aws-secret-access-key", "tu-secret-access-key",
        "--region-name", "us-east-1"
      ]
    }
  }
}
```

### Opción 2: Con uvx y variables de entorno (Más seguro)
```json
{
  "mcpServers": {
    "JobAnalyzerSupport": {
      "command": "uvx",
      "args": ["--from", "mcp-support", "server"],
      "env": {
        "AWS_LOG_GROUP_NAME": "tu-log-group-name",
        "AWS_ACCESS_KEY_ID": "tu-access-key-id",
        "AWS_SECRET_ACCESS_KEY": "tu-secret-access-key",
        "AWS_REGION_NAME": "us-east-1"
      }
    }
  }
}
```

### Opción 3: Instalación tradicional con pip
```bash
pip install mcp-support
```

```json
{
  "mcpServers": {
    "JobAnalyzerSupport": {
      "command": "mcp-job-analyzer",
      "args": [
        "--log-group-name", "tu-log-group-name",
        "--aws-access-key-id", "tu-access-key-id",
        "--aws-secret-access-key", "tu-secret-access-key",
        "--region-name", "us-east-1"
      ]
    }
  }
}
```

### Ventajas de uvx:
- ✅ **Sin instalación**: No contamina el entorno global
- ✅ **Siempre actualizado**: Usa la última versión de PyPI
- ✅ **Sin dependencias**: No necesita gestión de entornos virtuales
- ✅ **Limpio**: Se limpia automáticamente después del uso
- ✅ **Rápido**: Cache automático para ejecuciones futuras

## Comandos Útiles

### Limpiar builds anteriores
```bash
rm -rf dist/ build/ *.egg-info/
```

### Verificar versión actual
```bash
uv run python -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])"
```

### Incrementar versión
Edita manualmente la versión en `pyproject.toml` o usa herramientas como `bump2version`.

## Notas Importantes

- ✅ El paquete se llamará `mcp-support` en PyPI
- ✅ El comando para `uvx` es el mismo nombre del paquete
- ✅ Compatible con Python 3.10+
- ✅ Incluye todas las dependencias necesarias (boto3, mcp, etc.)
- ✅ Los usuarios con `uvx` no necesitan instalar nada globalmente
- ✅ `uvx` maneja automáticamente el entorno virtual y dependencias 