import math
import random
from functools import reduce
import psycopg2
from config import host, user, password, db_name
import json


# from main import message
def get_connection():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    return connection


def name_parser(name, result=''):
    fff = ''.join(name)
    result += fff + "\n"
    return result


def cortege_parser(cortege1):
    try:
        result = ''
        cortege2 = list(cortege1)
        b = []
        # print(cortege2)
        # cortege2[1] = ([tuple(x) for x in cortege2[1]])
        # print(type(cortege2[5]))
        # list1 = [[1, '1', 1], [2, '2', 2], [3, '3', 3]]
        # outlst = [' '.join([str(c) for c in lst]) for lst in list1]
        cortege2[0] = " ".join(cortege2[0])
        # cortege2[1] = [" ".join(c for c in ele) for ele in cortege2[1]]
        a = [" ".join(ele) for ele in cortege2[1]]
        cortege2[1] = "  ".join(a)
        for i in range(len(cortege2)):
            b.append(cortege2[i])
        print("B  ", b)
        print("C  ", len(cortege2))
        result += "Название рецепта:  " + b[2] + "\n" \
                                                 "Время приготовления:  " + b[3] + "\n" \
                                                                                   "Категории:  " + b[0] + "\n\n" \
                                                                                                           "Ингридиенты:  " + \
                  b[1] + "\n\n" \
                         "Количество порций:  " + b[5] + "\n" \
                                                         "Инструкции по приготовлению:  " + b[4] + "\n" \
                                                                                                   "Ссылка на первоисточник:  " + \
                  b[6] + "\n" \
                         "\n"
        # arr1 = ["Название рецепта: ", "Время приготовления: ", "Категории: ", "Ингридиенты: ", "Количество порций: ", "Инструкции по приготовлению: ", "Ссылка на первоисточ"]
        # arr2 = [b[2], b[3], b[0], b[1], b[5], b[4], b[6]]
        # i = 0
        # while i < len(arr1):
        #     buf_result = arr1[i] + str(arr2[i]) + "\n"
        #     print(buf_result)
        #     result = result + buf_result
        #     i += 1
        return (result)
    except Exception as e:
        print("asdasd ", e)


def add_user(user_id):
    try:
        id = str(user_id)
        connection = get_connection()
        cursor = connection.cursor()
        command = f"""Select id_user from users where id_user = (%s)::text"""
        command1 = f"Insert into users values(%s::text)"
        cursor.execute(command, (id,))
        add = cursor.fetchone()
        if add is None:
            cursor.execute(command1, (id,))
            connection.commit()
        else:
            pass
    except Exception as e:
        print(e)


def add_to_favorite(user_id, data):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        flag = False
        b = str(user_id)
        # command = f"""Update users set favorite = %s  where id_user= (%s)::text"""
        # command = f"""select array_cat(favorite, %s) as favorite
        #    from users where id_user= (%s)::text"""
        command2 = f"""Select favorite from users where id_user = (%s)::text"""
        command = "Update users set favorite = array_append(favorite, %s)  where id_user= (%s)::text"
        cursor.execute(command2, (user_id,))
        arr = cursor.fetchone()
        a = int(data)
        for i in arr[0]:
            if i == data:
                flag = True
        if flag == False:
            cursor.execute(command, (a, b))
            connection.commit()
        return (flag)
    except Exception as e:
        print(e)


def output_list(user_id):
    try:
        a = str(user_id)
        k = 0
        connection = get_connection()
        cursor = connection.cursor()
        command = "Select favorite from users where id_user = (%s)::text"
        command2 = "Select test2.name from test2 where id = %s"
        cursor.execute(command, (user_id,))
        arr = cursor.fetchone()
        result = ''
        result += "Список избранного:" + "\n\n"
        for i in arr[0]:
            cursor.execute(command2, (i,))
            name = cursor.fetchone()
            result += f"{k + 1}. " + name_parser(name)
            k += 1
        return (result, arr[0])
    except Exception as e:
        print(e)


def delete_from_favorite(user_id, data):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        b = str(user_id)
        a = int(data)
        command = "Update users set favorite = array_remove(favorite, %s)  where id_user= (%s)::text"
        cursor.execute(command, (a, b,))
        connection.commit()
        result = 'Рецепт успешно удален'
        return result
    except Exception as e:
        print(e)


def output_one1(data):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        command = f"""SELECT  cat1.categories, cat2.ingredients,test2.name, test2.time, test2.description,  test2.count,  test2.url, test2.id
            		 FROM test2
            	LEFT JOIN (
            		SELECT categorylist.id_recipe,array_agg(category1.name) as categories
            		from categorylist
            		LEFT JOIN category1 ON category1.id = categorylist.id_category
            		GROUP BY categorylist.id_recipe
            	) as cat1 ON cat1.id_recipe = test2.id
            	LEFT JOIN (
            		SELECT ingrlist.id_recipe,json_agg(json_build_array(ingrname.name, ingrlist.value, ingrlist.unit)) as ingredients
            		from ingrlist
            		LEFT JOIN ingrname ON ingrname.id = ingrlist.id_ingr
            		GROUP BY ingrlist.id_recipe
            	) as cat2 ON cat2.id_recipe = test2.id
            	WHERE   test2.id = %s
            	ORDER BY name;
            	"""
        cursor.execute(command, (data,))
        db_data = cursor.fetchall()
        result = ''
        for title in db_data:
            result += cortege_parser(title)
        return result
    except Exception as e:
        print(e)


def name_search(stri):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        result = ''
        # command1 = "SELECT COUNT(id) FROM test2 WHERE similarity(name, (%s))>0.2;"
        # command2 = "SELECT name FROM test2 WHERE similarity(name, (%s))>0.2;"
        command = f"""Select name From test2 WHERE tsv_name @@ plainto_tsquery('russian', %s);;
        	"""
        #     command = """SELECT  cat1.categories, cat2.ingredients,test2.name, test2.time, test2.description,  test2.count,  test2.url
        # 	 FROM test2
        # LEFT JOIN (
        # 	SELECT categorylist.id_recipe,array_agg(category1.name) as categories
        # 	from categorylist
        # 	LEFT JOIN category1 ON category1.id = categorylist.id_category
        # 	GROUP BY categorylist.id_recipe
        # ) as cat1 ON cat1.id_recipe = test2.id
        # LEFT JOIN (
        # 	SELECT ingrlist.id_recipe,json_agg(json_build_array(ingrname.name, ingrlist.value, ingrlist.unit)) as ingredients
        # 	from ingrlist
        # 	LEFT JOIN ingrname ON ingrname.id = ingrlist.id_ingr
        # 	GROUP BY ingrlist.id_recipe
        # ) as cat2 ON cat2.id_recipe = test2.id
        # WHERE  SIMILARITY (test2.name, (%s)) > 0.2
        # ORDER BY name;
        # """
        result = ''
        cursor.execute(command, (stri,))
        db_data = cursor.fetchall()
        a = ''
        count = len(db_data)
        a = str(count)
        b = math.ceil(count / 15)
        k = 0
        knew = 15
        array1 = []
        result += "По вашему запросу найдено " + a + " совпадений" + " \n\n"
        if count <= 15:
            for tit in db_data:
                result += f"{k + 1}. " + name_parser(tit)
                k += 1
            array1.append(result)
        elif count >= 15:
            for a in range(1, b + 1):
                if k < knew and k <= count:
                    for tit in db_data[k:knew]:
                        if tit:
                            result += f"{k + 1}. " + name_parser(tit)
                            k += 1
                else:
                    pass
                knew += 15
                array1.append(result)
                result = ''
        return (array1)
    except Exception as e:
        print('Error name_search ', e)


def repeat_name_serch(stri):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        command = f"""SELECT  cat1.categories, cat2.ingredients,test2.name, test2.time, test2.description,  test2.count,  test2.url, test2.id
    		 FROM test2
    	LEFT JOIN (
    		SELECT categorylist.id_recipe,array_agg(category1.name) as categories
    		from categorylist
    		LEFT JOIN category1 ON category1.id = categorylist.id_category
    		GROUP BY categorylist.id_recipe
    	) as cat1 ON cat1.id_recipe = test2.id
    	LEFT JOIN (
    		SELECT ingrlist.id_recipe,json_agg(json_build_array(ingrname.name, ingrlist.value, ingrlist.unit)) as ingredients
    		from ingrlist
    		LEFT JOIN ingrname ON ingrname.id = ingrlist.id_ingr
    		GROUP BY ingrlist.id_recipe
    	) as cat2 ON cat2.id_recipe = test2.id
    	WHERE   SIMILARITY (test2.name, (%s)) > 0.8
    	ORDER BY name;
    	"""
        result = ''
        cursor.execute(command, (stri,))
        db_data = cursor.fetchall()
        id_recipe = db_data[0][7]
        for title in db_data:
            result += cortege_parser(title)
        return (result, id_recipe)
    except Exception as e:
        print('Error name_search ', e)


def category_search(stri):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        res = ''
        k = 0
        knew = 15
        array = []
        array1 = []
        l = ''
        array = stri.split(", ")
        array = list(map(lambda x: x.lower(), array))
        #     command2 = """SELECT   test2.name
        # 	 FROM test2
        # LEFT JOIN (
        # 	SELECT categorylist.id_recipe,array_agg(category1.name1) as categories
        # 	from categorylist
        # 	LEFT JOIN category1 ON category1.id = categorylist.id_category
        # 	GROUP BY categorylist.id_recipe
        # ) as cat1 ON cat1.id_recipe = test2.id
        # LEFT JOIN (
        # 	SELECT ingrlist.id_recipe,json_agg(json_build_array(ingrname.name, ingrlist.value, ingrlist.unit)) as ingredients
        # 	from ingrlist
        # 	LEFT JOIN ingrname ON ingrname.id = ingrlist.id_ingr
        # 	GROUP BY ingrlist.id_recipe
        # ) as cat2 ON cat2.id_recipe = test2.id
        # WHERE cat1.categories @> (%s)
        # ORDER BY name;"""
        #
        #     cursor.execute(command2, (array,))
        #     db_data = cursor.fetchall()
        #     count = len(db_data)
        #     a = ''
        #     a = str(count)
        command = "Select id from category1 where name2 @@ plainto_tsquery('russian', %s)"
        command3 = "Select id_recipe from categorylist where id_category = %s"
        resa = []
        for i in array:
            cursor.execute(command, (i,))
            res = cursor.fetchall()
            resa.append(res)
        data = []
        dat = []
        for i in range(len(resa)):
            for j in range(len(resa[i])):
                cursor.execute(command3, (resa[i][j],))
                d = cursor.fetchall()
                dat += d
            data.append(dat)
            dat = []
        dat = data.copy()
        m = len(dat)
        gg = reduce(set.intersection, map(set, dat[0:m]))
        j = 1
        db_data = []
        check = 1
        while check == 1:
            if len(gg) == 0:
                gg = reduce(set.intersection, map(set, dat[0:m - 1]))
                m = m - 1
            else:
                check = 0
        for o in gg:
            cursor.execute("Select test2.name from test2 where id = %s", o)
            f = cursor.fetchone()
            db_data.append(f)
            j += 1
        count = len(db_data)
        a = ''
        a = str(count)
        res = ''
        b = math.ceil(count / 15)
        res += "По вашему запросу найдено " + a + " совпадений" + " \n\n"
        if count <= 15:
            for tit in db_data:
                res += f"{k + 1}. " + name_parser(tit)
                k += 1
            array1.append(res)
        elif count >= 15:
            for a in range(1, b + 1):
                if k < knew and k <= count:
                    for tit in db_data[k:knew]:
                        if tit:
                            res += f"{k + 1}. " + name_parser(tit)
                            k += 1
                else:
                    pass
                knew += 15
                array1.append(res)
                res = ''
        print('arr: ', array1)

        return (array1)
    except Exception as e:
        print('Error name_search ', e)


def ingredients_search(stri):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        result = ''
        res = ''
        k = 0
        knew = 15
        array = []
        array1 = []
        l = ''
        array = stri.split(", ")
        array = list(map(lambda x: x.lower(), array))
        # command2 = """SELECT   test2.name
        #      FROM test2
        # LEFT JOIN (
        #     SELECT categorylist.id_recipe,array_agg(category1.name) as categories
        #     from categorylist
        #     LEFT JOIN category1 ON category1.id = categorylist.id_category
        #     GROUP BY categorylist.id_recipe
        # ) as cat1 ON cat1.id_recipe = test2.id
        # LEFT JOIN (
        #     SELECT ingrlist.id_recipe,array_agg(ingrname.name1) as ingredients
        #     from ingrlist
        #     LEFT JOIN ingrname ON ingrname.id = ingrlist.id_ingr
        #     GROUP BY ingrlist.id_recipe
        # ) as cat2 ON cat2.id_recipe = test2.id
        # WHERE cat2.ingredients @> (%s)
        # ORDER BY name;"""
        command = "Select id from ii where tsv @@ plainto_tsquery('russian', %s)"
        command3 = "Select id_recipe from ingrlist where id_ingr = %s"
        resa = []
        for i in array:
            cursor.execute(command, (i,))
            res = cursor.fetchall()
            resa.append(res)
        data = []
        dat = []
        for i in range(len(resa)):
            for j in range(len(resa[i])):
                cursor.execute(command3, (resa[i][j],))
                d = cursor.fetchall()
                dat += d
            data.append(dat)
            dat = []
        dat = data.copy()
        m = len(dat)
        gg = reduce(set.intersection, map(set, dat[0:m]))
        j = 1
        db_data = []
        check = 1
        while check == 1:
            if len(gg) == 0:
                gg = reduce(set.intersection, map(set, dat[0:m - 1]))
                m = m-1
            else:
                check = 0
        for o in gg:
            cursor.execute("Select test2.name from test2 where id = %s", o)
            f = cursor.fetchone()
            db_data.append(f)
            j += 1
        count = len(db_data)
        a = ''
        a = str(count)
        res = ''
        b = math.ceil(count / 15)
        res += "По вашему запросу найдено " + a + " совпадений" + " \n\n"
        if count <= 15:
            for tit in db_data:
                res += f"{k + 1}. " + name_parser(tit)
                k += 1
            array1.append(res)
        elif count >= 15:
            for a in range(1, b + 1):
                if k < knew and k <= count:
                    for tit in db_data[k:knew]:
                        if tit:
                            res += f"{k + 1}. " + name_parser(tit)
                            k += 1
                else:
                    pass
                knew += 15
                array1.append(res)
                res = ''

        print('arr: ', array1)

        return array1
    except Exception as e:
        print('Error name_search ', e)


def random_recipe():
    connection = get_connection()
    cursor = connection.cursor()
    command = 'Select name from test2 where id = %s'
    ran = random.randrange(1, 1960)
    cursor.execute(command, (ran,))
    data = cursor.fetchone()
    new_data = repeat_name_serch(data)
    return new_data
