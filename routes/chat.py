from flask import request, jsonify
from openai import OpenAI
import io
import logging
import os

logging.basicConfig(level=logging.CRITICAL)

api_key = os.getenv('OPENAI_API_KEY')
assistant_id = os.getenv('ASSISTANT_ID')

client = OpenAI(api_key=api_key)

def chat_route():
    data = request.form
    message = data.get('message', '')
    thread_id = data.get('thread_id', None)
    files = request.files.getlist('files')

    logging.info(request)
    logging.info(files)

    if not message and not files:
        return jsonify({'error': 'No message or files provided'}), 400

    # Step 2: Create a Thread if not provided
    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id

    attachments = []

    # Step 3: Upload Files
    if files:
        for file in files:
            logging.info(file)

            # Use an in-memory file object
            file_stream = io.BytesIO(file.read())

            # Add a name attribute for OpenAI
            file_stream.name = file.filename
            logging.info(file_stream)

            upload_response = client.files.create(
                file=file_stream,
                purpose="assistants"
            )
            logging.info(upload_response)
            attachments.append({
                "file_id": upload_response.id,
                "tools": [{"type": "file_search"}]
            })

    # Step 4: Add a Message to the Thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message,
        attachments=attachments
    )

    # Step 5: Create a Run
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    response_messages = []

    if run.status == 'completed':
        messages = list(client.beta.threads.messages.list(thread_id=thread_id))

        logging.info(messages)

        # Log the content of the messages
        logging.info("messages: ")

        user_message = None
        assistant_message = None

        for msg in messages:
            logging.info(msg)
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

    return jsonify({
        'messages': response_messages,
        'thread_id': thread_id
    })