from concurrent.futures import ProcessPoolExecutor
from pyfiglet import Figlet
import requests

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/93.0.4577.63 Safari/537.36"
}

symbol = "'"

list_words = ['Error',
              'error',
              'failed']
try:
    with open('sites.txt', 'r', encoding='utf-8') as f:
        sites = f.read()
    SITES = sites.split('\n')

except FileNotFoundError:
    print('File sites.txt not found')


def start_check(site: str):
    try:
        with open('checkers_list.txt', 'r', encoding='utf-8') as f:
            strings = f.read()

    except FileNotFoundError:
        return 'File checkers_list.txt not found'

    list_string = strings.split('\n')
    list_string = set(list_string)
    checkers_list = list(list_string)

    for stroka in checkers_list:
        stroka = stroka.strip()
        url = f"{site}{stroka}{symbol}"
        res = requests.get(url=url, headers=headers).text
        count = 0
        for i in list_words:
            if i in res:
                count += 1
                print(
                    f"\033[32m\033[1m[GOOD]\033[0m \033[33m\033[1mSQL-INJECTION IS POSSIBLE\033[0m \033[1m{url}\033[0m")
                with open('inj_sites.txt', 'a+', encoding='utf-8') as file:
                    file.write(url + '\n')
            else:
                print(f"\033[31m\033[1m[BAD]\033[0m \033[1m{url}\033[0m \033[33m\033[1mNOT INJECTION\033[0m")


def main():
    with ProcessPoolExecutor(max_workers=10) as ex:
        ex.map(start_check, SITES)

    try:
        with open('inj_sites.txt', 'r') as f:
            urls = f.readlines()
        counter = len(urls)
    except FileNotFoundError:
        counter = 0

    return print(
        f"\n\033[33m\033[1m[INFO]\033[0m \033[33m\033[1m{counter}\033[0m "
        f"SQL-INJECTIONS URLS WRITTEN TO \033[31m\033[4minj_sites.txt\033[0m")


if __name__ == "__main__":
    preview_text = Figlet(font='doom', width=200)
    text = preview_text.renderText('SQL-Injections Checker')
    print(f'\033[35m\033[1m{text}\033[0m')
    main()
