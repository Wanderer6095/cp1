from flask import Flask
import csv
import sqlite3


app = Flask(__name__)


# @app.route("/vindict/<string:name>")
def wizard(name):
    result = [

    ]
    conn = sqlite3.connect('info.db')
    cursor = conn.cursor()
    data = cursor.execute("select * from education").fetchall()
    print(data)
    conn.close()
    
    # with open('you_know.csv', 'r') as csvfile:
    #     csvreader = csv.reader(csvfile, delimiter=";")
    #     for row in csvreader:
    #         result.append(row[4])
    #     result = result[1:]

wizard("")

# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=8080, debug=True)