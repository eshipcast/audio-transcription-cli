import json
import logging

from flask import Flask, jsonify, request, make_response
from urllib.parse import urlparse


app = Flask(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


@app.route('/ping')
def ping():
    return jsonify(status='up')


def listen_get():
    return make_response(jsonify(err='This endpoint does not support GET.'), 405)


def listen_post(datastores):
    for datastore in datastores:
        pass
        # insert
    return request.data


def add_callback_rules(config_fn='../task.json', rule='/collect'):
    with open(config_fn, encoding='utf-8') as config_file:
        config = json.loads(config_file.read())
        rule = urlparse(config.get('callback_url')).path
        logging.info("Added rule for callback_url at `{}`".format(rule))
        app.add_url_rule(rule,
                view_func=listen_post,
                methods=('POST'))
        app.add_url_rule(rule,
                view_func=listen_get,
                methods=('GET'))


if __name__ == "__main__":
    add_callback_rules()
    app.run()
