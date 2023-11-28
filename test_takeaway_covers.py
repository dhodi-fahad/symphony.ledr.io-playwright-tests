import pytest
from playwright.async_api import async_playwright, expect

from helpers import group_takeaway_cover_percentage_data
from utils import click_date_range_field, click_start_date_field, select_year, select_month, select_date, \
    click_end_date_field, apply_date_filter


@pytest.mark.asyncio
async def test_takeaway_covers_percentage_data(start_date, end_date, get_worksheet_excel_data):
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

        # the_meal_duration_table = page.get_by_text(
        #     "% Meal Duration > 4hr / <= 5minRestaurant5 min < No of Check<= 4hrNo. of Checks ")
        # await the_meal_duration_table.scroll_into_view_if_needed()

        # 5. Get worksheet data
        ws = 'Table 2'
        ws_data = await get_worksheet_excel_data(ws)

        # Prepare date ranges
        month_range = [start_date["month"], end_date["month"]]
        year_range = [start_date["year"], end_date["year"]]
        day_range = [start_date["day"], end_date["day"]]

        takeaway_cover_percentage_grouped_data = await group_takeaway_cover_percentage_data(ws_data, day_range, month_range, year_range)

        for values in takeaway_cover_percentage_grouped_data:
            restaurant_name = values
            non_takeaway_covers = takeaway_cover_percentage_grouped_data[values]["non_takeaway_covers"]
            takeaway_covers = takeaway_cover_percentage_grouped_data[values]["takeaway_covers"]
            total_covers = takeaway_cover_percentage_grouped_data[values]["total_covers"]
            takeaway_covers_percentage = takeaway_cover_percentage_grouped_data[values]["takeaway_covers_percentage"] * 100
            takeaway_covers_percentage = str(
                int(round(takeaway_covers_percentage) if takeaway_covers_percentage != 0.5 else 1)) + '%'
            print(f'{restaurant_name} {f"{non_takeaway_covers:,}"} {f"{takeaway_covers:,}"} '
                  f'{f"{total_covers:,}"} {takeaway_covers_percentage}')
            expect(page.get_by_role("row",
                                    name=f'{restaurant_name} {f"{non_takeaway_covers:,}"} {f"{takeaway_covers:,}"} '
                                         f'{f"{total_covers:,}"} {takeaway_covers_percentage}').get_by_role(
                "cell").first).to_contain_text(restaurant_name)

