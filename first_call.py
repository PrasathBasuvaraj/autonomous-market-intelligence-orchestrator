import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

# Load the API key from your .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the official OpenAI client
client = OpenAI(api_key=api_key)

def verify_connectivity():
    try:
        # Print the path of the interpreter to confirm we're in the correct venv
        print(f"--- Running with Python interpreter: {sys.executable} ---")

        # Perform a single programmatic (non-chat) API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant verifying API connectivity."},
                {"role": "user", "content": "Confirm that the connection is active."}
            ]
        )
        
        # Print the response content to verify success
        print("API Connection Successful!")
        print(f"Response: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    verify_connectivity()