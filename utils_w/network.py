import urllib.request


def download_url(url: str, out_file_name: str):
    urllib.request.urlretrieve(url, filename=out_file_name)