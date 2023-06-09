from PyPDF2 import PdfReader
import pandas as pd
import tqdm
import argparse
import textwrap
import os
import json
import logging

import core

from pprint import pprint


from pymongo.mongo_client import MongoClient

uri = "mongodb://localhost:27017"
client = MongoClient(uri)
docs_db = client['paragprapher'].news




def init_parser() -> argparse.ArgumentParser:
    description = textwrap.dedent('''
        Утилита для анализа текста
    ''')

    epilog = textwrap.dedent ('''
        Программа выделяет параграфы и именованные сущности из pdf файла. 
    ''')

    parser = argparse.ArgumentParser(
        prog='News dataset convertor',
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog
    )
    parser.add_argument('--pdf', type=str, help='Путь к pdf файлу')
    parser.add_argument('--spage', type=int, help='Страница с которой начинается основной текст')
    parser.add_argument('--epage', type=int, help='Страница на которой оканчивается основной текст')

    return parser

def main():
    parser = init_parser()
    args = parser.parse_args()

    
    pdf_filename = str(args.pdf)
    spage = int(args.spage)
    epage = int(args.epage) 


    if not os.path.exists(pdf_filename):
        exit('Input filename not found')

    if spage is None or spage < 0:
        exit('Start page is incorret')

    if epage is None or epage < 0:
        exit('Start page is incorret')


    reader = PdfReader(pdf_filename)
    page_count = reader.pages.__len__()

    metadata = reader.metadata

    print('Название:', metadata.title)
    print('Автор:', metadata.author)
    print('Создано:', metadata.creator)
    print('Дата создания:', metadata.creation_date)
    print('Количество страниц:', page_count)
    print('Будет проанализировано страниц:', epage - spage)

    par_list = []

    
    start = 1
    print('Разбиение текста на параграфы:')
    for index in tqdm.tqdm(range(epage - spage)): # получение параграфов из страниц
        page = reader.pages[spage + index]
        pars = core.text2par(
            page.extract_text()
        )

        if pars:
            par_list.append(
                list(enumerate(pars, start))
            )

            start += pars.__len__()

    print('Количество полученных абзацев:', start)

    output_filename = str(metadata.title) + '.csv'
    columns = ['par_num', 'par_text']

    df = pd.DataFrame([], columns=columns)
    df.set_index('par_num', inplace=True)
    df.to_csv(output_filename, sep=';')

    print('Сохранение абзацев в', output_filename)
    for pars in tqdm.tqdm(par_list): # сохранение абзацев в csv
        df = pd.DataFrame(pars, columns=columns)
        df.set_index('par_num', inplace=True)
        df.to_csv(output_filename, header=False, sep=';', mode='a')

    print('Загрузка параграфов из', output_filename)
    df = pd.read_csv(output_filename, sep=';', index_col=0)

    print('Выделение именованных сущностей')
    df['ents'] = df['par_text'].apply(core.text2ents)
    df['ents'] = df['ents'].apply(core.ents2norm)

    enteties_list = list(filter(lambda l: l != [], list(df['ents'].values)))

    enteties_list = []

    par_num = 1
    for entites in list(df['ents'].values):
        
        for e in entites:
            enteties_list.append((
                par_num,
                e
            ))

        par_num += 1

    # df['ents'] = tqdm.tqdm(df['ents'].apply(lambda ents_list: json.dumps(ents_list)))
    
    print('Сохранение именных сущностей в', str(metadata.title) + '_entites.csv')
    tqdm.tqdm(pd.DataFrame(enteties_list, columns=['par_num', 'entity']).to_csv(str(metadata.title) + '_entites.csv', sep=';'))

    print('Формирование мешка сущностей')
    entities_bag = core.wordbag(
        list(map(lambda e: e[1], enteties_list))
    )

    pprint(entities_bag)

    print('Сохранение мешка сущностей в', str(metadata.title) + '_entites_bag.json')
    fp = open(str(metadata.title) + '_entites_bag.json', mode='w', encoding='utf8')
    
    json.dump(entities_bag, fp, indent=0)

    fp.close()
    

    print('Сохранение абзацев в', output_filename)
    df.to_csv(output_filename, sep=';', mode='w')


if __name__ == '__main__':
    main()
