import sqlite3 as sql


def dictify(cursor, keys):
    """
    Arguments: cursor that is reading rows from table and keys
        containing names of each column
    Return Value: list containing each row as a dictionary with keys
        as column name and data as cell data
    """
    dict_list = []
    while True:
        data = cursor.fetchone()
        if not data:
            break
        dict_ = dict()
        for index, key in enumerate(keys):
            dict_[key[1]] = data[index]
        dict_list.append(dict_)
        # print(f"{key[1]}: {data[index]}")
    return dict_list


def print_dict(dict_):
    print("{")
    for key, value in dict_.items():
        print(f"\t{key}: {value}")
    print("}")


def find_dict(dict_list, reqd_key, reqd_value):
    reqd_dict_list = []
    for dict_ in dict_list:
        if dict_[reqd_key] == reqd_value:
            reqd_dict_list.append(dict_)
    return reqd_dict_list


def print_table_info(cursor, table_name):
    # Getting names of columns in table
    keys = cursor.execute(f"PRAGMA table_info('{table_name}')").fetchall()
    # Cursor now fetches data of each row in table
    cursor.execute(f"SELECT * from {table_name}")

    dict_list = dictify(cursor, keys)

    print("############################# keys ##############################")
    for row in keys:
        print(row)
    print("############################# keys ##############################")
    print("############################# element ##############################")
    if len(dict_list) > 0:
        print_dict(dict_list[0])
    print(f"{len(dict_list)} similar elements")
    print("############################# element ##############################")


db_path = "data/chatsettings.db"
connection = sql.connect(db_path)
print("Connection successful!!!")
cursor = connection.cursor()
print(
    f"############################# {db_path} ##############################")

print("############################# sql_master cols ##############################")
# Printing the available column names in sql_master
keys = cursor.execute("PRAGMA table_info('sqlite_master')").fetchall()
for row in keys:
    print(row)
print("############################# sql_master cols ##############################")

# Printing all available tables in sql_master
res = connection.execute("""
    SELECT type, name, tbl_name, rootpage FROM sqlite_master
    WHERE type = 'table';
    """)
# res = connection.execute("SELECT type, name, tbl_name, rootpage, sql FROM sqlite_master where type = 'table';")
for name in res:
    print()
    print(
        f"############################# {name[1]} ##############################")
    print(name)
    print_table_info(cursor, name[1])
    print(
        f"############################# {name[1]} ##############################")
    print()

print(
    f"############################# {db_path} ##############################")
