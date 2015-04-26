from django.shortcuts import render

import requests
import datetime


## .env  -  this needs to live in settings; having trouble importing it from settings
import os
assert 'idt_user' in os.environ, 'Set idt_user in your .env file!'
assert 'idt_token' in os.environ, 'Set idt_token in your .env file!'
assert 'idt_team' in os.environ, 'Set idt_team in your .env file!'
idt_user = os.environ['idt_user']
idt_token = os.environ['idt_token']
idt_team = os.environ['idt_team']


## configuration
user = idt_user
token = idt_token
team = idt_team
idt_url = "https://idonethis.com"
api_dones_url = "%s/api/v0.1/dones/?owner=%s&team=%s&page_size=100" % (idt_url, user, team)


## default status view
def index(request):

    ## helper functions
    def get_json_data(url):
        """
        fetch dones from the iDoneThis api, return list of dones from the json response
        """
        headers = {'content-type': 'application/json', 'authorization': 'token %s' % (token)}
        r = requests.get(url, headers=headers)
        data = r.json()
        dones = data['results']
        return dones

    def fix_rel_url(dones):
        """
        replace relative urls in markedup_text with absolute urls
        """
        for done in dones:
            done['markedup_text'] = done['markedup_text'].replace("/hashtags","%s/hashtags" % (idt_url))
            done['markedup_text'] = done['markedup_text'].replace("/cal","%s/cal" % (idt_url))
            return dones

    startdate = datetime.date.today() - datetime.timedelta(1)
    enddate = datetime.date.today() - datetime.timedelta(7)

    url_today = "%s&done_date=today" % (api_dones_url)
    dones_today = get_json_data(url_today)
    dones_today = fix_rel_url(dones_today)

    url_lastweek = "%s&done_date_after=%s&done_date_before=%s" % (api_dones_url, enddate, startdate)
    dones_lastweek = get_json_data(url_lastweek)
    dones_lastweek = fix_rel_url(dones_lastweek)

    context = {'team': team, 'user': user, 'dones_today': dones_today, 'dones_lastweek': dones_lastweek}

    return render(request, 'status/index.html', context)
