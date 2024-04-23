import mysql.connector
import json
import pandas as pd
import numpy as np
import sys
from collections import defaultdict
from db_connector import connect_to_db


def pearson_correlation_coefficent(u, v):
    u_diff = u - np.mean(u)
    v_diff = v - np.mean(v)
    numerator = np.dot(u_diff, v_diff)
    denominator = np.sqrt(sum(u_diff**2)) * np.sqrt(sum(v_diff**2))

    if denominator == 0:
        return 0.0
    return numerator / denominator


class DataAccessor:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def fetch_ratings_data(self) -> list[tuple[int, int, int]]:
        query = "SELECT user_id ,shop_id ,rating FROM ratings"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def delete_recommendations_from_db(self, user_id: int):
        sql = "DELETE FROM recommendations WHERE user_id = %s"
        val = (user_id,)
        self.cursor.execute(sql, val)

        self.connection.commit()

    def insert_recommendations_to_db(self, user_id, recommend_shops):
        try:
            self.delete_recommendations_from_db(user_id)

            for shop_id in recommend_shops:
                sql = "INSERT INTO recommendations (user_id, shop_id) VALUES (%s, %s)"
                val = (user_id, shop_id)
                self.cursor.execute(sql, val)

            self.connection.commit()

        except Exception as e:
            print(f"Error: {e}")


class RatingsManager:
    def __init__(self, ratings_data):
        self.ratings_table = self._load_data(ratings_data)

    @staticmethod
    def convert_ratings_data_to_dataframe(ratings_data: list) -> pd.DataFrame:
        data_array = np.array(ratings_data)
        columns = ["user_id", "shop_id", "rating"]
        df = pd.DataFrame(data_array, columns=columns)
        return df

    @staticmethod
    def dataframe_to_table(dataframe) -> pd.DataFrame:
        return pd.pivot_table(
            dataframe, index="user_id", columns="shop_id", values="rating"
        )

    def _load_data(self, ratings_data: list) -> pd.DataFrame | None:
        try:
            dataframe = self.convert_ratings_data_to_dataframe(ratings_data)
            ratings_table = self.dataframe_to_table(dataframe)
            return ratings_table
        except Exception as e:
            print(f"Error: {e}")
        return None


class UserSimilarity:
    def __init__(self, ratings_table: pd.DataFrame):
        self.ratings_table = ratings_table

    def find_common_shops(
        self, recommendee: int, candidate: int
    ) -> tuple[np.ndarray, np.ndarray]:
        recommendee_rated_shops = self.ratings_table.loc[recommendee, :].to_numpy()
        candidate_rated_shops = self.ratings_table.loc[candidate, :].to_numpy()

        common_shops_ids = ~np.isnan(recommendee_rated_shops) & ~np.isnan(
            candidate_rated_shops
        )

        recommendee_rated_common_shops = recommendee_rated_shops[common_shops_ids]
        candidate_rated_common_shops = candidate_rated_shops[common_shops_ids]

        return recommendee_rated_common_shops, candidate_rated_common_shops

    def find_similar_users(
        self, recommendee: int
    ) -> tuple[list[int], list[float], list[float]]:
        similar_users = defaultdict(list)

        for candidate in self.ratings_table.index:
            if recommendee == candidate:
                continue

            recommendee_rated_common_shops, candidate_rated_common_shops = (
                self.find_common_shops(user_id, candidate)
            )

            if not recommendee_rated_common_shops.any():
                continue

            correlation_coefficent = pearson_correlation_coefficent(
                recommendee_rated_common_shops, candidate_rated_common_shops
            )

            if correlation_coefficent > 0:
                avg_rating = np.mean(candidate_rated_common_shops)
                similar_users["similar_users_list"].append(candidate)
                similar_users["similarities"].append(correlation_coefficent)
                similar_users["avg_ratings"].append(avg_rating)

        return (
            similar_users["similar_users_list"],
            similar_users["similarities"],
            similar_users["avg_ratings"],
        )

    def select_rated_similar_users(
        self, user_id: int, shop_id: int
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        similar_users_list, similarities, avg_ratings = self.find_similar_users(user_id)

        similar_users_ratings = self.ratings_table.loc[
            similar_users_list, shop_id
        ].to_numpy()

        exists_similar_users_ratings = ~np.isnan(similar_users_ratings)

        return (
            similar_users_ratings[exists_similar_users_ratings],
            np.array(similarities)[exists_similar_users_ratings],
            np.array(avg_ratings)[exists_similar_users_ratings],
        )


class Recommender:
    def __init__(self, ratings_manager, user_id: int):
        self.user_id = user_id
        self.ratings_table = ratings_manager.ratings_table
        self.user_similarity = UserSimilarity(self.ratings_table)

    @staticmethod
    def calculate_normalized_rating_difference(
        similarities: np.ndarray, rating_differences: np.ndarray
    ) -> float:
        weighted_rating_difference = np.dot(similarities, rating_differences)

        return weighted_rating_difference / similarities.sum()

    def calculate_ratings(
        self,
        user_avg_rating: float,
        similar_users_similarities: np.ndarray,
        rating_difference: np.ndarray,
    ) -> float:
        normalized_rating_difference = self.calculate_normalized_rating_difference(
            similar_users_similarities, rating_difference
        )

        predict_rating = user_avg_rating + normalized_rating_difference

        return predict_rating

    def predict_rating(self, shop_id: int, user_avg_rating: float) -> float | None:
        (
            similar_users_ratings,
            similar_users_similarities,
            similar_users_avg_ratings,
        ) = self.user_similarity.select_rated_similar_users(self.user_id, shop_id)

        if not similar_users_ratings.any():
            return None

        rating_diffrences = similar_users_ratings - similar_users_avg_ratings

        predicted_rating = self.calculate_ratings(
            user_avg_rating,
            similar_users_similarities,
            rating_diffrences,
        )

        return predicted_rating

    @staticmethod
    def sort_key(item: tuple[str, float | None]) -> float:
        return item[1] if item[1] is not None else float("-inf")

    def recommend(self) -> list[int]:
        user_avg_rating = self.ratings_table.loc[self.user_id, :].mean()

        predicted_ratings = {}

        for shop_id in self.ratings_table.columns:
            predicted_ratings[shop_id] = self.predict_rating(shop_id, user_avg_rating)

        desc_sorted_ratings = sorted(
            predicted_ratings.items(), key=self.sort_key, reverse=True
        )

        recommended_shops = [shop_id for shop_id, _ in desc_sorted_ratings[:3]]

        return recommended_shops


def main(user_id):
    try:
        connection, cursor = connect_to_db()
        dataAccessor = DataAccessor(cursor, connection)
        ratings_table = dataAccessor.fetch_ratings_data()

        ratings_manager = RatingsManager(ratings_table)
        recommend_shops = Recommender(ratings_manager, user_id).recommend()

        dataAccessor.insert_recommendations_to_db(user_id, recommend_shops)
        print(recommend_shops)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        connection.close()


if __name__ == "__main__":
    user_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    main(user_id)
