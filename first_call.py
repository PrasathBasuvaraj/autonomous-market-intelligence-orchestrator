import os
import sys
import json

from dotenv import load_dotenv
from openai import OpenAI

# Load the API key from your .env file
load_dotenv()

# Initialize the official OpenAI client
# The client automatically looks for the OPENAI_API_KEY environment variable.
client = OpenAI()

def verify_connectivity():
    """
    Verifies connectivity to the OpenAI API by making a simple chat completion call
    and printing the request and response for clarity.
    """
    try:
        # --- Step 1: Diagnostic Information ---
        print(f"--- Running with Python interpreter: {sys.executable} ---")
        print("--- Attempting to connect to OpenAI API... ---")

        # --- Step 2: Define the API Call Payload ---
        # This is the data we will send to the OpenAI API.
        request_payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant verifying API connectivity."},
                {"role": "user", "content": "Confirm that the connection is active."}
            ]
        }
        
        print("\n--- Sending Request Payload: ---")
        print(json.dumps(request_payload, indent=2))

        # --- Step 3: Make the API Call ---
        # This sends the request to OpenAI and waits for the response.
        response = client.chat.completions.create(
            model=request_payload["model"],
            messages=request_payload["messages"]
        )
        
        # --- Step 4: Process and Display the Response ---
        print("\n--- Received Full API Response: ---")
        print(response.model_dump_json(indent=2))

        print("\n--- API Connection Successful! ---")
        print(f"Assistant's Message: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    verify_connectivity()