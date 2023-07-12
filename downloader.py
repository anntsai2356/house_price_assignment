import requests
import os
from pathlib import Path

base_directory = Path(__file__).parents[0]


class Downloader:
    def __init__(self) -> None:
        self.root_url = "https://plvr.land.moi.gov.tw/DownloadSeason"
        self.output_folder_path = Path(base_directory).joinpath("downloaded_files")
        self.checkFolder(self.output_folder_path)

    def checkFolder(self, output_folder_path: Path) -> None:
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

    def run(self, transaction_types: dict, years: list, quarters: list) -> None:
        for transaction_type, transaction_type_info in transaction_types.items():
            count = 0
            print(f"=== {transaction_type_info['name']} ===\n")

            for city_code, city_name in transaction_type_info["cities"].items():
                for year in years:
                    for quarter in quarters:
                        query_file_name = f"{city_code}_lvr_land_{transaction_type}.csv"
                        download_url = f"{self.root_url}?season={year}S{quarter}&fileName={query_file_name}"

                        print(f"download：{year}year S{quarter} {city_name}...")

                        response = requests.get(download_url)

                        if (
                            response.headers["Content-Type"]
                            != "application/octet-stream"
                        ):
                            print(
                                f"fail to download (or empty file)：{year}year S{quarter} {city_name}\n"
                            )
                            continue

                        output_file_name = f"{year}_{quarter}_{query_file_name}"
                        output_file = os.path.join(
                            self.output_folder_path, output_file_name
                        )
                        with open(output_file, "wb") as file:
                            file.write(response.content)

                        count += 1
                        print(f"done to download：{year}year S{quarter} {city_name}\n")

            print(f"there is {count} files for {transaction_type_info['name']}\n")


if __name__ == "__main__":
    from conditions import Conditions

    years = Conditions.years
    quarters = Conditions.quarters
    real_estate_cities = Conditions.real_estate_cities
    pre_sale_cities = Conditions.pre_sale_cities
    transaction_types = Conditions.transaction_types

    downloader = Downloader()
    downloader.run(transaction_types, years, quarters)
