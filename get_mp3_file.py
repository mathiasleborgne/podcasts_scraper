import os
import requests
from tqdm import tqdm

folder_mp3 = "mp3_files"

def get_html_text(url_input):
    # get html from url
    request = requests.get(url_input)
    return request.text

def get_mp3_url_culture(html_text):
    # get mp3 address by taking 1st .mp3 ocurrence
    for line in html_text.split("\n"):
    # example: data-asset-source="https://media.radiofrance-podcast.net/podcast09/17397-24.08.2019-ITEMA_22130614-0.mp3"
        if "data-asset-source" in line and ".mp3" in line:
            return line.split("\"")[1]
    return None

def get_mp3_url_unige(html_text):
    # <textarea cols="60" rows="6"><iframe src="https://elearn-services.unige.ch/medias/share/video?url=https://mediaserver.unige.ch/proxy/56362/CA3-1185-86_19A.mp3&width=453&height=64&id=56362&start=0" width="453" height="64" frameborder="0" allowfullscreen=1></iframe></textarea>
    # get mp3 address by taking 1st .mp3 ocurrence
    for line in html_text.split("\n"):
    # example: data-asset-source="https://media.radiofrance-podcast.net/podcast09/17397-24.08.2019-ITEMA_22130614-0.mp3"
        if "mediaserver" in line and ".mp3" in line:
            return line.split("url=")[1].split("&width")[0]
    return None


def save_mp3(mp3_url, file_name_output):
    # download mp3 from .mp3 url
    # https://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
    response = requests.get(mp3_url, stream=True)
    path_output = os.path.join(folder_mp3, file_name_output)
    with open(path_output, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)

def find_save_mp3(url_input):
    file_name_output = url_input.split("/")[-1] + ".mp3"
    if file_name_output in os.listdir(folder_mp3):
        print(f"Not saving {file_name_output} because it is already present")
    else:
        html_text = get_html_text(url_input)
        if "culture" in url_input:
            mp3_url = get_mp3_url_culture(html_text)
        elif "unige" in url_input:
            mp3_url = get_mp3_url_unige(html_text)
        print(f"Saving file {file_name_output} from url {mp3_url}")
        save_mp3(mp3_url, file_name_output)

# get list of urls in file
# example: url_input = 'https://www.franceculture.fr/emissions/conversations-secretes-le-monde-des-espions/des-espions-au-kremlin-la-russie'
with open('url_inputs.txt') as file_urls:
    url_inputs = file_urls.read().splitlines()
    for url_input in url_inputs:
        find_save_mp3(url_input)
