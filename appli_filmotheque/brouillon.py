import pandas
import typing
from typing import Dict
import requests
from bs4 import BeautifulSoup
import soup2dict


def get_movie_link(imdb_id: str) -> str:
    return f"https://www.imdb.com/title/{imdb_id}/"


def get_movie_html_content(url: str) -> str:
    headers: Dict[str, str] = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response: requests.models.Response = requests.get(url, headers=headers)
    # Vérifier si la requête s'est bien passée (statut 200 signifie succès)
    if response.status_code == 200:
        html_content = response.text
        return html_content
    else:
        return None


def get_movie_image_link(html_content: str) -> str:
    if html_content:
        soup = BeautifulSoup(html_content, "html.parser")
        script_tag = soup.find("script", type="application/ld+json")
        script_dico = soup2dict.convert(script_tag)
        text_script_dico = eval(script_dico['#text'])
        if 'image' in list(text_script_dico.keys()):
            return text_script_dico['image']
        else:
            return 'https://st3.depositphotos.com/1322515/35964/v/600/depositphotos_359648638-stock-illustration-image-available-icon.jpg'
    else:
        return 'https://st3.depositphotos.com/1322515/35964/v/600/depositphotos_359648638-stock-illustration-image-available-icon.jpg'

img_test = get_movie_image_link(get_movie_html_content(get_movie_link('tt0000001')))


data_tsv = pandas.read_csv('C:/Users/ELE6074735941708/Downloads/title.basics.tsv', sep='\t')
data_tsv_movie = data_tsv[data_tsv['titleType'] == 'movie']