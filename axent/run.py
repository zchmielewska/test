import sys

from cashflower import start
from axent.settings import settings


if __name__ == "__main__":
    start("axent", settings, sys.argv)
