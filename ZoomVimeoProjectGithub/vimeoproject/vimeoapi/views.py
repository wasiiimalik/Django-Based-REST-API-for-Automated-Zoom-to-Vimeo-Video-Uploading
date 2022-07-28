from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import vimeo
from rest_framework.decorators import api_view
import requests

zoom_token = "zoom Jwt token"


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


client = vimeo.VimeoClient(
  token='Vimeo Token',
  key='Vimeo Key',
  secret='vimeo secret key'
)






@api_view(['POST','GET'])
def uploadVideo(request):
    data = request.data
    print(data)
    file_name = data['path']
    uri = client.upload(file_name, data={
    'name': data['videoname'],
    'description': data['videodescription']
    })
    print("success")
    print('Your video URI is: %s' % (uri))
    return HttpResponse({"process":uri}.values() )



@api_view(['POST','GET'])
def uploadvideotospecificfolder(request):
    data = request.data
    folderid = data['folderid']
    videoid = data['videoid']
    endpoint = "https://api.vimeo.com/me/projects/"+str(folderid)+"/videos/"+str(videoid)
    requests.put(endpoint,auth=BearerAuth('vimeo jwt token'))
    return HttpResponse({"process":"Completed"}.values())
    

@api_view(['POST','GET'])
def getvideospresentinspecificfolder(request):
    data = request.data
    folderid =  data['folderid']
    endpoint = "https://api.vimeo.com/me/projects/"+str(folderid)+"/videos"
    data = requests.get(endpoint,auth=BearerAuth('vimeo jwt token'))
    print(data.json())
    return HttpResponse({"process":data.json()}.values())




@api_view(['POST','GET'])
def createfolder(request):
    data = request.data
    print(data)
    folder_name = data['name']
    endpoint = 'https://api.vimeo.com/me/projects'
    requests.post(endpoint,data = {'name':folder_name},auth=BearerAuth('vimeo jwt token'))
    return HttpResponse({"process":"worked"})

  




@api_view(['POST','GET'])
def listfolders(request):
    endpoint = 'https://api.vimeo.com/users/180421876/folders'
    data = requests.get(endpoint,auth=BearerAuth('vimeo jwt token'))
    data = data.json()
    Info_about_folders = {}
    count=0
    for i in range(len(data['data'])):
      dct = {}
      dct['FolderName'] = data['data'][i]['name']
      dct['FolderCreater'] = data['data'][i]['user']['name']
      dct['last_user_action_event_date'] = data['data'][i]['last_user_action_event_date']
      folder_id = str(data['data'][i]['uri']) 
      folder_id = folder_id.split('/')
      folder_id = folder_id[-1]
      dct['folder_id'] = folder_id
      Info_about_folders[count] = dct
      count = count + 1
    
    print(Info_about_folders)
    return HttpResponse({'foldersData':Info_about_folders}.values())






@api_view(['POST','GET'])
def specificfoldersdetail(request):
    folderid = request.data['folderid']
    endpoint = 'https://api.vimeo.com/me/projects/' + str(folderid)
    data = requests.get(endpoint,auth=BearerAuth('vimeo jwt token'))
    data=data.json()
    Info_about_folder = {}
    dct = {}
    dct['FolderName'] = data['name']
    dct['FolderCreater'] = data['user']['name']
    dct['last_user_action_event_date'] = data['last_user_action_event_date']
    folder_id = str(data['uri']) 
    folder_id = folder_id.split('/')
    folder_id = folder_id[-1]
    dct['folder_id'] = folder_id
    Info_about_folder['folderData'] = dct
    return HttpResponse({'foldersData':Info_about_folder}.values())








@api_view(['POST','GET'])
def webhookzoom(request):
    data = request.data
    db_data = {}

    if data['event'] == "meeting.participant_joined":
        db_data['account_id'] = data['payload']['account_id']
        db_data['user_id'] = data['payload']['object']['participant']['user_id']
        db_data['user_name'] = data['payload']['object']['participant']['user_name']
        db_data[''] = str(data['payload']['object']['participant']['date_time']).split('T')[-1]
        db_data['email'] = data['payload']['object']['participant']['email']
        print(db_data)

        
    if data['event'] == "meeting.participant_left":
        db_data['account_id'] = data['payload']['account_id']
        db_data['user_id'] = data['payload']['object']['participant']['user_id']
        db_data['user_name'] = data['payload']['object']['participant']['user_name']
        db_data['leave_time'] = str(data['payload']['object']['participant']['date_time']).split('T')[-1]
        db_data['email'] = data['payload']['object']['participant']['email']
        print(db_data)

        
    if data['event'] == "recording.started":
        db_data['topic'] = data['payload']['object']['topic']
        db_data['topic'] = data['payload']['object']['start_time']
        print(db_data)



    if data['event'] == "recording.stopped":
        db_data['topic'] = data['payload']['object']['topic']
        db_data['topic'] = data['payload']['object']['recording_file']['recording_end']
        print(db_data)


    return HttpResponse({'webhook':data}.values())









@api_view(['POST','GET'])
def listzoomrecording(request):
    data = request.data
    endpoint = "https://api.zoom.us/v2/users/"+str(data['userid'])+"/recordings?from="+str(data['from'])+"&to="+str(data['to'])
    data = requests.get(endpoint,auth=BearerAuth(zoom_token))
    data = data.json()
    print(data)
    meetingdata = {}
    count = 0
    for i in range(0,len(data['meetings'])):
        inside = {}
        inside['topic'] = data['meetings'][i]['topic']
        inside['uuid'] = data['meetings'][i]['uuid']
        try:
            for j in range(len(data['meetings'][i]['recording_files'])):
                if data['meetings'][i]['recording_files'][j]['recording_type'] == 'shared_screen_with_speaker_view':
                    inside['recording_start'] =  data['meetings'][i]['recording_files'][j]['recording_start']
                    inside['recording_end'] =  data['meetings'][i]['recording_files'][j]['recording_end']
                    inside['download_url'] =  data['meetings'][i]['recording_files'][j]['download_url']        
            meetingdata[count] = inside
            count = count + 1
        except:
            count = count + 1
    return HttpResponse({'meetingsData':meetingdata}.values())










@api_view(['POST','GET'])
def getspecificmeeting(request):
    data = request.data
    url = "https://api.zoom.us/v2/meetings/"+str(data['meeting_id'])+"/recordings?include_fields=download_access_token"
    data = requests.get(url,auth=BearerAuth(zoom_token))
    GSM = data.json()
    meetingData = {}
    meetingData['uuid'] = GSM['uuid']
    meetingData['topic'] = GSM['topic']
    meetingData['download_access_token'] = GSM['download_access_token']
    print(GSM)
    for i in range(len(GSM['recording_files'])):
        if GSM['recording_files'][i]['recording_type'] == 'shared_screen_with_speaker_view':
            meetingData['download_url'] = GSM['recording_files'][i]['download_url']
            meetingData['recording_start'] = GSM['recording_files'][i]['recording_start']
            meetingData['recording_end'] = GSM['recording_files'][i]['recording_end']
    return HttpResponse({'meetingsData':meetingData}.values())








@api_view(['POST','GET'])
def downloadzoomrecording(request):
    data = request.data
    url = data['url']
    token = data['token']
    topic = data['topic']
    params = {
    "access_token": token
    }
    res = requests.get(url,  params=params)
    with open("E:/My Documents/InsideAIML/apidownloadrecording/"+topic+".mp4", "wb") as f:
        f.write(res.content)
        f.close()
        print("data",data)
    return HttpResponse({'Response':"Video Downloaded Successfully "}.values())

    