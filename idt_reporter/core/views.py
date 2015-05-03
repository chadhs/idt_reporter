from django.conf import settings
from django.http import HttpResponse
from . models import Done

import requests
import datetime


def fetch_dones(request):
    ## configuration
    user = settings.IDT_USER
    token = settings.IDT_TOKEN
    team = settings.IDT_TEAM
    idt_url = "https://idonethis.com"
    api_dones_url = "%s/api/v0.1/dones/?owner=%s&team=%s&page_size=100" % (idt_url, user, team)

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

    startdate = datetime.date.today() - datetime.timedelta(3)
    enddate = datetime.date.today() - datetime.timedelta(6)

    url_filter_dones = "%s&done_date_after=%s&done_date_before=%s" % (api_dones_url, enddate, startdate)
    dones_filtered = get_json_data(url_filter_dones)
    dones_filtered = fix_rel_url(dones_filtered)

    def sync_dones(dones):
        """
        update local db with json done data.
        """
        for done in dones:
            d = Done(done_id=done['id'], owner=done['owner'], team_short_name=done['team_short_name'],
                    done_date=done['done_date'], last_updated=done['updated'], is_goal=done['is_goal'],
                    is_completed=done['goal_completed'], raw_text=done['raw_text'],
                    markedup_text=done['markedup_text'])
            cached_done = Done.objects.filter(done_id=done['id']).first()

            if not cached_done:
                d.save()
            elif d.last_updated != cached_done.last_updated:
                Done.objects.get(done_id=done['id']).delete()
                d.save()

    sync_dones(dones_filtered)

    return HttpResponse('fetching of dones complete')
