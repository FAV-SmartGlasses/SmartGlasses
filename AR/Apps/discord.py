import requests

WEBHOOK_URL = 'https://discord.com/api/webhooks/your_webhook_id/your_webhook_token'


def send_discord_message(content, username='RPiUser', avatar_url=None):
    payload = {
        'content': content,
        'username': username
    }

    if avatar_url:
        payload['avatar_url'] = avatar_url

    response = requests.post(WEBHOOK_URL, json=payload)

    if response.status_code == 204:
        print('Message sent!')
    else:
        print(f'Failed: {response.status_code}')
        print(response.text)


if __name__ == '__main__':
    name = input("Enter name: ")
    avatar = input("Enter avatar URL (or leave blank): ")
    msg = input("Enter your message: ")

    send_discord_message(msg, username=name, avatar_url=avatar or None)