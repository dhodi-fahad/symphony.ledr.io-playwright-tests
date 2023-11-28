import pytest
from playwright.async_api import async_playwright, expect

from helpers import group_open_items_percentage_data
from utils import click_date_range_field, click_start_date_field, select_year, select_month, select_date, \
    click_end_date_field, apply_date_filter


@pytest.mark.asyncio
async def test_open_items(start_date, end_date, get_worksheet_excel_data):
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

        the_open_items_table = page.get_by_text(
            "% Open ItemsRestaurantOpen Item SalesOther SalesTotal Revenue% Open ItemsOrchard")

        # await the_open_items_table.scroll_into_view_if_needed()

        # 5. Get worksheet data
        ws = 'Table 4'
        ws_data = await get_worksheet_excel_data(ws)

        # Prepare date ranges
        month_range = [start_date["month"], end_date["month"]]
        year_range = [start_date["year"], end_date["year"]]
        day_range = [start_date["day"], end_date["day"]]

        open_items_grouped_data = await group_open_items_percentage_data(ws_data, day_range, month_range,
                                                                         year_range)

        for values in open_items_grouped_data:
            restaurant_name = values
            open_item_sales = open_items_grouped_data[values]["open_item_sales"]
            other_item_sales = open_items_grouped_data[values]["other_item_sales"]
            grand_total_sales = open_items_grouped_data[values]["grand_total_sales"]
            open_item_sales_percentage = open_items_grouped_data[values]["open_item_sales_percentage"] * 100
            open_item_sales_percentage = str(
                int(round(open_item_sales_percentage) if open_item_sales_percentage != 0.5 else 1)) + '%'
            expect(the_open_items_table.get_by_role("row",
                                                    name=f'{restaurant_name} {f"{open_item_sales:,}"} {f"{other_item_sales:,}"} {f"{grand_total_sales:,}"} {open_item_sales_percentage}').get_by_role(
                "cell").nth(1)).to_contain_text(restaurant_name)

