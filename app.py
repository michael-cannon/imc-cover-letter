from flask import Flask
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
assistant_id = os.getenv('ASSISTANT_ID')

# Import routes
from routes.index import index_route
from routes.chat import chat_route

# Register routes
app.add_url_rule('/', 'index', index_route)
app.add_url_rule('/chat', 'chat', chat_route, methods=['POST'])

if __name__ == "__main__":
    app.run()