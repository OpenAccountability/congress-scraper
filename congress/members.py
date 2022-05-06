from argparse import Namespace

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from pandas import DataFrame
from requests import get
from requests.models import Response

from congress.args import memberArgs


def getRequest(url: str) -> Response:
    return get(url)


def buildSoup(resp: Response) -> BeautifulSoup:
    return BeautifulSoup(markup=resp.content, features="lxml")


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

    columns: list = ["Last Name", "First Name", "URL"]

    df: DataFrame = DataFrame(columns=columns)

    resp: Response = getRequest(
        "https://www.congress.gov/search?q={%22source%22:%22members%22}&pageSize=250"
    )

    soup: BeautifulSoup = buildSoup(resp)

    data: ResultSet = getElements(soup)

    extractMembers(data, df)
