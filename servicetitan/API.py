# API.py
# Author: Mahdi Hasan Shuvo
# Developer: Mahdi Hasan Shuvo
# Version: 1.0
# ---- Imports Libraries ----
from requests import get,post, Session,Response,request,RequestException
from json import loads,dumps
from time import sleep
from random import randint
from os import system
from sys import exit
import time 
import warnings,os
from datetime import datetime
import mimetypes
from requestssmm.utlites import __formate_coki__
warnings.filterwarnings("ignore")

os.makedirs('Downloads',exist_ok=True)

headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://go.servicetitan.com',
    'priority': 'u=1, i',
    'referer': 'https://go.servicetitan.com/',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    # 'x-csrf-token': 'kyBgMLDj9ECqT7Mz12/FvILiyMMfrrZ/LasxzQTCZdc=',
    'x-requested-with': 'XMLHttpRequest',
}

def DownloadFile(url,output_file:str,coki) -> str | None:
    try:
        response = get(url, headers=headers, stream=True,cookies=__formate_coki__(coki))

        if response.status_code == 200:
            with open('Downloads/' + output_file, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print("Download completed! File saved as:", output_file)
            return os.path.abspath('Downloads/' + output_file)
        else:
            print("Failed to download:", response.status_code)

    except Exception as e:
        print(f"An error occurred: {e}")

def make_request(url, cookies, headers, method, data = None) -> Response.json | None:
    try:
        response = request(method, url, cookies=cookies, headers=headers, json=data if data else None)
        return response.json()
    except RequestException as e:
        print(f'Failed to make request: {e}')

def get_all_folder_id(sourceId:str | int,coki:str) -> list | None:
    try:
        json_data = {'offset': 0,'limit': 100,'name': '','isRecursive': False,'pathTypes': [
        {
        'pathType': 'Folder',
        },],
        'sources': [
        {
        'sourceId': str(sourceId),
        'sourceType': 'Project',
        "jobNumber": str(sourceId),
        "createdOn": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        },
        ],
        'creators': [],
        'sortOrder': [
        {
        'field': 'Name',
        'direction': 'Asc',
        },],
        'labels': [],
        'isPinned': False,
        'isStarred': False,
        'createdOn': {
        'from': None,'to': None,
        },
        }      
        response=make_request('https://go.servicetitan.com/app/api/fam/documents/search',
                              cookies=__formate_coki__(coki),
                              headers = headers,
                              method='POST',
                              data=json_data,)
        # print(response)
        return [{'id': item['id'], 'name': item['name']} for item in response['data']['results']]

        # return [id['id'] for id in response['data']['results']]
    except Exception as e:
        print(e)
        pass

def get_file_info(sourceId:int | str,file_id:int|str,coki:str) -> dict | None:

    try:
        json_data = {
    'offset': 0,
    'limit': 30,
    'name': '',
    'parentId': int(file_id),
    'isRecursive': False,
    'pathTypes': [
        {
            'pathType': 'File',
        },
    ],
    'sources': [
        {
        'sourceId': str(sourceId),
        'sourceType': 'Project',
        # "jobNumber": str(sourceId),
        # "createdOn": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        },
        
    ],
    'creators': [],
    'sortOrder': [
        {
            'field': 'CreatedOn',
            'direction': 'Desc',
        },
    ],
    'labels': [],
    'isPinned': False,
    'isStarred': False,
    'createdOn': {
        'from': None,
        'to': None,
    },
}
        response=make_request(f'https://go.servicetitan.com/app/api/fam/documents/search',
                              cookies=__formate_coki__(coki),
                              headers = headers,
                              method='POST',
                              data=json_data
                              )
        return response['data']['results']
    except Exception as e:
        print(e)
        pass

def Uploads_file(file_path:str,sourceId:int|str,folder_id:int|str,coki:str) -> dict | None:
    try:
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        file_name_no_dot = file_name.replace('.', '')
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        # print(f"Uploading: {file_name}")
        # print(f"Size: {file_size} bytes")
        # print(f"MIME Type: {mime_type}")
        with open(file_path, 'rb') as f:
            files = {
                'file': ('blob', f, 'application/octet-stream')
            }
            
            data = {
                'resumableChunkNumber': '1',
                'resumableChunkSize': '1048576',
                'resumableCurrentChunkSize': str(file_size),
                'resumableTotalSize': str(file_size),
                'resumableType': mime_type,
                'resumableIdentifier': f'{file_size}-{file_name_no_dot}',
                'resumableFilename': file_name,
                'resumableRelativePath': file_name,
                'resumableTotalChunks': '1',
                'name': file_name,
                'parentId': str(folder_id),
                'sources': dumps([{"sourceType":"Project","sourceId":str(sourceId)}]),
                'duplicateResolution': '0'
            }
            # Remove content-type (lowercase!) - let requests set it
            headers_copy = headers.copy()
            headers_copy.pop('content-type', None)  # lowercase to match your key
            
            response = post(
                'https://go.servicetitan.com/app/api/fam/documents/files',
                cookies=__formate_coki__(coki),
                headers=headers_copy,
                data=data,
                files=files
            )
        # os.remove(file_path)
    except Exception as e:
        print(e)
        pass

    return response or None



def serch_project_id(coki:str) -> dict | None:
    try:
        all_uid=[]
        # for i in range(3):
        json_data = {
            'page': 1,
            'pageSize': 100,
            'filters': {
                'textSearch': 'test',
                'textSearchType': 4,
                'filterResultsSearchType': 4,
                'businessUnitIds': [],
                'projectTypeIds': [],
                'statusIds': [],
                'subStatusIds': [],
                'showProjectsWithoutStatus': False,
                'projectManagerIds': [],
                'dateType': 2,
                'total': {},
                'totalJobs': {},
                'completedJobs': {},
                'projectsWithoutGroupsOnly': False,
                'excludeProjectGroupProjects': True,
            },
            'includeTotal': True,
            'customFieldTypeIds': [],
        }

        response = make_request(
            url='https://go.servicetitan.com/app/api/project-search/search-projects',
            method='POST',
            cookies=__formate_coki__(coki),
            headers=headers,
            data=json_data,
        )
        # print(response)
        for i in response['data']:
            all_uid.append(i['id'])
        return set(all_uid)
    except Exception as e:
        print(e)
        pass




