from lib2to3.pytree import convert
import sqlite3
from flask import jsonify, url_for
from PIL import Image

DB_PATH = './todo.db'   # Update this path accordingly

def make_public_todo(row):
    new_todo = {}
    for field in row.keys():
        if field == 'todo_id':
            new_todo['uri'] = url_for('get_todo', todo_id = row['todo_id'], _external = True)
        else:
            new_todo[field] = row[field]

    return new_todo

def get_all_todos():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('select nickname, sex, email, cnt_game, cnt_win, cnt_lose, time from todos')
        rows = c.fetchall()
        result = { 'todos': list(map(make_public_todo, rows)) }
        return result
    except Exception as e:
        print('Error: ', e)
        return None


def get_todo(nn):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("select nickname, sex, email, cnt_game, cnt_win, cnt_lose, time from todos where nickname = ?;" , [nn])
        r = c.fetchone()
        return make_public_todo(r)
    except Exception as e:
        print('Error: ', e)
    return None


def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        return bytearray(file.read())

def parse_(req):
    return req["nickname"], convertToBinaryData(req["photo"]), req["sex"], req["email"]

def add_to_list(req):
    try:
        nn, photo, sex, email = parse_(req)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        sql_req = 'insert into todos(nickname, photo, sex, email, cnt_game, cnt_win, cnt_lose, time) values(?,?,?,?,?,?,?,?)'
        c.execute(sql_req, (nn, photo, sex, email, None, None, None, None))
        conn.commit()
        result = get_todo(nn)
        return result
    except Exception as e:
        print('Error: ', e)
        return None


def set_(c, nn, req):
    params = ["photo", "sex", "email", "cnt_game", "cnt_win", "cnt_lose", "time"]
    for i in params:
        if i in req:
            if i == "photo":
                img = convertToBinaryData(req[i])
                c.execute("update todos set "+ i + "=? where nickname = ?", (img, nn))
            else:
                c.execute("update todos set "+ i + "=? where nickname = ?", (req[i], nn))   

def update_todo(nn, req):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        set_(c, nn, req)
        conn.commit()
        result = get_todo(nn)
        return result
    except Exception as e:
        print('Error: ', e)
        return None

def remove_todo(nn):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM todos WHERE nickname=?', [nn])
        conn.commit()
        return { 'result': True } 
    except Exception as e:
        print('Error: ', e)
        return None

def get_all(nn):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("select * from todos where nickname = ?;" , [nn])
        r = c.fetchone()
        return make_public_todo(r)
    except Exception as e:
        print('Error: ', e)
    return None