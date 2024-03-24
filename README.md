# AniWatch to MAL Using MALAPI

A simple pastime to compare local data from aniwatch/anime watching sites watchlist with MAL's watchlist
Using MAL API to Get a Public list of a user and compare it with the local list
and find missing entries

Version1: Code to find the missing entries
TODO: Automatically add missing entries from aniwatch to mal

Version2: 
Automatically add missing entries from aniwatch to mal - Completed

Installing
1) Open File Explorer go to a new folder and open the terminal in that folder (By typing cmd into the search bar)
2) Enter git clone https://github.com/mNandhu/mal_api_client (and the files should be downloaded)
3) Run "py -m pip install -r requirements.txt" (and so dependencies are installed)

Get data from aniwatch, click on your profile, and select mal import/export
Select export and export as txt (make sure Group by folder is selected)
Paste it in the project directory

Running
Open cmd at that location and enter py main.py

TODO: Exception Handling and Code Cleanup
