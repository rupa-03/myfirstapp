import re
from flask import Flask, jsonify
from collections import defaultdict

app = Flask(__name__)

LOG_FILE_PATH = "hn_logs.tsv"

def parse_log_file():
    data = defaultdict(set)
    with open(LOG_FILE_PATH, 'r') as file:
        for line in file:
            timestamp, query = line.strip().split('\t')
            data[timestamp].add(query)
    return data

year_regex = re.compile(r'^\d{4}$')
month_regex = re.compile(r'^\d{4}-\d{2}$')
day_regex = re.compile(r'^\d{4}-\d{2}-\d{2}$')

def count_queries(date_prefix):
    log_data = parse_log_file()
    final = set()
    
    if year_regex.match(date_prefix):
        for timestamp in log_data:
            if timestamp.startswith(date_prefix):
                final.update(log_data[timestamp])
    elif month_regex.match(date_prefix):
        for timestamp in log_data:
            if timestamp.startswith(date_prefix):
                final.update(log_data[timestamp])
    elif day_regex.match(date_prefix):
        for timestamp in log_data:
            if timestamp.startswith(date_prefix):
                final.update(log_data[timestamp])
    else:
        for timestamp in log_data:
            if timestamp[:len(date_prefix)] == date_prefix:  # Check if the prefix matches the timestamp
                final.update(log_data[timestamp])
                
    return len(final)

@app.route('/1/queries/count/<date_prefix>')
def get_count(date_prefix):
    count = count_queries(date_prefix)
    return jsonify({"count": count})

if __name__ == '__main__':
    app.run(debug=True)