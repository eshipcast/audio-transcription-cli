[work-in-progress, don't use yet...]

# audio-transcription-cli [![Build Status](https://travis-ci.org/eshipcast/audio-transcription-cli.svg?branch=master)](https://travis-ci.org/eshipcast/audio-transcription-cli)

[Scale API](https://www.scaleapi.com) wraps manual tasks to be performed by real humans, such as image labeling, data collection, and audio transcription, around a developer-friendly API. I first heard about them on an episode of [Software Engineering Daily](https://softwareengineeringdaily.com/2016/12/16/scale-api-with-lucy-guo-and-alexandr-wang/). They are similar to Amazon Mechanical Turk but with a superior developer experience and reputation system for their workers, whom they have dubbed "scalers".

When making requests, they require a _callback url_, which is an endpoint you provide for them to POST the results (type:`application/json`) of a task to. Your endpoint is then required to respond to their POST request with a 2xx status code in order to set the task's `callback_succeeded` parameter as `True`. This seems mainly to confirm that you actually got (and hopefully, stored) the results of the task (actual human work plus your money did go into it, after all). And if they POST it and don't get a 2xx response from the server endpoint you specified, they'll retry it up to 20 times for 24 hours.

## Structure

The root directory contains `task_example.json`, which contains sample task and client/callback configuration parameters. If you don't want to change the default config file path, then once cloned, rename `task_example.json` to `task.json` and replace its values accordingly. It's in the root directory because it's used by both the client CLI and callback server.

The `server` directory contains a Flask application that will be listening for a POST request and will return a response.

The `client` directory contains the CLI program that the user can use to POST transcription tasks to Scale API.

The `client/tasks` directory contains logs for task creation and result events.

The `tests` directory contains tests for both the client and server applications.

## Usage

You need something to serve the callback URL. Assuming you're on a machine or planning to put the server code on a PaaS that will stay up for Scale API to POST back to, and that you're using Python 3 (ideally in a virtual environment):

```
pip install -r requirements.txt
```

### Make sure the callback server is deployed and up

Task and client/callback usage parameters are in `task.json`.

If I'm not using a PaaS like Heroku, such as a clean Linux VPS, then I generally follow these instructions to serve a Flask application:

[How To Serve Flask Applications with Gunicorn and Nginx on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-16-04) (DigitalOcean)

Once set up, you can run the tests to make sure the route is being served, or you can do:

```
$ curl <CALLBACK_URL_ROOT>/ping
```

from which you should get

```
{
  "status": "up"
}
```

### Make sure `task.json` or your configuration file is correct

...and run the client:

```
python client.py --filename <path/to/config/file>
```

When the `--filename` option is omitted, the default configuration path relative to the location of `client.py` is `../task.json`.

Once this succeeds, you should see creation logs in the `client/tasks` directory. That has a short README on the output file format. And if the callback server was deployed correctly, the result logs should appear there, too.

## Testing

Run `pytest .` from the root directory of this project. (_todo_)

## Features

(_todo_)

## Disclaimer

I am not affiliated with Scale API and make no promises that this code will stay up to date with the API forever. This code was written as part of the podcast deployment pipeline for [eshipcast.com](http://eshipcast.com/) (check it out 🎙).
