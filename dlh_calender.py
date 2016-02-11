# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import datetime

def get_contents(par_url):
    res = urllib2.urlopen(par_url)
    soup = BeautifulSoup(res.read(), "html.parser")
    return soup.find_all('div', attrs={'id':'singleContentWrapper'})[0].text[:-8]
    
def get_calender(par_url,include_contents=True,urlonly=False):
    res = urllib2.urlopen(par_url)
    soup = BeautifulSoup(res.read(), "html.parser")

    a = soup.find_all("dt")
    b = soup.find_all("a")
    output_data = []
    
    j = 0

    for i in b:
        if i.attrs['href'].find("live") != -1 and i.attrs['href'].find("html") != -1:
            event_date = datetime.datetime.strptime(a[j].text,'%Y-%m-%d')

            links = i.attrs['href']
            j += 1

            if include_contents == True:
                output_data.append([event_date,i.text,links,get_contents(links)])
            if include_contents == False:
                if urlonly == True:
                    output_data.append(links)
                if urlonly == False:
                    output_data.append([event_date,i.text,links])

    return output_data

if __name__ == "__main__":
    par_url = "http://dorothylittlehappy.jp/2016"
    print get_calender(par_url,include_contents=False,urlonly=True)
