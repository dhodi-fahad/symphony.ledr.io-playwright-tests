"""
This file contains utiliy functions for navigating the UI dashboard and asserting the dashboard data

"""

import datetime
from playwright.sync_api import expect, Playwright, Page
from helpers import get_short_month_name, get_full_month_name


async def click_date_range_field(page):
    """
        This function clicks the date range field on the dashboard.
        Note: The name of the element  is dynamic date range between the current
        date and the date 30 days back
    """
    # Get the current date
    today = datetime.date.today()

    # Get the date 30 days back
    thirty_days_ago = today - datetime.timedelta(days=31)

    # Format the dates as strings
    start_date = thirty_days_ago.strftime('%d/%m/%Y')
    end_date = today.strftime('%d/%m/%Y')
    # Click the button with the dynamic date range
    await page.get_by_role('button', name=f'{start_date} - {end_date}').click()


async def click_start_date_field(page):
    """
    Opens or Closes the start date field when selecting the date ranges

    :param page:
    :return:
    """
    await page.get_by_placeholder("Start Date").click()


async def click_end_date_field(page):
    """
    Opens or Closes the end date field when selecting the date ranges

    :param page:
    :return:
    """
    await page.get_by_placeholder("End Date").click()


async def select_year(page, year):
    """
    Selects the year when filling in the date range e.g. 2020
    :param page:
    :param year:
    :return:
    """
    await page.get_by_role("searchbox").nth(1).click()
    await page.get_by_role("option", name=f'{year}').click()


async def select_month(page, month):
    """
    Selects the month when filling in the date range e.g. Oct

    :param page:
    :param month:
    :return:
    """

    month_name = await get_short_month_name(int(month))
    await page.get_by_role("searchbox").first.click()
    await page.get_by_role("option", name=f'{month_name}').click()


async def select_date(page, date: int, month: int, year: int):
    """
    Selects the actual date when filling in the date range e.g. 1 November 2019
    :param page:
    :param date:
    :param month:
    :param year:
    :return:
    """
    month_name = await get_full_month_name(month)

    await page.get_by_label(f'{int(date)} {month_name} {year}', exact=True).click()


async def apply_date_filter(page):
    """
    Clicks the apply button to apply the date filter
    :param page:
    :return:
    """
    await page.get_by_role("button", name="Apply").click()


async def perform_zero_cover_percentage_table_assertions(page, restaurants):
    for values in restaurants:
        restaurant_name = values
        checks_with_covers = restaurants[values]["with_covers"]
        checks_with_zero_covers = restaurants[values]["with_zero_covers"]
        total_checks = restaurants[values]["total_checks"]
        zero_covers_percentage = restaurants[values]["zero_covers_percentage"] * 100
        zero_covers_percentage = str(int(round(zero_covers_percentage) if zero_covers_percentage != 0.5 else 1)) + '%'
        print(f'{restaurant_name} {f"{checks_with_covers:,}"} {f"{checks_with_zero_covers:,}"} '
              f'{f"{total_checks:,}"} {zero_covers_percentage}')
        expect(page.get_by_role("row",
                                name=f'{restaurant_name} {f"{checks_with_covers:,}"} {f"{checks_with_zero_covers:,}"} '
                                     f'{f"{total_checks:,}"} {zero_covers_percentage}').get_by_role(
            "cell").first).to_contain_text(restaurant_name)


async def perform_takeaway_cover_percentage_table_assertions(page, restaurants):
    for values in restaurants:
        restaurant_name = values
        non_takeaway_covers = restaurants[values]["non_takeaway_covers"]
        takeaway_covers = restaurants[values]["takeaway_covers"]
        total_covers = restaurants[values]["total_covers"]
        takeaway_covers_percentage = restaurants[values]["takeaway_covers_percentage"] * 100
        takeaway_covers_percentage = str(
            int(round(takeaway_covers_percentage) if takeaway_covers_percentage != 0.5 else 1)) + '%'
        print(f'{restaurant_name} {f"{non_takeaway_covers:,}"} {f"{takeaway_covers:,}"} '
              f'{f"{total_covers:,}"} {takeaway_covers_percentage}')
        expect(page.get_by_role("row",
                                name=f'{restaurant_name} {f"{non_takeaway_covers:,}"} {f"{takeaway_covers:,}"} '
                                     f'{f"{total_covers:,}"} {takeaway_covers_percentage}').get_by_role(
            "cell").first).to_contain_text(restaurant_name)


async def perform_revenue_outside_operating_hours_percentage_table_assertions(page, restaurants):
    for values in restaurants:
        restaurant_name = values
        op_hrs_revenue = round(restaurants[values]["op_hrs_revenue"], 2)
        closed_hrs_revenue = round(restaurants[values]["closed_hrs_revenue"], 2)
        total_revenue = round(restaurants[values]["total_revenue"], 2)
        closed_hrs_revenue_percentage = restaurants[values]["closed_hrs_revenue_percentage"] * 100
        closed_hrs_revenue_percentage = str(
            int(round(closed_hrs_revenue_percentage) if closed_hrs_revenue_percentage != 0.5 else 1)) + '%'
        # print(f'{restaurant_name} {"$" + f"{op_hrs_revenue:,}"} {"$" + f"{closed_hrs_revenue:,}"} '
        #       f'{"$" + f"{total_revenue:,}"} {closed_hrs_revenue_percentage}')
        expect(page.get_by_role("row",
                                name=f'{restaurant_name} {"$" + f"{op_hrs_revenue:,}"} {"$" + f"{closed_hrs_revenue:,}"}'
                                     f'{"$" + f"{total_revenue:,}"} {closed_hrs_revenue_percentage}').get_by_role(
            "cell").first).to_contain_text(restaurant_name)


# % Open Items
async def perform_open_items_percentage_table_assertions(page, restaurants):
    for values in restaurants:
        restaurant_name = values
        open_item_sales = restaurants[values]["open_item_sales"]
        other_item_sales = restaurants[values]["other_item_sales"]
        grand_total_sales = restaurants[values]["grand_total_sales"]
        open_item_sales_percentage = restaurants[values]["open_items_percentage"] * 100
        open_item_sales_percentage = str(
            int(round(open_item_sales_percentage) if open_item_sales_percentage != 0.5 else 1)) + '%'
        expect(page.get_by_role("row",
                                name=f'{restaurant_name} {f"{open_item_sales:,}"} {f"{other_item_sales:,}"} {f"{grand_total_sales:,}"} {open_item_sales_percentage}').get_by_role(
            "cell").nth(1)).to_contain_text(restaurant_name)


async def perform_meal_duration_table_assertions(page, restaurants):
    for values in restaurants:
        restaurant_name = values
        within_time_frame = restaurants[values]["within_time_frame"]
        more_than_4hrs = restaurants[values]["more_than_4hrs"]
        less_than_5mins = restaurants[values]["less_than_5mins"]
        total_counts = restaurants[values]["total_counts"]

        # more_than_4hrs_percentage
        more_than_4hrs_percentage = restaurants[values]["more_than_4hrs_percentage"] * 100
        more_than_4hrs_percentage = str(
            int(round(more_than_4hrs_percentage) if more_than_4hrs_percentage != 0.5 else 1)) + '%'

        # less_than_5mins_percentage
        less_than_5mins_percentage = restaurants[values]["less_than_5mins_percentage"]
        less_than_5mins_percentage = str(
            int(round(less_than_5mins_percentage))) + '%'
        print(f'{restaurant_name} {f"{within_time_frame:,}"} {f"{more_than_4hrs:,}"} {f"{less_than_5mins:,}"} '
              f'{f"{total_counts:,}"} {more_than_4hrs_percentage} {less_than_5mins_percentage}')

        the_table = page.locator("#chartContainer-0d33ec1f-4b69-43b9-814b-1777a2d8289c")
        the_restaurant_name = the_table.get_by_role("row",
                                                    name='').locator(
            "div").first.inner_html()
        assert the_restaurant_name == restaurant_name, f"The restaurant name {restaurant_name} is not the same as the table row {the_restaurant_name}"


# Individual Server Sales
"""
Each restaurant has servers(waiters & waitresses with pos devices)- they have server ids - so we track how much
sales each server makes from each meal category in a given period.
"""


async def perform_individual_server_sales_table_assertions(page, restaurants):
    """
    data[restaurant_name][server_id] = {
                        meal_period: gross_sales
                    }
    :param page:
    :param restaurants:
    :return:
    """
    for restaurant in restaurants:
        restaurant_name = restaurant
        for server in restaurant:
            for meal_period in server:
                pass

        # server_id = restaurants[values]["server_id"]
        # total_sales = restaurants[values]["total_sales"]
        #
        #
        # expect(page.get_by_role("row",
        #                         name=f'{restaurant_name} {server_id} {total_sales}').get_by_role(
        #     "cell").first).to_contain_text(restaurant_name)
