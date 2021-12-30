import requests #funny library to work with APIs weeeee
import json     #This sucks and I don't understand it
import os       #getting info from .env again

#Streamer must be a twitch username like at the end of the url
#Returns a dictionary of all the needed info from the streamer
def get_stream(streamer: str) -> dict:
    #region docstring
    """
    A function that takes in a twitch username, such as xqc, and returns a dictionary of their stream status

    Parameters
    ---------- 
    streamer: str
        the username of the streamer to be processed
    
    Returns
    -------
    Dictionary that always returns:
        live        : boolean 
        name        : string 
        pfp         : image
    And only returns if they're live:
        viewers     : string 
        stream_title: string
        game        : string 
        thumbnail   : image
    """
    #endregion
    
    #all these credentials should be in a secure file before hosting
    Client_ID = os.getenv('TwitchClientID')         #application id on twitch's website
    Client_Secret = os.getenv('TwitchClientSecret') #secret credential that might reset in however many days idk
    
    #request for an authenticator key for this session and converting it to an access token
    Auth = requests.post("https://id.twitch.tv/oauth2/token", {'client_id': Client_ID, 'client_secret': Client_Secret, 'grant_type': "client_credentials"})
    AuthJson = json.loads(Auth.text)
    AccessToken = "Bearer " + AuthJson['access_token']

    #combining the auth key and client id to get the stream information
    HEAD = {
        "Authorization": AccessToken, 
        "Client-Id": Client_ID
        }

    streamURL = "https://api.twitch.tv/helix/streams?user_login=" + streamer #streamer api link 
    #get the data on a specific stream from the api and convert it to json
    stream = requests.get(url = streamURL, headers = HEAD)
    streamData = json.loads(stream.text)

    #twitch return go [first object item (an array called data)][object 2 index within array][object 2 item]
    #get streamer's user profile
    streamerURL = "https://api.twitch.tv/helix/users?login=" + streamer
    streamUserProfile = requests.get(url = streamerURL, headers = HEAD)
    userProfileData = json.loads(streamUserProfile.text)
    
    #check if the streamer is live based on whether the data object exists
    # If so we grab a bunch of other data such as viewer count and format it as json for ease of use later
    streamInfo = {}
    if streamData['data'] != []:
        try: 
            #shortening the reference to stream/streamer data
            streamDataParsed = streamData['data'][0]
            userDataParsed = userProfileData['data'][0]
            streamInfo = {
                'live': True, 
                'name': userDataParsed['display_name'], 
                'pfp': userDataParsed['profile_image_url'], 
                'viewers': streamDataParsed['viewer_count'], 
                'stream_title': streamDataParsed['title'],
                'game': streamDataParsed['game_name'], 
                'thumbnail': str(streamDataParsed['thumbnail_url'])
                }
            
        except Exception as e:
            return e
    else:
        streamInfo = {
            'live': False, 
            'name': userProfileData['data'][0]['display_name'], 
            'pfp': userProfileData['data'][0]['profile_image_url'], 
            }
    return streamInfo