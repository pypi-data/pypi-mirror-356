import os
from jingzhi.constants import DEFAULT_JINGZHI_ENDPOINT 
from pycsghub.snapshot_download import snapshot_download
from pycsghub.file_download import get_file_download_url
from pycsghub.utils import get_repo_meta_path

def test_snapshot_download_model():

    endpoint = "https://aihub.caict.ac.cn"

    repo_id = "FuseAI/FuseChat-Qwen-2.5-7B-Instruct"
    repo_type = "model"

    token = "b4cf9112b6cbc9d15b2b29f57a9b8696871ebc09"

    snapshot_download(endpoint=endpoint, token=token, repo_id=repo_id, repo_type=repo_type)

def test_snapshot_download_dataset():

    endpoint = "https://aihub.caict.ac.cn"

    repo_id = "ww/test_model"
    repo_type = "model"



    snapshot_download(endpoint=endpoint, repo_id=repo_id, repo_type=repo_type)

# test_snapshot_download_model()

def test_get_file_download_url():
    model_id = "ww/test_model"
    file_path = "README.md"
    revision = "main"
    repo_type = "model"
    endpoint = DEFAULT_JINGZHI_ENDPOINT

    print(get_file_download_url(model_id, file_path, revision, repo_type,endpoint))

def test_get_repo_meta_path():
    model_id = "ww/test_model"
    file_path = "README.md"
    revision = "main"
    repo_type = "model"
    endpoint = DEFAULT_JINGZHI_ENDPOINT
    print(get_repo_meta_path(repo_type=repo_type,repo_id=model_id,revision=revision,endpoint=endpoint))

test_get_repo_meta_path()