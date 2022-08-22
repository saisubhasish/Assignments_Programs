"""
    This is my code to insert record to sql via api
"""

import logging
import mysql.connector as conn
from flask import Flask, request, jsonify

logging.basicConfig(filename='Task.log', level=logging.INFO, format='%(levelname)s %(asctime)s %(name)s %(message)s')


app = Flask(__name__)

connection = conn.connect(host='localhost', user='root', passwd='Root_mysql')
cursor = connection.cursor()

cursor.execute("create database if not exists taskdb")
cursor.execute("create table if not exists taskdb.tasktable (name varchar(30) , number int)")

@app.route('/insert', methods=['POST'])
def insert():
    if request.method =='POST':
        name = request.json['name']
        number = request.json['number']
        cursor.execute('insert into taskdb.tasktable values(%s, %s)',(name, number))
        connection.commit()
        logging.info(name,' ', number)
        return jsonify(str('Successfully inserted'))

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        get_name = request.json['get_name']
        cursor.execute('update taskdb.tasktable set number = number + 500 where name = %s', (get_name))
        connection.commit()
        return jsonify(str('Updated Successfully'))

@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        name_del = request.json['name_del']
        cursor.execute("delete from taskdb.tasktable where where name = %s", (name_del))
        connection.commit()
        return jsonify(str("deleted successfully"))

@app.route('/fetch', methods=['POST'])
def fetch_data():
    cursor.execute('select * from taskdb.tasktable')
    l = []
    for i in cursor.fetchall():
        l.append(i)
    return jsonify(str(l))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



