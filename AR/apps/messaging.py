import os.path
import threading
import time

import requests
from dotenv import load_dotenv

import settings_manager
from apps.app_base import App
from gui import keyboard

load_dotenv(os.path.abspath("../resources/.env"))

layout = [
    ['`', "1", "2", '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "\\"],
    ["\\", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
    [" "]
]

messages = []

class MessagingApp(App):
    def __init__(self, name, display_name, icon_path):
        super().__init__(name, display_name, icon_path)
        self.message_fetch = threading.Thread(target=self.fetch_messages)
        self.keyboard = keyboard.Keyboard()

    def launch(self):
        self.message_fetch.start()
        self.opened = True

    def fetch_messages(self):
        global messages

        url = get_endpoint_address("/messages/get")

        while self.opened:
            response = requests.get(url)
            if response.status_code == 200:
                messages = response.json()
                print(f"Updated messages to {messages}")
            else:
                print(response.text)

            time.sleep(10)

    def close(self):
        self.message_fetch.join()
        self.opened = False


    def draw(self, image, w, h,
             left_click_gesture_detected, right_click_gesture_detected,
             left_cursor_position, right_cursor_position):
        if self.opened:
            overlay = image.copy()


def send_message(message, server, channel):
    if server == "DM" or server == "DMraw":
        if server == "DMraw":
            tags = [channel]
        else:
            tags = get_tag(channel)

        for i in tags:
            send_dm(message, i["username"])

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

if __name__ == "__main__":
    send_message("Hello from OptiForge gui", "DM", "Tomáš Krůta")