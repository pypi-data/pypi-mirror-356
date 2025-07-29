# Configuración para MCP Job Analyzer Support

## Opción 1: Usar uvx (Recomendado) - Sin instalación

### Configuración con argumentos en mcp.json
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

### Configuración con variables de entorno (Más seguro)
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

## Opción 2: Variables de Entorno del Sistema

### Configuración de Variables de Entorno

Puedes configurar las variables de entorno de las siguientes maneras:

#### Windows (PowerShell)
```powershell
$env:AWS_LOG_GROUP_NAME = "tu-log-group-name"
$env:AWS_ACCESS_KEY_ID = "tu-access-key-id"
$env:AWS_SECRET_ACCESS_KEY = "tu-secret-access-key"
$env:AWS_REGION_NAME = "us-east-1"
```

#### Windows (CMD)
```cmd
set AWS_LOG_GROUP_NAME=tu-log-group-name
set AWS_ACCESS_KEY_ID=tu-access-key-id
set AWS_SECRET_ACCESS_KEY=tu-secret-access-key
set AWS_REGION_NAME=us-east-1
```

#### Linux/macOS (Bash)
```bash
export AWS_LOG_GROUP_NAME="tu-log-group-name"
export AWS_ACCESS_KEY_ID="tu-access-key-id"
export AWS_SECRET_ACCESS_KEY="tu-secret-access-key"
export AWS_REGION_NAME="us-east-1"
```

### Archivo .env (Opcional)
Puedes crear un archivo `.env` en la raíz del proyecto:

```env
AWS_LOG_GROUP_NAME=tu-log-group-name
AWS_ACCESS_KEY_ID=tu-access-key-id
AWS_SECRET_ACCESS_KEY=tu-secret-access-key
AWS_REGION_NAME=us-east-1
```

### Configuración del MCP (mcp.json)

```json
{
  "mcpServers": {
    "SimetrikDatabase": {
        "command": "npx",
        "args": [
          "-y",
          "@modelcontextprotocol/server-postgres",
          "postgresql://productuser:5K05WlsDghQYb4QXbqrC@rds-ro-ur.simetrik.com:5432/product_db"
        ]
      },
      "JobAnalyzerSupport": {
        "command": "C:\\Users\\User\\.local\\bin\\uv.exe",
        "args": [
          "--directory", 
          "C:\\Users\\User\\Documents\\Simetrik\\mcp-support",
          "run",
          "job_analyzer_support.py"
        ]
      }
  }
}
```

## Opción 2: Argumentos de Línea de Comandos

Si prefieres usar argumentos de línea de comandos (menos seguro):

```json
{
  "mcpServers": {
    "JobAnalyzerSupport": {
      "command": "C:\\Users\\User\\.local\\bin\\uv.exe",
      "args": [
        "--directory", 
        "C:\\Users\\User\\Documents\\Simetrik\\mcp-support",
        "run",
        "job_analyzer_support.py",
        "--log-group-name", "tu-log-group-name",
        "--aws-access-key-id", "tu-access-key-id",
        "--aws-secret-access-key", "tu-secret-access-key",
        "--region-name", "us-east-1"
      ]
    }
  }
}
```

## Ventajas de cada opción:

### uvx (Recomendada):
- ✅ **Sin instalación global**: No contamina el sistema
- ✅ **Siempre actualizado**: Usa la última versión automáticamente
- ✅ **Sin dependencias**: No requiere gestión de entornos
- ✅ **Limpio**: Se auto-limpia después del uso
- ✅ **Rápido**: Cache automático para ejecuciones futuras
- ✅ **Multiplataforma**: Funciona igual en Windows, macOS y Linux

### Variables de Entorno del Sistema:
- ✅ Más seguro (credenciales no visibles en configuración)
- ✅ Fácil de gestionar en diferentes entornos
- ✅ Sigue mejores prácticas de seguridad
- ✅ Reutilizable por otras aplicaciones

### Instalación Tradicional (pip):
- ✅ Familiaridad para usuarios de Python
- ❌ Contamina el entorno global
- ❌ Requiere gestión manual de actualizaciones 