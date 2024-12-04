from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
assistant_id = os.getenv('ASSISTANT_ID')

client = OpenAI(api_key = api_key)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')

    if not message:
        return jsonify({'error': 'No message provided'}), 400

    # Step 2: Create a Thread
    thread = client.beta.threads.create()

    # Step 3: Add a Message to the Thread
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )

    # Step 4: Create a Run
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=thread.id)

        # Log the content of the messages
        logging.info("messages: ")
        response_message = ""

        for message in messages:
            assert message.content[0].type == "text"
            logging.info({"role": message.role, "message": message.content[0].text.value})
            response_message += message.content[0].text.value + "\n"

        response_message = response_message.strip()
    else:
        response_message = "Error: Run did not complete successfully."

    return jsonify({
        'response': response_message
    })


if __name__ == "__main__":
    app.run()