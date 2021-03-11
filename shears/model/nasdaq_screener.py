"""Library for parsing and processing NASDAQ Screener data.

https://www.nasdaq.com/market-activity/stocks/screener
"""
import csv
from dataclasses import dataclass


@dataclass
class StockInfo:
    """Class for info on a stock."""
    symbol: str
    name: str


def parse_nasdaq_screener(filepath: str) -> list[StockInfo]:
    """Parses a NASDAQ screener CSV located at `filepath` into a list."""
    stocks = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stocks.append(StockInfo(row['Symbol'], row['Name']))
    return stocks
