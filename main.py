from mal import client  # Get the MAL list
import csv  # Read the aniwatch list
import pickle  # Save the MAL list
import custom_endpoint  # Couldn't find much endpoint with user_auth in mal_api.py


def get_mal_dict(client_id: str, username: str, get_new_list: int or bool, limit=400) -> dict:
    """
    Get the MAL list
    if (get_new_list) is set to 1, get the list from the MAL API and save it to a file
    else, load the list from the file
    return the MAL list as a dictionary - {anime_id: (anime_title, status), ...}
    :param client_id:
    :param username:
    :param get_new_list:
    :param limit: Number of entries to get from the list,default is 400
    :return:
    """
    if get_new_list:
        cli = client.Client(client_id)
        mal_list = cli.get_anime_list(username, limit=limit, include_nsfw=True)  # Get the list

        # api_mal_dict = {anime_id: (anime_title, status), ...}
        api_mal_dict = {i['node']['id']: (i['node']['title'], i['list_status']['status']) for i in
                        mal_list.raw['data']}

        with open('mal_list.data', 'wb') as g:  # Save the data to a file
            pickle.dump(api_mal_dict, g)
    else:
        try:
            with open('mal_list.data', 'rb') as g:  # Load the data from the file if (get_new_list) is set to 0
                api_mal_dict = pickle.load(g)
        except FileNotFoundError:
            print("MAL_LIST doesn't already exist, set get_new_mal_list = 1")
            exit(-1)

    return api_mal_dict


def get_aniwatch_dict(file_path: str) -> dict:
    """
    Get the aniwatch list from file
    return the aniwatch list as a dictionary as {anime_id: (anime_title, status), ...}
    :param file_path:
    :return:
    """
    try:
        with open(file_path, 'r') as g:
            data = list(csv.reader(g, delimiter='|'))
    except FileNotFoundError:
        print("File doesn't exist")
        exit(-1)

    ani_dict = {}
    status_tag = ''
    for entry in data:
        if entry[0].startswith('#'):  # Get the status tag
            status_tag = entry[0][1:].strip().lower().replace('-', '_').replace(' ', '_')
        else:
            anime_name, anime_url = entry
            ani_dict[int(anime_url[anime_url.rfind('/') + 1:])] = (anime_name.strip(), status_tag)
    if not status_tag:
        print("AniWatch Data doesn't have 'status' ")
        exit(-1)

    return ani_dict


def find_missing_entries(dict1, dict2):
    """
    Find the entries in dict2 that are not in dict1 aka (dict2 - dict1)
    :param dict1: {anime_id: (anime_title, status), ...}
    :param dict2: {anime_id: (anime_title, status), ...}
    :return:  {anime_id: (anime_title, status), ...} # Entries in dict2 but not in dict1
    """
    missing_entries = {}
    for element in dict2:
        if element not in dict1:
            missing_entries[element] = dict2[element]
    return missing_entries


if __name__ == '__main__':
    with open('.env', 'r') as f:
        CLIENT_ID = f.readline().strip()
    # Or Enter Client ID here:
    # CLIENT_ID = 'your_client_id'

    # ---Configuration variables-------------------------
    get_new_user_token = 1  # Set to 1 if you want to get a new user token
    get_new_mal_list = 1  # Set to 1 if you want to get a new list from MAL
    import_limit = 400  # Number of entries to get from the MAL list
    # ---------------------------------------------------

    mal_username = input('Enter your MAL Username: ')  # Your MAL username
    # Path to the aniwatch export file
    aniwatch_file_path = input('Enter the path to the aniwatch export file: ').strip('"\' ')

    # Get the MAL and aniwatch lists as dictionaries
    mal_dict = get_mal_dict(CLIENT_ID, mal_username, get_new_mal_list, limit=import_limit)
    aniwatch_dict = get_aniwatch_dict(aniwatch_file_path)

    # Find the missing entries
    not_in_mal = find_missing_entries(mal_dict, aniwatch_dict)  # Find the entries in aniwatch that are not in MAL

    print(f"Number of entries in MAL: {len(mal_dict)}",
          f"Number of entries in Aniwatch: {len(aniwatch_dict)}",
          f"Missing Entries ({len(aniwatch_dict) - len(mal_dict)}):",
          f"{'-' * 50}",
          f"In AniWatch but not in MAL:", sep='\n')
    for key in not_in_mal:
        print(f"{key}: {not_in_mal[key]}")

    if input("Do you want to view the missing entries in Aniwatch(y/n)?").lower() == 'y':
        not_in_ani = find_missing_entries(aniwatch_dict, mal_dict)  # Find the entries in MAL that are not in aniwatch
        print(
            f"{'-' * 50}\n{'-' * 50}",
            f"In MAL but not in Aniwatch:",
            f"{'-' * 50}", sep='\n')
        for key in not_in_ani:
            print(f"{key}: {not_in_ani[key]}")
    print('-' * 50)

    if input("Do you want to add the missing entries to your MAL List(y/n)?").lower() == 'y':
        endpoint = custom_endpoint.EndPoint(CLIENT_ID)
        if get_new_user_token:
            print(
                "Adding entries to your MAL List will require you to authorise this application to access your MAL "
                "account")
            endpoint.print_new_authorisation_url()  # Print the URL to get the authorisation code

            # I have set the mal api redirect url as my repo, so it opens that sit with param code
            print("mal_api_client git repo will open and from its url, copy the code (from after the code= part)")

            # Get the auth code
            endpoint.authorisation_code = input("Enter the authorisation code from the URL: ")

            # Generate new user token based on auth code
            user_token = endpoint.generate_new_token()
        else:
            from json import load as json_load

            # If already user token is created, reuse previous
            try:
                with open('token.json', 'r') as file:
                    user_token = json_load(file)
            except FileNotFoundError:
                print("User Token doesn't already exist, set get_new_user_token = 1")
                exit(-1)

        endpoint.print_user_info(user_token['access_token'])  # Print UserName for confirmation

        # Add the missing entries by id and update status
        for key in not_in_mal:
            # not_in_mal = {anime_id: (anime_title, status), ...}
            endpoint.add_entry(access_token=user_token['access_token'], anime_id=key, status=not_in_mal[key][1])
            print(f"Added {not_in_mal[key][0]} : '{not_in_mal[key][1]}' to your MAL List")
        print("All missing entries have been added to your MAL List")
