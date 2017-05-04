import json

from marshmallow import Schema, fields


DEFAULT_CONFIG_FN = './task.json'
ALLOWED_DS_TYPES = {'file', 'redis', 'mongodb'}


class ConfigSchema(Schema):
    # TODO: DatastoreSchema
    test_api_key = fields.String(required=True)
    live_api_key = fields.String(required=True)
    callback_url = fields.String(required=True)
    attachment_type = fields.String(required=True)
    attachment = fields.String(required=True)
    verbatim = fields.Boolean(required=True)
    test_callback_auth_key = fields.String(required=True)
    live_callback_auth_key = fields.String(required=True)
    datastores = fields.List(fields.Dict)


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


def get_log_filepath(conf):
    """Assuming a valid conf containing the `datastores` key, retrieves the
    'location' key of an object in the `datastores` list whose `type` is "file".

    Default is `./tasks/`.
    """
    return next(
        filter(
            lambda ds: ds.get('type').lower() == 'file',
            conf.get('datastores')
            ),
        {'location': './tasks/'}
        ).get('location')


if __name__ == "__main__":
    pass
