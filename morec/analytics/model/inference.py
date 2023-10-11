from analytics.model.kinotochka_helpers import data_metrics
import pandas as pd
import numpy as np

import joblib
from keras.models import load_model

def user_processing(test_user_slug, raw=False):
    fitted_metrics = data_metrics(mode='load')
    process1 = joblib.load('analytics/model/stage1preprocessor')
    process2 = joblib.load('analytics/model/stage2preprocessor')

    # loading datasets must be switched to database cons
    df_users = (pd.read_csv(
            '.\\analytics\\model\\cached_data\\User-2023-10-07.csv'
        ).rename(
            columns={'id': 'user', 'fav_genres.1': 'favorited_genres'}
        )
    )

    df_movies = (pd.read_csv(
            '.\\analytics\\model\\cached_data\\Movie-2023-10-08.csv'
        ).rename(
            columns={'id': 'movie_id'}
        )
    )

    df_ratings = (pd.read_csv(
            '.\\analytics\\model\\cached_data\\RatingMovie-2023-10-07.csv'
        ).rename(
            columns={'id': 'rate_id', 'movie': 'movie_id'}
        )
    )

    multiplied_test_user = pd.concat([df_users[df_users['user'] == test_user_slug]] * len(df_movies), ignore_index=True)

    df_test_merged = (
        pd.concat(
            [multiplied_test_user, df_movies], axis=1
        )
        .merge(
            df_ratings[df_ratings['user'] == test_user_slug], on=['movie_id', 'user'], how='left'
        )
        [[
            'user',
            'sex',
            'date_of_birth',
            'favorited_genres',
            'movie_id',
            'rate_imdb',
            'rate_kinopoisk',
            'duration_minutes',
            'premiere_date',
            'age_limit',
            'genres',
            'actors',
            'directors',
            'countries',
            'rate'
        ]]
    )

    df_test_merged['premiere_date'] = pd.to_datetime(df_test_merged['premiere_date']).dt.year
    df_test_merged['favorited_genres'] = df_test_merged['favorited_genres'].fillna('0')

    if len(df_users[df_users['user'] == test_user_slug]) == 0:
        df_test_merged['date_of_birth'] = df_test_merged['date_of_birth'].fillna(0)

    fixed_test_data = pd.DataFrame(process1.transform(df_test_merged),
                                   columns=[
                                       'user',
                                       'movie_id',
                                       'genres',
                                       'actors',
                                       'favorited_genres',
                                       'directors',
                                       'countries',
                                       'sex',
                                       'date_of_birth',
                                       'rate_imdb',
                                       'rate_kinopoisk',
                                       'duration_minutes',
                                       'premiere_date',
                                       'age_limit',
                                       'rate'
                                   ]
                                   )

    if len(fixed_test_data[fixed_test_data['rate'].isna()]) > 10:
        fixed_test_data = fixed_test_data[fixed_test_data['rate'].isna()]

    X_test_one_user_data = pd.DataFrame(process2.transform(fixed_test_data.drop('rate', axis=1)))

    one_user_input_user = np.array(X_test_one_user_data[8].astype(int))
    one_user_input_movie = np.array(X_test_one_user_data[9].astype(int))
    one_user_input_gender_0 = np.array(X_test_one_user_data[0].astype(int))
    one_user_input_gender_1 = np.array(X_test_one_user_data[1].astype(int))
    one_user_input_age = np.array(X_test_one_user_data[2])
    one_user_input_imdb = np.array(X_test_one_user_data[3])
    one_user_input_kinopoisk = np.array(X_test_one_user_data[4])
    one_user_input_duration = np.array(X_test_one_user_data[5])
    one_user_input_age_limit = np.array(X_test_one_user_data[6])
    one_user_input_year = np.array(X_test_one_user_data[7])

    one_user_input_genres = np.array(
        X_test_one_user_data[10].apply(
            lambda x: x + [0] * (fitted_metrics['len']['genres'] - len(x))).values.tolist()
    )

    one_user_input_actors = np.array(
        X_test_one_user_data[11].apply(
            lambda x: x + [0] * (fitted_metrics['len']['actors'] - len(x))).values.tolist()
    )

    one_user_input_favorited_genres = np.array(
        X_test_one_user_data[12].apply(
            lambda x: x + [0] * (fitted_metrics['len']['favorited_genres'] - len(x))).values.tolist()
    )

    one_user_input_directors = np.array(
        X_test_one_user_data[13].apply(
            lambda x: x + [0] * (fitted_metrics['len']['directors'] - len(x))).values.tolist()
    )

    one_user_input_countries = np.array(
        X_test_one_user_data[14].apply(
            lambda x: x + [0] * (fitted_metrics['len']['countries'] - len(x))).values.tolist()
    )

    one_user_inputs = [
        one_user_input_user,
        one_user_input_movie,
        one_user_input_gender_0,
        one_user_input_gender_1,
        one_user_input_age,
        one_user_input_imdb,
        one_user_input_kinopoisk,
        one_user_input_duration,
        one_user_input_age_limit,
        one_user_input_year,
        one_user_input_genres,
        one_user_input_actors,
        one_user_input_favorited_genres,
        one_user_input_directors,
        one_user_input_countries
    ]

    if raw:
        return fixed_test_data
    else:
        return [arr.astype(np.float64) for arr in one_user_inputs], fixed_test_data['movie_id']


def get_inference(data, raw=False) -> list:
    try:
        model = load_model('analytics/model/net.h5')

        one_user_preds = model.predict(data[0]).flatten()

        one_user_results = pd.DataFrame(
            {'movie_id': data[1].astype(int).tolist(),
             'rate': one_user_preds}
        )

        one_user_results_sampler = one_user_results.sort_values('rate', ascending=False).head(20).sample(n=10)

    except:
        one_user_results_sampler = pd.read_csv('.\\analytics\\model\\cached_data\\dflt_movies.csv').sample(n=10)

    return one_user_results_sampler['movie_id'].tolist()
