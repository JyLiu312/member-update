#!/usr/bin/python
# -*- coding: utf-8 -*-

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config, view_defaults
from main import Org_name,Team_id,add_a_member_to_team,remove_a_member_to_team,logger


ENDPOINT = "https://webhook.site/6e5b6e21-c460-4314-9110-bdfc47d16939"

#We only listen to org member added/removed event
@view_defaults(
    route_name=ENDPOINT, renderer="json", request_method="POST"
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
        try:
            if self.payload['action'] == "member_added":
                add_a_member_to_team(self.payload['user']['login'], Org_name, Team_id)
            elif self.payload['action']  == "member_removed":
                remove_a_member_to_team(self.payload['user']['login'], Org_name, Team_id)
        except Exception as e:
            logger.error('Failed change members in %s - %s', Team_id, str(e))
            logger.debug('Failed change members in %s', Team_id, exc_info=True)
        raise SystemExit(1) 
