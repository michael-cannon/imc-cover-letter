# IMC-Cover-Letter

Cover letter creator for Michael's job hunting.

## Setup

1. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

2. Create a `.env` file in the project root and add your OpenAI API key:

    ```plaintext
    OPENAI_API_KEY=your-openai-api-key
    ```

3. Run the Flask application:

    ```sh
    python app.py
    ```

4. Send a POST request to `http://127.0.0.1:5000/chat` with a JSON body containing the message:

    ```json
    {
        "message": "Hello, how are you?"
    }
    ```
