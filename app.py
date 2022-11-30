import random

from flask import Flask
from flask import request
from flask_mysqldb import MySQL
from flask_cors import CORS
import json

mysql = MySQL()
app = Flask(__name__)
CORS(app)
# My SQL Instance configurations
# Change these details to match your instance configurations
app.config['MYSQL_USER'] = 'A'
app.config['MYSQL_PASSWORD'] = 'B'
app.config['MYSQL_DB'] = 'student'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/add")  # Add Student
def add():
    name = request.args.get('name')
    email = request.args.get('email')
    print(name, email)
    if name is not None and email is not None:
        cur = mysql.connection.cursor()  # create a connection to the SQL instance
        s = '''INSERT INTO students(studentName, email) VALUES('{}','{}');'''.format(name,
                                                                                     email)  # kludge - use stored
        # proc or params
        cur.execute(s)
        mysql.connection.commit()
        response = {"Result": "Success"}
        ret = app.response_class(
            response=json.dumps(response),
            status=200,
            mimetype='application/json'
        )
        return ret
    else:
        response = {"Result": "Failure"}
        ret = app.response_class(
            response=json.dumps(response),
            status=400,
            mimetype='application/json'
        )
        return ret

@app.route("/delete")  # Delete Student
def add():
    id = request.args.get('id')
    if id is not None:
        cur = mysql.connection.cursor()  # create a connection to the SQL instance
        s = '''DELETE FROM Customers WHERE studentID={};'''.format(id)  
        cur.execute(s)
        mysql.connection.commit()
        response = {"Result": "Success"}
        ret = app.response_class(
            response=json.dumps(response),
            status=200,
            mimetype='application/json'
        )
        return ret
    else:
        response = {"Result": "Failure"}
        ret = app.response_class(
            response=json.dumps(response),
            status=400,
            mimetype='application/json'
        )
        return ret

@app.route("/")  # Default - Show Data
def read():  # Name of the method
    cur = mysql.connection.cursor()  # create a connection to the SQL instance
    cur.execute('''SELECT * FROM students''')  # execute an SQL statement
    rv = cur.fetchall()  # Retrieve all rows returned by the SQL statement
    Results = []
    for row in rv:  # Format the Output Results and add to return string
        Result = {}
        Result['Name'] = row[0].replace('\n', ' ')
        Result['Email'] = row[1]
        Result['ID'] = row[2]
        Results.append(Result)
    response = {'Results': Results, 'count': len(Results)}
    ret = app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )
    return ret  # Return the data in a string format


@app.route("/update")
def update():
    cur = mysql.connection.cursor()
    id = request.args.get('id')
    name = request.args.get('name')
    email = request.args.get('email')

    if id is not None:
        if name is None and email is None:
            response = {"Result": "Failure",
                        "Reason": "Either email or name needs to be set"}
            ret = app.response_class(
                response=json.dumps(response),
                status=400,
                mimetype='application/json'
            )
            return ret

        setStr = ""
        if name is not None and email is not None:
            setStr = "studentName='{}', email='{}'".format(name, email)
        elif name is not None:
            setStr = "studentName='{}'".format(name)
        elif email is not None:
            setStr = "email='{}'".format(email)

        s = '''UPDATE students SET {} WHERE studentID={};'''.format(setStr, id)

        cur.execute(s)
        mysql.connection.commit()

        response = {"Result": "Success"}
        ret = app.response_class(
            response=json.dumps(response),
            status=200,
            mimetype='application/json'
        )
        return ret
    else:
        response = {"Result": "Failure",
                    "Reason": "Id is not set"}
        ret = app.response_class(
            response=json.dumps(response),
            status=400,
            mimetype='application/json'
        )
        return ret


@app.route("/getGrades")
def getGrades():
    id = request.args.get('id')
    cur = mysql.connection.cursor()  # create a connection to the SQL instance
    cur.execute('''SELECT * FROM students WHERE studentID={}'''.format(id))  # execute an SQL statement
    row = cur.fetchone()  # Retrieve all rows returned by the SQL statement
    Result = {}
    Result['Name'] = row[0].replace('\n', ' ')
    Result['Email'] = row[1]
    Result['ID'] = row[2]
    Grades = [
      {
        "Intro to AI": random.randint(40, 100)
      },
      {
        "Cloud Computing": random.randint(40, 100)
      },
      {
        "Web Development": random.randint(40, 100)
      },
      {
        "Software engineering": random.randint(40, 100)
      },
      {
        "Advance Algorithms": random.randint(40, 100)
      },
      {
        "Maths": random.randint(40, 100)
      }
    ]
    response = {'StudentDetails': Result, 'Grades': Grades}
    ret = app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )
    return ret  # Return the data in a string format


if __name__ == "__main__":
    # sql = open("db.sql", "r")
    # cur = mysql.connection.cursor()
    # cur.execute(sql.read())
    # sql.close()
    app.run(host='0.0.0.0', port='80')  # Run the flask app at port 80
