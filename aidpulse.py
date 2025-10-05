from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql, pool
app = Flask(__name__)
# Database Configuration
HOST = 'localhost'
DATABASE = 'postgres'
DB_USERNAME = 'postgres'
DB_PASSWORD = 'chaitanyadb'
# Create a connection pool for better performance
connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 10, host=HOST, database=DATABASE, user=DB_USERNAME, password=DB_PASSWORD
)
# Get a database connection from the pool
def get_db_connection():
    return connection_pool.getconn()
# Release connection back to the pool
def release_db_connection(conn):
    connection_pool.putconn(conn)
# Initialize Tables
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create helpers table
    cursor.execute("""CREATE TABLE IF NOT EXISTS helpers (helper_id SERIAL PRIMARY KEY, helper_name VARCHAR UNIQUE NOT NULL, type VARCHAR NOT NULL, location VARCHAR NOT NULL);""")
    # Create aidrequests table
    cursor.execute("""CREATE TABLE IF NOT EXISTS aidrequests (aidrequest_id SERIAL PRIMARY KEY, requester_name VARCHAR NOT NULL, aid_type VARCHAR NOT NULL, location VARCHAR NOT NULL);""")
    conn.commit()
    cursor.close()
    release_db_connection(conn)
create_tables()
# Add a new helper
@app.route("/add-helpers", methods=['POST'])
def create_helpers():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        data = request.get_json()
        helper_name = data.get('helper_name')
        helper_type = data.get('type')
        location = data.get('location')
        if not all([helper_name, helper_type, location]):
            return jsonify({"error": "All fields (helper_name, type, location) are required"}), 400
        query = "INSERT INTO helpers (helper_name, type, location) VALUES (%s, %s, %s);"
        cursor.execute(query, (helper_name, helper_type, location))
        conn.commit()
        return jsonify({"message": "Helper registered successfully"}), 201
    except psycopg2.Error as e:
        return jsonify({"error": f"Database error: {e.pgcode} - {e.pgerror}"}), 500
    finally:
        cursor.close()
        release_db_connection(conn)
# Get all helpers
@app.route("/get-helpers", methods=['GET'])
def get_helpers():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM helpers;")
        helpers_list = cursor.fetchall()
        if helpers_list:
            response_list = [
                {
                    "helper_id": helper[0],
                    "helper_name": helper[1],
                    "type": helper[2],
                    "location": helper[3]
                }
                for helper in helpers_list
            ]
            return jsonify({"helpers_list": response_list}), 200
        return jsonify({"message": "No helpers found"}), 404
    finally:
        cursor.close()
        release_db_connection(conn)
# Get helpers by location
@app.route("/get-helpersbylocation/<string:location>", methods=['GET'])
def get_helpers_by_location(location):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM helpers WHERE location = %s;", (location,))
        helpers_list = cursor.fetchall()
        if helpers_list:
            response_list = [
                {
                    "helper_id": helper[0],
                    "helper_name": helper[1],
                    "type": helper[2],
                    "location": helper[3]
                }
                for helper in helpers_list
            ]
            return jsonify({"helpers_list": response_list}), 200
        return jsonify({"message": "No helpers found in this location"}), 404
    finally:
        cursor.close()
        release_db_connection(conn)
@app.route("/add-aidrequests", methods=['POST'])
def create_aidrequests():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        data = request.get_json()
        requester_name = data.get('requester_name')
        aid_type = data.get('aid_type')
        location = data.get('location')
        if not all([requester_name, aid_type, location]):
            return jsonify({"error": "All fields (requester_name, aid_type, location) are required"}), 400
        query = "INSERT INTO aidrequests (requester_name, aid_type, location) VALUES (%s, %s, %s);"
        cursor.execute(query, (requester_name, aid_type, location))
        conn.commit()
        return jsonify({"message": "Aid request registered successfully"}), 201
    except psycopg2.Error as e:
        return jsonify({"error": f"Database error: {e.pgcode} - {e.pgerror}"}), 500
    finally:
        cursor.close()
        release_db_connection(conn)
#update requests
@app.route("/update-helpers/<int:helper_id>", methods=['PUT'])
def update_helpers(helper_id):
    conn = get_db_connection()  
    cursor = conn.cursor()
    helper_name = request.json.get('helper_name')
    helper_type = request.json.get('type')
    location = request.json.get('location')
    if not all([helper_name, helper_type, location]):
        return jsonify({"error": "All fields (helper_name, type, location) are required"}), 400
    check_query = "SELECT * FROM helpers WHERE helper_id = %s;"
    cursor.execute(check_query, (helper_id,))
    task = cursor.fetchone()
    if task:
        update_query = "UPDATE helpers SET helper_name = %s, type = %s, location = %s WHERE helper_id = %s;"
        cursor.execute(update_query, (helper_name, helper_type, location, helper_id))
        conn.commit()
        cursor.close()
        release_db_connection(conn)  
        return jsonify({"message": "Helper data updated successfully"}), 200
    else:
        cursor.close()
        release_db_connection(conn)
        return jsonify({"error": "Helper not found! Try again"}), 404
# get aid requests
@app.route("/get-aidrequests", methods=['GET'])
def get_aidrequests():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM aidrequests;")
        aidrequests_list = cursor.fetchall()
        if aidrequests_list:
            response_list = [
                {
                    "aidrequest_id": aidrequest[0],
                    "requester_name": aidrequest[1],
                    "aid_type": aidrequest[2],
                    "location": aidrequest[3]
                }
                for aidrequest in aidrequests_list
            ]
            return jsonify({"aidrequests_list": response_list}), 200
        return jsonify({"message": "No aid requests found"}), 404
    finally:
        cursor.close()
        release_db_connection(conn)
# update aid requests
@app.route("/update-aidrequests/<int:aidrequest_id>", methods=['PUT'])
def update_aidrequests(aidrequest_id):
    conn = get_db_connection()  
    cursor = conn.cursor()
    requester_name = request.json.get('requester_name')
    aid_type = request.json.get('aid_type')
    location = request.json.get('location')
    if not all([requester_name, aid_type, location]):
        return jsonify({"error": "All fields (requester_name, aid_type, location) are required"}), 400
    check_query = "SELECT * FROM aidrequests WHERE aidrequest_id = %s;"
    cursor.execute(check_query, (aidrequest_id,))
    task = cursor.fetchone()
    if task:
        update_query = "UPDATE aidrequests SET requester_name = %s, aid_type = %s, location = %s WHERE aidrequest_id = %s;"
        cursor.execute(update_query, (requester_name, aid_type, location, aidrequest_id))
        conn.commit()
        cursor.close()
        release_db_connection(conn)  
        return jsonify({"message": "aidrequests data updated successfully"}), 200
    else:
        cursor.close()
        release_db_connection(conn)
        return jsonify({"error": "aidrequests not found! Try again"}), 404
#retrive aid requests through aid type
@app.route("/get-aidrequestbyaidtype/<string:aid_type>", methods=['GET'])
def get_aidrequest_by_location(aid_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM aidrequests WHERE aid_type = %s;", (aid_type,))
        aidrequests_list = cursor.fetchall()
        if aidrequests_list:
            response_list = [
                {
                    "aidrequest_id": helper[0],
                    "requester_name": helper[1],
                    "aid_type": helper[2],
                    "location": helper[3]
                }
                for helper in aidrequests_list
            ]
            return jsonify({"aidrequests_list": response_list}), 200
        return jsonify({"message": "No aidrequests found in this aidtype"}), 404
    finally:
        cursor.close()
        release_db_connection(conn)
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)
