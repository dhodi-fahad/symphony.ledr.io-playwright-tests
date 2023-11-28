import pytest
from playwright.async_api import async_playwright, expect
import logging

from helpers import group_meal_duration_percentage_data
from utils import click_date_range_field, click_start_date_field, select_year, select_month, select_date, \
    click_end_date_field, apply_date_filter


@pytest.mark.asyncio
async def test_meal_duration(start_date, end_date, get_worksheet_excel_data):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://test.symphony.ledr.io/dashboards/5fb64e6b-c41c-499b-86e9-2d6c6235f9f5")

        # 1. Open the date filter dialogue
        await click_date_range_field(page)

        # 2. Select the start date
        await click_start_date_field(page)
        await select_year(page, start_date["year"])
        await select_month(page, start_date["month"])
        await select_date(page, start_date["day"], start_date["month"], start_date["year"])
        await click_start_date_field(page)  # Close the date picker

        # 3. Select the end date
        await click_end_date_field(page)
        await select_year(page, end_date["year"])
        await select_month(page, end_date["month"])
        await select_date(page, end_date["day"], end_date["month"], end_date["year"])
        await click_end_date_field(page)  # Close the date picker

        # 4. Apply the selected date range
        await apply_date_filter(page)

        the_table = page.locator("#chartContainer-0d33ec1f-4b69-43b9-814b-1777a2d8289c")
        await the_table.scroll_into_view_if_needed()

        # 5. Get worksheet data
        ws = 'Table 3'
        ws_data = await get_worksheet_excel_data(ws)

        # Prepare date ranges
        month_range = [start_date["month"], end_date["month"]]
        year_range = [start_date["year"], end_date["year"]]
        day_range = [start_date["day"], end_date["day"]]
        meal_duration_grouped_data = await group_meal_duration_percentage_data(ws_data, day_range, month_range,
                                                                               year_range)

        for values in meal_duration_grouped_data:
            restaurant_name = values
            within_time_frame = meal_duration_grouped_data[values]["within_time_frame"]
            more_than_4hrs = meal_duration_grouped_data[values]["more_than_4hrs"]
            less_than_5mins = meal_duration_grouped_data[values]["less_than_5mins"]
            total_counts = meal_duration_grouped_data[values]["total_counts"]
            #
            # more_than_4hrs_percentage
            more_than_4hrs_percentage = meal_duration_grouped_data[values]["more_than_4hrs_percentage"] * 100
            more_than_4hrs_percentage = str(
                int(round(more_than_4hrs_percentage) if more_than_4hrs_percentage != 0.5 else 1)) + '%'

            # less_than_5mins_percentage
            less_than_5mins_percentage = meal_duration_grouped_data[values]["less_than_5mins_percentage"]
            less_than_5mins_percentage = str(
                int(round(less_than_5mins_percentage))) + '%'


            the_table.get_by_role("row",
                                  name=f'{restaurant_name}  {f"{more_than_4hrs:,}"} {f"{less_than_5mins:,}"} '
                                       f'{f"{total_counts:,}"} {more_than_4hrs_percentage} {less_than_5mins_percentage}').locator(
                "div").first.click()
            the_table.get_by_role("row",
                                         name=f'{restaurant_name} {f"{within_time_frame:,}"} {f"{more_than_4hrs:,}"} {f"{less_than_5mins:,}"} '
                                              f'{f"{total_counts:,}"} {more_than_4hrs_percentage} {less_than_5mins_percentage}').locator(
                "div").first.is_enabled()
