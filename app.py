from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key as an environment variable or replace directly
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/generate', methods=['POST'])
def generate_recipe():
    data = request.get_json()
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({"error": "Prompt is required."}), 400

    try:
        response = openai.ChatCompletion.create(
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)