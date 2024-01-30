import mysql.connector
import json
import pandas as pd
import numpy as np
import sys
from collections import defaultdict
from db_connector import connect_to_db
from ratings_data_loader import load_ratings_data


def pearson_correlation_coefficent(u, v):
    u_diff = u - np.mean(u)
    v_diff = v - np.mean(v)
    numerator = np.dot(u_diff, v_diff)
    denominator = np.sqrt(sum(u_diff**2)) * np.sqrt(sum(v_diff**2))

    if denominator == 0:
        return 0.0
    return numerator / denominator


def search_similar_users(
    recommendee, ratings_df, similar_users, similarities, candidate_avg_ratings
):
    for candidate in ratings_df.index:
        if recommendee == candidate:
            continue
        recommendee_rated_shops = ratings_df.loc[recommendee, :].to_numpy()
        candidate_rated_shops = ratings_df.loc[candidate, :].to_numpy()

        common_items = ~np.isnan(recommendee_rated_shops) & ~np.isnan(
            candidate_rated_shops
        )

        if not common_items.any():
            continue

        recommendee_rated_common_shops, candidate_rated_common_shops = (
            recommendee_rated_shops[common_items],
            candidate_rated_shops[common_items],
        )

        correlation_coefficent = pearson_correlation_coefficent(
            recommendee_rated_common_shops, candidate_rated_common_shops
        )

        if correlation_coefficent > 0:
            similar_users.append(candidate)
            similarities.append(correlation_coefficent)
            candidate_avg_ratings.append(np.mean(candidate_rated_common_shops))

    return similar_users, similarities, candidate_avg_ratings


def predict_ratings(
    recommendees, ratings_df, not_rated_ratings_df, shop_id_index, ratings_data
):
    for recommendee in recommendees.unique():
        similar_users = []
        similarities = []
        candidate_avg_ratings = []

        similar_users, similarities, candidate_avg_ratings = search_similar_users(
            recommendee,
            ratings_df,
            similar_users,
            similarities,
            candidate_avg_ratings,
        )
                
        recommendee_avg_rating = np.mean(
            ratings_df.loc[recommendee, :].dropna().to_numpy()
        )

        predict_ratings_shops = not_rated_ratings_df[
            not_rated_ratings_df["user_id"] == recommendee
        ].shop_id.values

        not_rated_ratings_df.loc[
            (not_rated_ratings_df["user_id"] == recommendee), "rating"
        ] = recommendee_avg_rating

        if not similar_users:
            continue

        for shop_id in predict_ratings_shops:
            if shop_id not in shop_id_index:
                return

            similar_users_ratings = ratings_df.loc[similar_users, shop_id].to_numpy()
            not_nan_similar_users_ratings = ~np.isnan(similar_users_ratings)
            
            if not not_nan_similar_users_ratings.any():
                continue

            similar_users_ratings = similar_users_ratings[not_nan_similar_users_ratings]

            similar_users_similarities = np.array(similarities)[not_nan_similar_users_ratings]
            similar_users_avg_ratings = np.array(candidate_avg_ratings)[not_nan_similar_users_ratings]
            
            predict_rating = (
                recommendee_avg_rating + np.dot(similar_users_similarities, (similar_users_ratings - similar_users_avg_ratings)) / similar_users_similarities.sum()
            )

            not_rated_ratings_df.loc[
                (not_rated_ratings_df["user_id"] == recommendee)
                & (not_rated_ratings_df["shop_id"] == shop_id),
                "rating",
            ] = predict_rating

    merged_ratings_df = pd.concat(
        [ratings_data, not_rated_ratings_df], ignore_index=True
    )

    predict_ratings_table = pd.pivot_table(
        merged_ratings_df, index="user_id", columns="shop_id", values="rating"
    )

    return predict_ratings_table


def select_recommend_shops(predict_ratings_table, selected_recommend_shops):
    for recommendee in predict_ratings_table.index:
        selected_recommend_shops[recommendee] = []
        shop_indexes = predict_ratings_table.loc[recommendee, :].sort_values(ascending=False).index
        for shop_id in shop_indexes:
            selected_recommend_shops[recommendee].append(shop_id)

            if len(selected_recommend_shops[recommendee]) == 3:
                break


def insert_recommend_shops_data(connection, cursor, selected_recommend_shops):
    truncate_sql = "TRUNCATE TABLE recommendations"
    cursor.execute(truncate_sql)
    connection.commit()
    
    for recommendee, recommended_shops in selected_recommend_shops.items():
        for shop_id in recommended_shops:
            sql = "INSERT INTO recommendations (user_id, shop_id) VALUES (%s, %s)"
            val = (recommendee, shop_id)
            cursor.execute(sql, val)

    connection.commit()


not_rated_ratings_df = None


def main(user_id):
    try:
        connection, cursor = connect_to_db()

        ratings_data = load_ratings_data(cursor, connection)

        ratings_data_array = np.array(
            [(row[0], row[1], row[2]) for row in ratings_data]
        )

        columns = ["user_id", "shop_id", "rating"]
        ratings_df = pd.DataFrame(ratings_data_array, columns=columns)

        ratings_table = pd.pivot_table(
            ratings_df, index="user_id", columns="shop_id", values="rating"
        )

        nan_mask = ratings_table.isna()
        nan_cells = np.column_stack(np.where(nan_mask))

        not_rated_ratings_df = [
            (ratings_table.index[row], ratings_table.columns[column])
            for row, column in nan_cells
        ]
        not_rated_ratings_df = pd.DataFrame(
            not_rated_ratings_df, columns=["user_id", "shop_id"]
        )

        shop_id_index = dict(
            zip(ratings_table.columns, range(len(ratings_table.columns)))
        )

        recommendee = not_rated_ratings_df["user_id"]

        predict_ratings_table = predict_ratings(
            recommendee,
            ratings_table,
            not_rated_ratings_df,
            shop_id_index,
            ratings_df,
        )

        selected_recommend_shops = {}

        select_recommend_shops(predict_ratings_table, selected_recommend_shops)

        insert_recommend_shops_data(connection, cursor, selected_recommend_shops)

        query = "SELECT shop_id FROM recommendations WHERE user_id = %s"
        val = (user_id,)
        cursor.execute(query, val)

        shops = cursor.fetchall()

        recommend_shops = []

        for shop in shops:
            recommend_shops.append(shop[0])

        print(recommend_shops)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        connection.close()


if __name__ == "__main__":
    userId = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    main(userId)
