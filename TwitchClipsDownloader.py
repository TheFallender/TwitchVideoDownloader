#------------------------------------------------------------------------------------------------------
#                                                IMPORTS
#------------------------------------------------------------------------------------------------------

from os import getcwd, system, path, name
import sys
from time import sleep
import re
from nerodia.browser import Browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as webDriverOptions
import urllib.parse as urlparse
from youtube_dl import YoutubeDL


#------------------------------------------------------------------------------------------------------
#                                                METHODS
#------------------------------------------------------------------------------------------------------

# Clear console
def clear (): 
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear') 


# Get the default download path
def get_download_path ():
    if name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return path.join(path.expanduser('~'), 'Downloads')


# Get the elements on the page
def getElements ():
    return browser.elements(css='.tw-hover-accent-effect__children > .tw-link.tw-interactive')


# Get the resource path bundled
def resource_path (relative_path):
    base_path = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))
    return path.join(base_path, relative_path)


#------------------------------------------------------------------------------------------------------
#                                          MAIN PROGRAM PARTS
#------------------------------------------------------------------------------------------------------

# Global Variables
creatorName = ""
videosToGet = 0
browser = None

# Get the Browser
def StartBrowserSetup ():
    # Browser defautls
    chromeOptions = webDriverOptions()          # Initialize options
    chromeOptions.add_argument('--headless')    # No pop-up window
    chromeOptions.add_argument("--mute-audio")  # No audio (thx god)

    # Try to get the browser
    try:    # Debug Mode
        chromeBrowser = webdriver.Chrome(executable_path = getcwd() + r'ChromeDrivers\\chromedriver.exe', options = chromeOptions)
    except: # Release Mode
        chromeBrowser = webdriver.Chrome(executable_path = resource_path(r'ChromeDrivers\\chromedriver.exe'), options = chromeOptions)

    # Clean mess
    clear()

    # Open browser
    return Browser(chromeBrowser)

# Intro of the system (gets the url)
def IntroSetup ():
    # Intro
    print(  
        "########### Twitch Vids Downloader ##########\n" +
        "############## by TheFallender ##############\n"
    )

    # Selection
    print("Hi there, welcome to the Twitch Clip Downloader, follow the steps to download the videos from Twitch\n")

    # Setup type
    setup = int(input("Select the setup:\n1. URL.\n2. Manual (clips only)\n3. Exit\nOption nº: "))

    # Padding
    print("")

    # Url set
    browserURL = ""
    if setup == 1:
        browserURL = input("Insert the url with the filters and the range: ")
    elif setup == 2:
        # Username request
        username = input("Enter the username:\nUsername: ") 

        # Range of the filter
        rangeDict = {
            "1": "all",
            "2": "30d",
            "3": "7d",
            "4": "24hr"
        }
        range = rangeDict[input("\nSelect the range from the list:\n1. All time.\n2. 30 days \n3. 7 days.\n4. 24 hours.\nOption nº: ")]

        # Format the URL
        browserURL = f'twitch.tv/{username}/clips?filter=clips&range={range}'
    else:
        sys.exit(0)

    # Clips to get
    global videosToGet
    videosToGet = int(input("\nNumber of videos/clips to get: "))

    return browserURL


# URL parse for the folders
def ParseURL2Folders (urlToUse: str):
    # Parse the url to get the filter and the range
    parsedURL = urlparse.parse_qs(urlparse.urlparse(urlToUse).query)

    # Folder destination
    folderStructure = get_download_path() + "\\"                                     # Downloads Path
    folderStructure += "Twitch" + "\\"                                               # Twitch folder
    global creatorName 
    creatorName = re.search(r'twitch.tv\/(.*)\/', urlToUse).group(1)
    folderStructure += creatorName + "\\"                                            # Creator folder
    if 'filter' in parsedURL:
        folderStructure += parsedURL['filter'][0] + "\\"                             # Filter folder (clips, videos, broadcasts)
    else:
        print("You need to enter a filter.")
        sys.exit(0)
    if 'range' in parsedURL:
        folderStructure += parsedURL['range'][0] + "\\"                              # Sort folder

    return folderStructure


# Element search and download
def SearchAndDownload ():
    # Get the videos
    elements = getElements()

    # Loop until all the videos are downloadeded
    i = 0
    while i < videosToGet:
        # Refresh if the elements are not enough 
        if i >= len(list(elements)):
            elements[i - 1].focus()
            elements = getElements()
            continue

        # URL
        urlVid = elements[i].attribute_value('href')

        # Get info of the vid and make the filename
        info = YoutubeDL().extract_info(url=urlVid, download=False)

        # Print the links
        print(
            f"\n{i + 1}. {info['title']}\n" +
            f"\tURL: {urlVid}"
        )

        # Get the output file
        fileName = f"{i + 1}. {info['title']}.{info['ext']}"

        # Download the vid with the filename setted
        YoutubeDL({
            'format': 'best',
            'outtmpl': folderStructure + fileName,
        }).download([urlVid])

        # Increase the index
        i += 1

#------------------------------------------------------------------------------------------------------
#                                               MAIN PROGRAM
#------------------------------------------------------------------------------------------------------

# Main program
if __name__ == '__main__':
    # Get the browser
    browser = StartBrowserSetup()

    # Clear the screen
    clear()

    # Setup parameters
    browserURL = IntroSetup()

    # Parse the URL to the folder structure
    folderStructure = ParseURL2Folders(browserURL)

    # Go to the address
    browser.goto(browserURL)

    # Search and Download
    SearchAndDownload()

    # Close browser
    browser.close()

    # Close Program
    print("\n\nThe software has finished downloading the videos.")
    print("It will close in 5s.")
    sleep(5)
    pass