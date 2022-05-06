from argparse import Namespace
from re import findall

import pandas
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from pandas import DataFrame
from progress.bar import Bar
from requests import get
from requests.models import Response

from congress.args import billsArgs


def getRequest(url: str) -> Response:
    return get(url)


def buildSoup(resp: Response) -> BeautifulSoup:
    return BeautifulSoup(markup=resp.content, features="lxml")


def getPageCount(soup: BeautifulSoup) -> int:
    pagination: Tag = soup.find(name="div", attrs={"class": "pagination"})
    try:
        pageCountText: str = pagination.findChild(
        name="span", attrs={"class": "results-number"}
    ).text
    except AttributeError:
        return 0
    return int(findall("\d+", pageCountText)[0])


def getElements(soup: BeautifulSoup) -> ResultSet:
    return soup.find_all(name="li", attrs={"class": "expanded"})


def main() -> None:
    args: Namespace = billsArgs()
    dfList: list = []

    searchURL: str = "https://www.congress.gov/quick-search/legislation?wordsPhrases=&wordVariants=on&congressGroups%5B%5D=0&congressGroups%5B%5D=1&congresses%5B%5D=all&legislationNumbers=&legislativeAction=&sponsor=on&representative={}&senator={}"

    memberDF: DataFrame = pandas.read_json(args.input).T

    with Bar("Scraping legislature data from https://congress.gov...", max=memberDF.shape[0]) as bar:

        for row in memberDF.itertuples(index=False):
            url: str = ""
            if row.Senator and row.Representative:
                url = searchURL.format(row.Key, row.Key)
            elif row.Senator:
                url = searchURL.format("", row.Key)
            elif row.Representative:
                url = searchURL.format(row.Key, "")
            else:
                url = searchURL.format("", "")

            resp: Response = getRequest(url)
            soup: BeautifulSoup = buildSoup(resp)
            pageCount: int = getPageCount(soup)

            print(pageCount)
            bar.next()
