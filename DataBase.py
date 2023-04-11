import math

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
def name_parser(name, result= ''):
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
        result +="Название рецепта:  " + b[2] + "\n" \
                "Время приготовления:  " + b[3] + "\n" \
                "Категории:  " + b[0] + "\n\n"\
                "Ингридиенты:  " + b[1] + "\n\n"\
                "Количество порций:  " + b[5] + "\n"\
                "Инструкции по приготовлению:  " + b[4] + "\n"\
                "Ссылка на первоисточник:  " + b[6] + "\n"\
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


def name_search(stri):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        result = ''
        command1 = "SELECT COUNT(id) FROM test2 WHERE similarity(name, (%s))>0.2;"
        command2 = "SELECT name FROM test2 WHERE similarity(name, (%s))>0.2;"
        command = f"""SELECT  cat1.categories, cat2.ingredients,test2.name, test2.time, test2.description,  test2.count,  test2.url
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
	WHERE  SIMILARITY (test2.name, (%s)) > 0.2
	ORDER BY name;
	"""
        result = ''
        cursor.execute(command1, (stri,))
        db_count = cursor.fetchone()
        a = ''
        a = str(db_count[0])
        k = 1
        if db_count[0] > 1:
            result += "Список возможных рецептов, который вы искали:  " + a +"\n\n"
            cursor.execute(command2, (stri,))
            db_data = cursor.fetchall()
            for title in db_data:
                result += f"{k}. " + name_parser(title)
                k += 1
        elif db_count[0] == 1:
            cursor.execute(command, (stri,))
            db_data = cursor.fetchall()
            for title in db_data:
                result += cortege_parser(title)
        elif db_count[0] == 0:
            result += "Не найдено рецептов, который вы искали"
        # cursor.execute(command, (str,))
        # db_data = cursor.fetchall()
        # result = ''
        # for title in db_data:
        #     result += cortege_parser(title)
        print('result ', result)
        return (result)
    except Exception as e:
        print('Error name_search ', e)
def repeat_name_serch(stri):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        command = f"""SELECT  cat1.categories, cat2.ingredients,test2.name, test2.time, test2.description,  test2.count,  test2.url
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
        for title in db_data:
            result += cortege_parser(title)
        return (result)
    except Exception as e:
        print('Error name_search ', e)

def category_search(stri):
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
        command2 = """SELECT   test2.name
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
	WHERE cat1.categories @> (%s)
	ORDER BY name;"""
        cursor.execute(command2, (array,))
        db_data = cursor.fetchall()
        count = len(db_data)
        a = ''
        a = str(count)
        b = math.ceil(count/15)
        res += "По вашему запросу найдено " + a + " совпадений." + " \n\n"
        if count <= 15:
            for tit in db_data:
                res += name_parser(tit)
            array1.append(res)
        elif count >= 15:
           for a in range(1, b+1):
                if k < knew and k<=count:
                    for tit in db_data[k:knew]:
                        if tit:
                            res +=f"{k+1}. " + name_parser(tit)
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
        command2 = """SELECT   test2.name
             FROM test2
        LEFT JOIN (
            SELECT categorylist.id_recipe,array_agg(category1.name) as categories
            from categorylist
            LEFT JOIN category1 ON category1.id = categorylist.id_category
            GROUP BY categorylist.id_recipe
        ) as cat1 ON cat1.id_recipe = test2.id
        LEFT JOIN (
            SELECT ingrlist.id_recipe,array_agg(ingrname.name) as ingredients
            from ingrlist
            LEFT JOIN ingrname ON ingrname.id = ingrlist.id_ingr
            GROUP BY ingrlist.id_recipe
        ) as cat2 ON cat2.id_recipe = test2.id
        WHERE cat2.ingredients @> (%s)
        ORDER BY name;"""
        cursor.execute(command2, (array,))
        db_data = cursor.fetchall()
        count = len(db_data)
        a = ''
        a = str(count)
        b = math.ceil(count / 15)
        res += "По вашему запросу найдено " + a + " совпадений." + " \n\n"
        if count <= 15:
            for tit in db_data:
                res += name_parser(tit)
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