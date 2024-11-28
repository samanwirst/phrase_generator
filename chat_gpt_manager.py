# chatgpt_client.py
import openai

class ChatGPTClient:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def get_response(self, prompt, role, model="gpt-3.5-turbo"):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": role},
                    {"role": "user", "content": prompt}
                ]
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
