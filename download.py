"""
# Question 1
不限制方式下載【內政部不動產時價登錄網 】中,【106年第1季】~【109年第4季】、位於【臺北市/新北市/高雄市】的
【不動產買賣】資料,【桃園市/臺中市】 的【預售屋買賣】資料,下載檔案格式選擇【CSV格式】,請選擇【非本期下載】。

# Question 2
使用【Pandas】,讀取所有檔名【 ?_lvr_land_? 】的資料集,分別建立 data frame 物件, 設定以【第二列英文】做為
data frame 欄位標頭,並新增欄位【df_name】(內容請用程式將資料補齊,例如: 106年第1季/新北市/不動產買賣 -> 106_1_F_A、
107年第2季/台中市/預售屋買賣-> 107_2_B_B)。
"""

import requests
import os
from pathlib import Path

base_directory = Path(__file__).parents[0]

years = ["106", "107", "108", "109"]
quarters = ["1", "2", "3", "4"]
cities = ["臺北市", "新北市", "高雄市"]
city_codes = ["A", "F", "E"]

presale_cities = ["桃園市", "臺中市"]
presale_city_codes = ["H", "B"]

output_folder = Path(base_directory).joinpath("download_files")
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

root_url = "https://plvr.land.moi.gov.tw/DownloadSeason"

print("== real estate sales ==")
count = 0
for year in years:
    for quarter in quarters:
        for city, city_code in zip(cities, city_codes):
            query_file_name = f"{city_code}_lvr_land_A.csv"  # A:real estate sales
            download_url = (
                f"{root_url}?season={year}S{quarter}&fileName={query_file_name}"
            )

            print(f"download：{year}年第{quarter}季 {city}...")

            response = requests.get(download_url)

            if response.headers["Content-Type"] != "application/octet-stream":
                print(f"fail to download (or empty file)：{year}年第{quarter}季 {city}\n")
                continue

            output_file_name = f"{year}_{quarter}_{query_file_name}"
            output_file = os.path.join(output_folder, output_file_name)
            with open(output_file, "wb") as file:
                file.write(response.content)

            count += 1
            print(f"done to download：{year}年第{quarter}季 {city}\n")

print(f"there is {count} files for real estate sales\n")


print("== pre-sale house sales ==")
count = 0
for year in years:
    for quarter in quarters:
        for city, city_code in zip(presale_cities, presale_city_codes):
            query_file_name = f"{city_code}_lvr_land_B.csv"  # B:pre-sale house sales

            download_url = (
                f"{root_url}?season={year}S{quarter}&fileName={query_file_name}"
            )

            print(f"download：{year}年第{quarter}季 {city}...")

            response = requests.get(download_url)

            if response.headers["Content-Type"] != "application/octet-stream":
                print(f"fail to download (or empty file)：{year}年第{quarter}季 {city}\n")
                continue

            output_file_name = f"{year}_{quarter}_{query_file_name}"
            output_file = os.path.join(output_folder, output_file_name)
            with open(output_file, "wb") as file:
                file.write(response.content)
            
            count += 1
            print(f"done to download：{year}年第{quarter}季 {city}\n")

print(f"there is {count} files for pre-sale house sales\n")