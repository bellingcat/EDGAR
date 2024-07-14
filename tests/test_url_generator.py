"""
This file tests code responsible for generating the EDGAR search URL.

Note that at the time of this writing, EDGAR double-encodes query search
parameters so that %-encoded characters, like a quote ("), are encoded
as %2520 in the browser's URL instead of %20. This is a quirk with the
SEC's search functionality. Local testing indicates that single-encoded
URLs (which is the norm) and double-encoded URLs produce the same
responses. 

I.e. this double-encoded URL produced on the SEC's EDGAR search page:
  https://www.sec.gov/edgar/search/#/q=%2522Insider%2520trading%2520report%2522

is functionally equivalent to our generated URL:
  https://www.sec.gov/edgar/search/#/q=%22Insider%20trading%20report%20
"""

from edgar_tool import url_generator


def test_should_correctly_generate_search_url_for_single_word():
    """Baseline test to assert that querying for a single word
    produces the correct search URL"""
    # GIVEN
    keywords = ["10-K"]
    expected_url = "https://www.sec.gov/edgar/search/#/q=10-K"

    # WHEN
    actual_url = url_generator.generate_search_url_for_kwargs({"keywords": keywords})

    # THEN
    assert actual_url == expected_url


def test_should_correctly_generate_search_url_for_exact_phrase():
    # GIVEN
    keywords = ["Insider trading report"]
    expected_url = (
        "https://www.sec.gov/edgar/search/#/q=%22Insider%20trading%20report%22"
    )

    # WHEN
    actual_url = url_generator.generate_search_url_for_kwargs({"keywords": keywords})

    # THEN
    assert actual_url == expected_url
