#!/usr/bin/python

#Custom Action Handler for BOT Server endpoint connectivity.
#Copyright (c) 2017, Choiceworx.

import json
import logging
import re
import base64
import sys

import requests
from docopt import docopt


class EmaActionHandler():
    """Represents an action handler that routes actions through an EMA server """

    def __init__(self, node_id, mesh_user, token):
        self.node_id = node_id
        self.mesh_user = mesh_user
        self.token = token


    def execute(self, command):
        """ Execute a command using the EMA API """
        logger = logging.getLogger("root")
        """ This is used to perform powershell encoding. TODO: segregate into function later""" 
        new_command = ""
        powershell_command = ""

        a=u'(\xef|\xbb|\xbf)'
        a=a.encode('utf-8')
        n = re.compile(a)

        for char in (n.sub("", command)):
            new_command += char + ("\x00")
        powershell_command = new_command.encode('utf-8')

        powershell_command = base64.b64encode(powershell_command)

        powershell_command = "PowerShell -EncodedCommand " + powershell_command

        post_url = "http://10.6.0.100:8081/process"

        post_data = {"nodeid" : self.node_id, "command" : powershell_command, "meshuser" : self.mesh_user,
                     "token" : self.token}

        logger.info(post_url)
        logger.info(post_data)

        response = requests.post(post_url, headers={u'content-type': u'application/json'},
                                 data=json.dumps(post_data))

        logger.info(response)

        response_body = json.loads(response.text)

        if response_body['stdout']:
            print(response_body['stdout'].encode('utf-8'))

        if response_body['stderr']:
           sys.stderr.write(response_body['stderr'].encode('utf-8'))

        sys.exit(response_body['exitcode'])

if __name__ == "__main__":
    usage = """Usage: {programName} <nodeId> <meshuser> <token> <command>
    
    Options:

    """.format(programName='emaactionhandler.py')

    args = docopt(usage)
    actionHandler = EmaActionHandler(args['<nodeId>'], args['<meshuser>'], args['<token>'])
    actionHandler.execute(args['<command>'])
        
        
