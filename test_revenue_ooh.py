import pytest
from playwright.async_api import async_playwright, expect

from helpers import group_revenue_outside_operating_hours_percentage_data
from utils import click_date_range_field, click_start_date_field, select_year, select_month, select_date, \
    click_end_date_field, apply_date_filter


@pytest.mark.asyncio
async def test_revenue_outside_operating_hours_percentage_data(start_date, end_date, get_worksheet_excel_data):
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

        # Scroll to Revenue Table
        revenue_table = page.locator("#chartContainer-ae3bf334-0ffe-4489-b5d0-fec4e73379a2")
        await revenue_table.scroll_into_view_if_needed()


        # 5. Get worksheet data
        ws = 'Table 7'
        ws_data = await get_worksheet_excel_data(ws)

        month_range = [start_date["month"], end_date["month"]]
        year_range = [start_date["year"], end_date["year"]]
        day_range = [start_date["day"], end_date["day"]]

        revenue_outside_operating_hours_grouped_data = await group_revenue_outside_operating_hours_percentage_data(
            ws_data, day_range, month_range, year_range)
        for values in revenue_outside_operating_hours_grouped_data:
            restaurant_name = values
            op_hrs_revenue = round(revenue_outside_operating_hours_grouped_data[values]["op_hrs_revenue"], 2)
            closed_hrs_revenue = round(revenue_outside_operating_hours_grouped_data[values]["closed_hrs_revenue"], 2)
            total_revenue = round(revenue_outside_operating_hours_grouped_data[values]["total_revenue"], 2)
            closed_hrs_revenue_percentage = revenue_outside_operating_hours_grouped_data[values][
                                                "closed_hrs_revenue_percentage"] * 100
            closed_hrs_revenue_percentage = str(
                int(round(closed_hrs_revenue_percentage) if closed_hrs_revenue_percentage != 0.5 else 1)) + '%'
            # print(f'{restaurant_name} {"$" + f"{op_hrs_revenue:,}"} {"$" + f"{closed_hrs_revenue:,}"} '
            #       f'{"$" + f"{total_revenue:,}"} {closed_hrs_revenue_percentage}')

            expect(revenue_table.get_by_role("row",
                                                  name=f'{restaurant_name} {"$" + f"{closed_hrs_revenue:,}"} '
                                                       f'{"$" + f"{total_revenue:,}"} {closed_hrs_revenue_percentage}').get_by_role(
                "cell").first).to_have_text(restaurant_name)
