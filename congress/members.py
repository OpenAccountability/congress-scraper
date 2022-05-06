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


def extractMembers(dataset: ResultSet) -> DataFrame:
    data: dict = {
        "Last Name": [],
        "First Name": [],
        "Key": [],
        "Senator": [],
        "Representative": [],
        "URL": [],
    }

    tag: Tag
    for tag in dataset:
        resultHeading: Tag = tag.findChild(
            name="span", attrs={"class": "result-heading"}
        )
        memberServed: Tag = tag.findChild(
            name="ul", attrs={"class": "member-served"}, recursive=True
        )

        heading: str = resultHeading.text
        heading.replace(",", "")
        splitHeading: list = heading.split(" ")

        data["Last Name"].append(splitHeading[1])
        data["First Name"].append(splitHeading[2])

        uri: str = resultHeading.findChild("a").get("href")
        data["URL"].append("https://congress.gov" + uri)
        data["Key"].append(uri.split("/")[-1].split("?")
                           [0])  # TODO: Replace with regex

        # TODO: Replace with a more concise solution
        if len(memberServed.find_all()) == 2:
            data["Senator"].append(True)
            data["Representative"].append(True)
        else:
            if memberServed.findChild(name="li").text[0] == "S":
                data["Senator"].append(True)
                data["Representative"].append(False)
            else:
                data["Senator"].append(False)
                data["Representative"].append(True)

    return DataFrame(data)


def main() -> None:
    args: Namespace = memberArgs()

    dfList: list = []
    url: str = (
        "https://www.congress.gov/search?q={%22source%22:%22members%22}&pageSize=250"
    )

    with Bar("Scraping Congress member data from https://congress.gov... ") as bar:

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
    df.T.to_csv(args.output)
