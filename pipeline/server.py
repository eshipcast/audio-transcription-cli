import json
import logging

import click
import redis

from flask import Flask, jsonify, request, make_response
from urllib.parse import urlparse

from common import get_config, DEFAULT_CONFIG_FN


app = Flask(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


@app.route('/ping')
def ping():
    return jsonify(status='up')


def insert_file(req_json, params):
    if not params:
        logging.info('Not writing anything to file.')
        return
    logging.info('Writing task results to file.')
    return True


def insert_redis(req_json, params):
    if not params:
        logging.info('Not writing anything to Redis.')
        return
    logging.info('Writing task results to Redis.')
    return True


def insert_mongo(req_json, params):
    if not params:
        logging.info('Not writing anything to MongoDB.')
        return
    logging.info('Writing task results to MongoDB.')
    return True


def listen_post():
    datastores = app.config.get('datastores')
    print(datastores)
    callback_auth_attempt = request.headers.get('scale-callback-auth')
    if not callback_auth_attempt \
        or callback_auth_attempt not in \
            {app.config.get('LIVE_CALLBACK_AUTH_KEY'), app.config.get('TEST_CALLBACK_AUTH_KEY')}:
        return make_response(jsonify(err='Unauthorized'), 401)

    ds_params = lambda ds_type: next(filter(lambda ds: ds.get('type').lower() == ds_type, datastores), None)
    insert_file(request.get_json(), ds_params('file'))
    insert_redis(request.get_json(), ds_params('redis'))
    insert_mongo(request.get_json(), ds_params('mongo'))

    return make_response(jsonify(results='received, thanks'), 200)


def listen_get():
    return make_response(jsonify(err='This endpoint does not support GET.'), 405)


def add_callback_rules(conf):
    """Adds the callback_url rule to the server ('/listen' by default)
    """
    rule = urlparse(conf.get('callback_url', '/listen')).path
    app.add_url_rule(rule,
            view_func=listen_post,
            methods=['POST'])
    app.add_url_rule(rule,
            view_func=listen_get,
            methods=['GET'])
    logging.info("Added rule for callback_url at `{}`".format(rule))


@click.command()
@click.option('--filename', default=DEFAULT_CONFIG_FN)
def run_app(filename):
    config_fn = DEFAULT_CONFIG_FN if not filename else filename
    conf = get_config(config_fn)

    app.config.update(
        LIVE_CALLBACK_AUTH_KEY=conf.get('test_callback_auth_key'),
        TEST_CALLBACK_AUTH_KEY=conf.get('live_callback_auth_key'),
        datastores=conf.get('datastores')
    )
    add_callback_rules(conf)
    app.run()


if __name__ == "__main__":
    run_app()
