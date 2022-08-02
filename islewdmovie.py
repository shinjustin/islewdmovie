import re
import requests
from bs4 import BeautifulSoup
from pprint import pprint

'''
name: violence
severity: mild
vote: 22
outof: 43
scenes: ['scene 1', 'scene 2']
spoilers: ['scene 1', 'scene 2']
'''

def get_severity(section):
    vote_container = section.find(class_='ipl-swapper__content-primary')
    if vote_container:
        vote_container = vote_container.find(class_='advisory-severity-vote__container')
    else:
        return None, None, None, None
    # severity vote examples:
    # 45 of 59 found this to have none
    # 22 of 43 found this mild
    # 32 of 46 found this moderate
    # 241 of 320 found this severe
    severity = vote_container.find('span').text
    vote = vote_container.find('a').text
    pattern = '([\d,]+)\sof\s([\d,]+)'
    m = re.match(pattern, vote)
    vote = int(m[1].replace(',', ''))
    outof = int(m[2].replace(',', ''))
    percent = round((vote/outof) * 100)
    return severity, vote, outof, percent

def get_scenes(section):
    scenes_raw = section.find_all('li', class_='ipl-zebra-list__item')
    scenes = list()
    for scene in scenes_raw:
        scene = scene.text.replace('\n', '')
        scene = scene.replace('     Edit    ', '')
        scene = scene.replace('                        ', '')
        scenes.append(scene)
    return scenes

def get_parents_guide(tid):
    pg_url = f'https://www.imdb.com/title/{tid}/parentalguide'
    r = requests.get(pg_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # Certification
    certs = soup.find(id='certificates')
    # Sex & Nudity
    section = soup.find(id='advisory-nudity')
    severity, vote, outof, percent = get_severity(section)
    scenes = get_scenes(section)
    nudity = {
            'name': 'Sex & Nudity',
            'severity': severity,
            'vote': vote,
            'outof': outof,
            'percent': percent,
            'scenes': scenes,
            }
    # Violence & Gore
    section = soup.find(id='advisory-violence')
    severity, vote, outof, percent = get_severity(section)
    scenes = get_scenes(section)
    violence = {
            'name': 'Violence & Gore',
            'severity': severity,
            'vote': vote,
            'outof': outof,
            'percent': percent,
            'scenes': scenes,
            }
    # Profanity
    section = soup.find(id='advisory-profanity')
    severity, vote, outof, percent = get_severity(section)
    scenes = get_scenes(section)
    profanity = {
            'name': 'Profanity',
            'severity': severity,
            'vote': vote,
            'outof': outof,
            'percent': percent,
            'scenes': scenes,
            }
    # Alcohol, Drugs & Smoking
    section = soup.find(id='advisory-alcohol')
    severity, vote, outof, percent = get_severity(section)
    scenes = get_scenes(section)
    alcohol = {
            'name': 'Alcohol, Drugs, & Smoking',
            'severity': severity,
            'vote': vote,
            'outof': outof,
            'percent': percent,
            'scenes': scenes,
            }
    # Frightening & Intense Scenes
    section = soup.find(id='advisory-frightening')
    severity, vote, outof, percent = get_severity(section)
    scenes = get_scenes(section)
    frightening = {
            'name': 'Frightening & Intense Scenes',
            'severity': severity,
            'vote': vote,
            'outof': outof,
            'percent': percent,
            'scenes': scenes,
            }
    # Spoilers
    spoilers = soup.find(id='advisory-spoilers')
    if spoilers:
        # Spoiler-Nudity
        section = spoilers.find(id='advisory-spoiler-nudity')
        if section:
            scenes = get_scenes(section)
            nudity['spoilers'] = scenes
        # Spoiler-Violence
        section = spoilers.find(id='advisory-spoiler-violence')
        if section:
            scenes = get_scenes(section)
            violence['spoilers'] = scenes
        # Spoiler-Profanity
        section = spoilers.find(id='advisory-spoiler-profanity')
        if section:
            scenes = get_scenes(section)
            profanity['spoilers'] = scenes
        # Spoiler-Alcohol
        section = spoilers.find(id='advisory-spoiler-alcohol')
        if section:
            scenes = get_scenes(section)
            alcohol['spoilers'] = scenes
        # Spoiler-Frightening
        section = spoilers.find(id='advisory-spoiler-frightening')
        if section:
            scenes = get_scenes(section)
            frightening['spoilers'] = scenes
    advisory = list()
    advisory.append(nudity)
    advisory.append(violence)
    advisory.append(profanity)
    advisory.append(alcohol)
    advisory.append(frightening)

    return advisory

def search_media(query):
    if not query:
        print('Request query cannot be left blank')
        return None

    search_url = f'https://v3.sg.media-imdb.com/suggestion/titles/x/{query}.json'
    search_url = search_url.replace(' ', '%20')
    r = requests.get(search_url)
    results = r.json()
    return results


if __name__ == '__main__':
    import sys
    flag = sys.argv[1]
    query = sys.argv[2]
    if flag == 'pg':
        results = get_parents_guide(query)
    elif flag == 's':
        results = search_media(query)
