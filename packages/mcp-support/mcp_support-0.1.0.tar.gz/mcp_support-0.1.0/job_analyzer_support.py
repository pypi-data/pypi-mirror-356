import argparse
import os
import sys
from mcp.server.fastmcp import FastMCP
from read_log_messages import read_log_stream
from read_zd_tickets import get_tickets

# Variables globales para AWS
AWS_CONFIG = {}

# Inicializa el servidor MCP con el nombre 'job-analyzer-support'
mcp = FastMCP("job-analyzer-support")

@mcp.tool()
async def get_logs_from_cloudwatch(log_stream_name: str) -> str:
    """Obtiene logs de CloudWatch reales."""
    return read_log_stream(log_stream_name, AWS_CONFIG)

@mcp.prompt()
def analizar_ejecucion_job(job_id: str) -> str:
    return f"""
Ejecuta una query para obtener el valor de la columna 'log_id' de la tabla reconciliation_executejobs donde id = {job_id}. Luego, consulta todos los log messages de CloudWatch usando el log_id como log_stream_name. Una vez obtenidos todos los mensajes del log stream, analiza la secuencia de eventos y genera un informe detallado que incluya:

- Un resumen paso a paso de cada acción ejecutada durante el job, indicando el orden y el propósito de cada paso.
- La identificación y explicación de cualquier mensaje de error encontrado, detallando la causa probable del error.
- La transacción o proceso específico que generó el error, incluyendo información relevante como identificadores, parámetros o datos involucrados.
- Deja ver el mensaje de error completo.
- Si es posible, sugiere acciones o recomendaciones para resolver los errores detectados.

Presenta el informe de manera clara y estructurada, facilitando la comprensión tanto técnica como operativa.
"""

@mcp.tool()
def obtener_tickets_zendesk(filters: dict = None, max_tickets: int = 100, keywords: list = None) -> list:
    """Obtiene tickets de Zendesk con filtros opcionales y palabras clave."""
    return get_tickets(filters=filters, output_format='json', max_tickets=max_tickets, keywords=keywords)

@mcp.prompt()
def buscar_tickets_zendesk(descripcion: str) -> str:
    """Permite buscar tickets de Zendesk usando una descripción en lenguaje natural (por ejemplo: 'tickets abiertos del último mes asignados a Juan')."""
    from read_zd_tickets import process_prompt
    tickets = process_prompt(descripcion)
    return f"Se encontraron {len(tickets)} tickets. Ejemplo: {tickets[:3]}"

def load_aws_config(args=None):
    """Carga la configuración AWS desde argumentos de línea de comandos o variables de entorno."""
    config = {}
    
    # Prioridad: argumentos de línea de comandos, luego variables de entorno
    if args:
        # Usar argumentos de línea de comandos si están disponibles
        config = {
            'log_group_name': args.log_group_name,
            'aws_access_key_id': args.aws_access_key_id,
            'aws_secret_access_key': args.aws_secret_access_key,
            'region_name': args.region_name or 'us-east-1'
        }
    else:
        # Usar variables de entorno como fallback
        env_mapping = {
            'log_group_name': 'AWS_LOG_GROUP_NAME',
            'aws_access_key_id': 'AWS_ACCESS_KEY_ID', 
            'aws_secret_access_key': 'AWS_SECRET_ACCESS_KEY',
            'region_name': 'AWS_REGION_NAME'
        }
        
        missing_vars = []
        
        for config_key, env_var in env_mapping.items():
            value = os.getenv(env_var)
            if config_key == 'region_name' and not value:
                # Región por defecto si no está configurada
                config[config_key] = 'us-east-1'
            elif not value:
                missing_vars.append(env_var)
            else:
                config[config_key] = value
        
        if missing_vars:
            raise ValueError(f"Faltan las siguientes variables de entorno: {', '.join(missing_vars)}")
    
    # Validar que todos los valores requeridos estén presentes
    required_keys = ['log_group_name', 'aws_access_key_id', 'aws_secret_access_key']
    missing_keys = [key for key in required_keys if not config.get(key)]
    
    if missing_keys:
        raise ValueError(f"Faltan los siguientes parámetros de configuración: {', '.join(missing_keys)}")
    
    return config

def main():
    """Función principal que maneja argumentos de línea de comandos y variables de entorno."""
    parser = argparse.ArgumentParser(description='Job Analyzer Support MCP Server')
    parser.add_argument('--log-group-name', help='AWS CloudWatch Log Group Name')
    parser.add_argument('--aws-access-key-id', help='AWS Access Key ID')
    parser.add_argument('--aws-secret-access-key', help='AWS Secret Access Key')
    parser.add_argument('--region-name', default='us-east-1', help='AWS Region Name (default: us-east-1)')
    
    args = parser.parse_args()
    
    try:
        # Configurar las variables globales de AWS
        global AWS_CONFIG
        
        # Si se proporcionaron argumentos de línea de comandos, úsalos
        if any([args.log_group_name, args.aws_access_key_id, args.aws_secret_access_key]):
            AWS_CONFIG = load_aws_config(args)
        else:
            AWS_CONFIG = load_aws_config()
        
        # Ejecutar el servidor MCP (sin prints de debug para no interferir con el protocolo MCP)
        mcp.run(transport='stdio')
        
    except ValueError as e:
        print(f"Error de configuracion: {e}")
        print("\nOpciones de configuracion:")
        print("1. Usar argumentos de linea de comandos:")
        print("   --log-group-name tu-log-group-name")
        print("   --aws-access-key-id tu-access-key-id") 
        print("   --aws-secret-access-key tu-secret-access-key")
        print("   --region-name us-east-1")
        print("\n2. Usar variables de entorno:")
        print("   AWS_LOG_GROUP_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME")
        exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        exit(1)

if __name__ == "__main__":
    main()
