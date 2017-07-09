from bs4 import BeautifulSoup
import requests

def scrape_rooms(week, year):
    room_data = []
    url = "https://www.lectio.dk/lectio/144/FindSkema.aspx?type=lokale"
    r = requests.get(url).text

    soup = BeautifulSoup(r, "html.parser")
    div = soup.find("div", attrs={"id":"m_Content_listecontainer"})
    els = div.find_all('a')

    for e in els:
        rooms = e.find('span')
        link = "http://www.lectio.dk"+e.get("href")+"&week="+str(week)+str(year)
        room_data.append([rooms.text,link])

    #time = check_if_free(room_data[0])
    #return(time)
    return(room_data)

def check_if_free(room,day,module):
    modules = {
    1:[495,585],
    2:[600,690],
    3:[720,810],
    4:[820,910],
    5:[915,1005]
    }

    room.append(True)
    arr = []
    url = room[1]
    r = requests.get(url).text

    soup = BeautifulSoup(r, "html.parser")
    table_div = soup.find("div", attrs={"id":"s_m_Content_Content_SkemaNyMedNavigation_skemaprintarea"})
    table = table_div.find("table")
    tr_body = table.find_all("tr")
    td_body = tr_body[3].find_all("td")

    for td in td_body[day:(day+1)]:
        td_div = td.find("div")
        for classes in td_div.find_all("a",attrs={"class":"s2skemabrik"}):
            class_info = classes.get("title")

            colon_index = [pos for pos,char in enumerate(class_info) if char==":"]

            t1a = int(str(class_info[colon_index[0]-2])+str(class_info[colon_index[0]-1]))
            t1b = int(str(class_info[colon_index[0]+1])+str(class_info[colon_index[0]+2]))
            t1 = t1a*60+t1b
            t2a = int(str(class_info[colon_index[1]-2])+str(class_info[colon_index[1]-1]))
            t2b = int(str(class_info[colon_index[1]+1])+str(class_info[colon_index[1]+2]))
            t2 = t2a*60+t2b

            if modules[module][0]>=t2 or modules[module][1]<=t1:
                room[2] = True
                #print("room is free")
            else:
                #print("room is taken")
                room[2] = False
                break

    return([room[0],room[2]])

list_of_rooms = []
temp = scrape_rooms(24,2017)
for r in temp:
    list_of_rooms.append(check_if_free(r,1,3))

print('\n'.join(' '.join(map(str,sl)) for sl in list_of_rooms))
