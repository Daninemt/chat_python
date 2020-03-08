# Chat_python


This is a simple chat.

### Usage for docker platforms


For server:

```sh
$ docker pull docker.pkg.github.com/daninemt/chat_python/chat_server:1.0
$ docker run --rm -it -p 4333:4333 docker.pkg.github.com/daninemt/chat_python/chat_server:1.0
```

For client:

```sh
$ docker pull docker.pkg.github.com/daninemt/chat_python/chat_client:1.0
$ docker run --rm -it docker.pkg.github.com/daninemt/chat_python/chat_client:1.0
```
When server's ip is requested, be sure to enter docker's ip.

### Usage for terminal platforms


For server:

```sh
$ python server.py
```

For client:

```sh
$ python client.py
```
