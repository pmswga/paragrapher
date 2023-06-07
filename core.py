
import re
import json
import spacy as sp

nlp = sp.load('ru_core_news_sm')

def text2par(text: str, start=0) -> list:
    if not text:
        return []

    text = text.replace('\xad\n', '')
    text = text.replace('. \n', '#')
    text = text.replace(' \n', ' ')
    text = text.split('#')

        
    for i in range(text.__len__()):
        text[i] = text[i].strip()
        text[i] = re.sub(' +', ' ', text[i])
        text[i] = re.sub(r'(\n\d)', '', text[i])


    return text


def text2ents(text: str) -> tuple:
    global nlp
    return tuple(nlp(text).ents)


def ents2norm(ents) -> list:
    if not ents:
        return []
    
    global nlp
    unique_ents = {}

    for e in ents:
        if e not in unique_ents:
            doc = nlp(str(e))
            entity = []

            for w in doc:
                entity.append(w.text) # получение леммы

            unique_ents.setdefault(' '.join(entity))

    return list(unique_ents)


def get_entity(string: str) -> tuple:
    global nlp

    entity = tuple(nlp(string).ents)

    print(entity)
    
    return (entity[0].text, entity[0].label_)


def wordbag(lemmas: list) -> dict:
    bag = {}
    
    for l in lemmas:
        if l not in bag.keys():
            bag.setdefault(l, 1)
        
        bag[l] += 1

    return bag

def save_json(filename: str, pars_list: list[tuple]) -> None:
    with open(filename, 'w', encoding='utf-8') as fp:
        fp.write(json.dumps(pars_list))

