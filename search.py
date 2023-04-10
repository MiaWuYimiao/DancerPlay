# # -*- coding: utf-8 -*-

# # Sample Python code for youtube.search.list
# # See instructions for running these code samples locally:
# # https://developers.google.com/explorer-help/code-samples#python

# import os

# import google_auth_oauthlib.flow
# import googleapiclient.discovery
# import googleapiclient.errors

# scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# def main():
#     # Disable OAuthlib's HTTPS verification when running locally.
#     # *DO NOT* leave this option enabled in production.
#     os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

#     api_service_name = "youtube"
#     api_version = "v3"
#     client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
#     DEVELOPER_KEY = 'AIzaSyAXlQataX1RHOLnxSk8U7eGZFbglWtFbbI'

#     # Get credentials and create an API client
#     # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
#     #     client_secrets_file, scopes)
#     # credentials = flow.run_console()
#     youtube = googleapiclient.discovery.build(
#         api_service_name, api_version, developerKey=DEVELOPER_KEY)

#     request = youtube.search().list(
#         part="snippet",
#         maxResults=10,
#         q="ballet+practice",
#         type="vedio",
#         videoDuration="short"
#     )
#     response = request.execute()

#     print(response)

# if __name__ == "__main__":
#     main()

import re

# API client library
import googleapiclient.discovery
# API information
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = 'AIzaSyAXlQataX1RHOLnxSk8U7eGZFbglWtFbbI'
# API client
youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
# Request body

def search_videos(type, subtype, length):
        count = int(length)/2;
        # Send request to youtube data api to get a list of video information.
        # The return information will contains videoId which used for embed youtube iframe
        idRequest = youtube.search().list(
                part="id,snippet",
                type='video',
                q=subtype+'music',
                videoDuration='short',
                videoDefinition='high',
                maxResults=count,
                videoEmbeddable='true',
                videoSyndicated='true',
        )
        # Request execution
        response = idRequest.execute()

        # Build initial list of videoId.
        playlist = []
        for item in response['items']:
                playlist.append(item['id']['videoId'])


        # Refine the list based on length
        # This request fetch the duration info of videos
        ids = ",".join(id for id in playlist)
        durationRequest = youtube.videos().list(
                part="contentDetails",
                id=ids
        )

        # Request execution
        response = durationRequest.execute()

        # Set target duration in sec
        # Note : length defines total duration in min
        durationTrg = (int(length))*60;
        # count the number of videos will be included in the playlist
        noVideos= 0
        durationTotal = 0
        for item in response['items']:
                dur = item['contentDetails']['duration']
                min = 0
                sec = 0
                if len(re.findall(r"(\d+)M", dur)) > 0:
                        min = int(re.findall(r"(\d+)M", dur)[0])
                if len(re.findall(r"(\d+)S", dur)) > 0:
                        sec = int(re.findall(r"(\d+)S", dur)[0])

                print(f"durationTrg {durationTrg}")
                
                if durationTrg-(min*60+sec) > 0:
                        durationTrg = durationTrg-(min*60+sec)
                        noVideos += 1
                        durationTotal += min*60+sec

        print(f"durationTotal {durationTotal}")
        return playlist[:noVideos], durationTotal
