import asyncio
from contextlib import suppress
from typing import Iterable, Optional

import requests
from httpx import AsyncClient, ConnectError, ConnectTimeout, Response, Timeout
from pyfiglet import Figlet

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
    "application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/93.0.4577.63 Safari/537.36",
}
SYMBOL = "'"
LIST_WORDS = ["Error", "error", "failed"]
SITES_FILENAME = "./sites.txt"
CHECKERS_LIST_FILENAME = "./checkers_list.txt"


def get_file_lines(filename: str) -> list[str]:
    try:
        with open(filename, encoding="utf-8") as f:
            sites = f.read().split("\n")
            return sites
    except FileNotFoundError:
        raise SystemExit(f"[ERROR]: Please check if file {filename} exists")


def error_in_body(response: Response) -> bool:
    for word in LIST_WORDS:
        if word in response.text:
            return False
    return True


async def fetch(url: str) -> Optional[Response]:
    """Fetch the URL and check next:
    - Status 100 < code < 400
    - No Invalide text from TEXT_TO_MATCH on site
    """
    async with AsyncClient(timeout=Timeout(5, read=None)) as client:
        with suppress(ConnectError, ConnectTimeout):
            response = await client.get(url)
            return response


async def attack(site: str, checkers: list) -> None:
    for payload in checkers:
        url = f"{site}{payload}{SYMBOL}"

        try:
            response = await fetch(url)
            if error_in_body(response):
                print(f"[CHECKING] -> {url}")
                continue
            print("Possible injection")
        except requests.exceptions.ConnectionError:
            print(f"[ERROR]: Connection error {site}")
            return


def main():
    preview_text = Figlet(font="doom", width=200)
    text = preview_text.renderText("SQL-Injections Checker")
    print(text)

    sites: Iterable = (site for site in get_file_lines(SITES_FILENAME) if site)
    checkers = get_file_lines(CHECKERS_LIST_FILENAME)

    loop = asyncio.get_event_loop()
    tasks = [attack(site, checkers) for site in sites]
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()


if __name__ == "__main__":
    main()
