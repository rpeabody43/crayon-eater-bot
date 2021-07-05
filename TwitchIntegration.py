import requests #funny library to work with APIs weeeee
import json     #This sucks and I don't understand it
import os       #getting info from .env again

def get_stream(streamer):
    #all these credentials should be in a secure file before hosting
    Client_ID = os.getenv('TwitchClientID')         #application id on twitch's website
    Client_Secret = os.getenv('TwitchClientSecret') #secret credential that might reset in however many days idk
    
    #request for an authenticator key for this session and converting it to an access token
    Auth = requests.post("https://id.twitch.tv/oauth2/token", {'client_id': Client_ID, 'client_secret': Client_Secret, 'grant_type': "client_credentials"})
    AuthJson = json.loads(Auth.text)
    AccessToken = "Bearer " + AuthJson['access_token']

    #combining the auth key and client id to get the stream information
    HEAD = {"Authorization": AccessToken, 
            "Client-Id": Client_ID}

    streamURL = "https://api.twitch.tv/helix/streams?user_login=" + streamer #streamer api link (tenz for now because he was live at the time)
    #get the data on a specific stream from the api and convert it to json
    stream = requests.get(url = streamURL, headers = HEAD)
    streamData = json.loads(stream.text)

    #twitch return go [first object item (an array called data)][object 2 index within array][object 2 item]
    #get streamer's user profile
    streamerURL = "https://api.twitch.tv/helix/users?login=" + streamer
    streamerProfile = requests.get(url = streamerURL, headers = HEAD)
    streamerProfileData = json.loads(streamerProfile.text)
    streamerPfp = streamerProfileData['data'][0]['profile_image_url']
    streamerName = streamerProfileData['data'][0]['display_name']

    #check if the streamer is live based on whether the data object exists, then trying to find the viewer count
    streamInfo = {}
    if streamData['data'] != []:
        try: 
            streamDataParsed = streamData['data'][0]
            viewers = streamDataParsed['viewer_count']
            streamTitle = streamDataParsed['title']
            streamGame = streamDataParsed['game_name']
            streamThumbnail = streamDataParsed['thumbnail_url']

            streamInfo = {
                'live': True, 
                'name': streamerName, 
                'pfp': streamerPfp, 
                'viewers': viewers, 
                'stream_title': streamTitle,
                'game': streamGame, 
                'thumbnail': str(streamThumbnail)
                }
            
        except Exception as e:
           return e
    else:
        streamInfo = {
                'live': False, 
                'name': streamerName, 
                'pfp': streamerPfp, 
                }
    return streamInfo
    #viewers = streamData['viewer_count']
    #print(streamData)
    #return streamData
