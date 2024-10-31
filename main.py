import json

import requests
from bs4 import BeautifulSoup

path_url = f'https://quotes.toscrape.com/page/'

parser_dict = {}  # Словарь для хранения спарсенных данных Имя автора цитата и теги


def save_data_url(url: str):
    '''
    Функция парсит необходимсыфе данные с сайта
    и записывает их в словарь
    '''
    global parser_dict # указываем переменную как глобальной
    count_index: int = 1  # Для заполнения словаря по порядку
    page = 1 # хранит номер страницы
    # В бесконечном цикле парсим данные с сайта и сохраняем их в словарь для дальнейшей сериализации
    while True:
        response = requests.get(url + str(page))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')  # Получить всю HTML страницу
        end_page = soup.find_all(name='div', class_='col-md-8')  # Проверить на конец страницы
        val = end_page[1].text.split()
        my_str = val[0] + val[1] + val[2]
        # Если попали на страницу без данных, то завершить работу функции, все данные спарсены
        if my_str == 'Noquotesfound!':
            return  # Закончить парсить страницы
        page += 1  # Перейти к следующей странице
        excerpt = soup.find_all('span', class_='text')  # Парсим все цитаты на данной странице
        authors = soup.find_all('small', class_='author')  # Парсим всех авторов на данной странице
        tags = soup.find_all('div', class_='tags')  # Парсим все теги на данной странице
        # В цикле пройти по полученным данным и записать их на свои места
        for ind in range(0, len(excerpt)):
            list_tags: list = []
            tag_excerpt = tags[ind].find_all('a', class_='tag') # Получить список всех тегов
            for tag in tag_excerpt:
                list_tags.append(tag.text) # Добавляем теги в список для дальнейшего сохранения их
            parser_dict[count_index] = {"Authors": authors[ind].text, "Quote": excerpt[ind].text, "Tags": list_tags} # Добавляем спарсенные данные в словарь
            count_index += 1  # Увеличить счётчик


def serialize_to_json(data: dict):
    '''
    Сериализация словаря в json файл
    '''
    with open('data.json', mode='w', encoding='utf-8') as file: # Открываем json файл для сериализации словаря
        json.dump(data, file)


save_data_url(path_url)
serialize_to_json(parser_dict)
print('Программа завершила работу!')
