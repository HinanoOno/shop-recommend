import mysql.connector
import json
import pandas as pd
import numpy as np
import sys
from collections import defaultdict
from db_connector import connect_to_db


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


def dataframe_to_table(dataframe):
    return pd.pivot_table(
        dataframe, index="user_id", columns="shop_id", values="rating"
    )


def transform_ratings_table_to_dataframe(pivot_table):
    return pd.melt(
        pivot_table.reset_index(),
        id_vars="user_id",
        var_name="shop_id",
        value_name="rating",
    ).dropna()


def load_data(cursor):
    try:
        ratings_data = fetch_ratings_data(cursor)

        dataframe = convert_ratings_data_to_dataframe(ratings_data)

        ratings_table = dataframe_to_table(dataframe)

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


def find_rated_shops(recommendee, ratings_table, candidate):
    return (
        ratings_table.loc[recommendee, :].to_numpy(),
        ratings_table.loc[candidate, :].to_numpy(),
    )


def find_common_shops_ids(recommendee_rated_shops, candidate_rated_shops):
    return ~np.isnan(recommendee_rated_shops) & ~np.isnan(candidate_rated_shops)


def find_common_shops(recommendee, ratings_table, candidate):
    recommendee_rated_shops, candidate_rated_shops = find_rated_shops(
        recommendee, ratings_table, candidate
    )

    common_shops_ids = find_common_shops_ids(
        recommendee_rated_shops, candidate_rated_shops
    )

    recommendee_rated_common_shops, candidate_rated_common_shops = (
        recommendee_rated_shops[common_shops_ids],
        candidate_rated_shops[common_shops_ids],
    )

    return recommendee_rated_common_shops, candidate_rated_common_shops


def find_similar_users(recommendee, ratings_table):
    similar_users_info = {"similar_user": [], "similarity": [], "avg_rating": []}

    for candidate in ratings_table.index:
        if recommendee == candidate:
            continue

        (
            recommendee_rated_common_shops,
            candidate_rated_common_shops,
        ) = find_common_shops(recommendee, ratings_table, candidate)

        if not recommendee_rated_common_shops.any():
            continue

        correlation_coefficent = pearson_correlation_coefficent(
            recommendee_rated_common_shops, candidate_rated_common_shops
        )

        if correlation_coefficent > 0:
            similar_users_info["similar_user"].append(candidate)
            similar_users_info["similarity"].append(correlation_coefficent)
            similar_users_info["avg_rating"].append(
                np.mean(candidate_rated_common_shops)
            )

    return similar_users_info


def calculate_normalized_rating_difference(similarities, rating_differences):
    weighted_rating_difference = np.dot(similarities, rating_differences)

    return weighted_rating_difference / similarities.sum()


def calculate_rating(
    user_avg_rating,
    similar_users_similarities,
    similar_users_ratings,
    similar_users_avg_ratings,
):
    rating_difference = similar_users_ratings - similar_users_avg_ratings

    normalized_rating_difference = calculate_normalized_rating_difference(
        similar_users_similarities, rating_difference
    )

    predict_rating = user_avg_rating + normalized_rating_difference

    return predict_rating


def select_rated_similar_users(similar_users_info, ratings_table, shop_id):
    similar_users_ratings = ratings_table.loc[
        similar_users_info["similar_user"], shop_id
    ].to_numpy()

    exists_similar_users_ratings = ~np.isnan(similar_users_ratings)

    return (
        similar_users_ratings[exists_similar_users_ratings],
        np.array(similar_users_info["similarity"])[exists_similar_users_ratings],
        np.array(similar_users_info["avg_rating"])[exists_similar_users_ratings],
    )


def predict_rating(shop_id, similar_users_info, ratings_table, user_avg_rating):
    (
        similar_users_ratings,
        similar_users_similarities,
        similar_users_avg_ratings,
    ) = select_rated_similar_users(similar_users_info, ratings_table, shop_id)

    if not similar_users_ratings.any():
        return

    predicted_rating = calculate_rating(
        user_avg_rating,
        similar_users_similarities,
        similar_users_ratings,
        similar_users_avg_ratings,
    )

    return predicted_rating


def sort_key(item):
    return item[1] if item[1] is not None else float("-inf")


def calculate_recommendations(ratings_table, user_id):
    similar_users = find_similar_users(user_id, ratings_table)

    user_avg_rating = ratings_table.loc[user_id, :].mean()

    predicted_ratings = {}

    for shop_id in ratings_table.columns:
        predicted_ratings[shop_id] = predict_rating(
            shop_id,
            similar_users,
            ratings_table,
            user_avg_rating,
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
