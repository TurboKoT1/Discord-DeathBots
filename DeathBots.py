import requests

from base64 import b64encode
from json import dumps
from httpagentparser import detect
from random import randint


class Bots:
    def __init__(self):
        self.tokens = []

        useragent = 'Mozilla/5.0 ' \
                    '(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
        parsed_useragent = detect(useragent)
        self.x_super_properties = {
            "os": parsed_useragent["os"]["name"],
            "browser": parsed_useragent["browser"]["name"],
            "device": "",
            "system_locale": "ru-RU",
            "browser_user_agent": useragent,
            "browser_version": parsed_useragent["browser"]["version"],
            "os_version": parsed_useragent["os"]["version"],
            "referrer": "",
            "referring_domain": "",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": randint(76000, 79999),
            "client_event_source": None
        }
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200'
        }

    def get_and_check_tokens(self, filename='tokens.txt'):
        with open('dead_tokens.txt', 'w') as dtokens_file:
            dtokens_file.write("")

        with open(filename, 'r') as tokens_file:
            file_lines = tokens_file.readlines()

        file_lines = [line.strip() for line in file_lines]
        if file_lines:
            for token in file_lines:
                request = requests.get(
                    'https://discord.com/api/v9/users/@me/library',
                    headers={
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
                        'Authorization': token,
                        'x-super-properties': b64encode(dumps(self.x_super_properties).replace(" ", "").encode("UTF-8")).decode("UTF-8")}
                )

                if request.status_code == 200:
                    self.tokens.append(token)
                else:
                    with open('dead_tokens.txt', 'a') as dtokens_file:
                        dtokens_file.write(f"{token}\n")
        else:
            return False

        return self.tokens

    def send_msg(self, cid, message):
        sent_msgs = 0
        url = f"https://discord.com/api/v9/channels/{cid}/messages"

        for token in self.tokens:
            request = requests.post(
                url,
                headers={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
                    'Authorization': token,
                    'x-super-properties': b64encode(
                        dumps(self.x_super_properties).replace(" ", "").encode("UTF-8")).decode("UTF-8")
                },
                json={'content': message}
            )

            if request.status_code == 200:
                sent_msgs += 1

        return sent_msgs

    def join_server(self, invite_code):
        joined = 0
        url = f"https://discord.com/api/v9/invites/{invite_code}?inputValue=https://discord.gg/{invite_code}&with_counts=true&with_expiration=true"

        for token in self.tokens:
            request = requests.post(
                url,
                headers={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
                    'Authorization': token,
                    'x-super-properties': b64encode(
                        dumps(self.x_super_properties).replace(" ", "").encode("UTF-8")).decode("UTF-8")
                }
            )

            if request.status_code == 200 and not "captcha_key" in request.text:
                joined += 1

        return joined

    def create_thread(self, cid, mid, name):
        created_threads = 0
        url = f"https://discord.com/api/v9/channels/{cid}/messages/{mid}/threads"

        for token in self.tokens:
            request = requests.post(
                url,
                headers={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
                    'Authorization': token,
                    'x-super-properties': b64encode(
                        dumps(self.x_super_properties).replace(" ", "").encode("UTF-8")).decode("UTF-8")
                },
                json={
                    'name': name,
                    'type': 11,
                    'auto_archive_duration': 4320,
                    'location': "Message"
                }
            )

            if request.status_code == 200:
                created_threads += 1

        return created_threads

    def add_friend(self, name, discriminator=None):
        added = 0
        url = "https://discord.com/api/v9/users/@me/relationships"

        for token in self.tokens:
            request = requests.post(
                url,
                headers={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
                    'Authorization': token,
                    'x-super-properties': b64encode(
                        dumps(self.x_super_properties).replace(" ", "").encode("UTF-8")).decode("UTF-8")
                },
                json={
                    'username': name,
                    'discriminator': discriminator
                }
            )

            if request.status_code == 200:
                added += 1

        return added
