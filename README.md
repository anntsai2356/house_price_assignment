# House Price Assignment

This project is about house price in Taiwan.

The data source is used from [內政部不動產成交案件實際資訊資料供應系統](https://plvr.land.moi.gov.tw/DownloadOpenData), which is the open data provided by the government.

## Purpose
The purpose of this project is to build a data pipeline from downloading multiple files to making a workflow.

## Requirements
- [Python](https://www.python.org/) > 3.11.2
- [pandas](https://pandas.pydata.org/) >= 2.0.2
- [requests](https://pypi.org/project/requests/) >= 2.28.2

## Features
 - Download files
 - Data Applications
   - Filter
   - Count

## Installation
Clone the repository into your develop environment.

## Usage

### Download Files
1. Set conditions for downloading in `conditions.py`.
    The conditions which you need to give:
     - years
     - quarters
     - real_estate_cities
     - pre_sale_cities
     - transaction_types
2. Run `downloader.py`
    ```
    python downloader.py
    ```
3. The downloaded files are saved in `downloaded_files` folder.

### Data Applications
There have some examples in `dataframe_builder.py` for filtering or counting data.
