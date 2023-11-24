import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
import json
import os


def get_random_user_agent():
    ua = UserAgent()
    print('Changed headers')
    return ua.random


def get_urls(url):
    ua = get_random_user_agent()
    header = {'User-Agent': ua}
    response = requests.get(url, headers=header)
    return response


def scrape_scroes(response):
    soup = BeautifulSoup(response.content, 'html5lib')
    conta = soup.find_all('a', class_='m')
    out_team = []
    for scores in conta:
        team1 = scores.find('t1').t.text
        score = scores.find('sc').text
        team2 = scores.find('t2').t.text
        teamLeague = {
            "Team1": team1,
            "score": score,
            'Team2': team2
        }
        out_team.append(teamLeague)
    return out_team


def writer_(data):
    path = 'data'
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        pass
    df = pd.DataFrame(data)
    df.to_csv('data/League_scroes.csv', index=False)
    df.to_excel('data/League_scroes.xlsx', index=False)
    with open('data/League_scroes.json', 'w') as file:
        json.dump(data, file, indent=2)


def main():
    url = 'https://www.livescore.bz/en/'
    response_data = get_urls(url)
    data = scrape_scroes(response_data)
    writer_(data)
    print("Done......")


if __name__ == '__main__':
    main()
