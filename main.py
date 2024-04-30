import argparse
import base64
import os

import requests


def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(str(content))


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def gpt_request(api_token, msg):
    req_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }

    payload = {
        "model": "gpt-4-turbo",
        "messages": [msg]
    }

    json_res = requests.post("https://api.openai.com/v1/chat/completions",
                             headers=req_headers, json=payload).json()
    return json_res['choices'][0]['message']['content']


def create_tc_msg(user_story_text, base64_screenshot):
    prompt = read_file("prompts/tc.txt")

    return {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": user_story_text
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_screenshot}"
                }
            },
            {
                "type": "text",
                "text": prompt,
            },
        ]
    }


def create_us_msg(base64_screenshot):
    prompt = read_file("prompts/us.txt")

    return {
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_screenshot}"
                }
            },
            {
                "type": "text",
                "text": prompt
            },
        ]
    }


def process(api_key, directory):
    for name in os.listdir(directory):
        file_path = os.path.join(directory, name)

        if not os.path.isfile(file_path):
            continue

        if not name.endswith(('.png')):
            continue

        base_name = os.path.splitext(name)[0]
        us_filename = f'{base_name}_us.md'
        tc_filename = f'{base_name}_tc.md'
        us_file_path = os.path.join(directory, us_filename)
        tc_file_path = os.path.join(directory, tc_filename)

        us_exists = os.path.exists(us_file_path)
        tc_exists = os.path.exists(tc_file_path)

        if us_exists and tc_exists:
            continue

        print(f"Processing {file_path}")

        if not us_exists:
            us_res = gpt_request(api_key, create_us_msg(encode_image(file_path)))
            write_file(us_file_path, us_res)
            us_context = us_res
        else:
            us_context = read_file(us_file_path)

        if not tc_exists:
            tc_res = gpt_request(api_key, create_tc_msg(us_context, encode_image(file_path)))
            write_file(tc_file_path, tc_res)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='US/TC Writer')

    parser.add_argument('--openai-key', type=str, required=True,
                        help='OpenAI API Key')
    parser.add_argument('--directory', type=str, default="images",
                        help='Directory to process')

    args = parser.parse_args()
    process(args.openai_key, args.directory)
