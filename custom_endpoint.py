import json
import requests
import secrets


class EndPoint:
    def __init__(self, client_id, authorisation_code=None):
        self.CLIENT_ID = client_id
        self.authorisation_code = authorisation_code
        self.code_verifier = self.get_new_code_verifier()

    # 1. Generate a new Code Verifier / Code Challenge.
    @staticmethod
    def get_new_code_verifier() -> str:
        token = secrets.token_urlsafe(100)
        return token[:128]

    # 2. Print the URL needed to authorise your application.
    def print_new_authorisation_url(self):
        url = (f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={self.CLIENT_ID}'
               f'&code_challenge={self.code_verifier}')
        print(f'Authorise your application by clicking here: {url}\n')

    # 3. Once you've authorised your application, you will be redirected to the webpage you've
    #    specified in the API panel. The URL will contain a parameter named "code" (the Authorisation
    #    Code). You need to feed that code to the application.
    def generate_new_token(self) -> dict:
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

    # 4. Test the API by requesting your profile information
    @staticmethod
    def print_user_info(access_token: str):
        url = 'https://api.myanimelist.net/v2/users/@me'
        response = requests.get(url, headers={
            'Authorization': f'Bearer {access_token}'
        })

        response.raise_for_status()
        user = response.json()
        response.close()

        print(f"\n>>> Accessed {user['name']}! <<<")

    @staticmethod
    def add_entry(access_token: str, anime_id: int, status: str):
        url = f'https://api.myanimelist.net/v2/anime/{anime_id}/my_list_status'
        data = {'status': status}
        response = requests.put(url, data=data, headers={
            'Authorization': f'Bearer {access_token}'
        })
        response.raise_for_status()
        response.close()


if __name__ == '__main__':
    with open('.env', 'r') as f:
        CLIENT_ID = f.readline().strip()
        auth_code = f.readline().strip()

    test = EndPoint(CLIENT_ID)  # Create an instance of the class

    test.print_new_authorisation_url()  # Print the URL needed to authorise the application
    # auth_code = input("Enter the authorisation code: ")
    test.authorisation_code = auth_code  # Set the authorisation code (get from file or input)

    user_token = test.generate_new_token()  # Generate a new token
    test.print_user_info(user_token['access_token'])  # Test the API by requesting the user's profile information
