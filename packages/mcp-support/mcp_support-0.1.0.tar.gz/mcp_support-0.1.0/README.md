# Job Analyzer Support

Herramienta de análisis y soporte de trabajos con integración MCP (Model Context Protocol).

## 🚀 Instalación Rápida con UV

Este proyecto utiliza [UV](https://docs.astral.sh/uv/) para el gestión de dependencias y entornos virtuales.

### Prerequisitos

- Python 3.13 o superior
- UV instalado en tu sistema

### Instalar UV

```bash
# En Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# En macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Con pip (alternativa)
pip install uv
```

### Configuración Automática del Proyecto

```bash
# Clonar el repositorio
git clone <repository-url>
cd job-analyzer-support

# Instalar automáticamente Python 3.13 (si no está instalado) y todas las dependencias
uv sync

# Activar el entorno virtual
source .venv/bin/activate  # En macOS/Linux
# O en Windows:
.venv\Scripts\activate
```

### Instalación en Una Línea

```bash
uv sync && source .venv/bin/activate
```

## 📦 Comandos Útiles

### Gestión de Dependencias

```bash
# Añadir nueva dependencia
uv add nombre-paquete

# Añadir dependencia de desarrollo
uv add --dev pytest

# Actualizar todas las dependencias
uv sync --upgrade

# Mostrar dependencias instaladas
uv pip list
```

### Ejecutar la Aplicación

```bash
# Ejecutar usando el script definido
uv run job-analyzer

# O ejecutar directamente
uv run python main.py
```

### Herramientas de Desarrollo

```bash
# Formatear código con Black
uv run black .

# Ordenar imports con isort  
uv run isort .

# Linting con flake8
uv run flake8 .

# Type checking con mypy
uv run mypy .

# Ejecutar tests
uv run pytest
```

## 🛠️ Desarrollo

### Instalar Dependencias de Desarrollo

```bash
# Las dependencias de desarrollo se instalan automáticamente con uv sync
uv sync --dev
```

### Estructura del Proyecto

```
job-analyzer-support/
├── job_analyzer_support.py    # Módulo principal
├── read_zd_tickets.py         # Lectura de tickets de Zendesk
├── read_log_messages.py       # Lectura de mensajes de log
├── main.py                    # Punto de entrada
├── pyproject.toml             # Configuración del proyecto y dependencias
├── uv.lock                    # Lock file de UV (NO editar manualmente)
├── .python-version            # Versión de Python del proyecto
└── README.md                  # Este archivo
```

## 📋 Características

- ✅ Instalación automática con UV
- ✅ Gestión de entornos virtuales
- ✅ Lock file para reproducibilidad
- ✅ Herramientas de desarrollo preconfiguradas
- ✅ Scripts de proyecto definidos
- ✅ Integración con MCP

## 🔧 Configuración Avanzada

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto para configuraciones locales:

```bash
# .env
DEBUG=true
LOG_LEVEL=info
```

### Configuración de UV

El archivo `pyproject.toml` contiene toda la configuración necesaria para UV. Las herramientas de desarrollo están preconfiguradas con estándares de la industria.

## 🤝 Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🏢 Simetrik

Desarrollado por el equipo de Simetrik para análisis y soporte de trabajos.
