
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
                entity.append(w.lemma_)

            unique_ents.setdefault(' '.join(entity).title())

    return list(unique_ents)


def save_json(filename: str, pars_list: list[tuple]) -> None:
    with open(filename, 'w', encoding='utf-8') as fp:
        fp.write(json.dumps(pars_list))

