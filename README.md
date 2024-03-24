# AniWatch to MAL Using MALAPI

A simple pastime project to compare local data from aniwatch/anime watching sites watchlist with MAL's watchlist and adding missing entries 
Using MAL API to Get a Public list of a user and compare it with the local list
and find missing entries and then adds them

Version1: Code to find the missing entries
TODO: Automatically add missing entries from aniwatch to mal

Version2:
Automatically add missing entries from aniwatch to mal - Completed

Installing:

1) Open File Explorer go to a new folder and open the terminal in that folder (By typing cmd into the search bar)
2) Enter ```git clone https://github.com/mNandhu/mal_api_client``` (and the files should be downloaded)
3) Go into the Folder by entering ```cd mal_api_client```
4) Run ```py -m pip install -r requirements.txt``` (and so dependencies are installed)
5) Create a file ".env" in that folder, and paste CLIENT_ID

6) Running the Code:
   Open cmd at that location and Enter ```py main.py ```
   and the code will run

7) Get data from aniwatch:
   Click on your profile, and select mal import/export
   Select export and export as txt (make sure Group by folder is selected)
   Paste it in the project directory

8) Authorisation:
   To add new entries to your anime list, the auth_code is needed
   This can be obtained by, selecting yes for "Add Missing Entries to MAL List" and following the steps
   or by running custom_endpoint.py

   Open the link and allow auth from MAL which will open this GithubRepo
   ```https://github.com/mNandhu/mal_api_client?code=adjhadsjhsajkhda...```
   Copy and paste adjhadsjhsajkhda... part in the terminal

TODO: Exception Handling and Code Cleanup
