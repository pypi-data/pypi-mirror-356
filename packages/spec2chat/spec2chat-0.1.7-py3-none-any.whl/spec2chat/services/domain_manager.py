"""
spec2chat - A Python library for building task-oriented conversational systems from OpenAPI service specifications.

Author: M. Jesús Rodríguez
License: Apache 2.0 License
Version: 0.1.6
Repository: https://github.com/mjesusrodriguez/spec2chat
Created on 17/05/2025 by M. Jesús Rodríguez
"""

import openai
from spec2chat.utils.openai_config import configure_openai

def classify_domain(input):
    configure_openai()

    messages = [
        {
            "role": "user",
            "content": f'You are a domain classifier in a dialogue system. Classify the following input: "{input}". The input might refer to more than one domain. Return all relevant domains from the following: "restaurants", "hotels", "attractions", or "out-of-domain" if the input does not fit in any domain. Return the domains as a comma-separated list of words, even if there is only one relevant domain.'        }
    ]

    # Crear la solicitud de ChatCompletion
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Puedes usar "gpt-4" si tienes acceso
        messages=messages,
        temperature=0,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )

    # Extraer la respuesta generada por el modelo
    generated_text = response.choices[0].message.content
    # Dividir la cadena por comas y quitar espacios innecesarios
    final_response = [domain.strip() for domain in generated_text.split(',')]
    print(f"Final response (as list): {final_response}")

    return final_response