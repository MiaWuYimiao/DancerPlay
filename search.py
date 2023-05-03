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

def search_videos(style, type, length):
        count = int(length)/2;
        # Send request to youtube data api to get a list of video information.
        # The return information will contains videoId which used for embed youtube iframe
        idRequest = youtube.search().list(
                part="id,snippet",
                type='video',
                q=type+'music',
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
                musicItem = {
                        "title" : item['snippet']['title'],
                        "style" : style,
                        "type" : type,
                        "videoId" : item['id']['videoId'],
                        "image_url" : item['snippet']['thumbnails']['high']['url']
                }
                print(musicItem)
                playlist.append(musicItem)


        # Refine the list based on length
        # This request fetch the duration info of videos
        ids = ",".join(item["videoId"] for item in playlist)
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
