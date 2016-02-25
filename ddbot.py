# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
import csv
import os
import datetime
import prizmmy_calender
import dlh_calender

def get_contents(par_url):
    res = urllib.request.urlopen(par_url)
    soup = BeautifulSoup(res.read(), "html.parser")

    output_str = ""

    if par_url.find("wa-suta") != -1 or par_url.find("girls-entertainment-mixture") != -1 or par_url.find("cheekyparade") != -1 or par_url.find("avex.jp/lol") != -1 or par_url.find("avex.jp/x21") != -1:
        a = soup.find_all(class_="wrap")
        for i in a:
            output_str +=  i.text

    if par_url.find("callme") != -1:
        a = soup.find_all(class_="item")
        j = a[2].find_all("div")

        if len(j) == 0:output_str += a[0].text
        if len(j) != 0:
            for i in j:
                output_str += i.text

    if par_url.find("supergirls") != -1:
        a = soup.find_all(class_="entryBody")
        for i in a:
            output_str += i.text

    if par_url.find("solidemo") != -1:
        a = soup.find_all(class_="block")
        for i in a:
            output_str += i.text
        output_str = output_str[:output_str.find("shareSoc")] + output_str[output_str.rfind("'tw,fl')")+8:]
        
    return output_str

def get_calender(par_url,include_contents=True,urlonly=False):
    res = urllib.request.urlopen(par_url)
    soup = BeautifulSoup(res.read(), "html.parser")

    b = soup.find_all("a")
    output_data = []

    if par_url.find("supergirls") != -1 or par_url.find("cheekyparade") != -1 or par_url.find("solidemo") != -1:group = "./detail"
    if par_url.find("girls-entertainment-mixture") != -1 or par_url.find("avex.jp/callme") != -1 or par_url.find("wa-suta.world") != -1 or par_url.find("avex.jp/x21") != -1:group = "live/detail"
    if par_url.find("avex.jp/lol") != -1:group = "schedule/detail"

    for i in b:
        if i.attrs["href"].find(group) != -1: #./detail == SG,CP,solidemo live/detail == GEM,callme,tws schedule/detail == lol
            try: #Others
                event_type = i.previousSibling.previousSibling.text.strip()
                if event_type == "LIVE_EVENT":
                    try: #GEM,callme,CP,tws,lol
                        if par_url.find("avex.jp/lol") != -1: #lol
                            day = i.parent.attrs["class"][1]
                            day = int(day[day.find("day")+3:])

                        else: #others
                            day = i.parent.parent.attrs["class"][1]
                            day = int(day[day.find("day")+3:])

                    except: #SG
                        day = int(i.parent.parent.find("td").text)

            except: #SOLIDEMO
                try:
                    day = i.parent.parent.attrs["class"][1]
                    day = int(day[day.find("day")+3:])
                except:
                    pass

            links = par_url[:par_url.rfind("/")] + i.attrs["href"][i.attrs["href"].find("detail")-1:]

            if include_contents == True:
                output_data.append([day,i.text,links,get_contents(links)])
            if include_contents == False:
                if urlonly == True:
                    output_data.append(links)
                if urlonly == False:
                    output_data.append([day,i.text,links])

    return output_data

def diff_pages(par_url,csv_file,csv_saveonly = False):
    if os.path.isfile("cal_log/" + csv_file) == True:
        if par_url.find("avex.jp/prizmmy") != -1:
            a = prizmmy_calender.get_calender(par_url,include_contents = False,urlonly = True)
        elif par_url.find("dorothylittlehappy.jp") != -1:
            a = dlh_calender.get_calender(par_url,include_contents = False,urlonly = True)
        else:
            a = get_calender(par_url,include_contents = False,urlonly = True)

        f = open("cal_log/" + csv_file, 'r')
        reader = csv.reader(f)
        for b in reader:
            pass
        f.close()
    
        diff = []
    
        set_ab = set(a) - set(b)
        list_ab = list(set_ab)

        if len(list_ab) > 0:
            if par_url.find("avex.jp/prizmmy") != -1:
                c = prizmmy_calender.get_calender(par_url)
            elif par_url.find("dorothylittlehappy.jp") != -1:
                c = dlh_calender.get_calender(par_url)
            else:
                c = get_calender(par_url)

        for i in list_ab:
            for k in c:
                if k[2] == i:
                    diff.append(k)
    
        f = open("cal_log/" + csv_file, 'w')
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(a)
        f.close()

        return diff

    if os.path.isfile("cal_log/" + csv_file) == False:
        if par_url.find("avex.jp/prizmmy") != -1:
            a = prizmmy_calender.get_calender(par_url,include_contents = False,urlonly = True)
        elif par_url.find("dorothylittlehappy.jp") != -1:
            a = dlh_calender.get_calender(par_url,include_contents = False,urlonly = True)
        else:
            a = get_calender(par_url,include_contents = False,urlonly = True)
            print(a)
            
        f = open("cal_log/" + csv_file, 'w')
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(a)
        f.close()

        if par_url.find("avex.jp/prizmmy") != -1:
            output_data = prizmmy_calender.get_calender(par_url)
        elif par_url.find("dorothylittlehappy.jp") != -1:
            output_data = dlh_calender.get_calender(par_url)
        else:
            output_data = get_calender(par_url)
            
        return output_data

if __name__ == "__main__":
    #par_url = "http://girls-entertainment-mixture.jp/live/index.php?viewmode=vertical&type=live&year=2016&month=1"
    #par_url = "http://avex.jp/callme/schedule/index.php?viewmode=&type=live&year=2016&month=1"
    #par_url = "http://www.cheekyparade.jp/live/index.php?viewmode=vertical&type=live&year=2016&month=1"
    #par_url = "http://supergirls.jp/live/index.php?viewmode=vertical&type=live&year=2016&month=1"
    #par_url = "http://wa-suta.world/live/index.php?viewmode=vertical&type=live&year=2016&month=1"

    #par_url = "http://avex.jp/lol/schedule/index.php?viewmode=horizontal&type=live&year=2016&month=1"
    #par_url = "http://solidemo.jp/schedule/index.php?viewmode=horizontal&type=live&year=2016&month=1"

    #print diff_pages(par_url,"GEM_event_link.csv")
    #print diff_pages("http://avex.jp/prizmmy/live/?year=2016","test.csv")
    #m = get_calender("http://avex.jp/x21/live/index.php?viewmode=vertical&type=all&year=2016&month=1",include_contents = False,urlonly = True)
    print((diff_pages("http://avex.jp/x21/live/index.php?viewmode=vertical&type=all&year=2016&month=1","x21.csv")))

    #print m
