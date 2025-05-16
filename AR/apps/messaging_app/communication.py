import asyncio
import time

import requests
import settings_manager
import os

messages = {}
ai_messages = {}
models = []
fetch = False

def fetch_messages():
    global messages, ai_messages

    url = get_endpoint_address("/messages/get")

    while fetch:
        response = requests.get(url)
        if response.status_code == 200:
            messages = response.json()[0]
            ai_messages = response.json()[1]
            print(f"Updated messages to {messages}")
        else:
            print(response.text)

        time.sleep(10)

def send_message(message, server, channel):
    if server == "DM" or server == "DMraw":
        if server == "DMraw":
            tags = [channel]
        else:
            tags = get_tag(channel)

        for i in tags:
            send_dm(message, i["username"])

        return

    if server.lower() == "ai":
        asyncio.run(send_llm(channel, message))
        return

    url = get_endpoint_address("/messages/send")

    webhook = get_webhook(server, channel)

    payload = {
        "message": message,
        "name": settings_manager.get_settings().discord_name,
        "pfp": settings_manager.get_settings().discord_pfp_url,
        "webhook": webhook
    }

    response = requests.post(url, json=payload)
    print(response.text)

def get_endpoint_address(endpoint):
    return "http://" + settings_manager.get_settings().discord_api_ip + endpoint + "?auth=" + os.getenv("DISCORD_API_AUTH_KEY")

def send_dm(message, tag):
    url = get_endpoint_address("/messages/send_private")

    payload = {
        "message": message,
        "name": settings_manager.get_settings().discord_name,
        "tag": tag
    }

    response = requests.post(url, json= payload)

    print(response.text + " to " + str(tag))

def get_tag(username):
    url = get_endpoint_address("/tag")

    response = requests.post(url, json={"username": username})
    return response.json()

def get_webhook(server, channel):
    url = get_endpoint_address("/webhooks")
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Could not get the webhook! error code: {response.status_code}")
        return None

    webhooks = response.json()
    return webhooks.get(server).get(channel)

def create_ai_message_from_text(text : str):
    text = text.split(":")
    role = text[0]
    message = ""
    for index, i in enumerate(text[1:]):
        message += i
        if index != len(text[1:]) - 1:
            message += ":"

    return create_ai_message(role, message)

def create_ai_message(role, message):
    return {
        "role": role,
        "content": message
            }

def get_models():
    url = get_endpoint_address("/models")
    response = requests.get(url)

    if response.ok:
        data = response.json()

        for i in data:
            models.append(i.get("id"))

        return models
    else:
        return None

async def send_llm(model, message, temperature = .7):
    url = get_endpoint_address("/llm")

    if ai_messages.get(model) is None:
        ai_messages[model] = []

    ai_messages.get(model).append(create_ai_message_from_text(message))

    chat = ai_messages

    payload = {
        "model": model,
        "messages": chat,
        "temperature": temperature
    }
    response = requests.post(url, json=payload)

    if response.ok:
        ai_messages.get(model).append({"role": "assistant", "content": response.text})
        print(ai_messages)
    else:
        print(f"Error: {response.status_code} - {response.text}")