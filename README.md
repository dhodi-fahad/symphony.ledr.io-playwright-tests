
# Playwright Python Tests for symphony.ledr.io Quality Data Dashboard

This project contains Playwright Python tests to validate the data displayed on the symphony.ledr.io Quality Data dashboard against the data in an Excel file.

## Prerequisites

To run these tests, you will need to have the following installed:


* Python 3.7 or higher: Ensure you have Python 3.7 or higher installed on your system.



1. Create and activate a virtual environment:
```bash
$ python -m venv venv_name 
$ source venv_name/bin/activate  # for Unix/Linux
$ venv_name\Scripts\activate    # for Windows
$ pip install -r requirements.txt 

```


2. Run the tests using pytest:


```bash
$ pytest --numprocesses 2 
```


 This will execute all the Playwright tests in the project and compare the data displayed on the dashboard with the data in the Excel file.

## Important Information

### Covered Dashboard Tables
Out of the 7 tables present on the dashboard, the tests only cover 4 specific aspects:

    1. % 0 Cover Checks
    2. % Takeaway Covers
    3. % Meal Duration > 4hr / <= 5min
    4. % Revenue Outside of Operating Hours

### Date Range
The data comparison is configured within test_dashboard.py using the following date range:
```python
start_date = {
    "year": 2019,
    "month": 11,
    "day": 1
}

end_date = {
    "year": 2023,
    "month": 11,
    "day": 15
}
```

## Additional Notes

* The Excel file containing the reference data should be placed in the same directory as the tests.

* The tests assume that the Symphony.Ledr.io Quality Data dashboard is accessible at `https://test.symphony.ledr.io/dashboards/5fb64e6b-c41c-499b-86e9-2d6c6235f9f5`. If the URL is different, you will need to update the test scripts accordingly.

* The tests now utilize Playwright's asynchronous capabilities for enhanced efficiency. Review the updated test scripts and the modified pytest command (pytest --numprocesses 2 )for parallel execution.

