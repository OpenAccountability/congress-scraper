from argparse import Namespace
from distutils.command.build import build
from re import findall

import pandas
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from pandas import DataFrame
from progress.bar import Bar
from requests import get
from requests.models import Response

from congress.args import memberArgs


def getRequest(url: str) -> Response:
    return get(url)


def buildSoup(resp: Response) -> BeautifulSoup:
    return BeautifulSoup(markup=resp.content, features="lxml")


def getPageCount(soup: BeautifulSoup) -> int:
    pagination: Tag = soup.find(name="div", attrs={"class": "pagination"})
    pageCountText: str = pagination.findChild(
        name="span", attrs={"class": "results-number"}
    ).text
    return int(findall("\d+", pageCountText)[0])


def getElements(soup: BeautifulSoup) -> ResultSet:
    return soup.find_all(name="li", attrs={"class": "expanded"})


def extractMembers(dataset: ResultSet) -> DataFrame:
    data: dict = {"Last Name": [], "First Name": [], "URL": []}

    tag: Tag
    for tag in dataset:
        element: Tag = tag.findChild(name="span", attrs={"class": "result-heading"})

        title: str = element.text
        title.replace(",", "")
        splitTitle: list = title.split(" ")

        data["Last Name"].append(splitTitle[1])
        data["First Name"].append(splitTitle[2])
        data["URL"].append("https://congress.gov" + element.findChild("a").get("href"))

    return DataFrame(data)


def main() -> None:
    args: Namespace = memberArgs()

    dfList: list = []
    url: str = (
        "https://www.congress.gov/search?q={%22source%22:%22members%22}&pageSize=250"
    )

    with Bar("Scraping data from https://congress.gov... ") as bar:

        resp: Response = getRequest(url)
        soup: BeautifulSoup = buildSoup(resp)
        pageCount: int = getPageCount(soup)

        bar.max = pageCount
        bar.update()

        page: int
        for page in range(1, pageCount + 1):
            if page == 1:
                data: ResultSet = getElements(soup)
                dfList.append(extractMembers(dataset=data))
            else:
                url = (
                    "https://www.congress.gov/search?q={%22source%22:%22members%22}&pageSize=250&page="
                    + str(page)
                )
                resp: Response = getRequest(url)
                soup: BeautifulSoup = buildSoup(resp)
                data: ResultSet = getElements(soup)
                dfList.append(extractMembers(dataset=data))
            bar.next()

    # pandas.concat(dfList).to_json("test.json")
