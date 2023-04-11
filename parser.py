import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
import psycopg2
from config import host, user, password, db_name
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0 (Edition Yx GX)"}

tic = datetime.now()
id=0
try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True
    cursor = connection.cursor()
    def get_url():
        for count in range(1, 50):

            url = f"https://povar.ru/mostnew/all/{count}/"
            response = requests.get(url, headers=headers)

            soup = BeautifulSoup(response.text, "lxml")

            data = soup.find_all("div", class_="h3")

            for i in data:
                card_url = "https://www.povar.ru" + i.find("a", class_="listRecipieTitle").get("href")
                yield card_url


    for card_url in get_url():
        response = requests.get(card_url, headers=headers)
        sleep(1)
        soup = BeautifulSoup(response.text, "lxml")
        card = soup.find("div", class_="cont_area hrecipe")
        time = card.find("span", class_="duration").text
        name = card.find("h1", class_="detailed fn").text
        count = card.find("span", class_="yield value").text
        ingr = card.find_all("li", class_="ingredient flex-dot-line")
        kats = card.find_all("span", class_="detailed_tags")
        category_list = []
        category_id = []
        description = []
        tags = card.find_all("div", class_="detailed_step_description_big")
        for tag in tags:
            description.append(tag.text)
        id += 1

        data = {
            # 'category': category_id,
            'id': id,
            'name': name,
            'time': time,
            # 'ingrName': ingr_id,
            # 'ingrs': ingr_info,
            'description': description,
            'count': count,
            'url': card_url
        }

        _SQL = """INSERT INTO test2 (id, name, time, description, count, url) values (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(
            _SQL, (data['id'], data['name'], data['time'], data['description'], data['count'], data['url'])
        )
        connection.commit()

        for kat in kats:
            links = kat.find_all("a")
            for link in links:
                category = link.text
                _SQL = 'INSERT INTO category1(category) values (\'' + category + '\');'
                _SQL2 = 'SELECT id FROM category1 WHERE category = %s'
                _SQL3 = 'INSERT INTO categorylist(id_category, id_recipe) values (%s,%s);'
                # _SQL4 = 'INSERT INTO categorylist(id_recipe) values (%s)'
                try:
                    cursor.execute(_SQL2, (category,))
                    check = cursor.fetchone()
                    if check is None:
                        cursor.execute(_SQL)
                        cursor.execute('SELECT id FROM category1 WHERE category = (\'' + category + '\')')
                        c = cursor.fetchone()
                        cursor.execute(_SQL3, (c, id,))
                        category_id.append(c)
                    else:
                        cursor.execute('SELECT id FROM category1 WHERE category = (\'' + category + '\')')
                        k = cursor.fetchone()
                        cursor.execute(_SQL3, (k, id,))
                        # cursor.execute(_SQL4, (id,))
                except psycopg2.IntegrityError:
                    cursor.execute('SELECT id FROM category1 WHERE category = (\'' + category + '\')')
                    k = cursor.fetchone()
                    cursor.execute(_SQL3, (k, id,))
                    category_id.append(c)
                    connection.rollback()
                else:
                    connection.commit()
                category_list.append(category)

        ingrNames = []
        ingrs = []
        ingr_id = []
        ingr_info = []
        ing = []
        for tag1 in ingr:
            ingrName = tag1.find("span", class_="name")
            ingrValue = tag1.find("span", class_="value")
            ingrUnit = tag1.find("span", class_="u-unit-name")
            _SQL3 = 'INSERT INTO ingrlist(id_ingr, id_recipe) values (%s,%s);'
            try:
                if ingrName:
                    ingrName = ingrName.text
                    a = ingrName
                    _SQL = 'INSERT INTO ingrname(ingrname) values (\''+a+'\');'
                    _SQL2 = 'SELECT id FROM ingrname WHERE ingrname = %s'
                    # _SQL3 = 'INSERT INTO ingrlist(id_ingr, id_recipe) values (%s,%s);'
                    try:
                        cursor.execute(_SQL2, (a,))
                        check = cursor.fetchone()
                        if check is None:
                            cursor.execute(_SQL)
                            cursor.execute('SELECT id FROM ingrname WHERE ingrname = (\''+a+'\')')
                            b = cursor.fetchone()
                            # cursor.execute(_SQL3, (b, id,))
                            ingr_id.append(b)
                        else:
                            cursor.execute('SELECT id FROM ingrname WHERE ingrname = (\'' + a + '\')')
                            b = cursor.fetchone()
                            # cursor.execute(_SQL3, (b, id,))
                    except psycopg2.IntegrityError:
                        cursor.execute('SELECT id FROM ingrname WHERE ingrname = (\'' + a + '\')')
                        b = cursor.fetchone()
                        # cursor.execute(_SQL3, (b, id,))
                        ingr_id.append(b)
                        connection.rollback()
                    else:
                            connection.commit()
                   # ingrNames.append(ingrName)
                else:
                    ingrName = ""
            except:
                ingrName = ""

            try:
                if ingrValue:
                    ingrValue = ingrValue.text
                    g = ingrValue
                    # cursor.execute('SELECT id_ingr FROM ingrlis')
                    # p = cursor.fetchone()
                    # cursor.execute('INSERT INTO ingrlist(value) values (%s);', )
                    # ingrs.append(ingrValue)
                else:
                    ingrValue = ""
                    g = ingrValue
            except:
                ingrValue = ""
                g = ingrValue
            try:
                if ingrUnit:
                    ingrUnit = ingrUnit.text
                    # ingrs.append(ingrUnit)
                    c = ingrUnit
                else:
                    ingrUnit = ""
                    c = ingrUnit
            except:
                ingrUnit = ""
                c = ingrUnit
            ingr_info.append(a + "  " + g + "  " + c)
        # print(ingr_info)
        # print(card_url)
        #     try:
        #         connection = psycopg2.connect(
        #             host=host,
        #             user=user,
        #             password=password,
        #             database=db_name
        #         )
        #         connection.autocommit = True
        #         cursor = connection.cursor()
        #         _SQL = 'INSERT INTO ingrall(ingr_id) values (%s);'
        #         _SQL4 = 'SELECT id FROM ingrname WHERE ingrname = (\'' + a + '\')'
        #         _SQL2 = 'INSERT INTO ingrall(ingr_value) values (\'' + g + '\');'
        #         _SQL3 = 'INSERT INTO ingrall(ingr_unit) values (\'' + c + '\');'
        #         try:
        #             cursor.execute('SELECT id FROM ingrname WHERE ingrname = (\'' + a + '\')')
        #             b = cursor.fetchone()
        #             print(b)
        #             cursor.execute(_SQL, b)
        #             cursor.execute(_SQL2)
        #             cursor.execute(_SQL3)
        #             # cursor.execute('SELECT id FROM ingrall WHERE ingr_id = (\'' + b + '\') AND ingr_values = (\'' + g + '\') AND ingr_unt = (\'' + c + '\') ')
        #             d = cursor.fetchone()
        #             ingr_info.append(d)
        #         except psycopg2.IntegrityError:
        #             cursor.execute('SELECT id FROM ingrall WHERE ingr_id = b AND ingr_values = (\'' + g + '\') AND ingr_unt = (\'' + c + '\') ')
        #             d = cursor.fetchone()
        #             ingr_info.append(d)
        #             connection.rollback()
        #         else:
        #             connection.commit()
        #     except Exception as _ex:
        #         print("Error", _ex)
        #
        #     finally:
        #         if connection:
        #             cursor.close()
        #             connection.close()
        # try:
        #     connection = psycopg2.connect(
        #         host=host,
        #         user=user,
        #         password=password,
        #         database=db_name
        #     )
        #     connection.autocommit = True
        #     cursor = connection.cursor()
        #     _SQL = 'INSERT INTO ingrname(ingrname) values (\'' + a + '\');'
        #     _SQL2 = 'SELECT last_insert_id() from ingrname'
        #     _SQL3 = 'INSERT INTO test(id_ingr) values (\'' + ingr_id + '\');'
        #     print(a)
        #     try:
        #         ingr_id = cursor.execute(_SQL2)
        #         print(ingr_id)
        #     except psycopg2.IntegrityError:
        #         connection.rollback()
        #     else:
        #         connection.commit()
        # except Exception as _ex:
        #     print("Error", _ex)
        #
        # finally:
        #     if connection:
        #         cursor.close()
        #         connection.close()
            _SQL3 = 'INSERT INTO ingrlist(id_ingr, id_recipe, value, unit) values (%s,%s,%s,%s);'
            cursor.execute(_SQL3, (b, id, g, c,))
        _SQL9 = f"""UPDATE test2 SET ingrs = (%s) WHERE id = (%s)"""
        cursor.execute(_SQL9, (ingr_info, id,))
        connection.commit()
        # print(ingr_info)
        # print(card_url)
    # try:
    #     connection = psycopg2.connect(
    #         host=host,
    #         user=user,
    #         password=password,
    #         database=db_name
    #     )
    #     connection.autocommit = True
    #     cursor = connection.cursor()
    #     _SQL = 'INSERT INTO ingrname (ingrname) values (%s);'
    #     print(ingrNames)
    #     cursor.executemany(
    #         _SQL, ingrNames
    #             )
    #     connection.commit()
    # except Exception as _ex:
    #     print("Error", _ex)
    #
    # finally:
    #     if connection:
    #         cursor.close()
    #         connection.close()
except Exception as _ex:
    pass
    print("Error ", _ex)
    # print(data)
finally:
    if connection:
        cursor.close()
        connection.close()
toc = datetime.now()
total = toc-tic
print(f"Программа заняла {total} секунд")