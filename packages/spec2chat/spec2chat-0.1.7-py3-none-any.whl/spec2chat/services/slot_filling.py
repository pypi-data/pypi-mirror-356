"""
spec2chat - A Python library for building task-oriented conversational systems from OpenAPI service specifications.

Author: M. Jesús Rodríguez
License: Apache 2.0 License
Version: 0.1.6
Repository: https://github.com/mjesusrodriguez/spec2chat
Created on 17/05/2025 by M. Jesús Rodríguez
"""

import json
import openai
from bson import ObjectId

from spec2chat.db.mongo import MongoDB
from spec2chat.utils.openai_config import configure_openai

db = MongoDB()

def extract_schema_properties(schema):
    """
    Función auxiliar para extraer las propiedades de un esquema referenciado en los components.
    """
    slots = []
    if 'properties' in schema:
        for prop_name, prop_details in schema['properties'].items():
            slots.append(prop_name)
    return slots

def extract_slots(intent, service_id, domain):
    # Asegurarte de que el intent comienza con "/"
    if not intent.startswith("/"):
        intent = "/" + intent
        print("el intent es ", intent)

    # Busco el servicio por id
    services = db.get_collection(domain, 'services')
    document = services.find_one({"_id": ObjectId(service_id)})

    if not document:
        raise ValueError(f"No se encontró ningún servicio con el ID: {service_id}")

    json_wsl = document

    if 'paths' not in json_wsl:
        raise ValueError("El documento no contiene 'paths', que es necesario para extraer los endpoints.")

    # Verifica si la ruta existe en paths
    if intent not in json_wsl['paths']:
        raise ValueError(f"No se encontró el endpoint con el intent: {intent}")

    slots = []

    # Función auxiliar para resolver referencias ($ref)
    def resolve_reference(ref):
        ref_path = ref.split('/')[1:]
        schema = json_wsl
        for part in ref_path:
            schema = schema.get(part)
            if schema is None:
                raise ValueError(f"No se pudo resolver la referencia: {ref}")
        return schema

    # Revisar todas las operaciones posibles en el endpoint
    endpoint = json_wsl['paths'][intent]
    for operation_key in endpoint:
        operation = endpoint[operation_key]

        # Extraer parámetros
        parameters = operation.get('parameters', [])
        print(f"Parámetros encontrados en {operation_key}:", parameters)  # Debugging print

        for param in parameters:
            if '$ref' in param:
                resolved_param = resolve_reference(param['$ref'])
                if 'x-value' in resolved_param.get('schema', {}):  # Saltar parámetros con x-value
                    continue
                name = resolved_param.get('name')
                if name:
                    slots.append(name)
            else:
                if 'x-value' in param.get('schema', {}):  # Saltar parámetros con x-value
                    continue
                name = param.get('name')
                if name:
                    slots.append(name)

        # Verifica si hay un requestBody y extrae sus propiedades
        if 'requestBody' in operation:
            request_body = operation['requestBody']
            if 'content' in request_body:
                for content_type, content_schema in request_body['content'].items():
                    if '$ref' in content_schema['schema']:
                        resolved_schema = resolve_reference(content_schema['schema']['$ref'])
                        schema_slots = extract_schema_properties(resolved_schema)
                        slots.extend(schema_slots)
                    else:
                        schema_slots = extract_schema_properties(content_schema['schema'])
                        slots.extend(schema_slots)

    print("Slots finales:", slots)  # Debugging print

    return slots

def slot_filling(userInput, slots, userAnswers = None):
    configure_openai()

    # Convertir la lista de slots a una cadena JSON
    slots_str = json.dumps(slots)

    # Comprobar si hay respuestas previas del usuario
    if userAnswers is not None:
        userAnswers_str = "\n".join(
            f"- {entry['chatbot']}: {entry['user']}" for entry in userAnswers if 'chatbot' in entry and 'user' in entry
        )
        messages = [
            {
                "role": "user",
                "content": f"Forget the information provided in our previous interactions. "
                           f"Provided the prompt: \"{userInput}\", these previous inputs during the conversation: {userAnswers_str} "
                           f"and the parameters that should be filled: {slots_str}, give me a JSON list with the slots name as the key "
                           f"and the values that are given in the prompt directly as the value. "
                           f"If the value is not given, give the value \"Null\"."
            }
        ]
    else:
        messages = [
            {
                "role": "user",
                "content":  f"Forget the information provided in our previous interactions. "
                            f"Provided the prompt: \"{userInput}\", and the parameters that should be filled: {slots_str}, "
                            f"give me a JSON list with the slots name as the key and the values that are given in the prompt directly as the value. "
                            f"If the value is not given, give the value \"Null\"."
            }
        ]

    print(messages)

    # Crear la solicitud de ChatCompletion
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Puedes usar "gpt-4" si tienes acceso
        messages=messages,
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )

    response = response.choices[0].message.content

    print("RESPUESTA CHATGPT")
    print(response)

    # Reemplazar cadenas "null" por valores null
    slotFillingResponse = response.replace('"Null"', 'null')
    print("RESPUESTA SIN NULL", slotFillingResponse)

    return slotFillingResponse