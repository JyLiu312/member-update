#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import logging
from github import Github
import argparse
from requests import ConnectionError
from logging.handlers import RotatingFileHandler

#credentials
Org_name = 'moodysanalytics' #'moodyssharedservices'
Team_id = 3027772    #3139517(test repo)  # github employees team id
Token = 'd4e9d219eaac1ae76e7a3eac00a585144d363c07' # github access token

g = Github(Token)

# Log 
logger = logging.getLogger(__name__)
file_handler = RotatingFileHandler('./tmp/log', maxBytes=2000,backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

logger.info('Starting Updater')


# Get Org

def get_org(Org_name):
    try:
        my_org = g.get_organization(Org_name)
        logger.info(my_org)
        return my_org
    except ConnectionError as e:
        logger.error('Failed to connect org %s', e)
        raise SystemExit(1)
    except Exception as e:
        logger.error('Failed to open %s - %s', Org_name, str(e))
        logger.debug('Failed to open org', exc_info=True)
        raise SystemExit(1)


# Get all members in the org

def get_org_members(org):
    try:
        org_members = org.get_members()
        return org_members
    except Exception as e:
        logger.error('Failed get all members in %s - %s', org,
                     str(e))
        logger.debug('Failed get all members in %s', org, exc_info=True)
        raise SystemExit(1)


# Get all members in the team and return a list

def get_team_members(org, Team_id):
    try:
        team_members = org.get_team(Team_id).get_members()
        team_logins = [t.login for t in team_members]
        logger.info(team_logins)
        return team_logins
    except Exception as e:
        logger.error('Failed get members in %s - %s', Team_id, str(e))
        logger.debug('Failed get members in %s', Team_id, exc_info=True)

        raise SystemExit(1)


# Add all team logins to a list

# Set difference between two lists, if not included - add member to the group.

def add_members(
    org_members,
    team_members,
    Team_id,
    org,
    ):
    try:
        for i in org_members:
            if i.login not in team_members:
                # Here's the trick, you should pass the user object, not the username
                user = g.get_user(i.login)
                org.get_team(Team_id).add_to_members(user)
                logger.info('Member %s has been added to the team %s',i.login, Team_id)
    except Exception as e:
        logger.error('Failed add member %s to the %s - %s', i.login,
                     Team_id, str(e))
        logger.debug('Failed add member %s to the %s', i.login, Team_id, exc_info=True)
        raise SystemExit(1)

def add_a_member_to_team(login, Org_name, Team_id):
    org = get_org(Org_name)
    try:
        if org.get_team(Team_id).has_in_members(login):
            user = g.get_user(login)
            org.get_team(Team_id).add_to_members(user)
    except Exception as e:
        logger.error('Failed add member %s to the %s - %s', login,
                     Team_id, str(e))
        logger.debug('Failed add member %s to the %s', login,
                     Team_id, exc_info=True)
        raise SystemExit(1)

def remove_a_member_to_team(login, Org_name, Team_id):
    org = get_org(Org_name)
    try:
        org.get_team(Team_id).remove_from_members(login)    
    except Exception as e:
        logger.error('Failed remove member %s to the %s - %s', login,
                     Team_id, str(e))
        logger.debug('Failed remove member %s to the %s', login,
                     Team_id, exc_info=True)
        raise SystemExit(1)

org = get_org(Org_name)
org_members = get_org_members(org)
team_members = get_team_members(org, Team_id)
add_members(org_members, team_members, Team_id, org)

logger.info('Updater finished running')

			