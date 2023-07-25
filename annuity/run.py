import sys

from cashflower import start
from annuity.settings import settings


if __name__ == "__main__":
    start("annuity", settings, sys.argv)
