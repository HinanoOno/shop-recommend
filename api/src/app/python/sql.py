import mysql.connector
import json
import pandas as pd
import numpy as np
import sys
from collections import defaultdict
from db_connector import connect_to_db
from ratings_data_loader import load_ratings_data


def fetch_ratings_data(cursor):
    query = "SELECT user_id ,shop_id ,rating FROM ratings"
    cursor.execute(query)
    data = cursor.fetchall()

    return data


def convert_ratings_data_to_dataframe(ratings_data):
    data_array = np.array([(row[0], row[1], row[2]) for row in ratings_data])
    columns = ["user_id", "shop_id", "rating"]
    df = pd.DataFrame(data_array, columns=columns)

    return df


def transform_ratings_df_to_table(ratings_df):
    return pd.pivot_table(
        ratings_df, index="user_id", columns="shop_id", values="rating"
    )


def transform_ratings_table_to_dataframe(pivot_table):
    return pd.melt(
        pivot_table.reset_index(),
        id_vars="user_id",
        var_name="shop_id",
        value_name="rating",
    ).dropna()


def create_unrated_df(ratings_table):
    unrated_mask = ratings_table.isna()

    unrated_table_position = np.column_stack(np.where(unrated_mask))

    unrated_user_shop_pairs = [
        (ratings_table.index[row], ratings_table.columns[column])
        for row, column in unrated_table_position
    ]

    unrated_df = pd.DataFrame(unrated_user_shop_pairs, columns=["user_id", "shop_id"])

    return unrated_df


def load_data(cursor):
    try:
        ratings_data = fetch_ratings_data(cursor)

        ratings_df = convert_ratings_data_to_dataframe(ratings_data)

        ratings_table = transform_ratings_df_to_table(ratings_df)

        return ratings_table

    except Exception as e:
        print(f"Error: {e}")


def pearson_correlation_coefficent(u, v):
    u_diff = u - np.mean(u)
    v_diff = v - np.mean(v)
    numerator = np.dot(u_diff, v_diff)
    denominator = np.sqrt(sum(u_diff**2)) * np.sqrt(sum(v_diff**2))

    if denominator == 0:
        return 0.0
    return numerator / denominator


def search_common_shops(recommendee, ratings_df, candidate):
    recommendee_rated_shops = ratings_df.loc[recommendee, :].to_numpy()
    candidate_rated_shops = ratings_df.loc[candidate, :].to_numpy()

    common_shops = ~np.isnan(recommendee_rated_shops) & ~np.isnan(candidate_rated_shops)

    recommendee_rated_common_shops, candidate_rated_common_shops = (
        recommendee_rated_shops[common_shops],
        candidate_rated_shops[common_shops],
    )
    return common_shops, recommendee_rated_common_shops, candidate_rated_common_shops


def find_similar_users(recommendee, ratings_df):
    similar_users = []
    similarities = []
    candidate_avg_ratings = []

    for candidate in ratings_df.index:
        if recommendee == candidate:
            continue

        (
            common_shops,
            recommendee_rated_common_shops,
            candidate_rated_common_shops,
        ) = search_common_shops(recommendee, ratings_df, candidate)

        if not common_shops.any():
            continue

        correlation_coefficent = pearson_correlation_coefficent(
            recommendee_rated_common_shops, candidate_rated_common_shops
        )

        if correlation_coefficent > 0:
            similar_users.append(candidate)
            similarities.append(correlation_coefficent)
            candidate_avg_ratings.append(np.mean(candidate_rated_common_shops))

    return similar_users, similarities, candidate_avg_ratings


def calculate_rating(
    recommendee_avg_rating,
    similar_users_similarities,
    similar_users_ratings,
    similar_users_avg_ratings,
):
    predict_rating = (
        recommendee_avg_rating
        + np.dot(
            similar_users_similarities,
            (similar_users_ratings - similar_users_avg_ratings),
        )
        / similar_users_similarities.sum()
    )
    return predict_rating


def predict_rating(
    recommendee,
    shop_id,
    similar_users,
    ratings_table,
    recommendee_avg_rating,
    similarities,
    candidate_avg_ratings,
):
    similar_users_ratings = ratings_table.loc[similar_users, shop_id].to_numpy()
    not_nan_similar_users_ratings = ~np.isnan(similar_users_ratings)

    if not not_nan_similar_users_ratings.any():
        return

    similar_users_ratings = similar_users_ratings[not_nan_similar_users_ratings]

    similar_users_similarities = np.array(similarities)[not_nan_similar_users_ratings]
    similar_users_avg_ratings = np.array(candidate_avg_ratings)[
        not_nan_similar_users_ratings
    ]

    predict_rating = calculate_rating(
        recommendee_avg_rating,
        similar_users_similarities,
        similar_users_ratings,
        similar_users_avg_ratings,
    )

    return predict_rating


def sort_key(item):
    return item[1] if item[1] is not None else float("-inf")


def calculate_recommendations(ratings_table, user_id):
    similar_users, similarities, candidate_avg_ratings = find_similar_users(
        user_id, ratings_table
    )

    user_avg_rating = ratings_table.loc[user_id, :].mean()

    predicted_ratings = {}

    for shop_id in ratings_table.columns:
        predicted_ratings[shop_id] = predict_rating(
            user_id,
            shop_id,
            similar_users,
            ratings_table,
            user_avg_rating,
            similarities,
            candidate_avg_ratings,
        )

    desc_sorted_ratings = sorted(predicted_ratings.items(), key=sort_key, reverse=True)

    recommended_shops = [shop_id for shop_id, _ in desc_sorted_ratings[:3]]

    return recommended_shops


def delete_recommendations_from_db(connection, cursor, user_id):
    sql = "DELETE FROM recommendations WHERE user_id = %s"
    val = (user_id,)
    cursor.execute(sql, val)
    connection.commit()


def insert_recommendations_to_db(connection, cursor, user_id, recommend_shops):
    try:
        delete_recommendations_from_db(connection, cursor, user_id)
        for shop_id in recommend_shops:
            sql = "INSERT INTO recommendations (user_id, shop_id) VALUES (%s, %s)"
            val = (user_id, shop_id)
            cursor.execute(sql, val)
        connection.commit()

    except Exception as e:
        print(f"Error: {e}")


def recommend(user_id):
    try:
        connection, cursor = connect_to_db()

        ratings_table = load_data(cursor)

        recommended_shops = calculate_recommendations(ratings_table, user_id)

        insert_recommendations_to_db(connection, cursor, user_id, recommended_shops)

        print(recommended_shops)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        connection.close()


def main(user_id):
    recommend(user_id)


if __name__ == "__main__":
    user_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    main(user_id)
