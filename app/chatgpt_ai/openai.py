from dotenv import load_dotenv
import openai
import os

load_dotenv()

openai.api_key = os.getenv('CHATGPT_API_KEY')
    
def check_for_offensive_content(text):
    # Use OpenAI API to analyze text for offensive content
    prompt = f'Tell me True or False if the following text contains a curse word in any language: "{text}"'
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    try:
        return response['choices'][0]['message']['content'].lower().split()[0] == 'true.'
    except (KeyError, IndexError):
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

def chatgpt_translate(text, language):
    prompt = f'Translate the following text: "{text}", to the following language: "{language}"'
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )    
    return response['choices'][0]['message']['content']

def chatgpt_quiz(topic):
    prompt = f'Please give me a quiz question on the topic: "{topic}", only the question with no introduction and with 4 choices, and separate the correct answer in format Answer: (insert here actual answer)'
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    print(response['choices'][0]['message']['content'])
    return response['choices'][0]['message']['content']