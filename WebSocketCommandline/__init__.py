#! /usr/bin/env python

# -*- coding: utf-8 -*-

from autobahn.twisted.choosereactor import install_reactor
from twisted.python import log

from autobahn.twisted.websocket import \
    WebSocketServerFactory, \
    WebSocketClientFactory, \
    WebSocketServerProtocol, \
    WebSocketClientProtocol

import argparse
import threading
import json
import cmd
import logging
import string
import sys
import os
import time

from PyTerminalCommander import Commander, CommandHandler, CommanderPopupLauncher

from datetime import datetime as dt
import datetime

DEFAULT_PORT = 10090

# Reactor will be started by the ServerService.
reactor = install_reactor()

class ClientManager:
    def __init__(self):
        self.clients = []

    def addClient(self, client):
        if client not in self.clients:
            print("registered client {}".format(client.peer))
            self.clients.append(client)

    def removeClient(self, client):
        if client in self.clients:
            print("unregistered client {}".format(client.peer))
            self.clients.remove(client)

    def getAllClients(self):
        return self.clients

# ClientManager is shared among threads.
clientManager = ClientManager()

def parseArguments():
    optParser = argparse.ArgumentParser()
    optParser.add_argument("--port", help="Port to listen on.", type=int, required=False, default=DEFAULT_PORT)
    optParser.add_argument("--verbose", help="Verbose Mode.", action='store_true', default=False)
    optParser.add_argument("--url-root", help="ws://host:port/[url-root].", type=str, required=False, default="")
    return optParser.parse_args(), optParser

class TesterServerFactory(WebSocketServerFactory):

    def __init__(self, url, clientManager):
        WebSocketServerFactory.__init__(self, url)
        self.clientManager = clientManager

    def register(self, client):
        self.clientManager.addClient(client)

    def unregister(self, client):
        self.clientManager.removeClient(client)

class TesterClientFactory(WebSocketClientFactory):
    def __init__(self, *args, **kwargs):
        clientManager = kwargs.pop("clientManager")
        self.clientManager = clientManager
        WebSocketClientFactory.__init__(self, *args, **kwargs)
        
    def register(self, client):
        self.clientManager.addClient(client)

    def unregister(self, client):
        self.clientManager.removeClient(client)

def getClientType(c):
    t = "unknown"
    if isinstance(c, TesterClientProtocol):
        t = "Server"
    elif isinstance(c, TesterServerProtocol):
        t = "Client"
    return t

def handleIncomingMessage(client, payload, isBinary):
    idx = clientManager.getAllClients().index(client)
    clientId = "Unknown"
    if idx != -1:
        c = clientManager.getAllClients()[idx]
        clientId = "id: {0}, type: {1}, peer: {2}".format(idx, getClientType(client), c.peer)

    if isBinary:
        print("Binary message received from({0}) size: {1}".format(cliendId, len(payload)))
    else:
        print("Text message received from({0}):\n\t{1}".format(clientId, payload.decode('utf8')))

class TesterServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        handleIncomingMessage(self, payload, isBinary)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class TesterServerService(threading.Thread):
    def __init__(self, opts, clientManager):
        threading.Thread.__init__(self)
        self.factory = TesterServerFactory("ws://0.0.0.0:{0}/{1}".format(opts.port, opts.url_root), clientManager)
        self.factory.protocol = TesterServerProtocol
        self.clientManager = clientManager
        self.opts = opts

    def run(self):
        reactor.listenTCP(self.opts.port, self.factory)
        print("WebSocket server is listing on: {0}".format("ws://0.0.0.0:{0}/{1}".format(self.opts.port, self.opts.url_root)))
        reactor.run( installSignalHandlers = 0 )


class TesterClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        handleIncomingMessage(self, payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print(wasClean, code, reason)
        self.factory.unregister(self)

class TesterClientService:
    def __init__(self, clientManager, host, port, path):
        self.f = TesterClientFactory("ws://{0}:{1}/{2}".format(host, port, path), clientManager = clientManager, reactor = reactor)
        self.f.protocol = TesterClientProtocol
        self.host = host
        self.port = int(port)
        self.clientManager = clientManager
        reactor.callFromThread(self.reactorSetup)

    def reactorSetup(self):
        reactor.connectTCP(self.host, self.port, self.f)

class CommandManager(CommandHandler):
    def __init__(self, service, clientManager):
        CommandHandler.__init__(self)
        self.__service = service
        self.clientManager = clientManager

    def do_list(self, commander, extra):
        '''
List all connected clients
        '''
        print("ID\tType\tClient")
        allCLients = self.clientManager.getAllClients()
        for i in range(0, len(allCLients)):
            c = allCLients[i]
            t = "unknown"
            if isinstance(c, TesterClientProtocol):
                t = "Server"
            elif isinstance(c, TesterServerProtocol):
                t = "Client"
            print("{0}\t{1}\t{2}".format(i, t, str(c.peer)))

    def do_send(self, commander, extra):
        '''
Send raw text to client
usage: send [dest_id] [text]
        '''
        try:
            dest_id, text = extra.split(" ", 1)
            dest_id = int(dest_id)
            allCLients = self.clientManager.getAllClients()
            if dest_id >= len(allCLients) or dest_id < 0:
                print("Wrong dest_id: {0}".format(dest_id))
                raise Exception()
        except Exception as e:
            print("usage: send [dest_id] [text]")
        else:
            allCLients[dest_id].sendMessage(text.encode('utf8'))

    def do_status(self, commander, extra):
        '''
Show connection status
        '''
        pass

    def do_quit(self, *args):
        '''Exit the program.'''
        return Commander.Exit

    # def emptyline(self):
    #     pass

    def do_connect(self, commander, extra):
        '''
Connect to another WebSocket Server
usage: connect ws://host:port/path
        '''
        try:
            s = extra.split()
            host = s[0]
            port = s[1] 
            path = ""
            if len(s) == 3:
                path = s[2] 
        except Exception:
            print("usage: connect [host] [port] [(OPTIONAL)path]")
        else:
            t = TesterClientService(self.clientManager, host, port, path)

def main():
    args, optparser = parseArguments()

    # TODO: Hook to the cmd out later
    if args.verbose:
        log.startLogging(sys.stdout)

    service = TesterServerService(args, clientManager)
    service.setDaemon(True)
    service.start()

    c = Commander('Websocket Commandline Test Tool(Whisky so awesome!).'
        , cmd_cb = CommandManager(service, clientManager)
        , hook_stdout = True
        , hook_stderr = True
        , show_help_on_start = True
        , show_line_num = False
    )

    c.loop()

if __name__ == '__main__':
    main()