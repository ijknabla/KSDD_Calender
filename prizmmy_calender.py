# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import datetime

def get_contents(par_url): #prizmmy
    res = urllib2.urlopen(par_url)
    soup = BeautifulSoup(res.read(), "html.parser")
    return soup.find_all(class_="detail")[2].text

def get_calender(par_url,include_contents=True,urlonly=False): #prizmmy
    res = urllib2.urlopen(par_url)
    soup = BeautifulSoup(res.read(), "html.parser")

    a = soup.find_all("dt")
    b = soup.find_all("a")
    output_data = []

    j = 0

    for k in b:
        if k.attrs['href'].find("./detail") != -1:
            event_date = datetime.datetime.strptime(a[j].text[:11].strip(),'%Y.%m.%d')
            links = "http://avex.jp/prizmmy/live" + k.attrs["href"][k.attrs["href"].find("detail")-1:]
        
            j += 1

            if include_contents == True:
                output_data.append([event_date,k.text,links,get_contents(links)])
            if include_contents == False:
                if urlonly == True:
                    output_data.append(links)
                if urlonly == False:
                    output_data.append([event_date,k.text,links])

    return output_data

if __name__ == "__main__":
    par_url = "http://avex.jp/prizmmy/live?year=2016"
    a = get_calender(par_url,include_contents = False)
    for i in a:
        print i[0],i[1],i[2]
