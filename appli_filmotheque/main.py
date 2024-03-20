import flask
from flask import Flask, request
from generator import *

my_api_url: str = 'https://imdb8.p.rapidapi.com/auto-complete'
data_path: str = 'data/'
total_movie_data_name: str = 'total_movie_data'

app: flask.app.Flask = Flask(__name__)


def search_new_movie(api_url: str = my_api_url,
                     data_path: str = data_path, total_movie_data_name: str = total_movie_data_name, id_col_name: str = 'id') -> str:
    if request.method == 'POST':
        user_input = request.form['user_input']
        old_movie_data: pandas.DataFrame = get_total_movie_data(path=data_path,
                                                                total_movie_data_name=total_movie_data_name,
                                                                id_col_name=id_col_name)
        new_movie_data: pandas.DataFrame = movie_filter(data_preprocessing(response_to_df(get_imbd_response(api_url=api_url,
                                                                                                            key_words=user_input))))
        save_updated_total_movie_data(update_total_movie_data(new_data=new_movie_data, old_data=old_movie_data))
        display_texts: List[str] = []
        for movie_id in  list(new_movie_data.index)[:4]:
            title_col_name, image_col_name = 'title', 'imageUrl'
            movie_html: str = f"""
            {new_movie_data.loc[movie_id][title_col_name]}<br><img src="{new_movie_data.loc[movie_id][image_col_name]}" 
            width="100" height="150">
            <input type="submit" name="submit_button" value="Pas vu">"""
            display_texts.append(movie_html)

        display_text_html: str = f"""
            <table style="border-collapse: collapse; vertical-align: middle; width: 100%;" border="1"><tr>"""
        for display_text in display_texts:
            display_text_html: str = f"""{display_text_html}
            <td style=" text-align: center; vertical-align: middle;">{display_text}</td>"""
        display_text_html: str = f"""{display_text_html} </tr></table>"""
    else:
        display_text_html = ''
    return '''
        <form method="post">
            <label for="user_input">Cherchez un film :</label>
            <input type="text" id="user_input" name="user_input"> 
            <input type="submit" value="Ok">
        </form>
        <div>{}</div>
        '''.format(display_text_html)

def get_8_cells_table() -> str:
    table: str = f"""
    <table style="border-collapse: collapse; vertical-align: middle; width: 100%;" border="1">
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
