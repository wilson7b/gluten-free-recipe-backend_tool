from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TURNSTILE_SECRET = os.getenv("TURNSTILE_SECRET")

@app.route('/generate', methods=['POST'])
def generate_recipe():
    data = request.get_json()
    prompt = data.get('prompt', '')
    turnstile_token = data.get('turnstile_token', '')

    if not prompt:
        return jsonify({"error": "Prompt is required."}), 400
    if not turnstile_token:
        return jsonify({"error": "Turnstile token is required."}), 400

    # Verify Turnstile
    try:
        verify_response = requests.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data={
                'secret': TURNSTILE_SECRET,
                'response': turnstile_token
            }
        )
        result = verify_response.json()
        if not result.get("success"):
            return jsonify({"error": "Turnstile verification failed."}), 403
    except Exception as e:
        return jsonify({"error": f"Turnstile validation error: {str(e)}"}), 500

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a friendly gluten-free recipe expert named Katie Wilson."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        recipe_text = response.choices[0].message.content.strip()
        return jsonify({"recipe": recipe_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.get_json()
    prompt = data.get('prompt', '')
    size = data.get('size', '1024x1024')

    if not prompt:
        return jsonify({"error": "Prompt is required."}), 400

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="standard",
            n=1
        )
        return jsonify({"image_url": response.data[0].url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
