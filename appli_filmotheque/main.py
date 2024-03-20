import flask
import numpy
import pandas
from flask import Flask, request
from generator import *

my_api_url: str = 'https://imdb8.p.rapidapi.com/auto-complete'
data_path: str = 'data/'
total_movie_data_name: str = 'total_movie_data'
personnal_movie_data_name: str = 'personnal_movie_data'

app: flask.app.Flask = Flask(__name__)


def search_new_movie(api_url: str = my_api_url, data_path: str = data_path,
                     total_movie_data_name: str = total_movie_data_name,
                     personnal_movie_data_name: str = personnal_movie_data_name, id_col_name: str = 'id') -> str:
    if request.method == 'POST':
        # user_input = request.form['user_input']
        user_input = request.form.get('user_input')
        old_movie_data: pandas.DataFrame = get_movie_data(path=data_path, movie_data_name=total_movie_data_name,
                                                          id_col_name=id_col_name)
        new_movie_data: pandas.DataFrame = movie_filter(data_preprocessing(response_to_df(get_imbd_response(api_url=api_url,
                                                                                                            key_words=user_input))))
        updated_total_movie_data: pandas.DataFrame = update_movie_data(new_data=new_movie_data, old_data=old_movie_data, id_col_name=id_col_name)
        save_updated_movie_data(updated_total_movie_data, movie_data_name=total_movie_data_name, path=data_path)
        title_col_name, image_col_name = 'title', 'imageUrl'
        display_text_html: str = f"""
         <table style="border-collapse: collapse; vertical-align: middle; width: 100%;" border="0"><tr>"""
        for movie_id in list(new_movie_data.index)[:4]:
            movie_html: str = f"""
                        <td style="text-align: center; vertical-align: middle;">
                        {new_movie_data.loc[movie_id][title_col_name]}<br><img src="{new_movie_data.loc[movie_id][image_col_name]}" 
                        width="100" height="150">
                        <form method="post">
                         <input type="hidden" name="user_input" value="{user_input}">
                         <input type="hidden" name="movie_id" value="{movie_id}">
                         <input type="submit" name="action_{movie_id}" style="background-color: #9CFFC5; border: 1px solid white;" value="Vu">
                         <input type="submit" name="action_{movie_id}" style="background-color: #F97C7C; border: 1px solid white;" value="Pas vu">
                        </form></td>
                        """
            display_text_html: str = f"""{display_text_html}{movie_html}"""

        display_text_html: str = f"""{display_text_html} </tr></table>"""
        personnal_movie_data: pandas.DataFrame = get_movie_data(path=data_path, movie_data_name=personnal_movie_data_name,
                                                                id_col_name=id_col_name)
        if id_col_name in list(personnal_movie_data.columns):
            personnal_movie_data.set_index(id_col_name, inplace=True, drop=True)
        is_seen_movies: Dict[str, str] = {}
        seen_movies_id = []
        for movie_id in list(new_movie_data.index)[:4]:
            seen = 'Vu' if request.form.get(f'action_{movie_id}') else 'Pas vu'
            is_seen_movies[movie_id] = {'title': new_movie_data.loc[movie_id]['title'], 'seen': seen}
            if seen == 'Vu':
                seen_movies_id.append(movie_id)
                seen_movies_id: List[str] = list(numpy.unique(seen_movies_id))
            # if request.form.get(f'action_{movie_id}') == 'Pas vu' and movie_id in list(personnal_movie_data.index):
            #     personnal_movie_data.drop(movie_id, axis=1)

        save_updated_movie_data(update_movie_data(new_data=updated_total_movie_data.loc[seen_movies_id],
                                                  old_data=personnal_movie_data, id_col_name=id_col_name),
                                movie_data_name=personnal_movie_data_name, path=data_path)

        display_text_html: str = display_text_html + '<br>'.join([f"'{key}': '{value}'" for key, value in is_seen_movies.items()])

    else:
        display_text_html = ''
    return_content: str = f"""
    <form method="post">
        <label for="user_input">Cherchez un film :</label>
        <input type="text" id="user_input" name="user_input"> 
        <input type="submit" style="border: 1px solid #d3d3d3;" value="Ok">
    </form>"""
    return_content: str = return_content + '<div>{}</div>'
    return return_content.format(display_text_html)

def get_8_cells_table() -> str:
    table: str = f"""
    <table style="border-collapse: collapse; vertical-align: middle; width: 100%; font-family: Verdana" border="0">
    <tbody>
    <tr>
    <td style="width: 100%; text-align: center; vertical-align: middle;" colspan="2">a</td>
    </tr>
    <tr>
    <td style="width: 50%; text-align: center; vertical-align: middle;">{search_new_movie()}</td>
    <td style="width: 50%; text-align: center;">c</td>
    </tr>
    <tr>
    <td style="width: 100%; text-align: center;" colspan="2">d</td>
    </tr>
    <tr>
    <td style="width: 50%; text-align: center;">e</td>
    <td style="width: 50%; text-align: center;">f</td>
    </tr>
    <tr>
    <td style="width: 100%; text-align: center;" colspan="2">g</td>
    </tr>
    <tr>
    <td style="width: 100%; text-align: center;" colspan="2">h</td>
    </tr>
    </tbody>
    </table>
    """
    return table


@app.route('/', methods=['GET', 'POST'])
def main_function():
    return get_8_cells_table()


if __name__ == '__main__':
    app.run(debug=True)
