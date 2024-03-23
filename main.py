from mal import client  # Get the MAL list
import csv  # Read the aniwatch list
import pickle  # Save the MAL list

mal_username = 'mNandhu'  # Your MAL username
get_new_list = 0  # Set to 1 if you want to get a new list from MAL

aniwatch_file_path = 'aniwatch_data.txt'  # Path to the aniwatch export file

# MAL Anime List
if get_new_list:
    with open('.env', 'r') as f:  # Get the client id from the .env file
        client_id = f.readline()
    cli = client.Client(client_id)
    mal_list = cli.get_anime_list(mal_username, fields=['id'], limit=350, include_nsfw=True)

    mal_dict = {i['node']['id']: i['node']['title'] for i in mal_list.raw['data']}  # Clean the data

    with open('mal_list.data', 'wb') as g:  # Save the data to a file for future use
        pickle.dump(mal_dict, g)
else:
    with open('mal_list.data', 'rb') as g:  # Load the data from the file if you get_new_list is set to 0
        mal_dict = pickle.load(g)

# Aniwatch animelist
with open(aniwatch_file_path, 'r') as file:
    data = list(csv.reader(file, delimiter='|'))
aniwatch_list = [entry for entry in data if not entry[0].startswith('#')]  # Clean the data
aniwatch_dict = {int(i[1][i[1].rfind('/') + 1:]): i[0] for i in aniwatch_list}  # dict with id as key and title as value

print(f"Number of entries in MAL: {len(mal_dict)}")
print(f"Number of entries in Aniwatch: {len(aniwatch_dict)}")

print(f"Missing Entries ({len(aniwatch_dict) - len(mal_dict)}):")

print('-' * 50)
print("In AniWatch but not in MAL:")
for element in aniwatch_dict:
    if element not in mal_dict:
        print(mal_dict[element], element)
print('-' * 50)

print('-' * 50)
print("In MAL but not in Aniwatch:")
print('-' * 50)
for element in mal_dict:
    if element not in aniwatch_dict:
        print(mal_dict[element], element)

# For Debugging
with open('mal_entries.txt', 'w') as fg:
    try:
        print(mal_dict, file=fg)
    except UnicodeEncodeError:
        pass
