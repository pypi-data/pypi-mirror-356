from jingzhi.file_download import get_file_download_url
from jingzhi.file_download import file_download


def test_get_file_download_url():
    model_id = "ww/test_model"
    file_path = "README.md"
    revision = "main"
    repo_type = "model"

    print(get_file_download_url(model_id, file_path, revision, repo_type))

def test_file_download():
    token = "b4cf9112b6cbc9d15b2b29f57a9b8696871ebc09"
    model_id = "ww/test_model"
    file_path = "README.md"
    revision = "main"
    repo_type = "model"
    file_download(model_id, file_name=file_path, revision=revision, repo_type=repo_type, token=token)

test_file_download()