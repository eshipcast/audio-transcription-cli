# tasks directory

Any **tasks** that are POSTed to Scale API by `client.py` will be placed in this directory with the following filename format:

`task_<creation time with format yyyy-mm-ddThh:mm:ss.msecZ>_create.log`

Any **results** that are POSTed to the `callback_url` endpoint by Scale API will be placed in this directory by `server.py`, and optionally, Redis and/or MongoDB (_todo_):

`task_<creation time with format yyyy-mm-ddThh:mm:ss.msecZ>_result.log`

As you can tell we use the **time of creation** as the unique identifier for task logs and _not_ the task ID as Scale API has it.
