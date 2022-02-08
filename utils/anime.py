import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from collections import namedtuple
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode
GOGO_ANIME_DOMAIN = "gogoanime.film"


def request(url, get="text", headers=None):
    if not headers:
        headers = {}
    if not headers.get("User-Agent"):
        headers["User-Agent"] = "Mozilla/7.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/7.0.4 Mobile/16B91 Safari/605.1.15"
    resp = requests.get(url, headers=headers)
    if get.lower() == "json":
        return resp.json()
    return resp.content


def search(keyword):
    animeTuple = namedtuple("anime", ["title", "url"])
    content = request(url=f"https://{GOGO_ANIME_DOMAIN}/search.html?keyword={keyword}", headers={
        "X-Requested-With": "XMLHttpRequest",
    }
    )
    soup = BeautifulSoup(content, "html.parser")
    return [animeTuple(anime.get("title"), f'https://{GOGO_ANIME_DOMAIN}{anime.get("href")}') for anime in soup.find_all("a")]


def getAnimeInfo(url):
    animeInfo = namedtuple("animeInfo", ["animeID", "episodes"])
    content = request(url)
    soup = BeautifulSoup(content, "html.parser")
    animeID = soup.find("input", {"id": "movie_id"}).get("value")
    episodes = soup.find("ul", {"id": "episode_page"}).find(
        "a", {"class": "active"}).get("ep_end")
    return animeInfo(animeID, episodes)


def getEpisodeID(url):
    content = request(url)
    soup = BeautifulSoup(content, "html.parser")
    downloadLink = soup.find("li", {"class": "dowloads"}).find("a").get("href")
    parsedDL = urlparse(downloadLink)
    episodeID = parse_qs(parsedDL.query)["id"][0]
    return episodeID


def getSources(url):
    episodeID = getEpisodeID(url)
    # ajax construct
    secretKey = "25746538592938396764662879833288"
    initializationVector = '4206913378008135'

    cipher = AES.new(secretKey.encode(), AES.MODE_CBC,
                     iv=initializationVector.encode())
    padded_data = pad(episodeID.encode(), cipher.block_size)
    ajax = b64encode(cipher.encrypt(padded_data)).decode()

    return request(f"https://gogoplay.io/encrypt-ajax.php?id={ajax}&time=62420691337800813569", headers={
        "X-Requested-With": "XMLHttpRequest",
    }, get="json")


def getEpisode(animeID, episode):
    episodeTuple = namedtuple("episode", ["name", "url", "type"])
    content = request(
        f"https://ajax.gogo-load.com/ajax/load-list-episode?ep_start={episode}&ep_end={episode}&id={animeID}")
    soup = BeautifulSoup(content, "html.parser")
    episodeHTML = soup.find("li")
    episode = [
        episodeHTML.find("div", {"class": "name"}).text,
        f'https://{GOGO_ANIME_DOMAIN}{episodeHTML.find("a").get("href").strip()}',
        episodeHTML.find("div", {"class": "cate"}).text
    ]
    return episodeTuple(*episode)
