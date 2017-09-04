# WebSocketCommandline

WebSocketCommandline is a command line tool to easily test the connectivity of WebSocket client/server in shell with Python.

## Compatibility

Tested with:
* Python 3.5.2
* Python 2.7.12

## Installation

pip it!

```sh
&> pip install WebSocketCommandline
```

## Usage

### Try it!

```sh
&> websocket_tester
```

### More Options

websocket_tester will automatically start a WebSocket server at startup. To change the default server port:

```sh
&> websocket_tester --port 12345
```

In addition to the port, you can also change the WebSocket URI path for the server:

```sh
&> websocket_tester --port 12345 --url-root iamawebsocket
```
> This will make the server listen on ws://localhost:12345/iamawebsocket

websocket_tester has both builtin Server and Client support, in order to connect to a server:

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