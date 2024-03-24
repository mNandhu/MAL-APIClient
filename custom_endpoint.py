import json
import requests
import secrets


class EndPoint:
    """
    Class to interact with the MyAnimeList API
    """
    def __init__(self, client_id, authorisation_code=None):
        self.CLIENT_ID = client_id
        self.authorisation_code = authorisation_code
        self.code_verifier = self.get_new_code_verifier()

    @staticmethod
    def get_new_code_verifier() -> str:
        """
        Generate a new Code Verifier / Code Challenge.
        :return:
        """
        token = secrets.token_urlsafe(100)
        return token[:128]

    def print_new_authorisation_url(self):
        """
        Print the URL needed to authorise the application
        :return:
        """
        url = (f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={self.CLIENT_ID}'
               f'&code_challenge={self.code_verifier}')
        print(f'Authorise your application by clicking here: {url}\n')

    def generate_new_token(self) -> dict:
        """
        Generate a new token using the authorisation code
        :return:
        """
        url = 'https://myanimelist.net/v1/oauth2/token'
        data = {
            'client_id': self.CLIENT_ID,
            'code': self.authorisation_code,
            'code_verifier': self.code_verifier,
            'grant_type': 'authorization_code'
        }

        response = requests.post(url, data)
        response.raise_for_status()  # Check whether the request contains errors

        token = response.json()
        response.close()
        print('Token generated successfully!')

        with open('token.json', 'w') as file:
            json.dump(token, file, indent=4)
            print('Token saved in "token.json"')

        return token

    @staticmethod
    def print_user_info(access_token: str):
        """
        Print the user's name
        :param access_token:
        :return:
        """
        url = 'https://api.myanimelist.net/v2/users/@me'
        response = requests.get(url, headers={
            'Authorization': f'Bearer {access_token}'
        })

        response.raise_for_status()
        user = response.json()
        response.close()

        print(f"\n>>> Accessed {user['name']}'s list <<<")

    @staticmethod
    def add_entry(access_token: str, anime_id: int, status: str):
        """
        Method to add a new AnimeEntry to the MAList
        :param access_token: user Token
        :param anime_id:
        :param status: completed/on_hold/plan_to_watch/dropped/watching
        :return:
        """
        url = f'https://api.myanimelist.net/v2/anime/{anime_id}/my_list_status'
        data = {'status': status}
        response = requests.put(url, data=data, headers={
            'Authorization': f'Bearer {access_token}'
        })
        response.raise_for_status()
        response.close()


if __name__ == '__main__':
    # Testing
    with open('.env', 'r') as f:
        CLIENT_ID = f.readline().strip()
        # auth_code = f.readline().strip()

    test = EndPoint(CLIENT_ID)  # Create an instance of the class

    test.print_new_authorisation_url()  # Print the URL needed to authorise the application
    # Set the authorisation code (get from file or input)
    auth_code = input("Enter the authorisation code: ")
    test.authorisation_code = auth_code

    user_token = test.generate_new_token()  # Generate a new token
    test.print_user_info(user_token['access_token'])  # Test the API by requesting the user's profile information
