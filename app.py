# Cover letter creator for Michael's job hunting.

from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Set your OpenAI API model and assistant ID from environment variables
openai_model = os.getenv('OPENAI_MODEL')
assistant_id = os.getenv('ASSISTANT_ID')

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.json
    prompt = data.get('prompt', '')

    response = client.chat.completions.create(
        model=openai_model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return jsonify({"text": response.choices[0].message.content.strip()})

if __name__ == "__main__":
    app.run()