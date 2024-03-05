import mysql.connector
import json
import pandas as pd
import numpy as np
import sys
from collections import defaultdict
from db_connector import connect_to_db
from typing import Any, Type


class DataLoader:
    # anyでいいのか？
    def __init__(self, cursor):
        self.cursor = cursor

    def fetch_ratings_data(self) -> list[tuple[int, int, int]]:
        query = "SELECT user_id ,shop_id ,rating FROM ratings"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

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

    def load_data(self) -> pd.DataFrame | None:
        try:
            ratings_data = self.fetch_ratings_data()
            dataframe = self.convert_ratings_data_to_dataframe(ratings_data)
            ratings_table = self.dataframe_to_table(dataframe)
            return ratings_table
        except Exception as e:
            print(f"Error: {e}")
        return None


class SimilarityCalculator:
    def __init__(self, u: np.ndarray, v: np.ndarray):
        self.u = u
        self.v = v

    def pearson_correlation_coefficent(self) -> float:
        u_diff = self.u - np.mean(self.u)
        v_diff = self.v - np.mean(self.v)
        numerator = np.dot(u_diff, v_diff)
        denominator = np.sqrt(sum(u_diff**2)) * np.sqrt(sum(v_diff**2))

        if denominator == 0:
            return 0.0
        return numerator / denominator


class SimilarUsersFinder:
    def __init__(self, recommendee: int, ratings_table: pd.DataFrame):
        self.recommendee = recommendee
        self.ratings_table = ratings_table

    def find_rated_shops(self, candidate: int) -> tuple[np.ndarray, np.ndarray]:
        return (
            self.ratings_table.loc[self.recommendee, :].to_numpy(),
            self.ratings_table.loc[candidate, :].to_numpy(),
        )

    @staticmethod
    def find_common_shops_ids(
        recommendee_rated_shops: np.ndarray, candidate_rated_shops: np.ndarray
    ) -> np.ndarray:
        return ~np.isnan(recommendee_rated_shops) & ~np.isnan(candidate_rated_shops)

    def find_common_shops(self, candidate: int) -> tuple[np.ndarray, np.ndarray]:
        recommendee_rated_shops, candidate_rated_shops = self.find_rated_shops(
            candidate
        )

        common_shops_ids = self.find_common_shops_ids(
            recommendee_rated_shops, candidate_rated_shops
        )

        recommendee_rated_common_shops, candidate_rated_common_shops = (
            recommendee_rated_shops[common_shops_ids],
            candidate_rated_shops[common_shops_ids],
        )

        return recommendee_rated_common_shops, candidate_rated_common_shops

    def find_similar_users(self) -> dict[str, list[int | float]]:
        similar_users_info: dict[str, list[int | float]] = {
            "similar_user": [],
            "similarity": [],
            "avg_rating": [],
        }

        for candidate in self.ratings_table.index:
            if self.recommendee == candidate:
                continue

            (
                recommendee_rated_common_shops,
                candidate_rated_common_shops,
            ) = self.find_common_shops(candidate)

            if not recommendee_rated_common_shops.any():
                continue
            # 継承の方がいいかも
            similarity_calculator = SimilarityCalculator(
                recommendee_rated_common_shops, candidate_rated_common_shops
            )

            if (
                correlation_coefficent := similarity_calculator.pearson_correlation_coefficent()
            ) > 0:
                similar_users_info["similar_user"].append(candidate)
                similar_users_info["similarity"].append(correlation_coefficent)
                similar_users_info["avg_rating"].append(
                    np.mean(candidate_rated_common_shops)
                )
        return similar_users_info


class RatingPredictor:
    def __init__(
        self,
        shop_id: int,
        similar_users_info: dict[str, list[int | float]],
        ratings_table: pd.DataFrame,
        user_avg_rating: float,
    ):
        self.shop_id = shop_id
        self.similar_users_info = similar_users_info
        self.ratings_table = ratings_table
        self.user_avg_rating = user_avg_rating

    @staticmethod
    def calculate_normalized_rating_difference(
        similarities: np.ndarray, rating_differences: np.ndarray
    ) -> float:
        weighted_rating_difference = np.dot(similarities, rating_differences)

        return weighted_rating_difference

    def calculate_rating(
        self,
        similar_users_similarities: np.ndarray,
        rating_difference: np.ndarray,
    ) -> float:
        normalized_rating_difference = self.calculate_normalized_rating_difference(
            similar_users_similarities, rating_difference
        )

        predict_rating = self.user_avg_rating + normalized_rating_difference

        return predict_rating

    def select_rated_similar_users(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        similar_users_ratings = self.ratings_table.loc[
            pd.Index(self.similar_users_info["similar_user"]), self.shop_id
        ].to_numpy()

        exists_similar_users_ratings = ~np.isnan(similar_users_ratings)

        return (
            similar_users_ratings[exists_similar_users_ratings],
            np.array(self.similar_users_info["similarity"])[
                exists_similar_users_ratings
            ],
            np.array(self.similar_users_info["avg_rating"])[
                exists_similar_users_ratings
            ],
        )

    def predict_rating(self) -> float | None:
        (
            similar_users_ratings,
            similar_users_similarities,
            similar_users_avg_ratings,
        ) = self.select_rated_similar_users()

        if not similar_users_ratings.any():
            return None

        rating_diffrence = similar_users_ratings - similar_users_avg_ratings

        predicted_rating = self.calculate_rating(
            similar_users_similarities,
            rating_diffrence,
        )

        return predicted_rating


class RecommendationCalculator:
    def __init__(self, ratings_table: pd.DataFrame, user_id: int):
        self.ratings_table = ratings_table
        self.user_id = user_id

    @staticmethod
    def sort_key(item: tuple[str, float | None]) -> float:
        return item[1] if item[1] is not None else float("-inf")

    def calculate_recommendations(self) -> list[int] | None:
        similar_users = SimilarUsersFinder(
            self.user_id, self.ratings_table
        ).find_similar_users()

        user_avg_rating = self.ratings_table.loc[user_id, :].mean()
        predicted_ratings = {}

        for shop_id in self.ratings_table.columns:
            predicted_ratings[shop_id] = RatingPredictor(
                int(shop_id),
                similar_users,
                self.ratings_table,
                float(user_avg_rating),
            ).predict_rating()

        desc_sorted_ratings = sorted(
            predicted_ratings.items(), key=self.sort_key, reverse=True
        )
        recommended_shops = [int(shop_id) for shop_id, _ in desc_sorted_ratings[:3]]
        return recommended_shops


class DatabaseHandler:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def delete_recommendations_from_db(self, user_id: int) -> None:
        sql = "DELETE FROM recommendations WHERE user_id = %s"
        val = (user_id,)
        self.cursor.execute(sql, val)
        self.connection.commit()

    def insert_recommendations_to_db(
        self, user_id: int, recommend_shops: list[int] | None
    ) -> None:
        try:
            DatabaseHandler.delete_recommendations_from_db(self, user_id)
            if recommend_shops is None:
                return
            for shop_id in recommend_shops:
                sql = "INSERT INTO recommendations (user_id, shop_id) VALUES (%s, %s)"
                val = (user_id, shop_id)
                self.cursor.execute(sql, val)
            self.connection.commit()
        except Exception as e:
            print(f"Error: {e}")


class ShopsRecommender:
    def __init__(self, user_id: int, connection, cursor):
        self.user_id = user_id
        self.connection = connection
        self.cursor = cursor

    def recommend(self) -> None:
        ratings_table = DataLoader(self.cursor).load_data()
        if ratings_table is None:
            return
        recommended_shops = RecommendationCalculator(
            ratings_table, self.user_id
        ).calculate_recommendations()
        DatabaseHandler(self.connection, self.cursor).insert_recommendations_to_db(
            self.user_id, recommended_shops
        )
        print(recommended_shops)

    def main(self) -> None:
        self.recommend()


if __name__ == "__main__":
    user_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    connection, cursor = connect_to_db()
    shops_recommender = ShopsRecommender(user_id, connection, cursor)
    shops_recommender.recommend()
