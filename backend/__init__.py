from flask import Flask, render_template, jsonify, request
from flask_cors import cross_origin
import sqlite3, re
from sqlite3 import Error
app = Flask(__name__)
# CORS(app)

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

@app.route("/")
@cross_origin()
def hello():
    resp = {"msg": "Hi. Welcome to HSBC. There's scope to increase your transaction limits, wanna proceed?"}
    return jsonify(resp)

@app.route("/messagehandler", methods=['POST'])
@cross_origin()
def messagehandler():
    # print(request.get_json())
    conn = create_connection('/Users/PranayReddy/Desktop/scratchpad/paylimits/backend/limits.db')
    cur = conn.cursor()
    
    cur.execute("SELECT UPPER_LIMIT FROM LIMITS WHERE ACCOUNT_ID=?",('100000004512', ))
    limit = cur.fetchone()[0]
    content = request.get_json()
    message = str(content['msg']['data']['text'])
    print(content['msg']['data']['text'])
    if message == 'yes':
        resp = {"msg": "Thank You. Your limit has been revised to 15,000"}
    elif re.search(".+increase.+", message):
        req_limit = re.findall('\d+',message)
        req_limit = list(map(int, req_limit))
        print(req_limit, limit)
        if req_limit[0] <= limit:
            resp = {"msg": "Okay. Thank You. Your limit has been upgraded"}
            cur.execute("UPDATE LIMITS set PAYMENT_LIMIT=?", (req_limit[0], ))
            conn.commit()
        else:
            resp = {"msg": "Your request has been received, we'll get back to you"}
    else:
        resp = {"msg": "Okay. Thank You."}  
    return jsonify(resp)