"""
spec2chat - A Python library for building task-oriented conversational systems from OpenAPI service specifications.

Author: M. Jesús Rodríguez
License: Apache 2.0 License
Version: 0.1.6
Repository: https://github.com/mjesusrodriguez/spec2chat
Created on 17/05/2025 by M. Jesús Rodríguez
"""

from spec2chat.db.mongo import MongoDB
import json
import openai
from spec2chat.utils.openai_config import configure_openai

db = MongoDB()

def getIntents(domain):
    print("[DEBUG] domain recibido en getIntents():", repr(domain))
    # Accede a la base de datos con nombre igual al dominio
    intents_collection = db.get_collection(domain, 'intents')
    print("[DEBUG] DB:", db.client.list_database_names())
    print("[DEBUG] Collections in domain:", db.client[domain].list_collection_names())
    # Step 3: Query the collection to get all the intents
    intents_cursor = intents_collection.find({}, {'intent': 1})  # Fetch all documents, but only the 'intent' field

    # Step 4: Extract intent names and save them into an array
    intents_list = [doc['intent'] for doc in intents_cursor if 'intent' in doc]
    print("[DEBUG]", "Intents list:", intents_list)  # Debugging line to check the intents list

    return intents_list

def recognize_intent(input, domain):
    configure_openai()
    intent_array = getIntents(domain)
    # Convertir el vector a una cadena de caracteres con comas
    intents = ','.join(map(str, intent_array))

    messages = [
        {
            "role": "user",
            "content": "You are a chatbot in the " + domain + " domain, and your task is to determine the intent behind a user's input or query. Below is a list of intents related to the " + domain + " domain: "+ intents +". Given the input '" + input + "', determine the intent of the user based on the provided intents, return a JSON with only one. Consider that users often want to make reservations when specifying a type of restaurant."
        }
    ]

    # Crear la solicitud de ChatCompletion
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Puedes usar "gpt-4" si tienes acceso
        messages=messages,
        temperature=0.3,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )

    # Extraer la respuesta generada por el modelo
    generated_text = response.choices[0].message.content

    # Procesar el JSON para obtener solo el "intent"
    try:
        data = json.loads(generated_text)  # Asegúrate de analizar el texto generado como JSON
        intent = data.get("intent")  # Obtener el valor de "intent"
    except json.JSONDecodeError:
        print("Error al decodificar JSON")
        intent = None

    return intent