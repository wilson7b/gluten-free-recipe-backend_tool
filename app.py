from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# Set your OpenAI API key and hCaptcha secret key as environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
HCAPTCHA_SECRET = os.getenv("HCAPTCHA_SECRET")

@app.route('/generate', methods=['POST'])
def generate_recipe():
    data = request.get_json()
    prompt = data.get('prompt', '')
    hcaptcha_token = data.get('hcaptcha_token', '')

    if not prompt:
        return jsonify({"error": "Prompt is required."}), 400
    if not hcaptcha_token:
        return jsonify({"error": "hCaptcha token is required."}), 400

    # Verify hCaptcha
    try:
        verify_response = requests.post(
            "https://hcaptcha.com/siteverify",
            data={
                'secret': HCAPTCHA_SECRET,
                'response': hcaptcha_token
            }
        )
        result = verify_response.json()
        if not result.get("success"):
            return jsonify({"error": "hCaptcha verification failed."}), 403
    except Exception as e:
        return jsonify({"error": f"hCaptcha validation error: {str(e)}"}), 500

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
    size = data.get('size', '1024x1024')  # Accept optional size from frontend

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
