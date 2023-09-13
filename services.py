import os

import requests
from telegram import InlineKeyboardButton

SOUNDCLOUD_USER_ID = os.getenv('SOUNDCLOUD_USER_ID')
SOUNDCLOUD_CLIENT_ID = os.getenv('SOUNDCLOUD_CLIENT_ID')


class SoundCloud:
    def search(self, name_of_song):
        url = f'https://api-v2.soundcloud.com/search/tracks?q={name_of_song}&variant_ids=&user_id={SOUNDCLOUD_USER_ID}&client_id={SOUNDCLOUD_CLIENT_ID}&limit=20&offset=0&linked_partitioning=1&app_version=1688120186&app_locale=en'
        headers = {'accept': 'application/json; charset=utf-8'}
        response = requests.get(url=url, headers=headers)
        response = response.json()
        collection = response['collection']
        return self.create_inline_button(collection)

    def create_inline_button(self, collection):
        keyboards = []
        for music in collection:
            keyboards.append(
                [InlineKeyboardButton(text=music['title'], url=music['permalink_url'])])
        return keyboards


def search_on_all_services(name_of_song):
    services = [SoundCloud]

    results = []
    for service in services:
        results.append(service().search(name_of_song))

    # TODO: process on results

    return results[0]
