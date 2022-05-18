import pandas as pd
import requests
from openpyxl import Workbook
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random, os

def coordination(url, header):
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.prettify()

    initial_pos = text.find(";window.APP_INITIALIZATION_STATE")
    data = text[initial_pos+36:initial_pos+85] #XX後36~85

    line = tuple(data.split(','))

    ## line[1] => lon
    ## line[2] => lat
    return line[1], line[2]

folder = '/Users/luo-j/Documents/competition/2022_interior_hackathon/data'
if os.path.exists(os.path.join(folder, 'remain_places.csv')):
    places = pd.read_csv(os.path.join(folder, 'remain_places.csv'))
else:
    df = pd.read_csv(f'{folder}/Stores_TP.csv')
    places = df[['商業名稱', '商業地址']].copy().rename(columns={'商業名稱': 'name', '商業地址': 'address'})

if places.empty:
    print('No stations to crawl', flush=True)
    sys.exit(1)
## copy places to do the iteration
pp = places.copy()

ua = UserAgent()
f = open(os.path.join(folder, "address.csv"), 'a')

fail_places = []
nn = 0
restart_num = 0
for i, place in pp.iterrows():
    name = place['name']
    address = place['address']
    url = f"https://www.google.com/maps/place?q={address}"
    random_ua = ua.random
    print('Use User Agent:', random_ua)
    r = {'user-agent': random_ua}
    try:
        lon, lat = coordination(url, r)
        ## write to file
        output = f'{name},{address},{lon},{lat}'
        print(output, flush=True)
        f.write(output+'\n')
        f.flush()

        ## sleep a little bit
        sleep_time = random.uniform(1, 5)
        print(f'sleep for {sleep_time} seconds', flush=True)
        time.sleep(sleep_time)
        ## drop the successful place
        places.drop(i, axis=0, inplace=True)
        nn += 1

    except Exception as e:
        print(f"Did not crawl {name}", flush=True)
        print(e, flush=True)
        restart_num += 1
        if restart_num > 5:
            print('Restart time exceed, break the loop', flush=True)
            break
        else:
            print('Sleep for 30 seconds and continue to crawl', flush=True)
            time.sleep(30)

print(f'{nn} succeess', flush=True)
print(f'remaining {len(places)}', flush=True)
places.to_csv(os.path.join(folder, 'remain_places.csv'), index=None)
f.close()

