import mysql.connector
import json
import pandas as pd
import numpy as np
import sys
from collections import defaultdict


# MySQL接続情報
config = {
    'user': 'posse',
    'password': 'password',
    'host': 'mysql',
    'database': 'website',
    'port': 3306,
}

def connect_to_db(config):
    connection = mysql.connector.connect(**config)
    return connection


connection = connect_to_db(config)

def load_ratings_data(connection,cursor):
    """truncate_sql = "TRUNCATE TABLE recommendations"
    cursor.execute(truncate_sql)

    connection.commit()"""

    query = "SELECT user_id ,shop_id ,rating FROM ratings"
    cursor.execute(query)

    result = cursor.fetchall()
    return result

def peason_coefficient(u,v):
    u_diff = u - np.mean(u)
    v_diff = v - np.mean(v)
    numerator = np.dot(u_diff, v_diff)
    denominator = np.sqrt(sum(u_diff ** 2)) * np.sqrt(sum(v_diff ** 2))
 
    if denominator == 0:
        return 0.0
    return numerator / denominator

def predict_ratings(test_users,df,shop_id2index,nan_df,data):

    for user1_id in test_users.unique():
        similar_users = [] #類似ユーザ
        similarities = [] #類似度
        avgs = [] #類似ユーザの平均評価値

        # ユーザ−１と評価値行列中のその他のユーザーとの類似度を算出する
        for user2_id in df.index:
            if user1_id == user2_id:
                continue

            # ユーザー１とユーザー２の評価値ベクトル
            u_1 = df.loc[user1_id, :].to_numpy() #ユーザ1の評価ベクトル
            u_2 = df.loc[user2_id, :].to_numpy()

            # `u_1` と `u_2` から、ともに欠損値でない要素のみ抜き出したベクトルを取得
            common_items = ~np.isnan(u_1) & ~np.isnan(u_2)

            # 共通して評価したアイテムがない場合はスキップ
            if not common_items.any():
                continue

            u_1, u_2 = u_1[common_items], u_2[common_items]

            # ユーザー１とユーザー２の類似度を算出
            rho_12 = peason_coefficient(u_1, u_2)

            # ユーザー1との類似度が0より大きい場合、ユーザー2を類似ユーザーとみなす
            if rho_12 > 0:
                similar_users.append(user2_id)
                similarities.append(rho_12)
                avgs.append(np.mean(u_2))
                
            # ユーザー１の平均評価値
            avg_1 = np.mean(df.loc[user1_id, :].dropna().to_numpy())


                        
            if user1_id in test_users.unique():
                # 予測対象の店のID
                test_shops = nan_df[nan_df["user_id"] == user1_id].shop_id.values
                # 予測できない店への評価値はユーザー１の平均評価値とする
                nan_df.loc[(nan_df["user_id"] == user1_id), "rating"] = avg_1

                #類似ユーザがいるのならば
                if similar_users:
                    for shop_id in test_shops:
                        if shop_id in shop_id2index:
                            #類似ユーザの予測対象に対する評価
                            r_xy = df.loc[similar_users, shop_id].to_numpy()

                            #欠損値ではないか
                            rating_exists = ~np.isnan(r_xy) 

                            # 類似ユーザーが対象となる店への評価値を持っていない場合はスキップ
                            if not rating_exists.any():
                                continue

                            #評価が存在するところのみ抽出
                            r_xy = r_xy[rating_exists]

                            #類似度と平均評価の評価が存在するユーザのみ
                            rho_1x = np.array(similarities)[rating_exists]
                            avg_x = np.array(avgs)[rating_exists]

                            #ユーザ1の評価値の予測
                            r_hat_1y = avg_1 + np.dot(rho_1x, (r_xy - avg_x)) / rho_1x.sum()

                            # 予測評価値を格納
                            nan_df.loc[
                                (nan_df["user_id"] == user1_id)
                                & (nan_df["shop_id"] == shop_id),
                                "rating",
                            ] = r_hat_1y 

                    
            
    #予測結果を入れたpivot_table
    merged_df = pd.concat([data, nan_df], ignore_index=True)

    # 結合後のデータを pivot_table に変換する
    result = pd.pivot_table(merged_df, index='user_id', columns='shop_id', values='rating')
    return result


def insert_recommendations_data(connection,cursor,pred_user2items):
    for user_id, recommended_shops in pred_user2items.items():
            for shop_id in recommended_shops:
                sql = "INSERT INTO recommendations (user_id, shop_id) VALUES (%s, %s)"
                val = (user_id, shop_id)
                cursor.execute(sql, val)

    connection.commit()
    return 'Sef'




def recommend():
    try:
        cursor = connection.cursor()

        result = load_ratings_data(connection,cursor)

        result_array = np.array([(row[0], row[1], row[2]) for row in result])

        columns = ['user_id','shop_id','rating']

        data = pd.DataFrame(result_array,columns=columns)

        df = pd.pivot_table(data,index='user_id', columns='shop_id', values='rating')
  
        nan_mask = df.isna()
        nan_cells = np.column_stack(np.where(nan_mask))

        nan_user_shop = [(df.index[row], df.columns[column]) for row, column in nan_cells]
        nan_df = pd.DataFrame(nan_user_shop, columns=['user_id', 'shop_id'])

        user_id2index = dict(zip(df.index, range(len(df.index)))) #key、valueが0始まりのindex
        shop_id2index = dict(zip(df.columns, range(len(df.columns))))

        # 予測対象のユーザーID
        test_users = nan_df['user_id']
        shop_rating_predict = nan_df.copy()

        result = predict_ratings(test_users,df,shop_id2index,nan_df,data)
    

        pred_user2items = {}

        #movie_idの名前を変える
        for user_id in result.index:
            pred_user2items[user_id] = [] 
            movie_indexes = result.loc[user_id, :].sort_values(ascending=False).index
            for movie_id in movie_indexes:
                pred_user2items[user_id].append(movie_id)
                # 各ユーザにおけるベスト3
                if len(pred_user2items[user_id]) == 3:
                    break

        #ans = insert_recommendations_data(connection,cursor,pred_user2items)

        print(result)
    
    except Exception as e:
        print(f"Error: {e}")


    finally:
        connection.close() 

if __name__ == "__main__":
    userId = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    recommend()

                    
        
