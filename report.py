#!/usr/bin/env python3

import urllib.request
import json
import csv
import os

from dotenv import load_dotenv

USER_COLS = ['User', 'Email', 'AdminAccess', 'IsAccountOwner']
FORM_COLS = ['Name', 'Email', 'Description', 'IsPublic', 'DateCreated', 'DateUpdated',
             'EntryCount', 'FirstEntry', 'LastEntry']

# Add any environment variables from .env
load_dotenv('.env')

# Get environment variables
env = {}
for key in ('base_url', 'api_key'):
    env[key] = os.environ.get(key)
    if env[key] is None:
        raise RuntimeError(f'Must provide environment variable: {key}')

# Setup the REST API connection information

password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
password_manager.add_password(None, env['base_url'], env['api_key'], '')

handler = urllib.request.HTTPBasicAuthHandler(password_manager)
opener = urllib.request.build_opener(handler)
urllib.request.install_opener(opener)


def get_users():
    ''' Get the list of users. '''

    response = urllib.request.urlopen(env['base_url']+'users.json')
    data = json.load(response)

    if 'Users' in data:
        users = data['Users']

        with open('users.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(USER_COLS)

            for user in users:
                row = []
                for col in USER_COLS:
                    row.append(user[col])
                print(row)
                writer.writerow(row)


def add_form_entries(form):
    ''' Add form entry information to the form data. '''

    hash = form['Hash']

    form['EntryCount'] = 0
    form['FirstEntry'] = 'n/a'
    form['LastEntry'] = 'n/a'

    # Get EntryCount
    response = urllib.request.urlopen(env['base_url'] + f'forms/{hash}/entries/count.json')
    data = json.load(response)

    if 'EntryCount' in data:
        form['EntryCount'] = data['EntryCount']

    # Get FirstEntry
    response = urllib.request.urlopen(
        env['base_url'] + f'forms/{hash}/entries.json?pageStart=0&pageSize=1&sort=EntryId&sortDirection=ASC'
    )
    data = json.load(response)
    # print(json.dumps(data, indent=4, sort_keys=True))

    if 'Entries' in data:
        entries = data['Entries']
        if len(entries) == 1:
            form['FirstEntry'] = entries[0]['DateCreated']

    # Get LastEntry
    response = urllib.request.urlopen(
        env['base_url'] + f'forms/{hash}/entries.json?pageStart=0&pageSize=1&sort=EntryId&sortDirection=DESC'
    )
    data = json.load(response)
    # print(json.dumps(data, indent=4, sort_keys=True))

    if 'Entries' in data:
        entries = data['Entries']
        if len(entries) == 1:
            form['LastEntry'] = entries[0]['DateCreated']


def get_forms():
    ''' Get the list of forms. '''

    response = urllib.request.urlopen(env['base_url']+'forms.json')
    data = json.load(response)

    if 'Forms' in data:
        forms = data['Forms']

        with open('forms.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(FORM_COLS)

            for form in forms:
                row = []

                add_form_entries(form)

                for col in FORM_COLS:
                    row.append(form[col])
                print(row)
                writer.writerow(row)


get_users()


get_forms()
