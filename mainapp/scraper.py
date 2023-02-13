from bs4 import BeautifulSoup
import requests
from itertools import product
from pathlib import Path
import environ
import os

# read variables from the .env file (for the api key)
env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

def get_synonyms(word):

    SHOW_ALL = True
    SITE = "api"

    headers = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 ("
            "KHTML, like Gecko) Version/4.0 Safari/534.30"}

    words = []
    if(SITE == "thesaurus.com"):
        response = requests.get("https://thesaurus.com/browse/" + word, headers=headers)
        webpage = response.content
        soup = BeautifulSoup(webpage, "html.parser")
        container = soup.find('div', {'data-testid': 'word-grid-container'})
        try:
            ul = container.find('ul')
        except:
            raise Exception("No synonyms found for word \"" + word + "\"")
        for li in ul:
            words.append(li.get_text())
    elif(SITE == "merriam-webster.com"):
        response = requests.get("https://www.merriam-webster.com/thesaurus/" + word, headers=headers)
        webpage = response.content
        soup = BeautifulSoup(webpage, "html.parser")
        container = soup.find_all('ul', {'class': 'mw-list'})
        for ul in container:
            # make sure it's a synonym, not antonym list
            container_header = ul.parent.find_previous_sibling().get_text().strip()
            if("Synonyms" in container_header):
                lis = ul.find_all('li')
                for li in lis:
                    possible_word = li.get_text().strip().replace(',', '')
                    if(possible_word.isalpha()):
                        words.append(possible_word)

    elif(SITE == "api"):
        response = requests.get(f'https://api.api-ninjas.com/v1/thesaurus?word={word}', headers={'X-Api-Key': env("API_KEY")})
        if response.status_code == requests.codes.ok:
            words = response.json()['synonyms']
        else:
            raise Exception("An error occurred while accessing the API")

    synonyms = []
    for synonym in words:
        # avoid anything with multiple words
        # since the second word might not be an alliteration
        if(' ' in synonym.strip() or '_' in synonym.strip()): continue
        synonyms.append(synonym.strip())

    return synonyms

# converts two lists of words into
# a list of alliterations
def get_alliterations(synonyms1, synonyms2):

    # each letter points to the alliterations
    # that start with that letter
    alliterations = {}

    # find possible letters the
    # alliterationcan start with
    letters1 = set()
    for word in synonyms1:
        letters1.add(word[0])

    letters2 = set()
    for word in synonyms2:
        letters2.add(word[0])

    # find the letters in common
    letters_in_common = letters1.intersection(letters2)

    # find words that share those common letters
    for letter in letters_in_common:
        filtered_word1 = [s for s in synonyms1 if s[0].lower() == letter]
        filtered_word2 = [s for s in synonyms2 if s[0].lower() == letter]
        # generate all possible combinations
        # from the two word lists
        all_combos = product(filtered_word1, filtered_word2)
        alliterations[letter] = all_combos

    return alliterations