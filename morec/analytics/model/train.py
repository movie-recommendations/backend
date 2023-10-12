from analytics.model import kinotochka_helpers as kh

import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow import random as tf_random
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adam
from keras.layers import (Embedding,
                          Input,
                          Flatten,
                          Concatenate,
                          BatchNormalization,
                          LeakyReLU,
                          Dense)


import joblib

RANDOM = 202309


def prepare_data(users_table, movies_table, ratings_table):

    df_users = pd.read_csv(users_table).rename(columns={'id': 'user', 'fav_genres.1': 'favorited_genres'})
    df_movies = pd.read_csv(movies_table).rename(columns={'id': 'movie_id'})
    df_ratings = pd.read_csv(ratings_table).rename(columns={'id': 'rate_id', 'movie': 'movie_id'})

    initial_columns_order = [
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
            ]

    new_columns_order_st1 = [
        'user', 'movie_id', 'genres', 'actors', 'favorited_genres',
        'directors', 'countries', 'sex', 'date_of_birth', 'rate_imdb',
        'rate_kinopoisk', 'duration_minutes', 'premiere_date', 'age_limit', 'rate'
    ]

    data = (
        df_ratings
        .merge(
            df_movies, how='left', on='movie_id'
        )
        .merge(
            df_users, how='left', on='user'
        )
        [initial_columns_order]
    )

    data['premiere_date'] = pd.to_datetime(data['premiere_date']).dt.year
    data['favorited_genres'] = data['favorited_genres'].fillna('0')

    data_metrics_json = kh.data_metrics(mode='load')
    preprocessor_st1 = joblib.load('analytics/model/stage1preprocessor')
    preprocessor_st2 = joblib.load('analytics/model/stage2preprocessor')

    fixed_data = pd.DataFrame(preprocessor_st1.transform(data), columns=new_columns_order_st1)

    # kh.data_metrics(fixed_data, mode='dump')

    X_train = pd.DataFrame(preprocessor_st2.transform(fixed_data.drop('rate', axis=1)))

    train_input_user = np.array(X_train[8].astype(int))
    train_input_movie = np.array(X_train[9].astype(int))
    train_input_gender_0 = np.array(X_train[0].astype(int))
    train_input_gender_1 = np.array(X_train[1].astype(int))
    train_input_age = np.array(X_train[2])
    train_input_imdb = np.array(X_train[3])
    train_input_kinopoisk = np.array(X_train[4])
    train_input_duration = np.array(X_train[5])
    train_input_age_limit = np.array(X_train[6])
    train_input_year = np.array(X_train[7])

    train_input_genres = np.array(
        X_train[10].apply(
            lambda x: x + [0] * (data_metrics_json['len']['genres'] - len(x))).values.tolist()
    )

    train_input_actors = np.array(
        X_train[11].apply(
            lambda x: x + [0] * (data_metrics_json['len']['actors'] - len(x))).values.tolist()
    )

    train_input_favorited_genres = np.array(
        X_train[12].apply(
            lambda x: x + [0] * (data_metrics_json['len']['favorited_genres'] - len(x))).values.tolist()
    )

    train_input_directors = np.array(
        X_train[13].apply(
            lambda x: x + [0] * (data_metrics_json['len']['directors'] - len(x))).values.tolist()
    )

    train_input_countries = np.array(
        X_train[14].apply(
            lambda x: x + [0] * (data_metrics_json['len']['countries'] - len(x))).values.tolist()
    )

    train_inputs = [
        train_input_user,
        train_input_movie,
        train_input_gender_0,
        train_input_gender_1,
        train_input_age,
        train_input_imdb,
        train_input_kinopoisk,
        train_input_duration,
        train_input_age_limit,
        train_input_year,
        train_input_genres,
        train_input_actors,
        train_input_favorited_genres,
        train_input_directors,
        train_input_countries
    ]

    return (
        [arr.astype(np.float64) for arr in train_inputs],
        fixed_data['rate']
    )


def net(learning_rate=0.001,
        loss='mean_squared_error',
        layer1_units=10,
        layer2_units=5,
        layer3_units=None,
        layer4_units=None,
        layer5_units=None,
        layer6_units=None,
        layer1_activation='relu',
        layer2_activation='relu',
        layer3_activation='relu',
        layer4_activation='relu',
        layer5_activation='relu',
        layer6_activation='relu'):

    tf_random.set_seed(RANDOM)
    np.random.seed(RANDOM)

    optimizer = Adam(learning_rate=learning_rate)
    data_metrics_json = kh.data_metrics(mode='load')

    # input layers
    layer_user_id = Input(shape=[1], name='user')
    layer_movie_id = Input(shape=[1], name='movie')
    layer_gender0 = Input(shape=[1], name='gender0')
    layer_gender1 = Input(shape=[1], name='gender1')
    layer_age = Input(shape=[1], name='age')
    layer_imdb = Input(shape=[1], name='imdb')
    layer_kinopoisk = Input(shape=[1], name='kinopoisk')
    layer_duration = Input(shape=[1], name='duration')
    layer_age_limit = Input(shape=[1], name='age_limit')
    layer_year = Input(shape=[1], name='year')

    layer_genres = Input(shape=[data_metrics_json['len']['genres']], name='genres')
    layer_actors = Input(shape=[data_metrics_json['len']['actors']], name='actors')
    layer_favorites = Input(shape=[data_metrics_json['len']['favorited_genres']], name='favorites')
    layer_directors = Input(shape=[data_metrics_json['len']['directors']], name='directors')
    layer_countries = Input(shape=[data_metrics_json['len']['countries']], name='countries')

    user_embedding = Embedding(output_dim=10, input_dim=int(data_metrics_json['max']['user']) + 5, input_length=1,
                               name='user_embedding')(layer_user_id)
    user_embedding = Flatten()(user_embedding)

    movie_embedding = Embedding(output_dim=10, input_dim=int(data_metrics_json['max']['movie_id']) + 5, input_length=1,
                                name='movie_embedding')(layer_movie_id)
    movie_embedding = Flatten()(movie_embedding)

    genres_embedding = Embedding(output_dim=5, input_dim=data_metrics_json['max']['genres'] + 1,
                                 input_length=data_metrics_json['len']['genres'], mask_zero=True)(layer_genres)
    genres_embedding = Flatten()(genres_embedding)

    actors_embedding = Embedding(output_dim=5, input_dim=data_metrics_json['max']['actors'] + 10,
                                 input_length=data_metrics_json['len']['actors'], mask_zero=True)(layer_actors)
    actors_embedding = Flatten()(actors_embedding)

    favorites_embedding = Embedding(output_dim=5, input_dim=data_metrics_json['max']['favorited_genres'] + 1,
                                    input_length=data_metrics_json['len']['favorited_genres'], mask_zero=True)(
        layer_favorites)
    favorites_embedding = Flatten()(favorites_embedding)

    directors_embedding = Embedding(output_dim=5, input_dim=data_metrics_json['max']['directors'] + 5,
                                    input_length=data_metrics_json['len']['directors'], mask_zero=True)(layer_directors)
    directors_embedding = Flatten()(directors_embedding)

    countries_embedding = Embedding(output_dim=5, input_dim=data_metrics_json['max']['countries'] + 1,
                                    input_length=data_metrics_json['len']['countries'], mask_zero=True)(layer_countries)
    countries_embedding = Flatten()(countries_embedding)

    x = Concatenate()(
        [
            user_embedding,
            movie_embedding,
            layer_gender0,
            layer_gender1,
            layer_age,
            layer_imdb,
            layer_kinopoisk,
            layer_duration,
            layer_age_limit,
            layer_year,
            genres_embedding,
            actors_embedding,
            favorites_embedding,
            directors_embedding,
            countries_embedding
        ]
    )

    x = BatchNormalization()(x)
    x = Dense(layer1_units, activation=layer1_activation, kernel_initializer='he_normal')(x)

    x = BatchNormalization()(x)
    x = Dense(layer2_units, activation=layer2_activation, kernel_initializer='he_normal')(x)

    if layer3_units:
        x = BatchNormalization()(x)
        x = Dense(layer3_units, activation=layer3_activation, kernel_initializer='he_normal')(x)

    if layer4_units:
        x = BatchNormalization()(x)
        x = Dense(layer4_units, activation=layer4_activation, kernel_initializer='he_normal')(x)

    if layer5_units:
        x = BatchNormalization()(x)
        x = Dense(layer5_units, activation=layer5_activation, kernel_initializer='he_normal')(x)

    if layer6_units:
        x = BatchNormalization()(x)
        x = Dense(layer6_units, activation=layer6_activation, kernel_initializer='he_normal')(x)

    output = Dense(1, activation='linear')(x)

    mod = tf.keras.Model(
        inputs=[
            layer_user_id,
            layer_movie_id,
            layer_gender0,
            layer_gender1,
            layer_age,
            layer_imdb,
            layer_kinopoisk,
            layer_duration,
            layer_age_limit,
            layer_year,
            layer_genres,
            layer_actors,
            layer_favorites,
            layer_directors,
            layer_countries
        ], outputs=output
    )
    mod.compile(optimizer=optimizer, loss=loss, metrics=['mean_absolute_error'])

    return mod


def train(model, X, y, batch_size=100, epochs=100, validation_split=.2, verbose=1):

    checkpoint = ModelCheckpoint("analytics/model/net.h5", save_best_only=True)

    model.fit(
        X,
        y.values.astype(np.float64),
        batch_size=batch_size,
        epochs=epochs,
        validation_split=validation_split,
        verbose=verbose,
        callbacks=[checkpoint])


if __name__ == '__main__':

    model = net(
        learning_rate=0.0025,
        loss='mean_squared_error',
        layer1_units=200,
        layer2_units=150,
        layer3_units=100,
        layer4_units=20,
        layer5_units=8,
        layer6_units=2,
        layer1_activation='relu',
        layer2_activation=LeakyReLU(alpha=.2),
        layer3_activation='relu',
        layer4_activation=LeakyReLU(alpha=.2),
        layer5_activation='relu',
        layer6_activation=LeakyReLU(alpha=.2))

    temporary_data = [
        'User-2023-10-07.csv',
        'Movie-2023-10-08.csv',
        'RatingMovie-2023-10-07.csv'
    ]

    pass_to_cached_data = '.\\analytics\model\cached_data\\'

    train_data = prepare_data(
        pass_to_cached_data + temporary_data[0],
        pass_to_cached_data + temporary_data[1],
        pass_to_cached_data + temporary_data[2]
    )

    train(
        model,
        train_data[0],
        train_data[1],
        90,
        100
    )
