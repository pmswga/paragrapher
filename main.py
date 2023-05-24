from PyPDF2 import PdfReader
import pandas as pd
import tqdm
import argparse
import textwrap
import os

import core

from pprint import pprint

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

    output_filename = 'pdf_result.csv'
    columns = ['par_num', 'par_text']

    df = pd.DataFrame([], columns=columns)
    df.set_index('par_num', inplace=True)
    df.to_csv(output_filename)

    print('Сохранение абзацев в', output_filename)
    for pars in tqdm.tqdm(par_list): # сохранение абзацев в csv
        df = pd.DataFrame(pars, columns=columns)
        df.set_index('par_num', inplace=True)
        df.to_csv(output_filename, header=False, mode='a')

    print('Загрузка параграфов из', output_filename)
    df = pd.read_csv(output_filename, index_col=0)

    print('Выделение именованных сущностей')
    df['ents'] = df['par_text'].apply(core.text2ents)
    df['ents'] = df['ents'].apply(core.ents2norm)
    
    print(df)

    print('Сохранение абзацев в', output_filename)
    df.to_csv(output_filename, mode='w')


if __name__ == '__main__':
    main()
