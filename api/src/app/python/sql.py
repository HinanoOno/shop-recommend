import mysql.connector
import json
import pandas as pd
import numpy as np
import sys
from collections import defaultdict
from db_connector import connect_to_db


class DataLoader:
    def __init__(self, cursor):
        self.cursor = cursor

    def fetch_ratings_data(self):
        query = "SELECT user_id ,shop_id ,rating FROM ratings"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    @staticmethod
    def convert_ratings_data_to_dataframe(ratings_data):
        data_array = np.array(ratings_data)
        columns = ["user_id", "shop_id", "rating"]
        df = pd.DataFrame(data_array, columns=columns)
        return df

    @staticmethod
    def dataframe_to_table(dataframe):
        return pd.pivot_table(
            dataframe, index="user_id", columns="shop_id", values="rating"
        )

    def load_data(self):
        try:
            ratings_data = self.fetch_ratings_data()
            dataframe = DataLoader.convert_ratings_data_to_dataframe(ratings_data)
            ratings_table = DataLoader.dataframe_to_table(dataframe)
            return ratings_table
        except Exception as e:
            print(f"Error: {e}")


class SimilarityCalculator:
    def __init__(self):
        u = self.u
        v = self.v

    def pearson_correlation_coefficent(self):
        u_diff = self.u - np.mean(self.u)
        v_diff = self.v - np.mean(self.v)
        numerator = np.dot(u_diff, v_diff)
        denominator = np.sqrt(sum(u_diff**2)) * np.sqrt(sum(v_diff**2))

        if denominator == 0:
            return 0.0
        return numerator / denominator


class SimilarUsersFinder:
    def __init__(self):
        recommendee = self.recommendee
        ratings_table = self.ratings_table

    def find_rated_shops(self):
        return (
            self.ratings_table.loc[self.recommendee, :].to_numpy(),
            self.ratings_table.loc[self.candidate, :].to_numpy(),
        )

    @staticmethod
    def find_common_shops_ids(recommendee_rated_shops, candidate_rated_shops):
        return ~np.isnan(recommendee_rated_shops) & ~np.isnan(candidate_rated_shops)

    def find_common_shops(self, candidate):
        recommendee_rated_shops, candidate_rated_shops = self.find_rated_shops(
            self.recommendee, self.ratings_table, candidate
        )

        common_shops_ids = self.find_common_shops_ids(
            recommendee_rated_shops, candidate_rated_shops
        )

        recommendee_rated_common_shops, candidate_rated_common_shops = (
            recommendee_rated_shops[common_shops_ids],
            candidate_rated_shops[common_shops_ids],
        )

        return recommendee_rated_common_shops, candidate_rated_common_shops

    def find_similar_users(self):
        similar_users_info = {"similar_user": [], "similarity": [], "avg_rating": []}

        for candidate in self.ratings_table.index:
            if self.recommendee == candidate:
                continue

            (
                recommendee_rated_common_shops,
                candidate_rated_common_shops,
            ) = self.find_common_shops(self.recommendee, self.ratings_table, candidate)

            if not recommendee_rated_common_shops.any():
                continue

            similarity_calculator = SimilarityCalculator(
                recommendee_rated_common_shops, candidate_rated_common_shops
            )

            if (
                correlation_coefficent := similarity_calculator.pearson_correlation_coefficent(
                    recommendee_rated_common_shops, candidate_rated_common_shops
                )
            ) > 0:
                similar_users_info["similar_user"].append(candidate)
                similar_users_info["similarity"].append(correlation_coefficent)
                similar_users_info["avg_rating"].append(
                    np.mean(candidate_rated_common_shops)
                )

        return similar_users_info


class RatingPredictor:
    def __init__(self):
        pass

    @staticmethod
    def predict_rating(shop_id, similar_users_info, ratings_table, user_avg_rating):
        (
            similar_users_ratings,
            similar_users_similarities,
            similar_users_avg_ratings,
        ) = Recommender.select_rated_similar_users(
            similar_users_info, ratings_table, shop_id
        )
        if not similar_users_ratings.any():
            return
        rating_diffrence = similar_users_ratings - similar_users_avg_ratings
        normalized_rating_difference = (
            RatingPredictor.calculate_normalized_rating_difference(
                similar_users_similarities, rating_diffrence
            )
        )
        predict_rating = RatingPredictor.calculate_rating(
            user_avg_rating,
            similar_users_similarities,
            rating_diffrence,
        )
        return predict_rating

    @staticmethod
    def calculate_normalized_rating_difference(similarities, rating_differences):
        weighted_rating_difference = np.dot(similarities, rating_differences)
        return weighted_rating_difference / similarities.sum()

    @staticmethod
    def calculate_rating(
        user_avg_rating,
        similar_users_similarities,
        rating_difference,
    ):
        normalized_rating_difference = (
            RatingPredictor.calculate_normalized_rating_difference(
                similar_users_similarities, rating_difference
            )
        )
        predict_rating = user_avg_rating + normalized_rating_difference
        return predict_rating


class RecommendationManager:
    def __init__(self):
        pass

    @staticmethod
    def calculate_recommendations(ratings_table, user_id):
        similar_users = Recommender.find_similar_users(user_id, ratings_table)
        user_avg_rating = ratings_table.loc[user_id, :].mean()
        predicted_ratings = {}
        for shop_id in ratings_table.columns:
            predicted_ratings[shop_id] = RatingPredictor.predict_rating(
                shop_id,
                similar_users,
                ratings_table,
                user_avg_rating,
            )
        desc_sorted_ratings = sorted(
            predicted_ratings.items(), key=lambda x: x[1], reverse=True
        )
        recommended_shops = [shop_id for shop_id, _ in desc_sorted_ratings[:3]]
        return recommended_shops


class DatabaseHandler:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    @staticmethod
    def delete_recommendations_from_db(connection, cursor, user_id):
        sql = "DELETE FROM recommendations WHERE user_id = %s"
        val = (user_id,)
        cursor.execute(sql, val)
        connection.commit()

    @staticmethod
    def insert_recommendations_to_db(connection, cursor, user_id, recommend_shops):
        try:
            DatabaseHandler.delete_recommendations_from_db(connection, cursor, user_id)
            for shop_id in recommend_shops:
                sql = "INSERT INTO recommendations (user_id, shop_id) VALUES (%s, %s)"
                val = (user_id, shop_id)
                cursor.execute(sql, val)
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")


class RecommenderApp:
    def __init__(self):
        pass

    @staticmethod
    def recommend(user_id, db_connection, cursor):
        ratings_table = DataLoader.load_data(cursor)
        recommended_shops = RecommendationManager.calculate_recommendations(
            ratings_table, user_id
        )
        DatabaseHandler.insert_recommendations_to_db(
            db_connection, cursor, user_id, recommended_shops
        )
        print(recommended_shops)

    @staticmethod
    def main(user_id):
        db_connection, cursor = connect_to_db()
        RecommenderApp.recommend(user_id, db_connection, cursor)


# if __name__ == "__main__":
#     user_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
#     RecommenderApp.main(user_id)


# def pearson_correlation_coefficent(u, v):
#     u_diff = u - np.mean(u)
#     v_diff = v - np.mean(v)
#     numerator = np.dot(u_diff, v_diff)
#     denominator = np.sqrt(sum(u_diff**2)) * np.sqrt(sum(v_diff**2))

#     if denominator == 0:
#         return 0.0
#     return numerator / denominator


# def find_rated_shops(recommendee, ratings_table, candidate):
#     return (
#         ratings_table.loc[recommendee, :].to_numpy(),
#         ratings_table.loc[candidate, :].to_numpy(),
#     )


# def find_common_shops_ids(recommendee_rated_shops, candidate_rated_shops):
#     return ~np.isnan(recommendee_rated_shops) & ~np.isnan(candidate_rated_shops)


# def find_common_shops(recommendee, ratings_table, candidate):
#     recommendee_rated_shops, candidate_rated_shops = find_rated_shops(
#         recommendee, ratings_table, candidate
#     )

#     common_shops_ids = find_common_shops_ids(
#         recommendee_rated_shops, candidate_rated_shops
#     )

#     recommendee_rated_common_shops, candidate_rated_common_shops = (
#         recommendee_rated_shops[common_shops_ids],
#         candidate_rated_shops[common_shops_ids],
#     )

#     return recommendee_rated_common_shops, candidate_rated_common_shops


# def find_similar_users(recommendee, ratings_table):
#     similar_users_info = {"similar_user": [], "similarity": [], "avg_rating": []}

#     for candidate in ratings_table.index:
#         if recommendee == candidate:
#             continue

#         (
#             recommendee_rated_common_shops,
#             candidate_rated_common_shops,
#         ) = find_common_shops(recommendee, ratings_table, candidate)

#         if not recommendee_rated_common_shops.any():
#             continue

#         if (
#             correlation_coefficent := pearson_correlation_coefficent(
#                 recommendee_rated_common_shops, candidate_rated_common_shops
#             )
#         ) > 0:
#             similar_users_info["similar_user"].append(candidate)
#             similar_users_info["similarity"].append(correlation_coefficent)
#             similar_users_info["avg_rating"].append(
#                 np.mean(candidate_rated_common_shops)
#             )

#     return similar_users_info


# def calculate_normalized_rating_difference(similarities, rating_differences):
#     weighted_rating_difference = np.dot(similarities, rating_differences)

#     return weighted_rating_difference / similarities.sum()


# def calculate_rating(
#     user_avg_rating,
#     similar_users_similarities,
#     rating_difference,
# ):
#     normalized_rating_difference = calculate_normalized_rating_difference(
#         similar_users_similarities, rating_difference
#     )

#     predict_rating = user_avg_rating + normalized_rating_difference

#     return predict_rating


# def select_rated_similar_users(similar_users_info, ratings_table, shop_id):
#     similar_users_ratings = ratings_table.loc[
#         similar_users_info["similar_user"], shop_id
#     ].to_numpy()

#     exists_similar_users_ratings = ~np.isnan(similar_users_ratings)

#     return (
#         similar_users_ratings[exists_similar_users_ratings],
#         np.array(similar_users_info["similarity"])[exists_similar_users_ratings],
#         np.array(similar_users_info["avg_rating"])[exists_similar_users_ratings],
#     )


# def predict_rating(shop_id, similar_users_info, ratings_table, user_avg_rating):
#     (
#         similar_users_ratings,
#         similar_users_similarities,
#         similar_users_avg_ratings,
#     ) = select_rated_similar_users(similar_users_info, ratings_table, shop_id)

#     if not similar_users_ratings.any():
#         return

#     rating_diffrence = similar_users_ratings - similar_users_avg_ratings

#     predicted_rating = calculate_rating(
#         user_avg_rating,
#         similar_users_similarities,
#         rating_diffrence,
#     )

#     return predicted_rating


# def sort_key(item):
#     return item[1] if item[1] is not None else float("-inf")


# def calculate_recommendations(ratings_table, user_id):
#     similar_users = find_similar_users(user_id, ratings_table)

#     user_avg_rating = ratings_table.loc[user_id, :].mean()

#     predicted_ratings = {}

#     for shop_id in ratings_table.columns:
#         predicted_ratings[shop_id] = predict_rating(
#             shop_id,
#             similar_users,
#             ratings_table,
#             user_avg_rating,
#         )

#     desc_sorted_ratings = sorted(predicted_ratings.items(), key=sort_key, reverse=True)

#     recommended_shops = [shop_id for shop_id, _ in desc_sorted_ratings[:3]]

#     return recommended_shops


# def delete_recommendations_from_db(connection, cursor, user_id):
#     sql = "DELETE FROM recommendations WHERE user_id = %s"
#     val = (user_id,)
#     cursor.execute(sql, val)

#     connection.commit()


# def insert_recommendations_to_db(connection, cursor, user_id, recommend_shops):
#     try:
#         delete_recommendations_from_db(connection, cursor, user_id)

#         for shop_id in recommend_shops:
#             sql = "INSERT INTO recommendations (user_id, shop_id) VALUES (%s, %s)"
#             val = (user_id, shop_id)
#             cursor.execute(sql, val)

#         connection.commit()

#     except Exception as e:
#         print(f"Error: {e}")


def recommend(user_id):
    try:
        connection, cursor = connect_to_db()

        dataloader = DataLoader(cursor)

        ratings_table = dataloader.load_data()

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
