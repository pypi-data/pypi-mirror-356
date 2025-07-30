import requests
from typing import Optional
from huggingface_hub.hf_api import ModelInfo, DatasetInfo, SpaceInfo

from jingzhi.constants import DEFAULT_JINGZHI_ENDPOINT
from jingzhi.constants import REPO_TYPE_MODEL, REPO_TYPE_DATASET
from jingzhi.utils import _get_token

from typing import Literal


class JzApi:
    """
    Jzapi is a class that interacts with the jingzhi API.
    """
    def __init__(self):

        self.endpoint = DEFAULT_JINGZHI_ENDPOINT
        self.token =  _get_token()

    def list_models(self,
        sort:Literal["trending", "recently_update","most_download", "most_favorite"],
        per_page:int,
        page:int,   
        ):
        """
        List all models available on the jingzhi API.
        """
        url = self.endpoint + "/api/v1/models"
        headers = {"Authorization": f"Bearer {self.token}"}

        params = {
            "sort": sort,
            "per": per_page,
            "page": page,
        }
        response = requests.get(url,params)
        response.raise_for_status()
        return response.json()
    
    def list_datasets(self,
        sort:Literal["trending", "recently_update","most_download", "most_favorite"],
        per_page:int,
        page:int,   
        ):
        """
        List all datasets available on the jingzhi API.
        """
        url = self.endpoint + "/api/v1/datasets"
        headers = {"Authorization": f"Bearer {self.token}"}

        params = {
            "sort": sort,
            "per": per_page,
            "page": page,
        }
        response = requests.get(url,params)
        response.raise_for_status()
        return response.json()
    
    def model_info(
            self, 
            model_id:str
        ):
        """
        Get information about a specific model.
        """
        url = self.endpoint + f"/api/v1/models/{model_id}"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.get(url,headers=headers)
        response.raise_for_status()
        return response.json()
    
    def dataset_info(
            self, 
            dataset_id:str
        ):
        """
        Get information about a specific dataset.
        """
        url = self.endpoint + f"/api/v1/datasets/{dataset_id}"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.get(url,headers=headers)
        response.raise_for_status()
        return response.json()
    

    def repo_info(
            self, 
            repo_id:str,
            repo_type:Literal["dataset","model"]
        ):
        """
        Get information about a specific dataset or model.
        """
        if repo_type == "dataset":
            return self.dataset_info(repo_id)
        elif repo_type == "model":
            return self.model_info(repo_id)
        else:
            raise ValueError("repo_type must be either 'dataset' or 'model'")
        
    def repo_exists(
            self, 
            repo_id:str,
            repo_type:Literal[REPO_TYPE_MODEL,REPO_TYPE_DATASET]
        ):
        """
        Check if a dataset or model exists.
        """
        try:
            self.repo_info(repo_id, repo_type)
            return True
        except requests.HTTPError as e:
            return False
        else:
            raise e
    
    def file_exists(
            self, 
            repo_id:str,
            repo_type:Literal["dataset","model"],
            revision:str,
            file_name:str
        ):
        if revision is None:
            revision = "main"
        if repo_type == "model":
            url = self.endpoint + f"/hf/{repo_id}/resolve/{file_name}"
        elif repo_type == "dataset":
            url = self.endpoint + f"/hf/datasets/{repo_id}/resolve/{file_name}"
        print(url)
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {
            "revision":revision
        }
        try:
            response = requests.get(url,params=params,headers=headers)
            print(response)
            response.raise_for_status()
            
            return True
        except requests.HTTPError as e:
            return False
        
    def list_files(
            self,
            repo_id:str,
            repo_type:Literal["dataset","model"],
            revision:str
        ):
        repo_type = repo_type + 's'
        url = self.endpoint + f"/api/v1/{repo_type}/{repo_id}/all_files"
        print(url)
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.get(url,headers=headers)
            print(response)
            response.raise_for_status()
            
            return response
        except requests.HTTPError as e:
            return False
        
    def create_model(
            self,
            repo_id:str,
            token:Optional[str],
            private:Optional[bool]
        ):
        url = self.endpoint + f"/api/v1/models"
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {
            "name": "test5",
            "nickname": "你好",
            "namespace": "ww",
            "license": "other",
            "description": "",
            "private": private,
            "external_sources": []
        }
        response = requests.post(url,headers=headers,data=data)
        response.raise_for_status()
        return response.json()
    
    def create_dataset(
            self,
            repo_id:str,
            token:Optional[str],
            private:Optional[bool]
        ):
        url = self.endpoint + f"/api/v1/datasets"
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {
            "name": "test5",
            "nickname": "你好",
            "namespace": "ww",
            "license": "other",
            "description": "",
            "private": private,
            "external_sources": []
        }
        response = requests.post(url,headers=headers,data=data)
        response.raise_for_status()
        return response.json()
    
        
    def create_repo(
            self,
            repo_id:str,
            *
            token:Optional[str],
            private:Optional[bool],
            repo_type:Enum[REPO_TYPE_MODEL,REPO_TYPE_DATASET],

    ):
        if repo_type == REPO_TYPE_MODEL:
            self.create_model(repo_id,token,private)
        elif repo_type == REPO_TYPE_DATASET:
            self.create_dataset(repo_id,token,private)

    
        








