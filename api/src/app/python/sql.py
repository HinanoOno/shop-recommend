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

    cursor = connection.cursor()
    
    cursor.execute("USE website")
    return connection,cursor

def load_ratings_data(cursor,connection):
    truncate_sql = "TRUNCATE TABLE recommendations"
    cursor.execute(truncate_sql)
    connection.commit()

    query = "SELECT user_id ,shop_id ,rating FROM ratings"
    cursor.execute(query)

    result = cursor.fetchall()
    return result

def pearson_correlation_coefficent(u,v):
    u_diff = u - np.mean(u)
    v_diff = v - np.mean(v)
    numerator = np.dot(u_diff, v_diff)
    denominator = np.sqrt(sum(u_diff ** 2)) * np.sqrt(sum(v_diff ** 2))
             
    if denominator == 0:
        return 0.0
    return numerator / denominator

def predict_ratings(test_users,df,nan_df,shop_id2index,data):
    for user1_id in test_users.unique():
        similar_users = [] 
        similarities = [] 
        avgs = [] 

        for user2_id in df.index:
            if user1_id == user2_id:
                continue

            u_1 = df.loc[user1_id, :].to_numpy() 
            u_2 = df.loc[user2_id, :].to_numpy()

            common_items = ~np.isnan(u_1) & ~np.isnan(u_2)

            if not common_items.any():
                continue

            u_1, u_2 = u_1[common_items], u_2[common_items]

            rho_12 = pearson_correlation_coefficent(u_1, u_2)

            if rho_12 > 0:
                similar_users.append(user2_id)
                similarities.append(rho_12)
                avgs.append(np.mean(u_2))
                
            avg_1 = np.mean(df.loc[user1_id, :].dropna().to_numpy())
                        
            if user1_id in test_users.unique():
                test_shops = nan_df[nan_df["user_id"] == user1_id].shop_id.values
                
                nan_df.loc[(nan_df["user_id"] == user1_id), "rating"] = avg_1

                if similar_users:
                    for shop_id in test_shops:
                        if shop_id in shop_id2index:
                                
                            r_xy = df.loc[similar_users, shop_id].to_numpy()

                            rating_exists = ~np.isnan(r_xy) 

                            if not rating_exists.any():
                                continue

                            r_xy = r_xy[rating_exists]

                            rho_1x = np.array(similarities)[rating_exists]
                            avg_x = np.array(avgs)[rating_exists]

                            r_hat_1y = avg_1 + np.dot(rho_1x, (r_xy - avg_x)) / rho_1x.sum()

                            nan_df.loc[
                                (nan_df["user_id"] == user1_id)
                                & (nan_df["shop_id"] == shop_id),
                                "rating",
                            ] = r_hat_1y 

    merged_df = pd.concat([data, nan_df], ignore_index=True)

    result = pd.pivot_table(merged_df, index='user_id', columns='shop_id', values='rating')
    return result

def recommend(result,pred_user2items):
    for user_id in result.index:
        pred_user2items[user_id] = [] 
        movie_indexes = result.loc[user_id, :].sort_values(ascending=False).index
        for movie_id in movie_indexes:
            pred_user2items[user_id].append(movie_id)

            if len(pred_user2items[user_id]) == 3:
                break

def insert_recommend_shops_data(connection,cursor,pred_user2items):
    for user_id, recommended_shops in pred_user2items.items():
        for shop_id in recommended_shops:
            sql = "INSERT INTO recommendations (user_id, shop_id) VALUES (%s, %s)"
            val = (user_id, shop_id)
            cursor.execute(sql, val)

    connection.commit()

nan_df = None

def main():
    try:
        connection,cursor = connect_to_db(config)

        result = load_ratings_data(cursor,connection)

        result_array = np.array([(row[0], row[1], row[2]) for row in result])
        
        columns = ['user_id','shop_id','rating']
        data = pd.DataFrame(result_array,columns=columns)

        df = pd.pivot_table(data,index='user_id', columns='shop_id', values='rating')
  
        nan_mask = df.isna()
        nan_cells = np.column_stack(np.where(nan_mask))

        nan_user_shop = [(df.index[row], df.columns[column]) for row, column in nan_cells]
        nan_df = pd.DataFrame(nan_user_shop, columns=['user_id', 'shop_id'])

        shop_id2index = dict(zip(df.columns, range(len(df.columns))))

        test_users = nan_df['user_id']

        result = predict_ratings(test_users,df,nan_df,shop_id2index,data)

        pred_user2items = {}
        
        recommend(result,pred_user2items)
    
        insert_recommend_shops_data(connection,cursor,pred_user2items)


    except Exception as e:
        print(f"Error: {e}")


    finally:
        connection.close()    
 

if __name__ == "__main__":
    userId = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    main()

                    
        
