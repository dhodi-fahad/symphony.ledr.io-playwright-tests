import pytest
import openpyxl
from datetime import date

from helpers import format_date_string


@pytest.fixture
def start_date():
    return {
        "year": 2019,
        "month": 11,
        "day": 1
    }


@pytest.fixture
def end_date():
    return {
        "year": 2023,
        "month": 11,
        "day": 15
    }


@pytest.fixture
def get_worksheet_excel_data():
    async def _filtered_excel_data(worksheet: str) -> list:
        """
        Returns a list of rows from the worksheet
        :param worksheet:
        :return:
        """
        file_path = './thedata.xlsx'
        wb = openpyxl.load_workbook(file_path)
        ws = wb[worksheet]
        filtered_rows = []
        for row in ws.rows:
            filtered_rows.append(row)

        return filtered_rows

    return _filtered_excel_data


@pytest.fixture
def zero_cover_percentage_data(start_date, end_date):
    async def _group_zero_cover_percentage_data(rows):
        rows.pop(0)  # remove header row
        data = {}

        month_range = [start_date["month"], end_date["month"]]
        year_range = [start_date["year"], end_date["year"]]
        day_range = [start_date["day"], end_date["day"]]

        # Positions of relevant columns (consider these constants)
        business_year_position = 1
        business_month_position = 2
        business_date_position = 3
        restaurant_position = 5
        with_covers_position = 8
        with_zero_covers_position = 9
        total_checks_position = 10
        # Process each row and update the data structure
        for row in rows:
            business_year = int(row[business_year_position].value)
            business_month = int(row[business_month_position].value)
            business_date = row[business_date_position].value
            business_date = await format_date_string(business_date)  # Assuming format_date_string exists
            restaurant_name = row[restaurant_position].value
            with_covers = int(row[with_covers_position].value)
            with_zero_covers = int(row[with_zero_covers_position].value)
            total_checks = int(row[total_checks_position].value)

            if business_year in year_range and business_month in month_range:
                if date(year_range[0], month_range[0], day_range[0]) < date(business_date["year"],
                                                                            business_date["month"],
                                                                            business_date["day"]) < date(year_range[1],
                                                                                                         month_range[1],
                                                                                                         day_range[1]):
                    # Process the data if all conditions are met
                    if restaurant_name not in data:
                        data[restaurant_name] = {
                            "with_covers": with_covers,
                            "with_zero_covers": with_zero_covers,
                            "total_checks": total_checks
                        }

                    else:
                        data[restaurant_name]["with_covers"] += with_covers
                        data[restaurant_name]["with_zero_covers"] += with_zero_covers
                        data[restaurant_name]["total_checks"] += total_checks
                        # Calculate zero cover percentage
                        zero_cover_percentage = data[restaurant_name]["with_zero_covers"] / data[restaurant_name][
                            "total_checks"]
                        data[restaurant_name]["zero_covers_percentage"] = zero_cover_percentage
                else:
                    # Skip processing if the business date is not within the date range
                    pass
            else:
                # Skip processing if the business year or month is not within the respective ranges
                pass

        return data

    return _group_zero_cover_percentage_data
