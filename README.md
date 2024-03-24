# AniWatch to MAL Using MALAPI

A simple pastime to compare local data from aniwatch/anime watching sites watchlist with MAL's watchlist
Using MAL API to Get a Public list of a user and compare it with the local list
and find missing entries

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

6) To Get data from aniwatch, click on your profile, and select mal import/export
Select export and export as txt (make sure Group by folder is selected)
Paste it in the project directory

Running
Open cmd at that location and enter 
```py main.py ```
1) Enter your MAL UserName
2) Path of the export file can be copied by right-clicking and selecting "copy as path"
TODO: Exception Handling and Code Cleanup
