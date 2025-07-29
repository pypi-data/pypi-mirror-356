import requests
from requests.auth import HTTPBasicAuth
import datetime
import json
import csv
import os
import pandas as pd
import argparse
import sys
from collections import Counter
import base64
from datetime import datetime, timedelta
import time

# Configuración: reemplaza estos valores por los de tu organización
ZENDESK_SUBDOMAIN = '' #TODO:: ADD TO ENVIRONMENT VARIABLES
ZENDESK_EMAIL = '' #TODO:: ADD TO ENVIRONMENT VARIABLES
ZENDESK_API_TOKEN = '' #TODO:: ADD TO ENVIRONMENT VARIABLES

BASE_URL = f'https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2'
auth = HTTPBasicAuth(f'{ZENDESK_EMAIL}/token', ZENDESK_API_TOKEN)

# Diccionario para almacenar campos de tickets y sus IDs
TICKET_FIELDS = {}

def format_date(date_str):
    """Formatea la fecha ISO a un formato más legible"""
    if not date_str:
        return "N/A"
    try:
        dt = datetime.datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return date_str

def get_ticket_fields():
    """Obtiene todos los campos de tickets disponibles en Zendesk"""
    url = f'{BASE_URL}/ticket_fields.json'
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        fields = response.json().get('ticket_fields', [])
        for field in fields:
            TICKET_FIELDS[field.get('title', '').lower()] = {
                'id': field.get('id'),
                'type': field.get('type')
            }
        print(f"Se cargaron {len(TICKET_FIELDS)} campos de tickets")
        
        # Buscar específicamente el campo de razón de contacto
        contact_reason_id = None
        for title, data in TICKET_FIELDS.items():
            if 'razón' in title or 'razon' in title or 'motivo' in title or 'contact reason' in title:
                print(f"Posible campo de razón de contacto: {title} (ID: {data['id']})")
                contact_reason_id = data['id']
        
        return contact_reason_id
    else:
        print(f"Error al obtener campos de tickets: {response.status_code}")
        return None

def get_user_name(user_id):
    """Obtiene el nombre del usuario por su ID"""
    if not user_id:
        return "No asignado"
    
    url = f'{BASE_URL}/users/{user_id}.json'
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        user = response.json().get('user', {})
        return user.get('name', f"Usuario {user_id}")
    return f"Usuario {user_id}"

def get_user_email(user_id):
    """Obtiene el email del usuario por su ID"""
    if not user_id:
        return "No asignado"
    url = f'{BASE_URL}/users/{user_id}.json'
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        user = response.json().get('user', {})
        return user.get('email', f"Usuario {user_id}")
    return f"Usuario {user_id}"

def get_organization_name(org_id):
    """Obtiene el nombre de la organización por su ID"""
    if not org_id:
        return "Sin organización"
    
    url = f'{BASE_URL}/organizations/{org_id}.json'
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        org = response.json().get('organization', {})
        return org.get('name', f"Organización {org_id}")
    return f"Organización {org_id}"

def get_ticket_comments(ticket_id):
    """Obtiene los comentarios de un ticket por su ID"""
    url = f'{BASE_URL}/tickets/{ticket_id}/comments.json'
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        comments = response.json().get('comments', [])
        return [c.get('body', '') for c in comments]
    return []

def get_tickets(filters=None, output_format='table', max_tickets=100, keywords=None):
    """
    Obtiene tickets de Zendesk con filtros opcionales y filtra por palabras clave en resumen, razón de contacto y comentarios.
    Esta función puede ser usada como herramienta MCP para exponer la consulta de tickets desde un agente conversacional o API.
    Args:
        filters (dict): Filtros para aplicar a la búsqueda (por ejemplo, {'estado': 'open', 'agente': 'juan@correo.com'})
        output_format (str): Formato de salida ('table', 'json', 'csv', 'pandas')
        max_tickets (int): Número máximo de tickets a recuperar
        keywords (list): Lista de palabras clave para filtrar tickets
    Returns:
        list or pandas.DataFrame: Los tickets recuperados en el formato especificado
    """
    contact_reason_id = get_ticket_fields()
    query = "type:ticket"
    if filters:
        for key, value in filters.items():
            if key == 'id':
                query += f" id:{value}"
            elif key == 'agente' or key == 'assignee':
                query += f" assignee:{value}"
            elif key == 'resumen' or key == 'subject':
                query += f" subject:\"{value}\""
            elif key == 'organizacion' or key == 'organization':
                query += f" organization:\"{value}\""
            elif key == 'estado' or key == 'status':
                query += f" status:{value}"
            elif key == 'fecha_solicitud' or key == 'created':
                query += f" created:{value}"
            elif key == 'fecha_actualizacion' or key == 'updated':
                query += f" updated:{value}"
            elif key == 'cliente' or key == 'requester':
                query += f" requester:\"{value}\""
            elif key == 'razon_contacto' or key == 'contact_reason':
                if contact_reason_id:
                    query += f" fieldvalue:{contact_reason_id} \"{value}\""
                else:
                    query += f" fieldvalue:\"razón de contacto\" \"{value}\""
    params = {
        'query': query,
        'include': 'users,organizations',
        'sort_by': 'created_at',
        'sort_order': 'desc',
        'per_page': 100
    }
    all_tickets = []
    users = {}
    organizations = {}
    url = f'{BASE_URL}/search.json'
    while len(all_tickets) < max_tickets and url:
        # Construir el curl equivalente
        auth_str = f"{ZENDESK_EMAIL}/token:{ZENDESK_API_TOKEN}"
        b64_auth = base64.b64encode(auth_str.encode()).decode()
        if params:
            param_str = '&'.join([f"{k}={requests.utils.quote(str(v))}" for k, v in params.items()])
            full_url = f"{url}?{param_str}"
        else:
            full_url = url
        print(f"\nCURL equivalente:")
        print(f"curl -X GET '{full_url}' -H 'Authorization: Basic {b64_auth}'")
        if params:
            response = requests.get(url, auth=auth, params=params)
        else:
            response = requests.get(url, auth=auth)
        print(f"Status code: {response.status_code}")
        if response.status_code != 200:
            print(f'Error al buscar tickets: {response.status_code} - {response.text}')
            break
        data = response.json()
        tickets = data.get('results', [])
        if not tickets:
            break
        all_tickets.extend(tickets)
        for user in data.get('users', []):
            users[user['id']] = user
        for org in data.get('organizations', []):
            organizations[org['id']] = org
        next_page = data.get('next_page')
        if not next_page:
            break
        url = next_page
        params = None
    all_tickets = all_tickets[:max_tickets]
    processed_tickets = []
    agentes_lista = None
    if filters and 'agente' in filters and filters['agente']:
        agentes_lista = [a.strip().lower() for a in filters['agente'].split(',')]
    for ticket in all_tickets:
        assignee_id = ticket.get('assignee_id')
        assignee_name = "No asignado"
        if assignee_id:
            if assignee_id in users:
                assignee_name = users[assignee_id].get('email', "No asignado")
            else:
                assignee_name = get_user_email(assignee_id)
        org_id = ticket.get('organization_id')
        org_name = "Sin organización"
        if org_id and org_id in organizations:
            org_name = organizations[org_id].get('name', "Sin organización")
        requester_id = ticket.get('requester_id')
        requester_name = "Desconocido"
        if requester_id and requester_id in users:
            requester_name = users[requester_id].get('name', "Desconocido")
        custom_fields = ticket.get('custom_fields', [])
        contact_reason = "No especificado"
        for field in custom_fields:
            if contact_reason_id and field.get('id') == contact_reason_id:
                if field.get('value'):
                    contact_reason = field.get('value')
                break
        created_at = format_date(ticket.get('created_at'))
        updated_at = format_date(ticket.get('updated_at'))
        resumen = ticket.get('subject', "")
        match = False
        if keywords:
            texto_busqueda = f"{resumen} {contact_reason}".lower()
            for kw in keywords:
                if kw in texto_busqueda:
                    match = True
                    break
            if not match:
                comentarios = get_ticket_comments(ticket.get('id'))
                for comentario in comentarios:
                    if any(kw in comentario.lower() for kw in keywords):
                        match = True
                        break
        else:
            match = True
        if match:
            if agentes_lista:
                if assignee_name.lower() not in agentes_lista:
                    continue
            processed_ticket = {
                'id': ticket.get('id', "N/A"),
                'agente_asignado': assignee_name,
                'resumen_solicitud': resumen,
                'estado': ticket.get('status', "N/A"),
                'fecha_solicitud': created_at,
                'fecha_actualizacion': updated_at,
                'cliente': requester_name
            }
            processed_tickets.append(processed_ticket)
    if output_format == 'json':
        return processed_tickets
    elif output_format == 'pandas':
        return pd.DataFrame(processed_tickets)
    elif output_format == 'csv':
        return processed_tickets
    else:
        return processed_tickets

def display_table(tickets):
    """Muestra los tickets en formato de tabla en la consola (sin organizacion ni razon_contacto)"""
    if not tickets:
        print("No se encontraron tickets que coincidan con los criterios.")
        return
    col_widths = {
        'id': 10,
        'agente_asignado': 30,
        'resumen_solicitud': 30,
        'estado': 15,
        'fecha_solicitud': 20,
        'fecha_actualizacion': 20,
        'cliente': 20
    }
    header = " | ".join([
        "ID".ljust(col_widths['id']),
        "Agente Asignado".ljust(col_widths['agente_asignado']),
        "Resumen de Solicitud".ljust(col_widths['resumen_solicitud']),
        "Estado".ljust(col_widths['estado']),
        "Fecha Solicitud".ljust(col_widths['fecha_solicitud']),
        "Última Actualización".ljust(col_widths['fecha_actualizacion']),
        "Cliente".ljust(col_widths['cliente'])
    ])
    print("\n" + header)
    print("-" * len(header))
    for ticket in tickets:
        resumen = ticket['resumen_solicitud']
        if len(resumen) > col_widths['resumen_solicitud'] - 3:
            resumen = resumen[:col_widths['resumen_solicitud'] - 3] + "..."
        agente = ticket['agente_asignado']
        if len(agente) > col_widths['agente_asignado'] - 2:
            agente = agente[:col_widths['agente_asignado'] - 2] + ".."
        row = " | ".join([
            str(ticket['id']).ljust(col_widths['id']),
            agente.ljust(col_widths['agente_asignado']),
            resumen.ljust(col_widths['resumen_solicitud']),
            ticket['estado'].ljust(col_widths['estado']),
            ticket['fecha_solicitud'].ljust(col_widths['fecha_solicitud']),
            ticket['fecha_actualizacion'].ljust(col_widths['fecha_actualizacion']),
            ticket['cliente'].ljust(col_widths['cliente'])
        ])
        print(row)

def save_to_csv(tickets, filename='zendesk_tickets.csv'):
    """Guarda los tickets en un archivo CSV (sin organizacion ni razon_contacto)"""
    if not tickets:
        print("No hay tickets para guardar.")
        return
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            # Excluir 'organizacion' y 'razon_contacto' si existen
            fieldnames = [k for k in tickets[0].keys() if k not in ['organizacion', 'razon_contacto']]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for ticket in tickets:
                ticket = {k: v for k, v in ticket.items() if k in fieldnames}
                writer.writerow(ticket)
        print(f"Tickets guardados en {filename}")
    except Exception as e:
        print(f"Error al guardar el archivo CSV: {e}")

def save_to_json(tickets, filename='zendesk_tickets.json'):
    """Guarda los tickets en un archivo JSON"""
    if not tickets:
        print("No hay tickets para guardar.")
        return
    
    try:
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(tickets, jsonfile, ensure_ascii=False, indent=4)
            
        print(f"Tickets guardados en {filename}")
    except Exception as e:
        print(f"Error al guardar el archivo JSON: {e}")

def save_to_excel(tickets, filename='zendesk_tickets.xlsx'):
    """Guarda los tickets en un archivo Excel"""
    if not tickets:
        print("No hay tickets para guardar.")
        return
    
    try:
        df = pd.DataFrame(tickets)
        df.to_excel(filename, index=False)
        print(f"Tickets guardados en {filename}")
    except Exception as e:
        print(f"Error al guardar el archivo Excel: {e}")

def print_assigned_agents(tickets):
    agentes = set()
    for t in tickets:
        if t.get('agente_asignado'):
            agentes.add(t['agente_asignado'])
    print("\nAgentes asignados encontrados en los tickets:")
    for a in sorted(agentes):
        print(f"- {a}")

def analyze_tickets_stats(tickets):
    """Analiza y muestra estadísticas históricas de tickets relacionados con asientos este año por mes."""
    current_year = datetime.now().year
    months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    month_counter = Counter()
    for t in tickets:
        try:
            fecha = t['fecha_solicitud'][:10]
            year, month, _ = map(int, fecha.split('-'))
            if year == current_year:
                month_counter[month] += 1
        except:
            continue
    print("\nEstadística de tickets relacionados con asientos/cambios de asiento este año:")
    for m in range(1, 13):
        print(f"{months[m-1]}: {month_counter[m]} tickets")

def print_agent_steps_report(tickets, output_file='informe_pasos_agentes.txt'):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("INFORME DE PASOS REALIZADOS POR LOS AGENTES PARA RESOLVER CADA REQUERIMIENTO:\n")
        for t in tickets:
            f.write(f"\nTicket ID: {t['id']}\n")
            f.write(f"Agente asignado: {t['agente_asignado']}\n")
            f.write(f"Estado: {t['estado']}\n")
            f.write(f"Fecha de solicitud: {t['fecha_solicitud']}\n")
            f.write(f"Resumen: {t['resumen_solicitud']}\n")
            comentarios = get_ticket_comments(t['id'])
            agente_email = t['agente_asignado']
            pasos = []
            agente_id = None
            for user in users.values():
                if user.get('email', '').lower() == agente_email.lower():
                    agente_id = user['id']
                    break
            if agente_id:
                url = f'{BASE_URL}/tickets/{t['id']}/comments.json'
                response = requests.get(url, auth=auth)
                if response.status_code == 200:
                    comments = response.json().get('comments', [])
                    for c in comments:
                        if c.get('author_id') == agente_id:
                            pasos.append(c.get('body', '').strip())
            if pasos:
                f.write("Pasos realizados por el agente:\n")
                for i, paso in enumerate(pasos, 1):
                    f.write(f"  {i}. {paso}\n")
            else:
                f.write("No hay comentarios del agente asignado para este ticket.\n")
    print(f"\nInforme guardado en {output_file}")

def count_tickets_with_asiento_in_comments(tickets):
    count = 0
    tickets_with_asiento = []
    for t in tickets:
        comentarios = get_ticket_comments(t['id'])
        if any('asiento' in c.lower() or 'asientos' in c.lower() for c in comentarios):
            count += 1
            tickets_with_asiento.append(t['id'])
    print(f"\nCantidad de tickets con al menos un comentario que contiene 'asiento' o 'asientos': {count}")
    print(f"IDs de tickets: {tickets_with_asiento}")

def process_prompt(prompt):
    """
    Procesa un prompt de usuario para filtrar y mostrar tickets
    
    Ejemplos de prompts:
    - "mostrar tickets con estado abierto"
    - "buscar tickets de la organización Simetrik"
    - "filtrar por agente Juan Pérez y exportar a excel"
    - "tickets creados en los últimos 7 días en formato json"
    """
    # Inicializamos variables
    filters = {}
    output_format = 'table'
    export_format = None
    max_tickets = 100
    
    # Procesamos el prompt para extraer filtros
    prompt = prompt.lower()
    
    # Detectamos el formato de salida
    if 'json' in prompt:
        export_format = 'json'
    elif 'csv' in prompt:
        export_format = 'csv'
    elif 'excel' in prompt:
        export_format = 'excel'
    
    # Detectamos filtros de estado
    status_keywords = {
        'abierto': 'open',
        'pendiente': 'pending',
        'resuelto': 'solved',
        'cerrado': 'closed',
        'caso problema': 'problem_case',
        'en gestión': 'hold',
        'en gestión': 'hold',
        'en gestión': 'hold',
        'en gestión': 'hold'
    }
    
    for es_status, en_status in status_keywords.items():
        if f"estado {es_status}" in prompt or f"status {en_status}" in prompt:
            filters['estado'] = en_status
    
    # Filtro por organización
    if 'organización' in prompt or 'organizacion' in prompt:
        for word in prompt.split():
            if word not in ['organización', 'organizacion', 'organization']:
                next_index = prompt.split().index(word) + 1
                if next_index < len(prompt.split()):
                    filters['organizacion'] = prompt.split()[next_index]
    
    # Filtro por agente (ahora permite lista separada por comas)
    if 'agente' in prompt or 'assignee' in prompt:
        agent_index = prompt.find('agente') + 7 if 'agente' in prompt else prompt.find('assignee') + 9
        if agent_index < len(prompt):
            agent_names = prompt[agent_index:].split(' en ')[0].split(' y ')[0].strip()
            filters['agente'] = agent_names  # Puede ser lista separada por comas
    
    # Filtro por cliente
    if 'cliente' in prompt or 'requester' in prompt:
        client_index = prompt.find('cliente') + 8 if 'cliente' in prompt else prompt.find('requester') + 10
        if client_index < len(prompt):
            client_name = prompt[client_index:].split(' y ')[0].split(' en ')[0].strip()
            filters['cliente'] = client_name
    
    # Filtro por fecha
    if 'últimos' in prompt or 'ultimos' in prompt or 'last' in prompt:
        # Extraemos el número de días
        for word in prompt.split():
            if word.isdigit():
                days = int(word)
                today = datetime.now()
                past_date = today - datetime.timedelta(days=days)
                filters['fecha_solicitud'] = f">={past_date.strftime('%Y-%m-%d')}"
    
    # Filtro por razón de contacto
    if 'razón de contacto' in prompt or 'razon de contacto' in prompt or 'motivo' in prompt:
        reason_index = -1
        if 'razón de contacto' in prompt:
            reason_index = prompt.find('razón de contacto') + 17
        elif 'razon de contacto' in prompt:
            reason_index = prompt.find('razon de contacto') + 16
        elif 'motivo' in prompt:
            reason_index = prompt.find('motivo') + 7
            
        if reason_index > 0 and reason_index < len(prompt):
            reason = prompt[reason_index:].split(' y ')[0].split(' en ')[0].strip()
            filters['razon_contacto'] = reason
    
    # Procesamos el número máximo de tickets
    if 'limitar' in prompt or 'limit' in prompt:
        for word in prompt.split():
            if word.isdigit():
                max_tickets = int(word)
    
    # Palabras clave para búsqueda sensible de asientos
    keywords = [
        'modificar asiento', 'editar asiento', 'cambiar estado de asiento',
        'modificar estado de asiento', 'asiento editado', 'asiento modificado',
        'asientos', 'asiento'
    ]
    # Permitir palabras clave personalizadas desde el prompt
    if 'tc' in prompt or 'traductor contable' in prompt or 'accounting' in prompt:
        keywords = ['tc', 'traductor contable', 'accounting']
    # Detectar si el prompt requiere búsqueda sensible de asientos o personalizada
    buscar_asiento = any(kw in prompt for kw in keywords)
    
    # Detectar filtro de tickets del último mes
    if ('último mes' in prompt or 'ultimo mes' in prompt or 'últimos 30 días' in prompt or 'ultimos 30 dias' in prompt):
        fecha_inicio = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        filters['fecha_solicitud'] = f'>={fecha_inicio}'
    
    # Obtenemos los tickets con los filtros aplicados y palabras clave si corresponde
    tickets = get_tickets(filters, output_format='json', max_tickets=max_tickets, keywords=keywords if buscar_asiento else None)
    print_assigned_agents(tickets)
    analyze_tickets_stats(tickets)
    
    # Mostrar resumen de los tickets encontrados si la búsqueda es personalizada
    if keywords == ['tc', 'traductor contable', 'accounting']:
        print('\nResumen de tickets relacionados con TC, traductor contable o accounting:')
        for t in tickets:
            print(f"ID: {t['id']} | Agente: {t['agente_asignado']} | Estado: {t['estado']} | Fecha: {t['fecha_solicitud']} | Resumen: {t['resumen_solicitud']}")
    
    # Mostrar informe de pasos realizados por los agentes si se solicita en el prompt
    if 'pasos' in prompt or 'resolución' in prompt or 'resolver' in prompt:
        print_agent_steps_report(tickets)
    
    # Contar tickets con comentarios que contienen 'asiento' o 'asientos' si se solicita en el prompt
    if 'comentario' in prompt or 'nota interna' in prompt or 'respuesta pública' in prompt or 'asiento' in prompt:
        count_tickets_with_asiento_in_comments(tickets)
    
    # Mostramos los resultados
    display_table(tickets)
    
    # Exportamos si es necesario
    if export_format == 'json':
        save_to_json(tickets)
    elif export_format == 'csv':
        save_to_csv(tickets)
    elif export_format == 'excel':
        save_to_excel(tickets)
    
    return tickets

def tickets_with_asiento_in_summary_and_comments_last_month():
    import csv
    # Calcular fecha de hace 30 días
    fecha_inicio = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    # Construir query para Zendesk Search API
    query = f'type:ticket created:>={fecha_inicio} asiento'
    params = {
        'query': query,
        'sort_by': 'created_at',
        'sort_order': 'desc',
        'per_page': 100
    }
    all_tickets = []
    users = {}
    organizations = {}
    url = f'{BASE_URL}/search.json'
    while url:
        response = requests.get(url, auth=auth, params=params)
        print(f"Status code: {response.status_code}")
        if response.status_code != 200:
            print(f'Error al buscar tickets: {response.status_code} - {response.text}')
            break
        data = response.json()
        tickets = data.get('results', [])
        if not tickets:
            break
        all_tickets.extend(tickets)
        for user in data.get('users', []):
            users[user['id']] = user
        for org in data.get('organizations', []):
            organizations[org['id']] = org
        next_page = data.get('next_page')
        if not next_page:
            break
        url = next_page
        params = None
    # Ahora buscar en comentarios públicos y notas internas
    tickets_with_asiento = []
    comentarios_relevantes = []
    for t in all_tickets:
        ticket_id = t.get('id')
        resumen = t.get('subject', '')
        # Si el resumen ya contiene 'asiento', lo incluimos
        resumen_match = 'asiento' in resumen.lower() or 'asientos' in resumen.lower()
        comentarios_match = False
        comentarios_encontrados = []
        # Buscar en comentarios
        url_comments = f'{BASE_URL}/tickets/{ticket_id}/comments.json'
        response_comments = requests.get(url_comments, auth=auth)
        if response_comments.status_code == 200:
            comments = response_comments.json().get('comments', [])
            for c in comments:
                if 'asiento' in c.get('body', '').lower() or 'asientos' in c.get('body', '').lower():
                    comentarios_match = True
                    comentarios_encontrados.append({
                        'public': c.get('public', False),
                        'body': c.get('body', ''),
                        'author_id': c.get('author_id')
                    })
        if resumen_match or comentarios_match:
            tickets_with_asiento.append(t)
            for c in comentarios_encontrados:
                comentarios_relevantes.append({
                    'ticket_id': ticket_id,
                    'resumen': resumen,
                    'public': c['public'],
                    'body': c['body'],
                    'author_id': c['author_id']
                })
    print(f"\nCantidad de tickets del último mes con 'asiento' en resumen o comentarios: {len(tickets_with_asiento)}")
    # Exportar CSV de tickets
    if tickets_with_asiento:
        with open('tickets_asiento_ultimo_mes.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'subject', 'status', 'created_at', 'updated_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for t in tickets_with_asiento:
                writer.writerow({k: t.get(k, '') for k in fieldnames})
        print("Listado de tickets exportado en tickets_asiento_ultimo_mes.csv")
    # Exportar TXT de comentarios relevantes
    if comentarios_relevantes:
        with open('comentarios_asiento_ultimo_mes.txt', 'w', encoding='utf-8') as f:
            for c in comentarios_relevantes:
                f.write(f"Ticket ID: {c['ticket_id']} | Público: {c['public']} | Autor: {c['author_id']}\n")
                f.write(f"Resumen: {c['resumen']}\n")
                f.write(f"Comentario: {c['body']}\n\n")
        print("Comentarios relevantes exportados en comentarios_asiento_ultimo_mes.txt")
    else:
        print("No se encontraron comentarios relevantes con 'asiento' o 'asientos'.")

def export_comments_ticket_43575():
    import csv
    ticket_id = 43575
    url = f'{BASE_URL}/tickets/{ticket_id}/comments.json'
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        comments = response.json().get('comments', [])
        with open('comentarios_ticket_43575.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['ticket_id', 'fecha', 'author_email', 'public', 'body']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for c in comments:
                author_id = c.get('author_id', '')
                # Obtener email del usuario
                email = None
                user_url = f'{BASE_URL}/users/{author_id}.json'
                user_resp = requests.get(user_url, auth=auth)
                if user_resp.status_code == 200:
                    user = user_resp.json().get('user', {})
                    email = user.get('email', author_id)
                else:
                    email = author_id
                writer.writerow({
                    'ticket_id': ticket_id,
                    'fecha': c.get('created_at', ''),
                    'author_email': email,
                    'public': c.get('public', ''),
                    'body': c.get('body', '').replace('\n', ' ').replace('\r', ' ')
                })
        print('Archivo comentarios_ticket_43575.csv generado.')
    else:
        print('No se pudieron obtener los comentarios del ticket 43575.')

def analizar_comentarios_asiento_ultimo_mes():
    from datetime import datetime, timedelta
    fecha_inicio = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    query = f'type:ticket created:>={fecha_inicio}'
    params = {
        'query': query,
        'sort_by': 'created_at',
        'sort_order': 'desc',
        'per_page': 100
    }
    all_tickets = []
    url = f'{BASE_URL}/search.json'
    page_count = 0
    while url:
        page_count += 1
        print(f"Buscando página {page_count} de tickets...")
        response = requests.get(url, auth=auth, params=params)
        if response.status_code != 200:
            print(f'Error al buscar tickets: {response.status_code} - {response.text}')
            break
        data = response.json()
        tickets = data.get('results', [])
        if not tickets:
            break
        all_tickets.extend(tickets)
        next_page = data.get('next_page')
        if not next_page:
            break
        url = next_page
        params = None
    print(f"\nTotal de tickets creados en el último mes: {len(all_tickets)}")
    print("IDs de tickets recuperados:", [t.get('id') for t in all_tickets])
    encontrados = 0
    for t in all_tickets:
        ticket_id = t.get('id')
        url_comments = f'{BASE_URL}/tickets/{ticket_id}/comments.json'
        response_comments = requests.get(url_comments, auth=auth)
        if response_comments.status_code == 200:
            comments = response_comments.json().get('comments', [])
            comentarios_asiento = []
            for c in comments:
                texto = c.get('body', '').lower()
                if 'asiento' in texto or 'asientos' in texto:
                    # Obtener email del autor
                    author_id = c.get('author_id', '')
                    email = None
                    user_url = f'{BASE_URL}/users/{author_id}.json'
                    user_resp = requests.get(user_url, auth=auth)
                    if user_resp.status_code == 200:
                        user = user_resp.json().get('user', {})
                        email = user.get('email', author_id)
                    else:
                        email = author_id
                    comentarios_asiento.append({
                        'fecha': c.get('created_at', ''),
                        'author_email': email,
                        'public': c.get('public', ''),
                        'body': c.get('body', '').replace('\n', ' ').replace('\r', ' ')
                    })
            if comentarios_asiento:
                encontrados += 1
                print(f"\nTicket ID: {ticket_id}")
                for i, c in enumerate(comentarios_asiento, 1):
                    resumen = c['body'][:120] + ('...' if len(c['body']) > 120 else '')
                    print(f"  Comentario {i} | Fecha: {c['fecha']} | Autor: {c['author_email']} | Público: {c['public']}")
                    print(f"    Resumen: {resumen}")
    print(f"\nTotal de tickets con comentarios que contienen 'asiento': {encontrados}")

def analizar_comentarios_asiento_ultimo_mes_incremental():
    from datetime import datetime, timedelta
    import time
    # Calcular timestamp de hace 90 días
    fecha_inicio = datetime.now() - timedelta(days=90)
    start_time = int(time.mktime(fecha_inicio.timetuple()))
    url = f'{BASE_URL}/incremental/tickets.json?start_time={start_time}'
    all_tickets = []
    page_count = 0
    while url:
        page_count += 1
        print(f"Buscando página {page_count} de tickets (incremental)...")
        response = requests.get(url, auth=auth)
        if response.status_code != 200:
            print(f'Error al buscar tickets: {response.status_code} - {response.text}')
            break
        data = response.json()
        tickets = data.get('tickets', [])
        if not tickets:
            break
        all_tickets.extend(tickets)
        if data.get('end_of_stream'):
            break
        url = data.get('next_page')
    print(f"\nTotal de tickets creados en los últimos 3 meses (incremental): {len(all_tickets)}")
    print("IDs de tickets recuperados:", [t.get('id') for t in all_tickets])
    encontrados = 0
    resumenes = []
    for t in all_tickets:
        ticket_id = t.get('id')
        url_comments = f'{BASE_URL}/tickets/{ticket_id}/comments.json'
        response_comments = requests.get(url_comments, auth=auth)
        if response_comments.status_code == 200:
            comments = response_comments.json().get('comments', [])
            comentarios_asiento = []
            for c in comments:
                texto = c.get('body', '').lower()
                if 'asiento' in texto or 'asientos' in texto:
                    # Obtener email del autor
                    author_id = c.get('author_id', '')
                    email = None
                    user_url = f'{BASE_URL}/users/{author_id}.json'
                    user_resp = requests.get(user_url, auth=auth)
                    if user_resp.status_code == 200:
                        user = user_resp.json().get('user', {})
                        email = user.get('email', author_id)
                    else:
                        email = author_id
                    comentarios_asiento.append({
                        'fecha': c.get('created_at', ''),
                        'author_email': email,
                        'public': c.get('public', ''),
                        'body': c.get('body', '').replace('\n', ' ').replace('\r', ' ')
                    })
            if comentarios_asiento:
                encontrados += 1
                resumen_ticket = f"\nTicket ID: {ticket_id}\n"
                for i, c in enumerate(comentarios_asiento, 1):
                    resumen = c['body'][:120] + ('...' if len(c['body']) > 120 else '')
                    resumen_ticket += f"  Comentario {i} | Fecha: {c['fecha']} | Autor: {c['author_email']} | Público: {c['public']}\n"
                    resumen_ticket += f"    Resumen: {resumen}\n"
                resumenes.append(resumen_ticket)
    with open('resumen_asiento_incremental.txt', 'w', encoding='utf-8') as f:
        f.write(f"Total de tickets con comentarios que contienen 'asiento': {encontrados}\n\n")
        for r in resumenes:
            f.write(r + '\n')
    print(f"\nResumen guardado en resumen_asiento_incremental.txt. Total de tickets con comentarios que contienen 'asiento': {encontrados}")

def main():
    parser = argparse.ArgumentParser(description='Consulta y filtra tickets de Zendesk')
    parser.add_argument('--prompt', help='Prompt para filtrar tickets', default=None)
    parser.add_argument('--estado', help='Filtrar por estado', default=None)
    parser.add_argument('--organizacion', help='Filtrar por organización', default=None)
    parser.add_argument('--agente', help='Filtrar por agente asignado', default=None)
    parser.add_argument('--cliente', help='Filtrar por cliente', default=None)
    parser.add_argument('--razon', help='Filtrar por razón de contacto', default=None)
    parser.add_argument('--formato', help='Formato de salida (table, json, csv, excel)', default='table')
    parser.add_argument('--max', help='Número máximo de tickets', type=int, default=100)
    
    args = parser.parse_args()
    
    # Si se proporciona un prompt, lo procesamos
    if args.prompt:
        if 'analizar_comentarios_asiento_ultimo_mes_incremental' in args.prompt:
            analizar_comentarios_asiento_ultimo_mes_incremental()
        elif 'analizar_comentarios_asiento_ultimo_mes' in args.prompt:
            analizar_comentarios_asiento_ultimo_mes()
        elif 'comentarios_ticket_43575' in args.prompt:
            export_comments_ticket_43575()
        elif 'solo_comentarios_asiento' in args.prompt or 'asiento' in args.prompt and ('último mes' in args.prompt or 'ultimo mes' in args.prompt or 'últimos 30 días' in args.prompt or 'ultimos 30 dias' in args.prompt):
            tickets_with_asiento_in_summary_and_comments_last_month()
        else:
            process_prompt(args.prompt)
        return
    
    # Si no hay prompt, usamos los argumentos individuales
    filters = {}
    if args.estado:
        filters['estado'] = args.estado
    if args.organizacion:
        filters['organizacion'] = args.organizacion
    if args.agente:
        filters['agente'] = args.agente
    if args.cliente:
        filters['cliente'] = args.cliente
    if args.razon:
        filters['razon_contacto'] = args.razon
    
    # Obtenemos los tickets
    tickets = get_tickets(filters, output_format='json', max_tickets=args.max)
    print_assigned_agents(tickets)
    analyze_tickets_stats(tickets)
    
    # Mostramos o exportamos según el formato solicitado
    if args.formato == 'table':
        display_table(tickets)
    elif args.formato == 'json':
        save_to_json(tickets)
    elif args.formato == 'csv':
        save_to_csv(tickets)
    elif args.formato == 'excel':
        save_to_excel(tickets)

if __name__ == '__main__':
    if len(sys.argv) > 1 and not sys.argv[1].startswith('--'):
        prompt = ' '.join(sys.argv[1:])
        if 'analizar_comentarios_asiento_ultimo_mes_incremental' in prompt:
            analizar_comentarios_asiento_ultimo_mes_incremental()
        elif 'analizar_comentarios_asiento_ultimo_mes' in prompt:
            analizar_comentarios_asiento_ultimo_mes()
        elif 'comentarios_ticket_43575' in prompt:
            export_comments_ticket_43575()
        elif 'solo_comentarios_asiento' in prompt or 'asiento' in prompt and ('último mes' in prompt or 'ultimo mes' in prompt or 'últimos 30 días' in prompt or 'ultimos 30 dias' in prompt):
            tickets_with_asiento_in_summary_and_comments_last_month()
        else:
            process_prompt(prompt)
    else:
        main()
