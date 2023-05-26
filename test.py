import psycopg2
import random
from functools import reduce
from DataBase import name_parser
host = "127.0.0.1"
user = "postgres"
password = "1234"
db_name = "Recipe"
connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)
connection.autocommit = True
cursor = connection.cursor()
command = "Select id from ii where tsv @@ plainto_tsquery('russian', %s)"
command3 = "Select id_recipe from ingrlist where id_ingr = %s"
stroka = 'яблоко, сахар'
a1 = "сахар"
a2 = "яблоко"
array = stroka.split(", ")
resa = []
print(array)
for i in array:
    cursor.execute(command, (i,))
    res = cursor.fetchall()
    resa.append(res)
print(resa)
print("len:  ", len(resa))
data = []
dat = []
for i in range(len(resa)):
    for j in range(len(resa[i])):
        cursor.execute(command3, (resa[i][j],))
        d = cursor.fetchall()
        dat += d
    data.append(dat)
    dat = []
print(data)
print(len(data))
dat = data.copy()
m = len(dat)
print(m)
# for i in range(len(data)):
#     data[i] = set(data[i])
# for i in range(len(data)):
#     data[i] = map(tuple, data[i])
# result = list(map(list, set(data[0]) & set(data[1])))
# print("res", result)
gg = reduce(set.intersection, map(set, dat[0:m]))
j = 1
res = ''
db_data = []
if len(gg) == 0:
    gg = reduce(set.intersection, map(set, dat[0:m-1]))
for o in gg:
    cursor.execute("Select test2.name from test2 where id = %s", o)
    f = cursor.fetchone()
    db_data.append(f)
    j += 1
# m = 1
# Flag = 0
# if len(result) < 15:
#     for i in range(len(dat)):
#         dat[i] = set(dat[i])
#     for i in range(len(dat)):
#         dat[i] = map(tuple, dat[i])
#     temp = list(map(list, (set(dat[0]) & (set(dat[1]) or (set(dat[2]))))))
#     Flag = 1
# if Flag == 0:
#     for o in result:
#         cursor.execute("Select test2.name from test2 where id = %s", o)
#         f = cursor.fetchone()
#         gg += f"{m}. " + name_parser(f)
#         m += 1
# else:
#     for o in temp:
#         cursor.execute("Select test2.name from test2 where id = %s", o)
#         f = cursor.fetchone()
#         gg += f"{m}. " + name_parser(f)
#         m += 1

print(db_data)
print(len(db_data))
ran = random.randrange(1, 1960)
print(ran)
# M1 = np.array(data[0])
# M2 = np.array(data[1])
# M = np.intersect1d(M1, M2)
# print(M)

# f3 = resa[0] + resa[1] + resa[2]
# data = []
# print(f3)
# for i in f3:
#     cursor.execute(command3, (i,))
#     d = cursor.fetchall()
#     data.append(d)
# print("DATA:   ", data)
# start = datetime.now()
# mas = []
# l = len(data)
# j = 1
# while j < l:
#     for i in range(l):
#         if i != j:
#             k = set(data[j]).intersection(data[i])
#             if k:
#                 print("i , j ", i, j)
#                 mas.append(k)
#     j += 1
# j = 1
# l1 = len(mas)
# print(mas[0])
# print(mas[3])
# start = datetime.now()
# mas = []
# l = len(data)
# j = 1
# while j < l:
#     for i in range(l):
#         if i != j:
#             k = set(data[j]).intersection(data[i])
#             if k:
#                 print("i , j ", i, j)
#                 mas.append(k)
#     j += 1
# j = 1
# l1 = len(mas)
# print(mas[0])
# print(mas[3])
# for m in range(l1):
#     if j < l1:
#         if collections.Counter(mas[m]) == collections.Counter(mas[j]):
#             mas.remove(mas[m])
#         j += 1
# print(mas)
# print(type(mas))

# print("5", data[5])
# print("7", data[7])
# kk = []
# for i in resa[0]:
#     for j in resa[1]:
#         a = []
#         a.append(i)
#         a.append(j)
#         cursor.execute(command2, (a,))
#         my = cursor.fetchall()
#         if my:
#             kk.append(my)
#         print(my)
# print('kk: ', kk)
# end = datetime.now()
# total = end - start
# print(total)
# command2 = "Select favorite from users where id_user = (%s)::text"
# command = "Update users set favorite = array_append(favorite, %s)  where id_user= (%s)::text"
# cursor.execute(command2, (b,))
# result = cursor.fetchone()
# cursor.execute(command, (a, b))
# results = cursor.fetchall()
# cursor.execute('''CREATE TABLE categorylist
# (
# id_category integer,
# id_recipe integer
#  );''')
# cursor.execute("Select id, ingrname From ingrname where id = 14;")
# a = [1, 2, 3, 4]
# result = len(a)
# print(result)
connection.commit()
connection.close()
