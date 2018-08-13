import requests


class Trello:
    base_url = 'https://api.trello.com/1'

    def __init__(self, api_key, api_token):
        self.key = api_key
        self.token = api_token
        self.auth_params = {'key': self.key, 'token': self.token}

    def get_boards(self):
        response = requests.get('{}/members/me/boards'.format(self.base_url), params=self.auth_params)
        return response.json()

    def get_lists(self, board_id):
        response = requests.get('{}/boards/{}/lists'.format(self.base_url, board_id), params=self.auth_params)
        return response.json()

    def get_board_cards(self, board_id):
        response = requests.get('{}/boards/{}/cards'.format(self.base_url, board_id), params=self.auth_params)
        return response.json()

    def get_list_cards(self, list_id):
        response = requests.get('{}/lists/{}/cards'.format(self.base_url, list_id), params=self.auth_params)
        return response.json()

    def create_card(self, list_id, **kwargs):
        params = kwargs
        params.update({'idList': list_id})
        params.update(self.auth_params)
        response = requests.post('{}/lists/{}/cards'.format(self.base_url, list_id), params=params)
        return response.json()


