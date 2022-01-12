from flask import Flask, render_template, request, send_file
import pandas as pd
import json
import requests

# needs to be accessed at localhost:8080
app = Flask(__name__)

# we will use a pandas dataframe to store our data
df = pd.DataFrame(columns=['sensor', 'timestamp', 'value'])


# if we do localhost:8080... where ... can be anything but for the listed routes, it will go to this page by default.
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    temp = df.to_json()
    return render_template("index.html", content=path, jsonfile=json.dumps(temp))


# accepts JSON documents in the request body, add the data
@app.route('/data', methods=['POST'])
def post_data():
    # [{"sensor": <str: sensor_id>, "timestamp": <str: iso 8601 timestamp>, "value": <float>}, ...]
    content = request.get_json()
    global df
    df = df.append(content, ignore_index=True, sort=True)
    print(df)
    temp = df.to_json()
    return render_template('index.html', content='/data', jsonfile=json.dumps(temp))


# return a JSON document with thr form {"last_measurement": <str: iso 8601 timestamp>, "count": <int>, "avg": <float>}
@app.route('/statistics/<path:path>', methods=['GET'])
def get_statistics(path):
    # last_measurement is the timestamp of the last measurement posted to /data (so the bottom row)
    # count is the total number of measurements received (so the length of the dataframe)
    # avg is the average of the values
    # by default, it is this (no sensor case)
    data = {"last_measurement": "null", "count": 0, "avg": 0}
    # if there is data and the sensor name is in the data, then send the stats
    if len(df.index) != 0:
        # create lists of df columns
        sensor_list = df['sensor'].tolist()
        value_list = df['value'].tolist()
        indexes = df.index.values.tolist()
        total = 0
        tot_count = 0
        if path in sensor_list:
            for i in range(len(sensor_list)):
                if sensor_list[i] == path:
                    total += float(value_list[i])
                    tot_count += 1
            data = {"last_measurement": df['timestamp'].iloc[-1], "count": len(df.index), "avg": float(total/tot_count)}

    json_data = json.dumps(data)
    print(data)

    # create json file then send it
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    return send_file('data.json')


# clear any statistics for the sensor with the given ID
@app.route('/statistics/<path:path>', methods=['DELETE'])
def delete_statistics(path):
    global df
    # make the sensor column into a list since it is currently a series with object type
    temp = df['sensor'].tolist()
    indexes = df.index.values.tolist()

    # if the name exists in the dataframe, then remove row with the sensor name
    if path in temp:
        df = df.drop(indexes[temp.index(path)])
        print('removed')

    # response should not include body so send 204
    return '', 204


# should return 204 response with no body if the server is ready to receive request or 400 response otherwise
@app.route('/healthz')
def get_healthz():
    # sample response to the default page
    response = requests.get('http://localhost:8080')
    # if the response code is 200 (it went through) then the server is ready
    if response.status_code == 200:
        return '', 204
    # otherwise, return error response and message
    else:
        return 'The server is not ready to receive requests', 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)




