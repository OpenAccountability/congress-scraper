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


def extractBills(dataset: ResultSet, sponsorKey: str) -> DataFrame:
    data: dict = {
        "Bill": [],
        "Congress Session": [],
        "Sponsor Key": [],
        "Bill URL": [],
        "Cosponsor URL": [],
    }
    tag: Tag
    for tag in dataset:
        data["Sponsor Key"].append(sponsorKey)

        resultHeading: Tag = tag.findChild(
            name="span", attrs={"class": "result-heading"}
        )
        congressSession: str = int(findall("\d+", resultHeading.text.split('—')[1].strip().split(' ')[0])[0]) # TODO: Make this more concise
        data["Congress Session"].append(congressSession)

        uri: Tag = resultHeading.findChild("a")
        uriHREF: str = uri.get("href")
        data["Bill URL"].append("https://congress.gov" + uriHREF)
        data["Cosponsor URL"].append(
            "https://congress.gov" + uriHREF.split("?")[0] + "/cosponsor"
        )  # TODO: Make this more concise
        data["Bill"].append(uri.text)

    return DataFrame(data)


def main() -> None:
    args: Namespace = billsArgs()
    dfList: list = []

    searchURL: str = "https://www.congress.gov/quick-search/legislation?wordsPhrases=&wordVariants=on&congressGroups%5B%5D=0&congressGroups%5B%5D=1&congresses%5B%5D=all&legislationNumbers=&legislativeAction=&sponsor=on&representative={}&senator={}"

    memberDF: DataFrame = pandas.read_json(args.input).T

    with Bar(
        "Scraping legislature data from https://congress.gov...", max=memberDF.shape[0]
    ) as bar:

        for row in memberDF.itertuples(index=False):
            url: str = searchURL.format(row.Key, row.Key)

            resp: Response = getRequest(url)
            soup: BeautifulSoup = buildSoup(resp)
            pageCount: int = getPageCount(soup)

            data: ResultSet = getElements(soup)
            dfList.append(extractBills(dataset=data, sponsorKey=row.Key))

            bar.next()

            page: int
            for page in range(2, pageCount + 1):
                url = searchURL.format(row.Key, row.Key) + f"&page={page}"
                resp: Response = getRequest(url)
                soup: BeautifulSoup = buildSoup(resp)
                data: ResultSet = getElements(soup)
                dfList.append(extractBills(dataset=data, sponsorKey=row.Key))
            bar.next()

    df: DataFrame = pandas.concat(dfList, ignore_index=True)
    df.T.to_json(args.output)
