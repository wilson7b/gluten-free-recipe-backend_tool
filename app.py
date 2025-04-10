from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Set your OpenAI API key as an environment variable or replace directly
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/generate', methods=['POST'])
def generate_recipe():
    data = request.get_json()
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({"error": "Prompt is required."}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
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

    if not prompt:
        return jsonify({"error": "Prompt is required."}), 400

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        return jsonify({"image_url": response.data[0].url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
