import os


DEFAULT_JINGZHI_ENDPOINT = "https://aihub.caict.ac.cn"
DEFAULT_REVISION = "main"



REPO_TYPE_DATASET = "dataset"
REPO_TYPE_MODEL = "model"
REPO_TYPES = [None, REPO_TYPE_MODEL, REPO_TYPE_DATASET]


OPERATION_ACTION_API = "api"
OPERATION_ACTION_GIT = "git"
OPERATION_ACTION = [OPERATION_ACTION_API, OPERATION_ACTION_GIT]


default_home = os.path.join(os.path.expanduser("~"), ".cache")

JZ_HOME = os.path.expanduser(
    os.getenv(
        "JZ_HOME",
        os.path.join(os.getenv("XDG_CACHE_HOME", default_home), "jingzhi"),
    )
)


JZ_GIT_ACCESS_TOKEN_PATH = os.path.join(JZ_HOME, "git_access_token")
JZ_USER_NAME = os.path.join(JZ_HOME, "username")
JZ_ORG_NAME = os.path.join(JZ_HOME, "orgname")


DEFAULT_MAX_RETRIES = 3
DEFAULT_TIMEOUT = 5
DEFAULT_CHUNK_SIZE = 1024 * 1024

# mass
JZ_MASS_ENDPOINT = "https://aihub.caict.ac.cn/mapi/v1/"


# pt
JZ_PT_ENDPOINT = "https://aihub.caict.ac.cn/pt"
JZ_PT_HOME = os.path.join(JZ_HOME,"pt")
JZ_PT_TORRENT_PATH = os.path.join(JZ_PT_HOME,"torrents")

JZ_PT_USER_TOKEN = os.path.join(JZ_HOME, "user_token") 


GIT_ATTRIBUTES_CONTENT = """
*.duckdb filter=lfs diff=lfs merge=lfs -text
*.7z filter=lfs diff=lfs merge=lfs -text
*.arrow filter=lfs diff=lfs merge=lfs -text
*.bin filter=lfs diff=lfs merge=lfs -text
*.bz2 filter=lfs diff=lfs merge=lfs -text
*.ckpt filter=lfs diff=lfs merge=lfs -text
*.ftz filter=lfs diff=lfs merge=lfs -text
*.gz filter=lfs diff=lfs merge=lfs -text
*.h5 filter=lfs diff=lfs merge=lfs -text
*.joblib filter=lfs diff=lfs merge=lfs -text
*.lfs.* filter=lfs diff=lfs merge=lfs -text
*.lz4 filter=lfs diff=lfs merge=lfs -text
*.mlmodel filter=lfs diff=lfs merge=lfs -text
*.model filter=lfs diff=lfs merge=lfs -text
*.msgpack filter=lfs diff=lfs merge=lfs -text
*.npy filter=lfs diff=lfs merge=lfs -text
*.npz filter=lfs diff=lfs merge=lfs -text
*.onnx filter=lfs diff=lfs merge=lfs -text
*.ot filter=lfs diff=lfs merge=lfs -text
*.parquet filter=lfs diff=lfs merge=lfs -text
*.pb filter=lfs diff=lfs merge=lfs -text
*.pickle filter=lfs diff=lfs merge=lfs -text
*.pkl filter=lfs diff=lfs merge=lfs -text
*.pt filter=lfs diff=lfs merge=lfs -text
*.pth filter=lfs diff=lfs merge=lfs -text
*.rar filter=lfs diff=lfs merge=lfs -text
*.safetensors filter=lfs diff=lfs merge=lfs -text
saved_model/**/* filter=lfs diff=lfs merge=lfs -text
*.tar.* filter=lfs diff=lfs merge=lfs -text
*.tar filter=lfs diff=lfs merge=lfs -text
*.tflite filter=lfs diff=lfs merge=lfs -text
*.tgz filter=lfs diff=lfs merge=lfs -text
*.wasm filter=lfs diff=lfs merge=lfs -text
*.xz filter=lfs diff=lfs merge=lfs -text
*.zip filter=lfs diff=lfs merge=lfs -text
*.zst filter=lfs diff=lfs merge=lfs -text
*tfevents* filter=lfs diff=lfs merge=lfs -text
# Audio files - uncompressed
*.pcm filter=lfs diff=lfs merge=lfs -text
*.sam filter=lfs diff=lfs merge=lfs -text
*.raw filter=lfs diff=lfs merge=lfs -text
# Audio files - compressed
*.aac filter=lfs diff=lfs merge=lfs -text
*.flac filter=lfs diff=lfs merge=lfs -text
*.mp3 filter=lfs diff=lfs merge=lfs -text
*.ogg filter=lfs diff=lfs merge=lfs -text
*.wav filter=lfs diff=lfs merge=lfs -text
# Image files - uncompressed
*.bmp filter=lfs diff=lfs merge=lfs -text
*.gif filter=lfs diff=lfs merge=lfs -text
*.png filter=lfs diff=lfs merge=lfs -text
*.tiff filter=lfs diff=lfs merge=lfs -text
# Image files - compressed
*.jpg filter=lfs diff=lfs merge=lfs -text
*.jpeg filter=lfs diff=lfs merge=lfs -text
*.webp filter=lfs diff=lfs merge=lfs -text
"""

OPERATION_ACTION_GIT = "git"

GIT_HIDDEN_DIR = ".git"
GIT_ATTRIBUTES_FILE = ".gitattributes"
