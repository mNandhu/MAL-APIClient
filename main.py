from mal import client  # Get the MAL list
import csv  # Read the aniwatch list
import pickle  # Save the MAL list
import custom_endpoint


def get_mal_dict(client_id, username, get_new_list) -> dict:
    """
    Get the MAL list
    if (get_new_list) is set to 1, get the list from the MAL API and save it to a file
    if (get_new_list) is set to 0, load the list from the file

    :param client_id:
    :param username:
    :param get_new_list:
    :return:
    """
    if get_new_list:
        cli = client.Client(client_id)
        mal_list = cli.get_anime_list(mal_username, fields=['id'], limit=350, include_nsfw=True)

        api_mal_dict = {i['node']['id']: (i['node']['title'], i['list_status']['status']) for i in
                        mal_list.raw['data']}  # Clean the data

        with open('mal_list.data', 'wb') as g:  # Save the data to a file for future use
            pickle.dump(api_mal_dict, g)
    else:
        with open('mal_list.data', 'rb') as g:  # Load the data from the file if you get_new_list is set to 0
            api_mal_dict = pickle.load(g)
    return api_mal_dict


def get_aniwatch_dict(file_path):
    # Aniwatch animelist
    with open(file_path, 'r') as g:
        data = list(csv.reader(g, delimiter='|'))
    # aniwatch_list = [entry for entry in data if not entry[0].startswith('#')]  # Clean the data
    ani_dict = {}
    status_tag = ''
    for entry in data:
        if entry[0].startswith('#'):
            status_tag = entry[0][1:].strip().lower().replace('-', '_').replace(' ', '_')
        else:
            anime_name, anime_url = entry
            ani_dict[int(anime_url[anime_url.rfind('/') + 1:])] = (anime_name.strip(), status_tag)

    # return {int(i[1][i[1].rfind('/') + 1:]): i[0] for i in aniwatch_list}  # dict with id as key and title as value
    return ani_dict


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


# for i, j in get_aniwatch_dict('aniwatch_data.txt').items():
#     print(i, j)

if __name__ == '__main__':
    with open('.env', 'r') as f:
        CLIENT_ID = f.readline().strip()

    mal_username = 'mNandhu'  # Your MAL username
    aniwatch_file_path = 'export (2).txt'  # Path to the aniwatch export file

    new_user_token = 0  # Set to 1 if you want to get a new user token
    new_list = 0  # Set to 1 if you want to get a new list from MAL

    mal_dict = get_mal_dict(CLIENT_ID, mal_username, new_list)
    aniwatch_dict = get_aniwatch_dict(aniwatch_file_path)

    not_in_mal = find_missing_entries(mal_dict, aniwatch_dict)  # Find the entries in aniwatch that are not in MAL
    not_in_aniwatch = find_missing_entries(aniwatch_dict, mal_dict)  # Find the entries in MAL that are not in aniwatch

    print(f"Number of entries in MAL: {len(mal_dict)}",
          f"Number of entries in Aniwatch: {len(aniwatch_dict)}",
          f"Missing Entries ({len(aniwatch_dict) - len(mal_dict)}):",
          f"\n{'-' * 50}",
          f"\nIn AniWatch but not in MAL:",
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
    print('-' * 50)
    if input("Do you want to add the missing entries to your MAL List(y/n)?").lower() == 'y':
        endpoint = custom_endpoint.EndPoint(CLIENT_ID)
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

        for key in not_in_mal:
            # not_in_mal = {anime_id: (anime_title, status), ...}
            endpoint.add_entry(access_token=user_token['access_token'], anime_id=key, status=not_in_mal[key][1])
            print(f"Added {not_in_mal[key][0]} : '{not_in_mal[key][1]}' to your MAL List")
