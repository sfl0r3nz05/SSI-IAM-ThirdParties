from flask import *
import json, time

app = flask(__name__)

@app.route('/',methods_['GET'])
def home_page()
    data_set = {'Succes loading page': time.time()}
    json_dump = json.dumps(data_set)
    return json_dump

@app.route('/user/', methods=['GET'])
def request_page()
    user_query = str(request.arg.get('user'))
    data_set = {'Succes loading page': time.time()}
    json_dump = json.dumps(data_set)
    return json_dump

if __name__ == '__main__':
    app.run(debug=True)