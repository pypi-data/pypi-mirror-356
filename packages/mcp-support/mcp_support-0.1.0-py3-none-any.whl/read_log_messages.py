import boto3
import json

def read_log_stream(log_stream_name: str, aws_config: dict):
    """
    Lee los mensajes de un log stream de CloudWatch.
    
    Args:
        log_stream_name (str): Nombre del log stream
        aws_config (dict): Configuración AWS con las siguientes claves:
            - log_group_name: Nombre del log group
            - aws_access_key_id: AWS Access Key ID
            - aws_secret_access_key: AWS Secret Access Key
            - region_name: Región de AWS
    
    Returns:
        str: JSON string con los logs
    """
    log_group_name = aws_config.get('log_group_name')
    aws_access_key_id = aws_config.get('aws_access_key_id')
    aws_secret_access_key = aws_config.get('aws_secret_access_key')
    region_name = aws_config.get('region_name')
    
    if not all([log_group_name, aws_access_key_id, aws_secret_access_key, region_name]):
        raise ValueError("Faltan parámetros de configuración AWS requeridos")
    
    # Create a CloudWatch Logs client
    client = boto3.Session(
        aws_access_key_id=aws_access_key_id, 
        aws_secret_access_key=aws_secret_access_key
    ).client('logs', region_name=region_name)
    
    logs = []
    next_token = None
    last_token = None
    while True:
        kwargs = {'logGroupName': log_group_name, 'logStreamName': log_stream_name, 'startFromHead': True}
        if next_token:
            kwargs['nextToken'] = next_token
        response = client.get_log_events(**kwargs)
        for event in response['events']:
            logs.append({'timestamp': event['timestamp'], 'message': event['message']})
        last_token = next_token
        next_token = response.get('nextForwardToken')
        # Si el token no cambia, ya no hay más páginas
        if not next_token or next_token == last_token:
            break
    return json.dumps(logs)