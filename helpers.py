"""
This contains helper functions for manipulating the excel file data

"""

import datetime
from datetime import date
from typing import List

import openpyxl


async def get_full_month_name(month_number: int):
    """
    Converts month_number to full month name
    :param month_number:
    :return:
    """

    if 1 <= month_number <= 12:
        month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                       "November", "December"]
        return month_names[month_number - 1]
    else:
        raise ValueError("Invalid month number")


async def get_short_month_name(month_number: str):
    """
    Converts month_number to short month name
    :param month_number:
    :return:
    """
    month_number = int(month_number)

    if 1 <= month_number <= 12:
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        return month_names[month_number - 1]
    else:
        raise ValueError("Invalid month number")


async def format_date_string(date_string):
    """
    Formats a date string from the format "YYYY-MM-DD HH:MM:SS" to "YYYY-MM-DD".

    Args:
        date_string (str): The date string to format.

    Returns:
        dict: The formatted date dict.
    """
    # Split the date string into date and time components
    date_time_components = date_string.strftime("%d-%m-%y %H:%M:%S").split(" ")

    # date_time_components = date_string.split(" ")
    date_component = date_time_components[0]

    components = date_component.split("-")
    year = int(components[2])
    month = int(components[1])
    day = int(components[0])

    # Create a dictionary with the year, month, and day
    date_dict = {
        "year": year,
        "month": month,
        "day": day,
    }

    return date_dict
    # return date_component


async def filter_excel_data(file_path, worksheet):
    wb = openpyxl.load_workbook(file_path)
    ws = wb[worksheet]
    filtered_rows = []
    for row in ws.rows:
        filtered_rows.append(row)

    return filtered_rows


# Function to group the data into the required structure
async def group_zero_cover_percentage_data(rows, day_range: List, month_range: List, year_range: List):
    """
    Groups the data passed in as rows into a dict of this structure
    the_dict = {"the_restaurant":{
                  "with_covers":1
                  "with_zero_covers":23,
                  "total": 24,
                  "zero_cover_percentage": 0.01}}

    :param year_range: 
    :param month_range: 
    :param day_range: 
    :param rows: 
   
    :return: dict
    """""
    rows.pop(0)  # remove header row
    data = {}

    # Positions of relevant columns
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
        business_date = await format_date_string(business_date)
        restaurant_name = row[restaurant_position].value
        with_covers = int(row[with_covers_position].value)
        with_zero_covers = int(row[with_zero_covers_position].value)
        total_checks = int(row[total_checks_position].value)

        if business_year in year_range and business_month in month_range:
            if date(year_range[0], month_range[0], day_range[0]) < date(business_year,
                                                                        business_month,
                                                                        business_date["day"]) < date(year_range[1],
                                                                                                     month_range[
                                                                                                         1],
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
                        "total_checks"] if data[restaurant_name]["total_checks"] > 0 else 0
                    data[restaurant_name]["zero_covers_percentage"] = zero_cover_percentage
            else:
                # Skip processing if the business date is not within the date range
                pass
        else:
            # Skip processing if the business year or month is not within the respective ranges
            pass

    return data


async def group_takeaway_cover_percentage_data(rows, day_range: List, month_range: List, year_range: List):
    """
    Groups the data passed in as rows into a dict of this structure
    the_dict = {"the_restaurant":{
                  "non_takeaway_covers":1
                  "takeaway_covers":23,
                  "total_covers": 24,
                  "takeaway_cover_percentage": 0.01}}
    :param year_range: 
    :param month_range: 
    :param day_range: 
    :param rows: 
   
    :return: 
    """""
    rows.pop(0)  # remove header row
    data = {}

    # Positions of relevant columns
    business_year_position = 1
    business_month_position = 2
    business_date_position = 3
    restaurant_position = 5
    non_takeaway_covers_position = 8
    takeaway_covers_position = 9
    total_covers_position = 10

    # Process each row and update the data structure
    for row in rows:
        business_year = int(row[business_year_position].value)
        business_month = int(row[business_month_position].value)
        business_date = row[business_date_position].value
        business_date = await format_date_string(business_date)
        restaurant_name = row[restaurant_position].value
        non_takeaway_covers = int(row[non_takeaway_covers_position].value)
        takeaway_covers = int(row[takeaway_covers_position].value)
        total_covers = int(row[total_covers_position].value)

        if business_year in year_range and business_month in month_range:
            if date(year_range[0], month_range[0], day_range[0]) < date(business_year,
                                                                        business_month,
                                                                        business_date["day"]) < date(year_range[1],
                                                                                                     month_range[1],
                                                                                                     day_range[1]):
                # Process the data if all conditions are met
                if restaurant_name not in data:
                    data[restaurant_name] = {
                        "non_takeaway_covers": non_takeaway_covers,
                        "takeaway_covers": takeaway_covers,
                        "total_covers": total_covers
                    }

                else:
                    data[restaurant_name]["non_takeaway_covers"] += non_takeaway_covers
                    data[restaurant_name]["takeaway_covers"] += takeaway_covers
                    data[restaurant_name]["total_covers"] += total_covers
                    # Calculate zero cover percentage
                    takeaway_cover_percentage = data[restaurant_name]["takeaway_covers"] / data[restaurant_name][
                        "total_covers"] if data[restaurant_name]["total_covers"] != 0 else 0
                    data[restaurant_name]["takeaway_covers_percentage"] = takeaway_cover_percentage
            else:
                # Skip processing if the business date is not within the date range
                pass
        else:
            # Skip processing if the business year or month is not within the respective ranges
            pass

    return data


async def group_revenue_outside_operating_hours_percentage_data(rows, day_range: List, month_range: List,
                                                                year_range: List):
    """
    Groups the data passed in as rows into a dict of this structure
    the_dict = {"the_restaurant":{
                  "op_hrs_revenue":1
                  "closed_hrs_revenue":23,
                  "total_revenue": 24,
                  "revenue_outside_operating_hours_percentage": 0.01}}
    
    :param year_range: 
    :param month_range: 
    :param day_range: 
    :param rows: 
   
    :return: 
    """""
    rows.pop(0)  # remove header row
    data = {}

    # Positions of relevant columns
    business_year_position = 1
    business_month_position = 2
    business_date_position = 3
    restaurant_position = 5
    op_hrs_revenue_position = 11
    closed_hrs_revenue_position = 12

    # Process each row and update the data structure
    for row in rows:
        business_year = int(row[business_year_position].value)
        business_month = int(row[business_month_position].value)
        business_date = row[business_date_position].value
        business_date = await format_date_string(business_date)
        restaurant_name = row[restaurant_position].value
        op_hrs_revenue = float(row[op_hrs_revenue_position].value)
        closed_hrs_revenue = float(row[closed_hrs_revenue_position].value)
        total_revenue = op_hrs_revenue + closed_hrs_revenue

        if business_year in year_range and business_month in month_range:
            if date(year_range[0], month_range[0], day_range[0]) < date(business_year,
                                                                        business_month,
                                                                        business_date["day"]) < date(year_range[1],
                                                                                                     month_range[1],
                                                                                                     day_range[1]):
                # Process the data if all conditions are met
                if restaurant_name not in data:
                    data[restaurant_name] = {
                        "op_hrs_revenue": op_hrs_revenue,
                        "closed_hrs_revenue": closed_hrs_revenue,
                        "total_revenue": total_revenue
                    }

                else:
                    data[restaurant_name]["op_hrs_revenue"] += op_hrs_revenue
                    data[restaurant_name]["closed_hrs_revenue"] += closed_hrs_revenue
                    data[restaurant_name]["total_revenue"] += total_revenue
                    # Calculate zero cover percentage
                    closed_hrs_revenue_percentage = data[restaurant_name]["closed_hrs_revenue"] / data[restaurant_name][
                        "total_revenue"]
                    data[restaurant_name]["closed_hrs_revenue_percentage"] = closed_hrs_revenue_percentage
            else:
                # Skip processing if the business date is not within the date range
                pass
        else:
            # Skip processing if the business year or month is not within the respective ranges
            pass

    return data


async def group_meal_duration_percentage_data(rows, day_range: List, month_range: List, year_range: List):
    """
    Groups the data passed in as rows into a dict of this structure
    the_dict = {"the_restaurant":{
                  "within_time_frame":1
                  "more_than_4hrs":23,
                  "less_than_5mins": 24,
                  "total_counts": 25,
                  "more_than_4hrs_percentage": 0.2,
                  "less_than_5mins_percentage": 0.01
                  }}
    
    :param year_range: 
    :param month_range: 
    :param day_range: 
    :param rows: 
   
    :return: 
    """""
    rows.pop(0)  # remove header row
    data = {}


    # Positions of relevant columns
    business_year_position = 1
    business_month_position = 2
    business_date_position = 3
    restaurant_position = 5
    within_time_frame_position = 8
    more_than_4hrs_position = 9
    less_than_5mins_position = 10
    total_counts_position = 11

    # Process each row and update the data structure
    for row in rows:


        business_year = row[business_year_position].value
        business_month = row[business_month_position].value
        business_date = row[business_date_position].value
        business_date = await format_date_string(business_date)
        restaurant_name = row[restaurant_position].value
        within_time_frame = int(row[within_time_frame_position].value)
        more_than_4hrs = int(row[more_than_4hrs_position].value)
        less_than_5mins = int(row[less_than_5mins_position].value)
        total_counts = int(row[total_counts_position].value)

        if business_year in year_range and business_month in month_range:

            if date(year_range[0], month_range[0], day_range[0]) < date(business_year,
                                                                        business_month,
                                                                        business_date["day"]) < date(year_range[1],
                                                                                              month_range[1],
                                                                                              day_range[1]):

                # Process the data if all conditions are met
                if restaurant_name not in data:

                    data[restaurant_name] = {
                        "within_time_frame": within_time_frame,
                        "more_than_4hrs": more_than_4hrs,
                        "less_than_5mins": less_than_5mins,
                        "total_counts": total_counts,
                        "more_than_4hrs_percentage": 0.0,
                        "less_than_5mins_percentage": 0.0
                    }

                else:
                    data[restaurant_name]["within_time_frame"] += within_time_frame
                    data[restaurant_name]["more_than_4hrs"] += more_than_4hrs
                    data[restaurant_name]["less_than_5mins"] += less_than_5mins
                    data[restaurant_name]["total_counts"] += total_counts

                    # Calculate more_than_4hrs percentage
                    more_than_4hrs_percentage = data[restaurant_name]["more_than_4hrs"] / data[restaurant_name][
                        "total_counts"]
                    data[restaurant_name]["more_than_4hrs_percentage"] = more_than_4hrs_percentage

                    # Calculate less_than_5mins percentage
                    less_than_5mins_percentage = data[restaurant_name]["less_than_5mins"] / data[restaurant_name][
                        "total_counts"]
                    data[restaurant_name]["less_than_5mins_percentage"] = less_than_5mins_percentage
            else:
                # Skip processing if the business date is not within the date range
                pass
        else:
            # Skip processing if the business year or month is not within the respective ranges
            pass

    return data


# Individual Server Sales
async def group_individual_server_sales(rows, day_range: List, month_range: List, year_range: List):
    rows.pop(0)  # remove header row
    data = {}

    business_year_position = 0
    business_month_position = 1
    business_date_position = 2
    restaurant_position = 4
    meal_period_position = 6
    server_id_position = 7
    gross_sales_position = 8

    for row in rows:
        business_year = int(row[business_year_position].value)
        business_month = int(row[business_month_position].value)
        business_date = row[business_date_position].value
        business_date = await format_date_string(business_date)
        restaurant_name = row[restaurant_position].value
        meal_period = row[meal_period_position].value
        server_id = row[server_id_position].value
        gross_sales = row[gross_sales_position].value

        if business_year in year_range and business_month in month_range:
            if date(year_range[0], month_range[0], day_range[0]) < date(business_year,
                                                                        business_month,
                                                                        business_date["day"]) < date(year_range[1],
                                                                                                     month_range[1],
                                                                                                     day_range[1]):
                if restaurant_name not in data:
                    data[restaurant_name] = dict()

                if server_id not in data[restaurant_name]:
                    data[restaurant_name][server_id] = dict()

                if meal_period not in data[restaurant_name][server_id]:
                    data[restaurant_name][server_id] = {
                        meal_period: gross_sales
                    }

    return data


# % Open Items
async def group_open_items_percentage_data(rows, day_range: List, month_range: List, year_range: List):
    """

    :param rows:
    :param day_range:
    :param month_range:
    :param year_range:
    :return:
    """
    rows.pop(0)  # remove header row
    data = {}

    # Positions of relevant columns
    business_year_position = 1
    business_month_position = 2
    business_date_position = 3
    restaurant_position = 5
    open_item_sales_position = 8
    other_item_sales_position = 9
    grand_total_sales_position = 10

    for row in rows:
        business_year = int(row[business_year_position].value)
        business_month = int(row[business_month_position].value)
        business_date = row[business_date_position].value
        business_date = await format_date_string(business_date)
        restaurant_name = row[restaurant_position].value
        open_item_sales = float(row[open_item_sales_position].value)
        other_item_sales = float(row[other_item_sales_position].value)
        grand_total_sales = float(row[grand_total_sales_position].value)

        if business_year in year_range and business_month in month_range:

            if date(year_range[0], month_range[0], day_range[0]) < date(business_year,
                                                                        business_month,
                                                                        business_date["day"]) < date(year_range[1],
                                                                                                     month_range[1],
                                                                                                     day_range[1]):

                if restaurant_name not in data:
                    data[restaurant_name] = {
                        "open_item_sales": open_item_sales,
                        "other_item_sales": other_item_sales,
                        "grand_total_sales": grand_total_sales,
                        "open_item_sales_percentage": 0.0
                    }

                else:
                    data[restaurant_name]["open_item_sales"] += open_item_sales
                    data[restaurant_name]["other_item_sales"] += other_item_sales
                    data[restaurant_name]["grand_total_sales"] += grand_total_sales

                    # Calculate open item sales percentage
                    open_item_sales_percentage = data[restaurant_name]["open_item_sales"] / data[restaurant_name][
                        "grand_total_sales"]
                    data[restaurant_name]["open_item_sales_percentage"] = open_item_sales_percentage

            else:
                # Skip processing if the business date is not within the date range
                pass
        else:
            # Skip processing if the business year or month is not within the respective ranges
            pass

    return data
