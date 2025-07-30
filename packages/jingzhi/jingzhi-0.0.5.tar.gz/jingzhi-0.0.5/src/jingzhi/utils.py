import os
import hashlib
from pathlib import Path
from typing import Optional,Dict,Union
from urllib.parse import quote
import urllib
import requests
from datetime import datetime, timezone


from jingzhi.constants import JZ_GIT_ACCESS_TOKEN_PATH, REPO_TYPE_MODEL, REPO_TYPE_DATASET
from jingzhi.constants import DEFAULT_JINGZHI_ENDPOINT, DEFAULT_REVISION,JZ_HOME
from jingzhi.constants import JZ_HOME

from jingzhi.errors import FileIntegrityError

from huggingface_hub.hf_api import ModelInfo, DatasetInfo, SpaceInfo


def build_jz_headers(
        token: Optional[Union[bool, str]] ,
        headers: Optional[Dict[str, str]] = None ,
    ) -> Optional[Dict[str, str]]:
    if token is None:
        token = _get_token()
    if headers is None:
        headers = dict()
    jz_headers = {}
    if token is not None:
        jz_headers["authorization"] = f"Bearer {token}"
        jz_headers.update(headers)
    jz_headers["Accept-Encoding"] = ""
    return jz_headers



def _get_token():
    token = _get_token_from_environment() or _get_token_from_file()
    return token

def _get_token_from_file():
    try:
        return Path(JZ_GIT_ACCESS_TOKEN_PATH).read_text()
    except FileNotFoundError:
        return None

def _get_token_from_environment():
    return os.environ.get("JZ_GIT_ACCESS_TOKEN")


def compute_hash(file_path) -> str:
    BUFFER_SIZE = 1024 * 64  # 64k buffer size
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BUFFER_SIZE)
            if not data:
                break
            sha256_hash.update(data)
    return sha256_hash.hexdigest()



def get_repo_meta_path(repo_type: str, repo_id: str, revision: Optional[str] = None, endpoint: Optional[str] = None) -> str:
    if revision is None:
        revision = DEFAULT_REVISION
    if endpoint is None:
        endpoint = DEFAULT_JINGZHI_ENDPOINT
    if repo_type == REPO_TYPE_MODEL or repo_type == REPO_TYPE_DATASET :
        path = (
            f"{endpoint}/hf/api/{repo_type}s/{repo_id}/revision/main"
            if revision is None
            else f"{endpoint}/hf/api/{repo_type}s/{repo_id}/revision/{quote(revision, safe='')}"
        )
    else:
        raise ValueError("repo_type must be one of 'model', 'dataset'")
    print(path)
    return path


def get_file_download_url(
    model_id: str,
    file_path: str,
    revision: str,
    repo_type: Optional[str] = None,
    endpoint: Optional[str] = None,
) -> str:
    """Format file download url according to `model_id`, `revision` and `file_path`.
    Args:
        model_id (str): The model_id.
        file_path (str): File path
        revision (str): File revision.

    Returns:
        str: The file url.
    """
    if endpoint is None:
        endpoint = DEFAULT_JINGZHI_ENDPOINT
    file_path = urllib.parse.quote(file_path)
    revision = urllib.parse.quote(revision)
    download_url_template = '{endpoint}/hf/{model_id}/resolve/{revision}/{file_path}'
    if repo_type == REPO_TYPE_DATASET:
        download_url_template = '{endpoint}/hf/datasets/{model_id}/resolve/{revision}/{file_path}'
    return download_url_template.format(
        endpoint=endpoint,
        model_id=model_id,
        revision=revision,
        file_path=file_path,
    )



def get_cache_dir(model_id: Optional[str] = None, repo_type: Optional[str] = None) -> Union[str, Path]:
    """cache dir precedence:
        function parameter > environment > ~/.cache/jingzhi/hub

    Args:
        model_id (str, optional): The model id.
        repo_type (str, optional): The repo type

    Returns:
        str: the model_id dir if model_id not None, otherwise cache root dir.
    """
    default_cache_dir = JZ_HOME
    sub_dir = 'hub'
    if repo_type == "dataset":
        sub_dir = 'dataset'
    base_path = os.getenv('JZ_HOME', os.path.join(default_cache_dir, sub_dir))
    return base_path if model_id is None else os.path.join(
        base_path, model_id + '/')


def model_id_to_group_owner_name(model_id: str):
    if "/" in model_id:
        group_or_owner = model_id.split("/")[0]
        name = model_id.split("/")[1]
    return group_or_owner, name


def file_integrity_validation(file_path,
                              expected_sha256) -> None:
    """Validate the file hash is expected, if not, delete the file

    Args:
        file_path (str): The file to validate
        expected_sha256 (str): The expected sha256 hash

    Raises:
        FileIntegrityError: If file_path hash is not expected.

    """
    file_sha256 = compute_hash(file_path)
    if not file_sha256 == expected_sha256:
        os.remove(file_path)
        msg = 'File %s integrity check failed, the download may be incomplete, please try again.' % file_path
        raise FileIntegrityError(msg)


def model_info(
    repo_id: str,
    *,
    revision: Optional[str] = None,
    timeout: Optional[float] = None,
    securityStatus: Optional[bool] = None,
    files_metadata: bool = False,
    token: Union[bool, str, None] = None,
    endpoint: Optional[str] = None
) -> ModelInfo:
    """
    Note: It is a huggingface method moved here to adjust Jinzhi server response.

    Get info on one specific model on huggingface.co

    Model can be private if you pass an acceptable token or are logged in.

    Args:
        repo_id (`str`):
            A namespace (user or an organization) and a repo name separated
            by a `/`.
        revision (`str`, *optional*):
            The revision of the model repository from which to get the
            information.
        timeout (`float`, *optional*):
            Whether to set a timeout for the request to the Hub.
        securityStatus (`bool`, *optional*):
            Whether to retrieve the security status from the model
            repository as well.
        files_metadata (`bool`, *optional*):
            Whether or not to retrieve metadata for files in the repository
            (size, LFS metadata, etc). Defaults to `False`.
        token (Union[bool, str, None], optional):
            A valid user access token (string). Used to build Jinzhi server request
            header.

    Returns:
        [`huggingface_hub.hf_api.ModelInfo`]: The model repository information.

    <Tip>

    Raises the following errors:

        - [`~utils.RepositoryNotFoundError`]
          If the repository to download from cannot be found. This may be because it doesn't exist,
          or because it is set to `private` and you do not have access.
        - [`~utils.RevisionNotFoundError`]
          If the revision to download from cannot be found.

    </Tip>
    """
    headers = build_jz_headers(token=token)
    path = get_repo_meta_path(repo_type=REPO_TYPE_MODEL, repo_id=repo_id, revision=revision, endpoint=endpoint)
    params = {}
    if securityStatus:
        params["securityStatus"] = True
    if files_metadata:
        params["blobs"] = True
    r = requests.get(path, headers=headers, timeout=timeout, params=params)
    r.raise_for_status()
    data = r.json()
    return ModelInfo(**data)

def dataset_info(
    repo_id: str,
    *,
    revision: Optional[str] = None,
    timeout: Optional[float] = None,
    files_metadata: bool = False,
    token: Union[bool, str, None] = None,
    endpoint: Optional[str] = None,
) -> DatasetInfo:
    """
    Get info on one specific dataset on huggingface.co.

    Dataset can be private if you pass an acceptable token.

    Args:
        repo_id (`str`):
            A namespace (user or an organization) and a repo name separated
            by a `/`.
        revision (`str`, *optional*):
            The revision of the dataset repository from which to get the
            information.
        timeout (`float`, *optional*):
            Whether to set a timeout for the request to the Hub.
        files_metadata (`bool`, *optional*):
            Whether or not to retrieve metadata for files in the repository
            (size, LFS metadata, etc). Defaults to `False`.
        token (Union[bool, str, None], optional):
            A valid user access token (string). Defaults to the locally saved
            token, which is the recommended method for authentication (see
            https://huggingface.co/docs/huggingface_hub/quick-start#authentication).
            To disable authentication, pass `False`.

    Returns:
        [`hf_api.DatasetInfo`]: The dataset repository information.

    <Tip>

    Raises the following errors:

        - [`~utils.RepositoryNotFoundError`]
            If the repository to download from cannot be found. This may be because it doesn't exist,
            or because it is set to `private` and you do not have access.
        - [`~utils.RevisionNotFoundError`]
            If the revision to download from cannot be found.

    </Tip>
    """
    headers = build_jz_headers(token=token)
    path = get_repo_meta_path(repo_type=REPO_TYPE_DATASET, repo_id=repo_id, revision=revision, endpoint=endpoint)
    params = {}
    if files_metadata:
        params["blobs"] = True
    r = requests.get(path, headers=headers, timeout=timeout, params=params)
    r.raise_for_status()
    data = r.json()
    return DatasetInfo(**data)




def get_repo_info(
    repo_id: str,
    *,
    revision: Optional[str] = None,
    repo_type: Optional[str] = None,
    timeout: Optional[float] = None,
    files_metadata: bool = False,
    token: Union[bool, str, None] = None,
    endpoint: Optional[str] = None
) -> Union[ModelInfo, DatasetInfo, SpaceInfo]:
    """
    Get the info object for a given repo of a given type.

    Args:
        repo_id (`str`):
            A namespace (user or an organization) and a repo name separated
            by a `/`.
        revision (`str`, *optional*):
            The revision of the repository from which to get the
            information.
        repo_type (`str`, *optional*):
            Set to `"dataset"` or `"space"` if getting repository info from a dataset or a space,
            `None` or `"model"` if getting repository info from a model. Default is `None`.
        timeout (`float`, *optional*):
            Whether to set a timeout for the request to the Hub.
        files_metadata (`bool`, *optional*):
            Whether or not to retrieve metadata for files in the repository
            (size, LFS metadata, etc). Defaults to `False`.
        token (Union[bool, str, None], optional):
            A valid user access token (string). Defaults to the locally saved
            token.

    Returns:
        `Union[SpaceInfo, DatasetInfo, ModelInfo]`: The repository information, as a
        [`huggingface_hub.hf_api.DatasetInfo`], [`huggingface_hub.hf_api.ModelInfo`]
        or [`huggingface_hub.hf_api.SpaceInfo`] object.

    <Tip>

    Raises the following errors:

        - [`~utils.RepositoryNotFoundError`]
          If the repository to download from cannot be found. This may be because it doesn't exist,
          or because it is set to `private` and you do not have access.
        - [`~utils.RevisionNotFoundError`]
          If the revision to download from cannot be found.

    </Tip>
    """
    if repo_type is None or repo_type == REPO_TYPE_MODEL:
        method = model_info
    elif repo_type == REPO_TYPE_DATASET:
        method = dataset_info
    else:
        raise ValueError("Unsupported repo type.")
    return method(
        repo_id,
        revision=revision,
        token=token,
        timeout=timeout,
        files_metadata=files_metadata,
        endpoint=endpoint
    )


def filter_repo_objects(
                items,
                allow_patterns,
                ignore_patterns,
            ):
    if allow_patterns is not None:
        items = [item for item in items if any(re.search(p, item) for p in allow_patterns)]
    if ignore_patterns is not None:
        items = [item for item in items if not any(re.search(p, item) for p in ignore_patterns)]
    return items

def pack_repo_file_info(repo_file_path,
                        revision) -> Dict[str, str]:
    repo_file_info = {'Path': repo_file_path,
                      'Revision': revision}
    return repo_file_info



    
