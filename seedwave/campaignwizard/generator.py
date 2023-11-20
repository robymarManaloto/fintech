import sys
import os
import re
import json

module_dir = os.path.join(os.path.dirname(__file__), '../libraries')
sys.path.append(module_dir)
from libraries.gpt4free import g4f

translate_prompt = "Translate this in readable form. Answer in JSON format only  [message: '']. The transcription: {}"
result_prompt ="Here is the format I want to fill: ['title': '<string>', 'description': '<string>', 'category': '<string>', 'fundgoal': <int>, 'duration': <int>, 'rewards': [['title': '<string>', 'description': '<string>', 'amount': <int>], ['title': '<string>', 'description': '<string>', 'amount': <int>], ['title': '<string>', 'description': '<string>', 'amount': <int>]]]. Fill it up using the following (Translate to english if needed): {}. Generate suggested rewards if no information mentioned. Give the answer only. Don't respond json if there is no information mentioned."
html_prompt = "Your role is now the best designer for this campaign page. You must not include nav bars. You have client has the following for their campaign: {}. If the request is not possible or lack of details continue to create an awesome website in Bootstrap 4. Don't use Lorem Ipsum, think some content for your client. Use https://picsum.photos/ as placeholders of random image. Make the website complete with header, body, footer. Give the complete html only. "
input_prompt = "The client says: {}. For a crowdfunding campaign, think of a text for the field {}. Answer in this JSON only(translate to english if needed): ['answer': <datatype>] If it doesn't answer the question, just think some for your client."

def generate_results(transcript):
    translated = translate(transcript, translate_prompt)
    results = get_results(translated['message'], result_prompt)
    web_context = translated.copy()
    web_context.update(results)
    return web_context
    
def generate_html(context):
    website = generate_campaign(context, html_prompt)
    return website

def analyze(input):
    analyzed = get_two_data(input, input_prompt, ['answer'])
    return analyzed

def get_two_data(context, prompt, keys):
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt.format(context['field'], context['transcript'])}],
    )
    print(response)
    data = parse_json(response)
    if not isinstance(data, dict) or data is None or not len([key for key in keys if key in data]) == len(keys):
        return get_two_data(context, prompt, keys)
    return data

def parse_json(response):
    pattern = r'\{.*\}'
    match = re.search(pattern, response, re.DOTALL)
    if match:
        try:
            json_str = match.group(0)
            json_str = json_str.replace("'", '"')
            return json.loads(json_str)
        except:
            return None
    else:
        return None

def get_data(context, prompt, keys):
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt.format(context)}],
    )
    print(response)
    data = parse_json(response)
    if not isinstance(data, dict) or data is None or not len([key for key in keys if key in data]) == len(keys):
        return get_data(context, prompt, keys)
    
    return data

def translate(transcript, prompt):
    return get_data(transcript, prompt, ['message'])

def get_results(transcript, prompt):
    return get_data(transcript, prompt, ['title', 'description', 'category', 'fundgoal', 'duration', 'rewards', ])

def parse_html(response):
    pattern = re.compile(r'<!DOCTYPE html>[\s\S]*?</html>', re.DOTALL)
    match = pattern.search(response)
    return match.group(0) if match else None

def generate_campaign(web_context, prompt):
    str_context = "\n".join([f"{key}: {value}" for key, value in web_context.items()])
    content = (
        prompt.format(str_context)
    )
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": content}],
    )
    website = parse_html(response)
    if website is None:
        return generate_campaign(web_context, prompt)
    else:
        return website
    