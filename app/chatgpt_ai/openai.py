from dotenv import load_dotenv
import openai
import os

load_dotenv()

openai.api_key = os.getenv('CHATGPT_API_KEY')

# def check_for_offensive_content(text):
#     # Use OpenAI API to analyze text for offensive content
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             [{"role": "user", "content": 'Tell me True or False if the following text contains a curse word in any language: "{text}"'}]
#         ]
#     )
#     try:
#         return response['choices'][0]['message']['content'].lower() == 'true'
#     except (KeyError, IndexError):
#         # Handle errors and return False in case of issues
#         return False
    
def check_for_offensive_content(text):
    # Use OpenAI API to analyze text for offensive content
    prompt = f'Tell me True or False if the following text contains a curse word in any language: "{text}"'
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    try:
        return response['choices'][0]['message']['content'].lower().split()[0] == 'true.'
    except (KeyError, IndexError):
        # Handle errors and return False in case of issues
        return False


def chatgpt_response(prompt):
    response = openai.Completion.create(
        model = "gpt-3.5-turbo-instruct",
        prompt = prompt,
        temperature = 1,
        max_tokens = 100
    )
    response_dict = response.get("choices")
    if response_dict and len(response_dict) > 0:
        prompt_response = response_dict[0]["text"]
    return prompt_response