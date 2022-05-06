from argparse import Namespace
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


def _extractCommittee(committeeStr: str)    ->  tuple:
    splitCommittee: list = committeeStr.split("|")
    return ()

def extractMembers(dataset: ResultSet) -> DataFrame:
    data: dict = {"Bill Code": [], "Title": [], "Committees": [], "URL": []}

    tag: Tag
    for tag in dataset:
        elementHeading: Tag = tag.findChild(name="span", attrs={"class": "result-heading"})
        elementTitle: Tag = tag.findChild(name="span", attrs={"class": "result-title"})

        heading: str = elementHeading.text
        splitHeading: list = heading.split(" ")

        title: str = elementTitle.text

        data["Bill Code"].append(splitHeading[0])
        data["URL"].append("https://congress.gov" + elementHeading.findChild("a").get("href"))

        data["Title"].append(title)
        data["First Name"].append(splitTitle[2])

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

        data: ResultSet = getElements(soup)
        dfList.append(extractMembers(dataset=data))
        bar.next()

        page: int
        for page in range(2, pageCount + 1):
            url = (
                "https://www.congress.gov/search?q={%22source%22:%22members%22}&pageSize=250&page="
                + str(page)
            )
            resp: Response = getRequest(url)
            soup: BeautifulSoup = buildSoup(resp)
            data: ResultSet = getElements(soup)
            dfList.append(extractMembers(dataset=data))
            bar.next()

    df: DataFrame = pandas.concat(dfList, ignore_index=True)
    df.T.to_json(args.output)
