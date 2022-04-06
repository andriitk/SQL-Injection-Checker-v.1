from concurrent.futures import ProcessPoolExecutor
from pyfiglet import Figlet
from requests import Response
import requests
import datetime
import urllib.parse

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/93.0.4577.63 Safari/537.36"
}

SYMBOL = ["1'", '1"', '1`']

LIST_WORDS = ['SQL',
              'Sql',
              'DBError',
              'Error',
              'error',
              'ERROR']


def get_file_lines(filename: str):
    try:
        with open(filename, encoding="utf-8") as f:
            sites = f.read().split("\n")
            sites = set(sites)
            sites = list(sites)
            return sites
    except FileNotFoundError:
        raise SystemExit(f"\n\033[31m\033[1m[ERROR]\033[0m Please check if file "
                         f"\033[31m\033[4m{filename}\033[0m exists\n")


def error_in_body(response: Response):
    for word in LIST_WORDS:
        if word in response.text:
            return True
    return False


SITES = get_file_lines('sites.txt')


def start_check(site: str):
    checkers_list = get_file_lines('checkers_list.txt')

    for dork in checkers_list:
        dork = dork.strip()
        for symbol in SYMBOL:
            symbol = urllib.parse.quote_plus(symbol)
            if site[-1] == '/':
                url = f"{site}{dork}{symbol}"
            else:
                url = f"{site}/{dork}{symbol}"
            res = requests.get(url=url, headers=HEADERS)

            if error_in_body(res):
                if 100 < res.status_code < 400:
                    cur_time = datetime.datetime.now().strftime("%H:%M:%S")
                    print(
                        f"\033[32m\033[1m[{cur_time} - GOOD]\033[0m \033[33m\033[1mSQL-INJECTION IS POSSIBLE\033[0m "
                        f"\033[34m\033[4m{url}\033[0m")
                    with open('inj_sites.txt', 'a+', encoding='utf-8') as file:
                        file.write(f'[SITE] {site}\n'
                                   f'[URL] {url}\n\n')
            else:
                cur_time = datetime.datetime.now().strftime("%H:%M:%S")
                print(
                    f"\033[31m\033[1m[{cur_time} - BAD]\033[0m \033[34m\033[4m{url}\033[0m "
                    f"\033[33m\033[1mNOT INJECTION\033[0m")


def main():
    with ProcessPoolExecutor(max_workers=3) as ex:
        ex.map(start_check, SITES)

    try:
        with open('inj_sites.txt', 'r') as f:
            urls = f.readlines()
        counter = len(urls)

    except FileNotFoundError:
        counter = 0

    return print(
        f"\n\033[33m\033[1m[INFO]\033[0m \033[34m\033[1m{counter}\033[0m "
        f"SQL-INJECTIONS URLS WRITTEN TO \033[31m\033[4minj_sites.txt\033[0m\n")


if __name__ == "__main__":
    preview_text = Figlet(font='doom', width=200)
    text = preview_text.renderText('SQL - Injections  Checker')
    print(f'\033[35m\033[1m{text}\033[0m')

    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[33m\033[1m[INFO]\033[0m PROGRAM STOPPED BY USER\n")
