def load_ratings_data(cursor, connection):
    query = "SELECT user_id ,shop_id ,rating FROM ratings"
    cursor.execute(query)

    result = cursor.fetchall()
    return result
