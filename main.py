from mal import client  # Get the MAL list
import csv  # Read the aniwatch list
import pickle  # Save the MAL list
import custom_endpoint


def get_mal_dict(CLIENT_ID, username, get_new_list):
    # MAL Anime List
    if get_new_list:
        cli = client.Client(CLIENT_ID)
        mal_list = cli.get_anime_list(mal_username, fields=['id'], limit=350, include_nsfw=True)

        mal_dict = {i['node']['id']: i['node']['title'] for i in mal_list.raw['data']}  # Clean the data

        with open('mal_list.data', 'wb') as g:  # Save the data to a file for future use
            pickle.dump(mal_dict, g)
    else:
        with open('mal_list.data', 'rb') as g:  # Load the data from the file if you get_new_list is set to 0
            mal_dict = pickle.load(g)
    return mal_dict


def get_aniwatch_dict(file_path):
    # Aniwatch animelist
    with open(file_path, 'r') as g:
        data = list(csv.reader(g, delimiter='|'))
    aniwatch_list = [entry for entry in data if not entry[0].startswith('#')]  # Clean the data
    return {int(i[1][i[1].rfind('/') + 1:]): i[0] for i in aniwatch_list}  # dict with id as key and title as value


def find_missing_entries(dict1, dict2):
    """
    Find the entries in dict2 that are not in dict1
    :param dict1: {anime_id: anime_title, ...}
    :param dict2: {anime_id: anime_title, ...}
    :return:  {anime_id: anime_title, ...} where anime_id is in dict2 but not in dict1
    """
    missing_entries = {}
    for element in dict2:
        if element not in dict1:
            missing_entries[element] = dict2[element]
    return missing_entries


if __name__ == '__main__':
    with open('.env', 'r') as f:
        client_id = f.readline().strip()

    mal_username = 'mNandhu'  # Your MAL username
    aniwatch_file_path = 'aniwatch_data.txt'  # Path to the aniwatch export file

    new_user_token = 0  # Set to 1 if you want to get a new user token
    new_list = 0  # Set to 1 if you want to get a new list from MAL

    mal_dict = get_mal_dict(client_id, mal_username, new_list)
    aniwatch_dict = get_aniwatch_dict(aniwatch_file_path)

    not_in_mal = find_missing_entries(mal_dict, aniwatch_dict)  # Find the entries in aniwatch that are not in MAL
    not_in_aniwatch = find_missing_entries(aniwatch_dict, mal_dict)  # Find the entries in MAL that are not in aniwatch

    print(f"Number of entries in MAL: {len(mal_dict)}",
          f"Number of entries in Aniwatch: {len(aniwatch_dict)}",
          f"Missing Entries ({len(aniwatch_dict) - len(mal_dict)}):",
          f"{'-' * 50}",
          f"In AniWatch but not in MAL:",
          )
    for key in not_in_mal:
        print(f"{key}: {not_in_mal[key]}")
    print(
        f"{'-' * 50}",
        f"{'-' * 50}",
        f"In MAL but not in Aniwatch:",
        f"{'-' * 50}", sep='\n')
    for key in not_in_aniwatch:
        print(f"{key}: {not_in_aniwatch[key]}")

    if input("Do you want to add the missing entries to your MAL List(y/n)?") == 'y':
        endpoint = custom_endpoint.EndPoint(client_id)
        if new_user_token:
            print(
                "Adding entries to your MAL List will require you to authorise this application to access your MAL "
                "account")
            endpoint.print_new_authorisation_url()  # Print the URL to get the authorisation code
            endpoint.authorisation_code = input("Enter the authorisation code from the URL: ")

            user_token = endpoint.generate_new_token()
        else:
            from json import load as json_load

            with open('token.json', 'r') as file:
                user_token = json_load(file)

        endpoint.print_user_info(user_token['access_token'])
        endpoint.add_entry(access_token=user_token['access_token'], anime_id=52701, status='on_hold')
