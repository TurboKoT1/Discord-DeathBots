"""
DeathBots Library
~~~~~~~~~~~~~~~~~~~

DeathBots is a library for creating discord raidbots.

Example how to use:
    >>> from DeathBots import Bots
    >>> bots = Bots()
    >>> tokens = bots.get_and_check_tokens()
    >>> if tokens:
    >>>    print(f'{len(tokens)} tokens were loaded!')
    >>> bots.change_bio('Hello! I am discord raid-bot <3')

(C) 2023 by TurboKoT1.
"""

import requests
from base64 import b64encode
from json import dumps
from httpagentparser import detect
from random import randint


class Bots:
    def __init__(self):
        """
        Init class.
        """

        self.tokens = []

        self.BASE_URL = 'https://discord.com/api/v9/'

        self.useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                         'Chrome/98.0.4758.102 Safari/537.36'
        parsed_useragent = detect(self.useragent)
        self.x_super_properties = {
            "os": parsed_useragent["os"]["name"],
            "browser": parsed_useragent["browser"]["name"],
            "device": "",
            "system_locale": "ru-RU",
            "browser_user_agent": self.useragent,
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

    def send_request(self, method, endpoint, token, json_data=None):
        headers = {
            'user-agent': self.useragent,
            'Authorization': token,
            'x-super-properties': b64encode(dumps(self.x_super_properties).replace(" ", "").encode("UTF-8")).decode(
                "UTF-8")
        }

        try:
            with requests.Session() as session:
                response = session.request(method, f'{self.BASE_URL}{endpoint}', headers=headers, json=json_data)
                return response
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return None

    def get_and_check_tokens(self, filename='tokens.txt'):
        """
        This function gets and checks tokens from file.

        Args:
            filename (string): The name of the file from where the tokens will be parsed and checked

        Returns:
           List: List of working tokens.
        """

        with open('dead_tokens.txt', 'w') as dtokens_file:
            dtokens_file.write("")

        with open(filename, 'r') as tokens_file:
            file_lines = tokens_file.readlines()

        file_lines = [line.strip() for line in file_lines]
        if file_lines:
            for token in file_lines:
                request = self.send_request('GET', 'users/@me/library', token)

                if request.status_code == 200:
                    self.tokens.append(token)
                else:
                    with open('dead_tokens.txt', 'a') as dtokens_file:
                        dtokens_file.write(f"{token}\n")
        else:
            return False

        return self.tokens

    def send_msg(self, cid, message):
        """
        This function sends a message from all bots.

        Args:
            cid (integer): Channel ID to which the message will be sent
            message (string): Message that will be sent

        Returns:
           Integer: The count of bots, that have successfully sent a message.
        """

        sent_msgs = 0

        for token in self.tokens:
            request = self.send_request('POST', f"channels/{cid}/messages", token, {'content': message})
            if request.status_code == 200:
                sent_msgs += 1

        return sent_msgs

    def join_server(self, invite_code):
        """
        This function joins bots to the server.

        Args:
            invite_code (string): Server invite code (from https://discord.gg/XXXXXXXX invite code will be XXXXXXXX)

        Returns:
           Integer: The count of bots, that have successfully joined to server.
        """

        joined = 0

        for token in self.tokens:
            request = self.send_request('POST',
                                        f'invites/{invite_code}?inputValue=https://discord.gg/{invite_code}'
                                        f'&with_counts=true&with_expiration=true', token)

            if request.status_code == 200 and "captcha_key" not in request.text:
                joined += 1

        return joined

    def create_thread(self, cid, mid, name):
        """
        This function creates threads from all bots.

        Args:
            cid (integer): Channel ID where threads will be created
            mid (integer): Message ID for which threads will be created
            name (string): Name of the threads

        Returns:
           Integer: The count of bots, that have successfully created a thread.
        """

        created_threads = 0

        for token in self.tokens:
            request = self.send_request('POST', f'channels/{cid}/messages/{mid}/threads', token,
                                        {'name': name, 'type': 11, 'auto_archive_duration': 4320, 'location': "Message"})

            if request.status_code == 200:
                created_threads += 1

        return created_threads

    def add_friend(self, name, discriminator=None):
        """
        This function sends friend request to user from all bots.

        Args:
            name (string): Name of user
            discriminator (integer): User discriminator

        Returns:
           Integer: The count of bots, that have successfully sent friend request.
        """

        added = 0

        for token in self.tokens:
            request = self.send_request('POST', 'users/@me/relationships', token, {'username': name,
                                                                                   'discriminator': discriminator})

            if request.status_code == 200:
                added += 1

        return added

    def change_server_nickname(self, gid, nickname):
        """
        This function changes bots nicknames on specific guild.

        Args:
            gid (integer): Guild ID
            nickname (string): New bots nickname

        Returns:
           Integer: The count of bots, that have successfully changed their nicknames.
        """

        changed = 0

        for token in self.tokens:
            request = self.send_request('PATCH', f'guilds/{gid}/members/@me', token, {'nick': nickname})
            if request.status_code == 200:
                changed += 1

        return changed

    def change_bio(self, bio):
        """
        This function changes bots bio.

        Args:
            bio (string): New bots bio

        Returns:
           Integer: The count of bots, that have successfully changed their bio.
        """

        changed = 0

        for token in self.tokens:
            request = self.send_request('PATCH', 'users/@me/profile', token, {'bio': bio})
            if request.status_code == 200:
                changed += 1

        return changed

    # def your_own_bots_function(self):
    #     """
    #     This function - is example of your own function.
    #     You can add your own functions to the library, it's very easy!
    #
    #     Returns:
    #        Integer: The count of authorized bots.
    #     """
    #
    #     authorized = 0
    #
    #     for token in self.tokens:
    #         request = self.send_request('GET', 'users/@me/library', token)
    #         if request.status_code == 200:
    #             authorized += 1
    #
    #     return authorized
