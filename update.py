#!/usr/bin/python
# -*- coding: utf-8 -*-

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config, view_defaults
from main import Org_name,Team_id,add_a_member_to_team,remove_a_member_to_team,logger


#We only listen to org member added/removed event
@view_defaults(
     renderer="json", request_method="POST"
)

class PayloadView(object):
    """
    View receiving of Github payload. By default, this view it's fired only if
    the request is json and method POST.
    """
 
    def __init__(self, request):
        self.request = request
        # Payload from Github, it's a dict
        self.payload = self.request.json
    
    @view_config(header="X-Github-Event:organization")
    def member_change(self):
        """This method is a continuation of PayloadView process, triggered if
        header HTTP-X-Github-Event type is organization"""
        logger.info(self.payload['action'])
        try:
            if self.payload['action'] == "member_added":
                add_a_member_to_team(self.payload['user']['login'], Org_name, Team_id)
                logger.info(self.payload)
            elif self.payload['action']  == "member_removed":
                remove_a_member_to_team(self.payload['user']['login'], Org_name, Team_id)
                logger.info(self.payload)
        except Exception as e:
            logger.error('Failed change members in %s - %s', Team_id, str(e))
            logger.debug('Failed change members in %s', Team_id, exc_info=True)
        raise SystemExit(1) 

if __name__ == "__main__":
    config = Configurator()
    app = config.make_wsgi_app()
    server = make_server("0.0.0.0", 443, app)
    server.serve_forever()
