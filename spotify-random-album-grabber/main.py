# Developer: Demarjio Brady
# Developed on: 19/05/2025 at ??:?? PM
# Last Revision: 26/05/2025 at 2:09PM
# Description: This Python script automatically retrieves a random song/album from the desired arist listed in the get_url variable.
#              It handles generating the authentication keys needed for the Spotify API.
# Notes: The Spotify Developer Settings HAVE to be correct for the POST request to grab the Basic authentication key correctly, if not this script will function as intended.

# Imports
from base64 import b64encode
from random import randint
import requests

# Spotify Developer Settings
CLIENT_ID         = ""
CLIENT_SECRET     = ""

# Spotify Artist Settings
ARTIST_ID           = "1zNqQNIdeOUZHb8zbZRFMX"
ARTIST_ALBUM_OFFSET = "20"
ARTIST_ALBUM_LIMIT  = "20"

# Global HTTP Settings
VERIFY_SSL_CERTIFICATE = False # Used to disable the SSL certificate, since for some reason Ara doesn't like the requests library
                               # https://www.geeksforgeeks.org/ssl-certificate-verification-python-requests/
                               # Possible fix: Supply a Client Side SSL Certificate

# Encode the Spotify Developer Credentials into Base64
# This'll be used for the POST request since it requires a basic access authentication token
client_credentials         = f"{CLIENT_ID}:{CLIENT_SECRET}"
client_credentials_encoded = b64encode(client_credentials.encode())
basic_authentication_token = client_credentials_encoded.decode()

# Basic Authentication Token Settings
basic_auth_token_url     = "https://accounts.spotify.com/api/token"
basic_auth_token_headers = {
    "Authorization": f"Basic {basic_authentication_token}",
    "Content-Type": "application/x-www-form-urlencoded"
}
basic_auth_token_data    = {
    "grant_type": "client_credentials"
}

# Request the General Spotify API Key
basic_auth_token_response      = requests.post(url=basic_auth_token_url, headers=basic_auth_token_headers, data=basic_auth_token_data, verify=VERIFY_SSL_CERTIFICATE)
basic_auth_token_response_json = basic_auth_token_response.json()

# Grab the OAuth Access Token (this'll be used for Bearear authorization)
oauth_access_token         = basic_auth_token_response_json["access_token"]
bearer_auth_token          = f"Bearer {oauth_access_token}"

# Album Settings
album_url     = f"https://api.spotify.com/v1/artists/{ARTIST_ID}/albums?album_type=SINGLE&offset={ARTIST_ALBUM_OFFSET}&limit={ARTIST_ALBUM_LIMIT}"
album_headers = {
    "Authorization": bearer_auth_token
}

# Request the Spotify Albums from our selected artist
album_response      = requests.get(url=album_url, headers=album_headers, verify=VERIFY_SSL_CERTIFICATE)

# JSONify our album response
album_response_json = album_response.json()

def get_random_album(response):
    # Checks if the response list is empty or if items doesn't exist in the list
    if not response or not "items" in response:
        # Output telling the user the response was empty or items was null
        print("Response was empty, or items was null.")
        return "null", "null"

    # Grabs the albums from the response
    albums_list        = response["items"]

    # Get the length of the albums list table this is used for randomizing an index
    albums_list_length = len(albums_list)

    # Grabs an album from the list with a randomized index
    # Fixed the indexing from my poem script
    random_index       = randint(0, albums_list_length - 1)

    # Grabs an album from the list with the randomized index
    random_album       = albums_list[random_index]

    # Basic album details
    album_name         = random_album["name"]
    album_release_date = random_album["release_date"]
    album_uri          = random_album["uri"]

    # Return the album details
    return album_name, album_release_date, album_uri

def play_song(uri):
    # Playback API settings
    playback_api_url = "https://api.spotify.com/v1/me/player/play"
    playback_headers = {
        "Authorization": bearer_auth_token,
        "Content-Type": "application/json"
    }
    playback_data    = {
        "context_uri": uri,
    }

    # Send our song data to the playback api 
    playback_response    = requests.put(url=playback_api_url, headers=playback_headers, data=playback_data, verify=VERIFY_SSL_CERTIFICATE)

    # JSONify our playback response
    playback_json        = playback_response.json()

    # Get the response status code
    playback_status_code = playback_response.status_code

    # Match the status codes
    match playback_status_code:
        # Status code 204 (No content)
        case 204:
        
            # Output to the user that playback was successful
            print("Playback started successfully.")

        # Status code 403 (Forbidden)
        case 403:

            # Output to the user that the request was forbidden
            print("Playback request forbidden (403).")

            # Checks if the response list is empty or if error doesn't exist in the list
            if not playback_json or not "error" in playback_json:
                # Output telling the user the response was empty or error was null
                print("Play response was empty, or error was null")
            else:
                # Get the error from the response
                error         = playback_json["error"]

                # Get the error message
                error_message = error["message"]

                # Checks the error message to see if it was caused by the user not having spotify premium
                if error_message == "Player command failed: Premium required":
                    # Output telling the user they need spotify premium
                    print("Spotify Premium is required to use this feature.")
                else:
                    # We don't know the reason let the user know the error message
                    print(f"An unknown error has occured, message: {error_message}")
                    
        # For any other status code that isn't 204 or 403
        case default:
                # We don't know the reason let the user know the status code
                print(f"An unknown error has occured, status code: {playback_status_code}")

# Grab a random album and get its details
random_album_name, random_album_release_date, random_album_uri = get_random_album(album_response_json)

# Check the data returned by the function to make sure we have valid data
# Output the name and release date in a nice format
print(f"The random album is {random_album_name} released on {random_album_release_date}")
play_song(random_album_uri)
