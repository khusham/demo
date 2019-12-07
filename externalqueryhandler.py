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


class ExternalQueryHandler():
    """Represents an action handler that routes actions through an external data source """

    def __init__(self, QueryType, Parameters, MachineID, BotNodeId, OrganizationId, ServiceUrl):
        self.QueryType = QueryType
        self.Parameters= Parameters
        self.MachineID = MachineID
        self.BotNodeId = BotNodeId
        self.OrganizationId = OrganizationId
        self.ServiceUrl=ServiceUrl


    def execute(self):
        """ Execute a query using the ElasticSearch"""
        logger = logging.getLogger("root")
        
        
        size=len(self.MachineID)
        #newMachineId= self.MachineID[size-24:] 
        
        #print(newMachineId)
        
        if "machine" in self.QueryType:
          hiroId_split = self.MachineID.split(":")
          get_url = "http://%s/%s/%s/%s" % (self.ServiceUrl, self.QueryType, self.Parameters, hiroId_split[3])
        
        if "organization" in self.QueryType:
          get_url = "http://%s/%s/%s/%s" % (self.ServiceUrl, self.QueryType, self.Parameters, self.OrganizationId)
        
        #print (get_url)
        
        data={}
          
        #get_url = "http://localhost:8080/machine_agg_statistics/processes/now-90d/columns.resident_size/5a6ca4e021f1ea606cc24a09" % (ServiceUrl, QueryType, Parameters, MachineID)
        #get_url = "http://localhost:8080/organization_agg_statistics/processes/now-90d/columns.resident_size/5a6ca4e021f1ea606cc24a09" % (ServiceUrl, QueryType, Parameters, OrganizationId)

        # call get service with headers and params
        response = requests.get(get_url,headers = {"Accept": "application/json"}, data = data)

        logger.info(response)
        
        

        logger.info(get_url)

        response_body = json.loads(response.text)

        if response.status_code == 200:
            print(response.text)
            sys.exit(0)

        if response.status_code != 200:
           errormessage = "Error occurred. Status: %s . Message: %s" % (response.status_code,response.text)
           sys.stderr.write(response.text.encode('utf-8'))
           sys.exit(response_body['exitcode'])

if __name__ == "__main__":
    usage = """Usage: {programName} <QueryType> <Parameters> <MachineID> <BotNodeId> <OrganizationId> <ServiceUrl>
    
    Options:

    """.format(programName='externalqueryhandler.py')

    args = docopt(usage)
    actionHandler = ExternalQueryHandler(args['<QueryType>'], args['<Parameters>'], args['<MachineID>'], args['<BotNodeId>'], args['<OrganizationId>'], args['<ServiceUrl>'])
    actionHandler.execute()
        
        


