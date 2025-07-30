import requests
from requests.exceptions import HTTPError



class RequestError(Exception):
    pass


class FileIntegrityError(Exception):
    pass


class InvalidParameter(Exception):
    pass

class FileDownloadError(Exception):
    pass
