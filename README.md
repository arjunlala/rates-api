# rates-api

## Part 1 
### Time Spent - 2 hours
- 0.5 hours learning basics of BeautifulSoup/sqlite setup
- 1.5 hours to develop and adjust with Part 2

### Running the program
The ETL is run in the root folder `rates-api\` where it will create a rates database in the `\FastAPI` folder and `monthly_rates` table that stores the daily Pensford data.

- You can run this file using `python3 .\etl.py`

- Can be run anytime and will handle any duplicate values as the date is the primary key in string mdyyyy form.

- Added quick drop program just to get rid of the table while developing so I didn't have to comment out my insert statement: `python3 .\quick_drop.py`

### Improvements
- This could definitely be improved to take a datetime value, but for type casting/inserting into sqlite I skipped getting around this as the datetimes were being inserted as a string anyway and I'd have to do the conversions after pulling them out. I also removed the '/' in the dates to just make unique id's when I was working on the API portion in Part 2.

- Note: single m and d since the format is very exact to what the Pensford site returns. For example, June 5, 2022 would be written to the table as 652022.

- I am used to using sqlAlchemy for DB connections so using sqlite was new. I could probably have used any connection type and done more research on the safer/more reliable db connections to use. Small in this case, but something to think about.

- Another weakness of the code is in the BeautifulSoup parsing. I have worked on web scraping before and any changes that the Pensford site makes to their html/css could cause a breakage in reading the Forward Curve table. I would hope to use something more robust such as an API call from another host to get the curve values and store them. If not that, maybe download the file and parse the xls/csv to know what target we are actively searching for. What I currently developed is more of a blind guess and hope that they don't change their frontend html.

- I thought about edge cases for production since date is a primary key. On June 5, 2023 (the one year mark), we'd have duplicated entries for 652023 which would NOT throw an error. We have the `INSERT OR REPLACE INTO` statement that would cover repeated values, but our forward curve would be corrupted and inaccurate. That then leads to the question of do we need this data to persist over time, or do we just want a daily snapshot? If the former, improvements could be adding an integer id or date_inserted to only use the latest data yet have the all of the data available for historical checks. If not we could just add a truncate table statement before the insert loop.

- Keeping the quick_drop.py file in my codebase would never be recommended. It's there for testing ease for the user. So that is something that would need to be removed for production in any case and worth mentioning. 

- To make this production ready, we'd also need to add a scheduler to have this program run once a day after Pensford publishes the current day's forward rates. Personally, I would use an airflow dag since that's what I'm most comfortable with. And it could be run all morning every X minutes to check for new_dates before performing a new pull. 

## Part 2
### Time Spent - 6.0 hours
- 3.0 hours learning FastAPI basics and connecting the API to DB
- 3.0 hours to develop and add adjustments with Part 1

### Running the program
The API is run in the `rates-api\FastAPI\` folder where we have 4 files:
- `rates.db` - the db created in Part 1 with `monthly_rates` table with values in it

- `database.py` - db connection/session 

- `models.py` - create db table if it does not exist, which is just a class to hold the `monthly_rates` table structure.

- `main.py` - this is where the actual API functions sit.

You can run this API using `rates-api\FastAPI\uvicorn main:app --port 8000`
- From there you'd want to navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to see the Pensford rates directly in the monthly_rates table sorted by inserted date (up to one year).

- To use the API on the web and test, you can go to [http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/).

- Input would be written as a string for `maturity_date` in mdyyyy form to exactly match the Pensford `monthly_rates` table (i.e. June 28, 2025 = 6282025) and the `floor, ceiling, spread` would be written in decimal form with a preceding 0 (i.e. 0.02).

- The returned response is a list of json objects up to the maturity_date inclusive.

### Improvements
- First off, I simply calculated the final interest rate by adding the reference rate's projected value + the fixed spread and if past the floor or ceiling thresholds provided by parameters then default to those. From what I understood in the prompt, that's what I needed to do and the forward rates are what are provided by Pensford. If that's not the case then I would need to perform a more complex calculation.

- The prompt asked to have the input payload in the form of a json where I only added inputs in the form of query parameters. I have seen examples of json parameters, but also read that those are not recommended in the case of GET REQUESTS. Nonetheless, I do not have much experience in API development but was able to deliver the result given input params. I left out the reference_rate input since I made two different GET REQUESTS as well. Spending more time on this, I definitely could learn to apply the json input to the API by adding a Loan to `models.py` but I spent way over the alloted time already and believe this is functional for the case of testing and getting a response from a set of inputs. 

- I also can improve the parameter entry and response by using proper datetime formatting to get an actual date and not just a string response. This ties into the quick input I used in Part 1 just to get the ball rolling and not spend as much time on the semantics. 

- The sofr and libor GET REQUESTS can definitely be written cleaner. They are both very simple calculations and I could have created a parser function to run the loops and take sofr or libor params then each GET REQUEST just call that function. What I essentially did was go through the logic for the first sofr curve and copy-paste for libor, the exact time you'd want to define a separate function. For time's sake I did not bother. It is ugly, but it does work for now!

- I am aware that these APIs are not safe to use for any production environment. They are vulnerable to malicious users so authentication would be the first step to improve security.

## Closing
There is a lot more than can be done to these programs to improve their usability and reliability. Given the opportunity I would like to spend more time in further developing the APIs to complete the requirements in full.

# Update
It currently does not work over multi-days as the response order gets messed up due to the indexing based on the maturity_date.
6/28 can run in full and be all 6/28
But then when we pull 6/29 then it will show as 
6282022
6292022
7282022
7292022

Adding the truncate before load as mentioned up top. Further adjustments can be made if we want persistent data.
