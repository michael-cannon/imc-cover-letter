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

client = OpenAI(api_key=api_key)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    thread_id = data.get('thread_id', None)

    if not message:
        return jsonify({'error': 'No message provided'}), 400

    # Step 2: Create a Thread if not provided
    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id

    # Step 3: Add a Message to the Thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
    )

    # Step 4: Create a Run
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    if run.status == 'completed':
        messages = list(client.beta.threads.messages.list(thread_id=thread_id))

        logging.info(messages)

        # Log the content of the messages
        logging.info("messages: ")

        response_messages = []

        user_message = None
        assistant_message = None

        for msg in messages:
            if msg.role == "user" and user_message is None:
                user_message = msg
            elif msg.role == "assistant" and assistant_message is None:
                assistant_message = msg
            if user_message and assistant_message:
                break

        if user_message and assistant_message:
            assert user_message.content[0].type == "text"
            assert assistant_message.content[0].type == "text"
            logging.info({"role": user_message.role, "message": user_message.content[0].text.value})
            logging.info({"role": assistant_message.role, "message": assistant_message.content[0].text.value})
            response_messages.append({
                'role': user_message.role,
                'message': user_message.content[0].text.value
            })
            response_messages.append({
                'role': assistant_message.role,
                'message': assistant_message.content[0].text.value
            })
        else:
            response_messages = [{"role": "system", "message": "Error: Run did not complete successfully."}]

    else:
        response_messages = [{"role": "system", "message": "Error: Run did not complete successfully."}]

    return jsonify({
        'messages': response_messages,
        'thread_id': thread_id
    })


if __name__ == "__main__":
    app.run()