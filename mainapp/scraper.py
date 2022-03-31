from bs4 import BeautifulSoup
import requests
import random
from itertools import product

def getSynonyms(word1, word2):

    SHOW_ALL = True
    SITE = "thesaurus.com"

    # num_word1 = input("How many adjectives do you want?")

    headers = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 ("
            "KHTML, like Gecko) Version/4.0 Safari/534.30"}

    synonyms = {word1: [], word2: []}

    for word in [word2, word1]:
        words = []
        if(SITE == "thesaurus.com"):
            response = requests.get("https://thesaurus.com/browse/" + word, headers=headers)
            webpage = response.content
            # Check Status Code (Optional)
            # print(response.status_code)
            # Create a Beautiful Soup Object
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
            # Check Status Code (Optional)
            # print(response.status_code)
            # Create a Beautiful Soup Object
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

        for syn in words:
            # WIP
            # avoid anything with multiple words
            # since the second word might not be an alliteration
            if(' ' in syn.strip()): continue
            synonyms[word].append(syn.strip())

    return synonyms

def getAlliterations(synonyms):
    word1, word2 = list(synonyms)[0], list(synonyms)[1]
    # dict where a char points to all alliterations starting with that char
    alliterations = {}

    # find possible letters the alliteration can start with
    letters = {word1: set(), word2: set()}

    # key = word1/word2
    for key in synonyms:
        for word in synonyms[key]:
            letters[key].add(word[0])

    letters_in_common = letters[word1].intersection(letters[word2])
    
    for char in letters_in_common:
        filtered_word1 = [s for s in synonyms[word1] if s[0].lower() == char]
        filtered_word2 = [s for s in synonyms[word2] if s[0].lower() == char]
        # generate all possible combinations from the two word lists
        allCombos = product(filtered_word1, filtered_word2)
        alliterations[char] = allCombos

    return alliterations
