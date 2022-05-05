from argparse import Namespace

from bs4 import BeautifulSoup
from bs4.element import ResultSet
from requests import get
from requests.models import Response

from congress.args import memberArgs

def getRequest(url: str)    -> Response:
    return get(url)

def buildSoup(resp: Response)   ->  BeautifulSoup:
    return BeautifulSoup(markup=resp.content, features="lxml")

def getElements(soup: BeautifulSoup)    ->  ResultSet:
    return soup.find_all(name="li", attrs={"class": "expanded"})

def extractMembers(data: ResultSet, df)

def main()  ->  None:
    args: Namespace = memberArgs()

    resp: Response = getRequest('https://www.congress.gov/search?q={%22source%22:%22members%22}&pageSize=250')

    soup: BeautifulSoup = buildSoup(resp)

    print(getElements(soup))
