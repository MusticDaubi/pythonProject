# import psycopg2
# host = "127.0.0.1"
# user = "postgres"
# password = "1234"
# db_name = "Recipe"
# connection = psycopg2.connect(
#             host=host,
#             user=user,
#             password=password,
#             database=db_name
#         )
# connection.autocommit = True
# # a = "Палау"
# cursor = connection.cursor()
# # command = "SELECT name, time, category, ingrs, count, description, url FROM test2 WHERE name = %s "
# # cursor.execute(command, (a,))
# # results = cursor.fetchall()
# # cursor.execute('''CREATE TABLE categorylist
# # (
# # id_category integer,
# # id_recipe integer
# #  );''')
# cursor.execute("Select id, ingrname From ingrname where id = 14;")
# result = cursor.fetchone()
# print(result)
# connection.commit()
# connection.close()

