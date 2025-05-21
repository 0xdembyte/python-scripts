# Developer: Demarjio Brady
# Developed on: 19/05/2025 at ??:?? PM
# Last Revision: 21/05/2025 at 2:21 PM
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
ARTIST_ID = ""

# Encode the Spotify Developer Credentials into Base64
# This'll be used for the POST request since it requires a basic access authentication token
# https://en.wikipedia.org/wiki/Basic_access_authentication
client_credentials         = f"{CLIENT_ID}:{CLIENT_SECRET}"
client_credentials_encoded = b64encode(client_credentials.encode())
basic_authentication_token = client_credentials_encoded.decode()

# HTTP POST Settings
POST_url     = "https://accounts.spotify.com/api/token"
POST_headers = {
    "Authorization": f"Basic {basic_authentication_token}",
    "Content-Type": "application/x-www-form-urlencoded"
}
POST_data    = {
    "grant_type": "client_credentials"
}
POST_verify  = False # Used to disable the SSL certificate, since for some reason Ara doesn't like the requests library
                     # https://www.geeksforgeeks.org/ssl-certificate-verification-python-requests/
                     # Possible fix: Supply a Client Side SSL Certificate

# Request the General Spotify API Key
POST_response        = requests.post(url=POST_url, headers=POST_headers, data=POST_data, verify=POST_verify)
POST_response_json   = POST_response.json()

# Grab the OAuth Access Token (this'll be used for Bearear authorization)
# https://auth0.com/intro-to-iam/what-is-oauth-2
spotify_access_token = POST_response_json["access_token"]

# HTTP GET Settings
GET_url     = f"https://api.spotify.com/v1/artists/{ARTIST_ID}/albums?album_type=SINGLE&offset=20&limit=20"
print(GET_url)
GET_headers = {
    "Authorization": f"Bearer {spotify_access_token}" # https://swagger.io/docs/specification/v3_0/authentication/bearer-authentication/
}
GET_verify  = False # Used to disable the SSL certificate, since for some reason Ara doesn't like the requests library
                    # https://www.geeksforgeeks.org/ssl-certificate-verification-python-requests/
                    # Possible fix: Supply a Client Side SSL Certificate

# Request the Spotify Albums from our selected artist
GET_response      = requests.get(url=GET_url, headers=GET_headers, verify=GET_verify)
GET_response_json = GET_response.json()

def get_random_album(response):
    # Checks if the response list is empty or if items doesn't exist in the list
    if not response or not "items" in response:
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

    return album_name, album_release_date


# Grab a random album and get its details
random_album_name, random_album_release_date = get_random_album(GET_response_json)

# Check the data returned by the function to make sure we have valid data
if not random_album_name == "null" or not random_album_release_date == "null":
    # Output the name and release date in a nice format
    print(f"The random album is {random_album_name} released on {random_album_release_date}")
