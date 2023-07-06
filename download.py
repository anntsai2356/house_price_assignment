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

root_url = "https://plvr.land.moi.gov.tw/DownloadSeason"

years = ["106", "107", "108", "109"]
quarters = ["1", "2", "3", "4"]
real_estate_cities = {
    "A": "臺北市",
    "F": "新北市",
    "E": "高雄市",
}
pre_sale_cities = {
    "H": "桃園市",
    "B": "臺中市",
}

transaction_types = {
    "A": {
        "name": "real estate sales",
        "cities": real_estate_cities,
    },
    "B": {
        "name": "pre-sale house sales",
        "cities": pre_sale_cities,
    },
}

output_folder = Path(base_directory).joinpath("download_files")
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for transaction_type, transaction_type_info in transaction_types.items():
    count = 0
    print(f"=== {transaction_type_info['name']} ===\n")

    for city_code, city_name in transaction_type_info["cities"].items():
        for year in years:
            for quarter in quarters:
                query_file_name = f"{city_code}_lvr_land_{transaction_type}.csv"
                download_url = (
                    f"{root_url}?season={year}S{quarter}&fileName={query_file_name}"
                )

                print(f"download：{year}year S{quarter} {city_name}...")

                response = requests.get(download_url)

                if response.headers["Content-Type"] != "application/octet-stream":
                    print(
                        f"fail to download (or empty file)：{year}year S{quarter} {city_name}\n"
                    )
                    continue

                output_file_name = f"{year}_{quarter}_{query_file_name}"
                output_file = os.path.join(output_folder, output_file_name)
                with open(output_file, "wb") as file:
                    file.write(response.content)

                count += 1
                print(f"done to download：{year}year S{quarter} {city_name}\n")

    print(f"there is {count} files for {transaction_type_info['name']}\n")
