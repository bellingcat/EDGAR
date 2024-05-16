# edgar_test_script.py
import os
from datetime import date, timedelta
from edgar_tool.cli import SecEdgarScraperCli


# Function to test text search with various parameters
def test_text_search(keywords, start_date, end_date, filing_type=None, filing_form_group=None, output=None):
    # Default output filename if not provided
    if output is None:
        output = f"edgar_test_results_{date.today().strftime('%Y%m%d_%H%M%S')}_test_both.csv"

    # Instantiate the CLI class
    cli = SecEdgarScraperCli()

    # Perform the text search with the given parameters
    cli.text_search(
        *keywords,
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d"),
        filing_type=filing_type,
        filing_form_group=filing_form_group,
        output=output
    )

    print(f"Results written to {output}")


# Test parameters
keywords = ["Elon Musk"]  # Example keywords
start_date = date.today() - timedelta(days=365 * 5)  # Last 5 years
end_date = date.today()  # Up to today

# Example test with a specific filing type
test_text_search(keywords,
                 start_date,
                 end_date,
                 filing_type="all_annual_quarterly_and_current_reports",
                 filing_form_group="Insider equity awards, transactions, and ownership (Section 16 Reports)"
                 )

