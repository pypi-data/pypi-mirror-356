import os
import requests
from torrentp import TorrentDownloader
from io import BytesIO

from constants import JZ_PT_ENDPOINT, JZ_PT_USER_TOKEN,JZ_PT_HOME, JZ_PT_TORRENT_PATH
from constants import REPO_TYPE_MODEL, REPO_TYPE_DATASET

class JingzhiPT():
    def __init__(self, endpoint, user_token):
        
        self.endpoint = endpoint or JZ_PT_ENDPOINT
        self.user_token = user_token or JZ_PT_USER_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.user_token}"
        }
    def torrent_exists(self, repo_id, repo_type):
        if repo_type == REPO_TYPE_MODEL:
            url = f"{self.endpoint}/api/tf/model/{repo_id}/status"
        elif repo_type == REPO_TYPE_DATASET:
            url = f"{self.endpoint}/api/tf/dataset/{repo_id}/status"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            return True
        except requests.HTTPError as e:
            return False

    def get_torrent_metadata(self, repo_id, repo_type):
        check_exists = self.torrent_exists(repo_id, repo_type)
        if not check_exists:
            raise ValueError(f"{repo_type} {repo_id} does not exist")
        if repo_type == REPO_TYPE_MODEL:
            url = f"{self.endpoint}/api/tf/models/{repo_id}"
        elif repo_type == REPO_TYPE_DATASET:
            url = f"{self.endpoint}/api/tf/datasets/{repo_id}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            raise ValueError(f"Failed to get metadata for {repo_type} {repo_id}")
    def download_torrent(self,repo_id,repo_type,local_path,store_local=True):
        if local_path is None:
            local_path = JZ_PT_TORRENT_PATH
        if repo_type == REPO_TYPE_MODEL:
            url = f"{self.endpoint}/api/tf/models/{repo_id}/download/"
        elif repo_type == REPO_TYPE_DATASET:
            url = f"{self.endpoint}/api/tf/datasets/{repo_id}/download/"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            torrent = BytesIO(response.content)
            if store_local:
                local_path = os.path.join(local_path,f"{repo_type}_{repo_id}.torrents")
                with open(os.path.join(local_path,f"{repo_type}_{repo_id}.torrents"), "wb") as f:
                    f.write(response.content)
                return local_path
            return torrent
        except requests.HTTPError as e:
            raise ValueError(f"Failed to download torrent for {repo_type} {repo_id}")
    
    def download_repo(self,repo_id,repo_type,local_path=None):
        if local_path is None:
            local_path = JZ_PT_HOME
        torrent = self.download_torrent(repo_id,repo_type,store_local=True)
        torrent_file = TorrentDownloader(torrent,save_path=local_path)
        torrent_file.start_download()
        
        