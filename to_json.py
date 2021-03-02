import sqlite3 as sql
import json
import javaobj
from dotenv import load_dotenv
import os


def get_properties_of(object):
    for property, value in vars(object).items():
        try:
            print(f"{property} : {value} {len(value)}")
        except:
            print(f"{property} : {value}")


load_dotenv()

connection = sql.connect("data/msgstore.db")
print("Connection successful!!!")
cursor = connection.cursor()

keys = cursor.execute("PRAGMA table_info('messages')").fetchall()
cursor.execute(
    f"SELECT * FROM messages WHERE key_remote_jid = '{os.getenv('REQUIRED_JID')}'")
json_messages_list = []

javaobject = 0
javaobject2 = 0

while True:
    message = cursor.fetchone()
    if not message:
        break
    message_json = dict()
    for index, key in enumerate(keys):
        if isinstance(message[index], bytes):
            # FIXME: deal with JavaByteArray
            value = javaobj.loads(message[index])
            if javaobject == 0:
                javaobject = value
            elif javaobject2 == 0:
                javaobject2 = value
        else:
            value = message[index]
        message_json[key[1]] = value
        json_messages_list.append(message_json)


get_properties_of(javaobject)
get_properties_of(javaobject2)
# print(json_messages_list)
# to_be_dumped = json.JSONEncoder().encode(json_messages_list)

with open('data/messages_formatted.json', 'w', encoding="utf-8") as json_file:
    json.dump(list(json_messages_list), json_file, indent=4)
