import pandas as pd
import os
import re
from pandas import DataFrame
from pathlib import Path

base_directory = Path(__file__).parents[0]


class DataFrameBuilder:
    def __init__(self) -> None:
        pass

    def createDataFrame(self, downloaded_files_folder: Path, file_name: str) -> DataFrame:
        # Extract the year, quarter, city, and data type from the filename
        match = re.search(
            r"(?P<year>\d+)_(?P<quarter>\d)_(?P<city_code>\w)_lvr_land_(?P<transaction_type>\w).csv",
            file_name,
        )
        year = match.group("year")
        quarter = match.group("quarter")
        city_code = match.group("city_code")
        transaction_type = match.group("transaction_type")

        # Set the header as the second row in English
        df = pd.read_csv(os.path.join(downloaded_files_folder, file_name), header=1)
        df["df_name"] = f"{year}_{quarter}_{city_code}_{transaction_type}"

        return df

    def mergeAllDataFrames(self, downloaded_files_folder: Path) -> DataFrame:
        # Get all files that match the filename pattern
        files = []
        for file_name in os.listdir(downloaded_files_folder):
            if "_lvr_land_" in file_name:
                files.append(file_name)

        files_counts = len(files)
        print(f"{files_counts} files will be merge")

        # Create DataFrames
        dfs = []
        for file_name in files:
            df = self.createDataFrame(downloaded_files_folder, file_name)
            dfs.append(df)

        # Merge all DataFrames
        df_all = pd.concat(dfs, ignore_index=True)

        return df_all

    def chineseToInteger(self, chinese_number: str) -> int:
        number_mapping = {
            "一": 1,
            "二": 2,
            "三": 3,
            "四": 4,
            "五": 5,
            "六": 6,
            "七": 7,
            "八": 8,
            "九": 9,
            "十": 10,
        }

        number = 0
        for chinese in chinese_number:
            if chinese == "十":
                number = 10 if number == 0 else number * 10
            elif chinese not in number_mapping:
                assert False, f"undefined string: {chinese_number}"
            else:
                number += number_mapping[chinese]

        return number

    def processFloor(self, floor):
        if not isinstance(floor, str):
            return 0 if pd.isnull(floor) else floor

        floor = floor.strip().replace("層", "")
        if re.match(r"^[一二三四五六七八九十百]+$", floor):
            return self.chineseToInteger(floor)
        return 0

    def filterImpl(self, df: DataFrame):
        filter_main_user = df["main use"] == "住家用"
        filter_state = df["building state"].apply(
            lambda value: re.search("住宅大樓", value)
        )
        filter_floor = df["total floor number"].apply(self.processFloor) >= 13

        return filter_main_user & filter_state & filter_floor

    def filterAndExport(self, df_all: DataFrame, data_folder: Path):
        filter = self.filterImpl(df_all)
        filtered_df = df_all.loc[filter]

        # export filtered data to filter.csv
        file_path = data_folder.joinpath("filter.csv")
        filtered_df.to_csv(file_path, index=False)

        print(f"export filtered data to file ({file_path})")

    def countImpl(self, df_all: DataFrame):
        total_items = len(df_all)
        total_berths = (
            df_all["transaction pen number"]
            .str.split(pat="車位", n=1, expand=True)[1]
            .astype("int")
            .sum()
        )
        avg_price = df_all["total price NTD"].mean(axis=0)
        avg_berth_total_price = (
            df_all["the berth total price NTD"]
            .where(df_all["the berth total price NTD"] != 0)
            .mean(axis=0)
        )

        counted_df = {
            "Total items": total_items,
            "Total berths": total_berths,
            "Average price": avg_price,
            "Average berth total price": avg_berth_total_price,
        }

        return pd.DataFrame([counted_df])

    def countAndExport(self, df_all: DataFrame, data_folder: Path):
        counted_df = self.countImpl(df_all)

        # export counted data to count.csv
        file_path = data_folder.joinpath("count.csv")
        counted_df.to_csv(file_path, index=False)

        print(f"export counted data to file ({file_path})")


if __name__ == "__main__":
    df_builder = DataFrameBuilder()

    downloaded_files_folder = Path(base_directory).joinpath("downloaded_files")
    data_folder = Path(base_directory).joinpath("data")

    df_all = df_builder.mergeAllDataFrames(downloaded_files_folder)

    df_builder.filterAndExport(df_all, data_folder)
    df_builder.countAndExport(df_all, data_folder)
