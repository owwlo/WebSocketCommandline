# WebSocketCommandline

WebSocketCommandline is a command line tool to easily test the connectivity of WebSocket client/server in shell with Python.

## Compatibility

Tested with:
* Python 3.4
* Python 2.7

## Installation

### Option A
pip it!
```sh
&> pip install -e git+https://github.com/owwlo/WebSocketCommandline.git@master#egg=websocket_tester
```
### Option B
No special installation needed for now. Download the file and run it with python interpreter.
```sh
&> python websocket_tester.py
```

Dependencies can be installed by:
```sh
&> sudo pip install -r requirements.txt
```

## Usage

websocket_tester.py will automatically start a WebSocket server at startup. To change the default server port:

```sh
&> python websocket_tester.py --port 12345
```

In addition to the port, you can also change the WebSocket URI path for the server:

```sh
&> python websocket_tester.py --port 12345 --url-root iamawebsocket
```
> This will make the server listen on ws://localhost:12345/iamawebsocket

websocket_tester.py has both builtin Server and Client support, in order to connect to a server:

```sh
# After starting the tool.
# Assumed the tool starts with --port 12345 --url-root iamawebsocket
>> connect 127.0.0.1 12345 iamawebsocket
```

List all connected Clients/Servers

```sh
# After starting the tool.
>> list
```

Send text message to the Client/Server

```sh
# After starting the tool.
# The client_id can be found in 'list' command
>> send [client_id] [text you want to send]
```

# TODOs

* Better log/output handling
* ~~Can be installed by pip~~
* ~~Tested against python2~~
* ...

# License
The MIT License (MIT)

Copyright (c) 2016 owwlo

Licensed under the MIT License. See the top-level file LICENSE.

那时候我们说话都喜欢用终于，就像终于放假了，终于毕业了，终于离开这里了，终于过年了，仿佛任何的告别都像一种解脱。最后我们才发现，那些自以为是的如释重负，才是让人想念的东西。没什么会等你。就像所有曲终人散和分道扬镳，到最后可惜的不是离散，而是没有好好的和那些道别。——转自《一言》
