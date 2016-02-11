# -*- coding: utf-8 -*-
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

from time import sleep
import datetime
import time
import ddbot

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    #home_dir = os.path.expanduser('~')
    #credential_dir = os.path.join(home_dir, '.credentials')
    #if not os.path.exists(credential_dir):
    #    os.makedirs(credential_dir)
    credential_path = "calendar-python-quickstart.json"#os.path.join(credential_dir,
                                   #'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def add_event(cal_data,cal_year,cal_month,service,calID,colorID):
    for i in cal_data:
        if isinstance(i[0],int) == True:
            print (i[0])
        else:
            cal_year = i[0].year
            cal_month = i[0].month
            i[0] = i[0].day
            print (cal_month,i[0])
            
        caldate = datetime.datetime(year=cal_year,month=cal_month,day=i[0]).strftime("%Y-%m-%d")
        
        event = {
          'summary': i[1],
          'htmlLink': i[2],
          'description': i[3],
          'colorId': colorID,
          'start': {
              'date': caldate,
          },
          'end': {
            'date': caldate,
          },
        }

        event = service.events().insert(calendarId=calID, body=event).execute()

def create_calender(service,name):
    calendar = {
        'summary': name
    }
    
    created_calendars = service.calendars().insert(body=calendar).execute()
    print (created_calendars['id'])

def auto_add_events(service,url,groupname,calID,colorID):
    now = datetime.datetime.now()

    for i in range(-12,13):
        caldate = datetime.datetime.fromtimestamp(time.mktime((now.year,now.month + i,1,0,0,0,0,0,0)))

        print (caldate.year,caldate.month)
        par_url = url + str(caldate.year) + "&month=" + str(caldate.month)
        a = ddbot.diff_pages(par_url,groupname + "_event_link_" + str(caldate.year) + "_" + str(caldate.month) + ".csv")
        add_event(a,caldate.year,caldate.month,service,calID,colorID)

def auto_add_events_prizmmy(service,url,groupname,calID,colorID,y_range):
    for i in y_range:
        par_url = url + str(i)
        print (par_url)
        a = ddbot.diff_pages(par_url,groupname + "_event_link_" + str(i) + ".csv")
        add_event(a,0,0,service,calID,colorID)

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    #create_calender(service,"Dorothy Little Happy")

    auto_add_events(service,"http://supergirls.jp/live/index.php?viewmode=vertical&type=live&year=","SG","vl4eanrlp3suf22pom5iv0l0mo@group.calendar.google.com",1)
    auto_add_events(service,"http://www.cheekyparade.jp/live/index.php?viewmode=vertical&type=live&year=","CP","dh9k5teeh3ngmj16epsj12nfmk@group.calendar.google.com",2)
    auto_add_events(service,"http://girls-entertainment-mixture.jp/live/index.php?viewmode=vertical&type=live&year=","GEM","b6irogftonrhhr8djsnhj6t1j0@group.calendar.google.com",3)
    auto_add_events(service,"http://wa-suta.world/live/index.php?viewmode=vertical&type=live&year=","tws","0qhea09dq3e2h94aqk0qisu47o@group.calendar.google.com",4)
    auto_add_events(service,"http://solidemo.jp/schedule/index.php?viewmode=horizontal&type=live&year=","SOLIDEMO","ha51ni6vseogm5sehlonbfvftg@group.calendar.google.com",5)
    auto_add_events(service,"http://avex.jp/callme/schedule/index.php?viewmode=&type=live&year=","callme","1nn55sdit4kb7j4vet1mdtpl50@group.calendar.google.com",6)
    auto_add_events(service,"http://avex.jp/lol/schedule/index.php?viewmode=horizontal&type=live&year=","lol","hlbr5ugekj0qh63ur41oksuekg@group.calendar.google.com",7)
    auto_add_events_prizmmy(service,"http://avex.jp/prizmmy/live/?year=","Prizmmy","2v58103h3kkvrgjvuq755lvlts@group.calendar.google.com",8,range(2012,2017))
    auto_add_events(service,"http://avex.jp/x21/live/index.php?viewmode=vertical&type=live&year=","X21","u6hua9gjng9gufn0dman70ggdk@group.calendar.google.com",9)
    auto_add_events_prizmmy(service,"http://dorothylittlehappy.jp/","DLH","a26s7iutphv3d26bp9phpksg14@group.calendar.google.com",10,range(2015,2017))

if __name__ == '__main__':
    main()
