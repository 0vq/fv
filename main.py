import json
import random
import time
from flask import Flask, jsonify
import requests
import os

# --- Configuration Section ---
# IMPORTANT: Replace this placeholder with the actual Discord Webhook URL.
DISCORD_WEBHOOK_URL = os.getenv("WEBHOOK")

# Initialize the Flask application instance.
app = Flask(__name__)

# --- Data Generation Functions ---

def generate_cute_embed():
    """Generates a random, aesthetically pleasing Discord embed payload."""
    
    # Pool of sweet messages (in Spanish, for user-facing content).
    messages = [
        "Tu presencia es un rayo de sol en un día nublado. ¡Sigue brillando!",
        "Recordatorio amistoso: Eres más fuerte y más capaz de lo que piensas.",
        "Que tu café esté fuerte y tu lunes sea corto. ¡Tú puedes con todo!",
        "El universo te sonríe hoy. Acepta el regalo de este momento.",
        "Un pequeño momento de paz y cariño, solo para ti.",
        "Hay magia en la forma en que ves el mundo. ¡Nunca la pierdas!",
        "Tu esfuerzo y dedicación inspiran a quienes te rodean. ¡Eres increíble!",
        "La vida es mejor cuando tienes algo bello que mirar, como este mensaje.",
    ]
    
    # Pool of embed titles.
    titles = [
        "Un Abrazo Digital",
        "Recordatorio de Felicidad",
        "Tu Dosis de Belleza",
        "Mensaje Secreto del Universo",
        "Motivación Bonita",
        "Estrella Fugaz de Cariño",
    ]

    # Pool of aesthetic colors (decimal representation of hex codes).
    colors = [
        0xFFA07A, # Light Salmon
        0xADD8E6, # Light Blue
        0x90EE90, # Light Green
        0xFFD700, # Gold
        0xEE82EE, # Violet
        0xF08080, # Light Coral
    ]

    # Randomly select content components.
    message = random.choice(messages)
    title = random.choice(titles)
    color = random.choice(colors)

    # Construct the Discord Embed structure.
    embed_data = {
        "title": title,
        "description": f"✨ **{message}**",
        "color": color,
        # Use ISO 8601 format for Discord timestamp requirement.
        "timestamp": f"{time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())}",
        "footer": {
            "text": "Enviado con amor desde la API de Yami. ❤️"
        },
        "thumbnail": {
            # Placeholder image URL for consistent aesthetics.
            "url": "https://placehold.co/128x128/99B898/FECEA8?text=%E2%99%A5"
        }
    }
    
    return embed_data

# --- External API Interaction ---

def send_discord_webhook(embed_data):
    """Posts the generated embed payload to the configured Discord Webhook URL."""
    
    # Security check for unconfigured webhook URL.
    if DISCORD_WEBHOOK_URL == "TU_WEBHOOK_DE_DISCORD_AQUÍ":
        print("ERROR: Por favor, reemplaza DISCORD_WEBHOOK_URL con tu URL de webhook real.")
        return False
        
    # Construct the final Discord POST payload.
    payload = {
        "content": "¡Tu mensaje lindo ha llegado!", 
        "embeds": [embed_data],
        "username": "API del Cariño (Yami Bot)",
        # Custom avatar URL for the webhook message sender.
        "avatar_url": "https://placehold.co/64x64/2a363b/e84a5f?text=Y"
    }
    
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Execute the HTTP POST request to Discord.
        response = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(payload), headers=headers)
        # Check for HTTP error status codes (4xx or 5xx).
        response.raise_for_status()
        print(f"Webhook enviado exitosamente. Estado: {response.status_code}")
        return True
    except requests.exceptions.HTTPError as errh:
        # Handle specific HTTP protocol errors (e.g., 400 Bad Request, 404 Not Found).
        print(f"Error HTTP al enviar Webhook: {errh}")
        return False
    except requests.exceptions.RequestException as e:
        # Handle connection-related errors (e.g., DNS failure, refused connection).
        print(f"Error de conexión al enviar Webhook: {e}")
        return False

# --- Flask Routes (Endpoints) ---

@app.route('/yami', methods=['GET'])
def yami_route():
    """Main endpoint to trigger the embed generation and webhook sending process."""
    print("Ruta /yami accedida. Generando contenido lindo...")
    
    # Core application logic flow.
    cute_embed = generate_cute_embed()
    success = send_discord_webhook(cute_embed)
    
    # Return appropriate JSON response based on webhook success.
    if success:
        return jsonify({
            "status": "success",
            "message": "Mensaje lindo enviado a Discord.",
            "embed_title": cute_embed['title']
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Error al enviar el webhook de Discord. Verifica el URL."
        }), 500

@app.route('/', methods=['GET'])
def home_route():
    """Health check and simple instruction route."""
    return jsonify({
        "status": "ok",
        "service": "Yami Cute Message API",
        "instructions": "Accede a la ruta /yami para enviar un mensaje lindo a Discord."
    }), 200

# --- Application Startup ---

if __name__ == '__main__':
    # Run the Flask development server.
    app.run(host='0.0.0.0', port=5000)
