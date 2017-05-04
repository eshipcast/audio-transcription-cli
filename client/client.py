import sys
import json

import click
import scaleapi

from marshmallow import Schema, fields


DEFAULT_CONFIG_FN = '../task.json'


class ConfigSchema(Schema):
    test_api_key = fields.String(required=True)
    live_api_key = fields.String(required=True)
    callback_url = fields.String(required=True)
    attachment_type = fields.String(required=True)
    attachment = fields.String(required=True)
    verbatim = fields.Boolean(required=True)
    test_callback_auth_key = fields.String(required=True)
    live_callback_auth_key = fields.String(required=True)


def get_config(config_fn):
    with open(config_fn, encoding='utf-8') as config_file:
        try:
            config = json.loads(config_file.read())
        except json.decoder.JSONDecodeError:
            sys.exit('\nMalformed JSON.\n\n(exited with error code 1)\n')
        schema = ConfigSchema(strict=False)

        valid_conf, errors = schema.load(config)
        if errors: sys.exit('\nMissing or invalid config file parameters (see below):\
                \n{}\n\n(exited with error code 1)\n'.format(str(errors)))
        return valid_conf


@click.command()
@click.option('--filename', default=DEFAULT_CONFIG_FN)
def send_task(filename):
    config_fn = DEFAULT_CONFIG_FN if not filename else filename
    conf = get_config(config_fn)
    client = scaleapi.ScaleClient(conf['test_api_key'])
    try:
        ret_obj = client.create_audiotranscription_task(
                callback_url = conf.get('callback_url'),
                attachment_type = conf.get('attachment_type'),
                attachment = conf.get('attachment'),
                verbatim = conf.get('verbatim')
                )
    except scaleapi.ScaleException as e:
        sys.exit('\nStatus Code {}: {}\n\n(exited with error code 1)\n'.format(e.code, str(e)))
    nod = lambda x: "Yes." if True else "No."
    fmt_strs = (ret_obj.task_id,
            ret_obj.created_at,
            nod(ret_obj.is_test),
            ret_obj.callback_url,
            json.dumps(ret_obj.params, indent=4))
    message = "Task (task_id={}) created at {}.\nWas this a test? {}\n\
Make sure this URL is listening for POST requests: {}\n\
Here are the parameters you used:\n{}".format(*fmt_strs)
    create_log_filename = 'tasks/task_{}_create.log'.format(ret_obj.created_at)
    with open(create_log_filename, 'w') as create_log_file:
        create_log_file.write(message)
    print("\n{}\n\n(A file containing this message has been written to `{}`.)\n"\
            .format(message, create_log_filename))


if __name__ == "__main__":
    send_task()
