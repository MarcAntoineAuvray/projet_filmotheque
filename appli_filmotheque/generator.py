import typing
from typing import Dict, Optional, List, Union

import pandas
import requests
from utils import *


my_api_url: str = 'https://imdb8.p.rapidapi.com/auto-complete'

data_path: str = 'data/'
total_movie_data_name: str = 'total_movie_data'


nan_col_names: List[str] = ['i']
new_col_names: Dict[str, str] = {'i': 'height_imageUrl_width', 'l': 'title', 's': 'description',
                                 'q': 'content_type', 'qid': 'content_type_2', 'y': 'year', 'yr': 'year_2'}


def get_imbd_response(api_url: str, key_words: str) -> requests.models.Response:
    querystring: Dict[str, str] = {'q': key_words}
    headers: Dict[str, str] = {'X-RapidAPI-Key': '54c037a69bmsh55cefb44460a062p1b7901jsn1d8ab6ef51bb',
                               'X-RapidAPI-Host': 'imdb8.p.rapidapi.com'}

    response: requests.models.Response = requests.get(api_url, headers=headers, params=querystring)
    return response


def response_to_df(response: requests.models.Response) -> pandas.DataFrame:
    return pandas.DataFrame.from_records(response.json()['d'])


def data_preprocessing(content_data: pandas.DataFrame,
                       nan_col_names: List[str] = nan_col_names,
                       new_col_names: Dict[str, str] = new_col_names) -> pandas.DataFrame:
    clean_content_data: pandas.DataFrame = content_data.copy()
    for nan_col_name in nan_col_names:
        clean_content_data.dropna(subset=[nan_col_name], inplace=True)
    movies_data_is_dict: pandas.Series = clean_content_data.transform(lambda x: x.apply(type).eq(dict)).any()
    dict_col_names: List[str] = list(movies_data_is_dict[movies_data_is_dict == True].index)
    if str(dict_col_names) not in ['', '[]', 'None', '[None]', "['']"]:
        for dict_col_name in dict_col_names:
            detailled_data: pandas.DataFrame = pandas.DataFrame(clean_content_data[dict_col_name].tolist())
            clean_content_data[list(detailled_data.columns)] = detailled_data
            clean_content_data.drop(columns=[dict_col_name], inplace=True)
    clean_content_data.rename(columns=new_col_names, inplace=True)
    return clean_content_data


def movie_filter(clean_content_data: pandas.DataFrame, new_index_col_name: str = 'id',
                 content_type_col_name: str = 'content_type', year_col_name: str = 'year',
                 next_year: float = 2025,
                 movie_name: Union[str, List[str]] = 'feature') -> pandas.DataFrame:
    if isinstance(movie_name, str):
        movie_name: List[str] = [movie_name]
    movie_data: pandas.DataFrame = clean_content_data.copy()[clean_content_data[content_type_col_name].isin(movie_name)]
    movie_data.set_index(new_index_col_name, drop=True, inplace=True)
    return movie_data[movie_data[year_col_name] < next_year]


def get_total_movie_data(path: str = data_path, total_movie_data_name: str = total_movie_data_name,
                         id_col_name: str = 'id') -> pandas.DataFrame:
    return pandas.read_csv(f'{path}{total_movie_data_name}.csv')


def update_total_movie_data(new_data: pandas.DataFrame, old_data: pandas.DataFrame, id_col_name: str = 'id') -> pandas.DataFrame:
    new_data_copy, old_data_copy = new_data.copy(), old_data.copy()
    if id_col_name in list(new_data_copy.columns):
        new_data_copy.set_index(id_col_name, drop=True, inplace=True)
    if id_col_name in list(old_data_copy.columns):
        old_data_copy.set_index(id_col_name, drop=True, inplace=True)
    if 'Unnamed: 0' in list(new_data_copy.columns):
        new_data_copy.drop(columns=['Unnamed: 0'], inplace=True)
    if 'Unnamed: 0' in list(old_data_copy.columns):
        old_data_copy.drop(columns=['Unnamed: 0'], inplace=True)
    new_movies_id: List[str] = [id for id in list(new_data_copy.index) if id not in list(old_data_copy.index)]
    if new_movies_id in [[]]:
        return old_data_copy
    else:
        return pandas.concat([old_data_copy, new_data_copy.loc[new_movies_id]], axis=0)


def save_updated_total_movie_data(updated_data: pandas.DataFrame, path: str = data_path,
                                  total_movie_data_name: str = 'total_movie_data') -> None:
    updated_data.to_csv(f'{path}{total_movie_data_name}.csv')



old_m: pandas.DataFrame = get_total_movie_data(path=data_path,
                                                                total_movie_data_name=total_movie_data_name,
                                                                id_col_name='id')
m_df: pandas.DataFrame = movie_filter(data_preprocessing(content_data=response_to_df(response=get_imbd_response(api_url=my_api_url,
                                                                                                                key_words='movie'))))

# pandas.read_csv(data_path + 'total_movie_data.csv').columns

