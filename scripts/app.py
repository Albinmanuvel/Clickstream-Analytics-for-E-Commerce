from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from elasticsearch import Elasticsearch

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# PostgreSQL Connection
pg_conn = psycopg2.connect(
    dbname="clickstream_db",
    user="your_username",
    password="your_password",
    host="localhost",
    port="5432"
)
pg_cursor = pg_conn.cursor()

# Elasticsearch Connection
es = Elasticsearch("http://localhost:9200")

# Route to get session-based analytics from PostgreSQL
@app.route('/sessions', methods=['GET'])
def get_sessions():
    pg_cursor.execute("SELECT * FROM clickstream_sessions ORDER BY total_events DESC LIMIT 10;")
    sessions = pg_cursor.fetchall()
    return jsonify({"sessions": [{"session_id": s[0], "total_events": s[1]} for s in sessions]})

# Route to get real-time analytics from Elasticsearch
@app.route('/real-time-events', methods=['GET'])
def get_real_time_events():
    query = {
        "size": 10,
        "query": {"match_all": {}},
        "sort": [{"timestamp": {"order": "desc"}}]
    }
    response = es.search(index="clickstream_data", body=query)
    events = [{"user_id": hit["_source"]["user_id"], "event_type": hit["_source"]["event_type"], "timestamp": hit["_source"]["timestamp"]}
              for hit in response["hits"]["hits"]]
    return jsonify({"real_time_events": events})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
