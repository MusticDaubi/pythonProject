# import psycopg2

host = "127.0.0.1"
user = "postgres"
password = "1234"
db_name = "Recipe"


# connection = psycopg2.connect(
#             host=host,
#             user=user,
#             password=password,
#             database=db_name
#         )
# connection.autocommit = True
# cursor = connection.cursor()
# cursor.execute('''CREATE TABLE category
# (
# id serial NOT NULL,
# category varchar(60) UNIQUE ,
#  PRIMARY KEY (id, category));''')
# connection.commit()
# connection.close()

# '''CREATE TABLE ingrall
# (
# id serial NOT NULL PRIMARY KEY,
# category varchar(300) NOT NULL,
# name varchar(60) NOT NULL,
# time varchar(30) NOT NULL,
# ingrname varchar(250) NOT NULL,
# ingrs varchar(350) NOT NULL,
# description text NOT NULL,
# count integer,
# url varchar(100) NOT NULL);''')