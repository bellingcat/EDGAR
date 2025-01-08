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

import datetime

import pytest

from edgar_tool import url_generator
from edgar_tool.constants import Location


def test_should_correctly_generate_search_url_for_single_word():
    """Baseline test to assert that querying for a single word
    produces the correct search URL"""
    # GIVEN
    keywords = ["10-K"]
    expected_url = f"https://efts.sec.gov/LATEST/search-index?q=10-K"

    # WHEN
    actual_url = url_generator.generate_search_url_for_kwargs({"keywords": keywords})

    # THEN
    assert actual_url == expected_url


def test_should_correctly_generate_search_url_for_exact_phrase():
    # GIVEN
    keywords = ["Insider trading report"]
    expected_url = (
        "https://efts.sec.gov/LATEST/search-index?q=%22Insider%20trading%20report%22"
    )

    # WHEN
    actual_url = url_generator.generate_search_url_for_kwargs({"keywords": keywords})

    # THEN
    assert actual_url == expected_url


@pytest.mark.parametrize(
    "test_kwarg",
    [
        {"keywords": []},
        {"entity": []},
    ],
)
def test_should_raise_if_keywords_or_entity_missing(test_kwarg):
    # GIVEN
    expected_error_msg = (
        "Invalid search arguments. You must provide keywords or an entity."
    )

    # WHEN / THEN
    with pytest.raises(ValueError, match=expected_error_msg):
        url_generator.generate_search_url_for_kwargs(test_kwarg)


@pytest.mark.parametrize(
    "date_kwarg",
    [
        {"start_date": datetime.date.today()},
        {"end_date": datetime.date.today()},
    ],
)
def test_should_raise_if_date_range_custom_but_missing_dates(date_kwarg):
    # GIVEN
    expected_error_msg = (
        "Invalid date parameters. "
        "You must provide both a start and end date if searching a custom date range."
    )
    base_kwargs = {"keywords": ["Ford Motor Co"], "date_range_select": "custom"}
    test_kwargs = {**base_kwargs, **date_kwarg}

    # WHEN / THEN
    with pytest.raises(ValueError, match=expected_error_msg):
        url_generator.generate_search_url_for_kwargs(test_kwargs)


def test_should_raise_if_date_range_select_invalid():
    # GIVEN
    expected_error_msg = (
        "Invalid date_range_select. "
        'Value must be one of "all", "10y", "1y", "30d", or "custom"'
    )
    test_kwargs = {"keywords": ["Ford Motor Co"], "date_range_select": "1m"}

    # WHEN / THEN
    with pytest.raises(ValueError, match=expected_error_msg):
        url_generator.generate_search_url_for_kwargs(test_kwargs)


@pytest.mark.parametrize(
    "date_kwargs,url_ending",
    [
        (
            {
                "date_range_select": "custom",
                "start_date": datetime.date.fromisoformat("2024-07-10"),
                "end_date": datetime.date.fromisoformat("2024-07-15"),
            },
            "&dateRange=custom&startdt=2024-07-10&enddt=2024-07-15",
        ),
        ({"date_range_select": "all"}, "&dateRange=all"),
        ({"date_range_select": "10y"}, "&dateRange=10y"),
        # TODO: Test 5y doesn't add anything to the URL
        ({"date_range_select": "1y"}, "&dateRange=1y"),
        ({"date_range_select": "30d"}, "&dateRange=30d"),
    ],
)
def test_generates_correct_url_for_date_ranges(date_kwargs, url_ending):
    """Tests that various date range options are correctly translated
    into the seach URL."""
    # GIVEN
    expected_url = f"https://efts.sec.gov/LATEST/search-index?q=%22Ford%20Motor%20Co%22{url_ending}"
    test_kwargs = {**{"keywords": ["Ford Motor Co"]}, **date_kwargs}

    # WHEN
    actual_url = url_generator.generate_search_url_for_kwargs(test_kwargs)

    # THEN
    assert actual_url == expected_url


@pytest.mark.parametrize(
    "filing_category, url_ending",
    (
        ("all", ""),
        ("all_except_section_16", "&category=form-cat0"),
        ("all_annual_quarterly_and_current_reports", "&category=form-cat1"),
        ("all_section_16", "&category=form-cat2"),
        ("beneficial_ownership_reports", "&category=form-cat3"),
        ("exempt_offerings", "&category=form-cat4"),
        ("registration_statements", "&category=form-cat5"),
        ("filing_review_correspondence", "&category=form-cat6"),
        ("sec_orders_and_notices", "&category=form-cat7"),
        ("proxy_materials", "&category=form-cat8"),
        ("tender_offers_and_going_private_tx", "&category=form-cat9"),
        ("trust_indentures", "&category=form-cat10"),
    ),
)
def test_generates_correct_url_for_filing_category(filing_category, url_ending):
    # GIVEN
    expected_url = f"https://efts.sec.gov/LATEST/search-index?q=Ignore{url_ending}"
    test_kwargs = {"keywords": ["Ignore"], "filing_category": filing_category}

    # WHEN
    actual_url = url_generator.generate_search_url_for_kwargs(test_kwargs)

    # THEN
    assert actual_url == expected_url


@pytest.mark.parametrize(
    "single_forms, url_ending",
    (
        (["1"], "&forms=1"),
        (["CORRESP"], "&forms=CORRESP"),
        (
            ["F-4, PREC14A, SEC STAFF ACTION"],
            "&forms=F-4%2C%20PREC14A%2C%20SEC%20STAFF%20ACTION",
        ),
    ),
)
def test_generates_correct_url_for_single_forms(single_forms, url_ending):
    # GIVEN
    expected_url = (
        f"https://efts.sec.gov/LATEST/search-index?q=Ignore&category=custom{url_ending}"
    )
    test_kwargs = {"keywords": ["Ignore"], "single_forms": single_forms}

    # WHEN
    actual_url = url_generator.generate_search_url_for_kwargs(test_kwargs)

    # THEN
    assert actual_url == expected_url


def test_raises_an_exception_if_user_passes_both_filing_category_and_single_forms():
    """When a user filters based on single form type the filing category is automatically
    set to "custom." Therefore passing a filing category when using single forms both does
    not make sense and will potentially give the user confusing results if the code ignores
    the passed filing category and sets it as custom. It's best to raise an error and let
    the user use either a filing category or single forms.
    """
    # GIVEN
    test_kwargs = {
        "keywords": ["Ignore"],
        "single_forms": ["F-4, PREC14A, SEC STAFF ACTION"],
        "filing_category": "beneficial_ownership_reports",
    }
    expected_error_msg = (
        "Cannot specify both filing_category and single_forms. "
        "Passing single_forms automatically sets the filing_category"
        " to custom. Please choose one or the other."
    )

    # WHEN / THEN
    with pytest.raises(ValueError, match=expected_error_msg):
        url_generator.generate_search_url_for_kwargs(test_kwargs)


@pytest.mark.parametrize(
    "abbreviation, expected_location_code",
    [
        # US States - All use 2-letter state & territory abbreviations (ISO 3166-2)
        (Location.ALABAMA, "AL"),
        (Location.ALASKA, "AK"),
        (Location.ARIZONA, "AZ"),
        (Location.ARKANSAS, "AR"),
        (Location.CALIFORNIA, "CA"),
        (Location.COLORADO, "CO"),
        (Location.CONNECTICUT, "CT"),
        (Location.DELAWARE, "DE"),
        (Location.DISTRICT_OF_COLUMBIA, "DC"),
        (Location.FLORIDA, "FL"),
        (Location.GEORGIA, "GA"),
        (Location.HAWAII, "HI"),
        (Location.IDAHO, "ID"),
        (Location.ILLINOIS, "IL"),
        (Location.INDIANA, "IN"),
        (Location.IOWA, "IA"),
        (Location.KANSAS, "KS"),
        (Location.KENTUCKY, "KY"),
        (Location.LOUISIANA, "LA"),
        (Location.MAINE, "ME"),
        (Location.MARYLAND, "MD"),
        (Location.MASSACHUSETTS, "MA"),
        (Location.MICHIGAN, "MI"),
        (Location.MINNESOTA, "MN"),
        (Location.MISSISSIPPI, "MS"),
        (Location.MISSOURI, "MO"),
        (Location.MONTANA, "MT"),
        (Location.NEBRASKA, "NE"),
        (Location.NEVADA, "NV"),
        (Location.NEW_HAMPSHIRE, "NH"),
        (Location.NEW_JERSEY, "NJ"),
        (Location.NEW_MEXICO, "NM"),
        (Location.NEW_YORK, "NY"),
        (Location.NORTH_CAROLINA, "NC"),
        (Location.NORTH_DAKOTA, "ND"),
        (Location.OHIO, "OH"),
        (Location.OKLAHOMA, "OK"),
        (Location.OREGON, "OR"),
        (Location.PENNSYLVANIA, "PA"),
        (Location.RHODE_ISLAND, "RI"),
        (Location.SOUTH_CAROLINA, "SC"),
        (Location.SOUTH_DAKOTA, "SD"),
        (Location.TENNESSEE, "TN"),
        (Location.TEXAS, "TX"),
        (Location.UTAH, "UT"),
        (Location.VERMONT, "VT"),
        (Location.VIRGINIA, "VA"),
        (Location.WASHINGTON, "WA"),
        (Location.WEST_VIRGINIA, "WV"),
        (Location.WISCONSIN, "WI"),
        (Location.WYOMING, "WY"),
        # Canadian Provinces - P.E.O. in to use internationally approved alpha codes (ISO 3166-2)
        (Location.ALBERTA, "A0"),
        (Location.BRITISH_COLUMBIA, "A1"),
        (Location.CANADA, "Z4"),
        (Location.MANITOBA, "A2"),
        (Location.NEW_BRUNSWICK, "A3"),
        (Location.NEWFOUNDLAND_AND_LABRADOR, "A4"),
        (Location.NOVA_SCOTIA, "A5"),
        (Location.ONTARIO, "A6"),
        (Location.PRINCE_EDWARD_ISLAND, "A7"),
        (Location.QUEBEC, "A8"),
        (Location.SASKATCHEWAN, "A9"),
        (Location.YUKON, "B0"),
        # Other Countries - All use internationally approved 3-letter alpha codes (ISO 3166-1)
        (Location.AFGHANISTAN, "B2"),
        (Location.ALAND_ISLANDS, "Y6"),
        (Location.ALBANIA, "B3"),
        (Location.ALGERIA, "B4"),
        (Location.AMERICAN_SAMOA, "B5"),
        (Location.ANDORRA, "B6"),
        (Location.ANGOLA, "B7"),
        (Location.ANGUILLA, "1A"),
        (Location.ANTARCTICA, "B8"),
        (Location.ANTIGUA_AND_BARBUDA, "B9"),
        (Location.ARGENTINA, "C1"),
        (Location.ARMENIA, "1B"),
        (Location.ARUBA, "1C"),
        (Location.AUSTRALIA, "C3"),
        (Location.AUSTRIA, "C4"),
        (Location.AZERBAIJAN, "1D"),
        (Location.BAHAMAS, "C5"),
        (Location.BAHRAIN, "C6"),
        (Location.BANGLADESH, "C7"),
        (Location.BARBADOS, "C8"),
        (Location.BELARUS, "1F"),
        (Location.BELGIUM, "C9"),
        (Location.BELIZE, "D1"),
        (Location.BENIN, "G6"),
        (Location.BERMUDA, "D0"),
        (Location.BHUTAN, "D2"),
        (Location.BOLIVIA, "D3"),
        (Location.BOSNIA_AND_HERZEGOVINA, "1E"),
        (Location.BOTSWANA, "B1"),
        (Location.BOUVET_ISLAND, "D4"),
        (Location.BRAZIL, "D5"),
        (Location.BRITISH_INDIAN_OCEAN_TERRITORY, "D6"),
        (Location.BRUNEI_DARUSSALAM, "D9"),
        (Location.BULGARIA, "E0"),
        (Location.BURKINA_FASO, "X2"),
        (Location.BURUNDI, "E2"),
        (Location.CAMBODIA, "E3"),
        (Location.CAMEROON, "E4"),
        (Location.CAPE_VERDE, "E8"),
        (Location.CAYMAN_ISLANDS, "E9"),
        (Location.CENTRAL_AFRICAN_REPUBLIC, "F0"),
        (Location.CHAD, "F2"),
        (Location.CHILE, "F3"),
        (Location.CHINA, "F4"),
        (Location.CHRISTMAS_ISLAND, "F6"),
        (Location.COCOS_KEELING_ISLANDS, "F7"),
        (Location.COLOMBIA, "F8"),
        (Location.COMOROS, "F9"),
        (Location.CONGO, "G0"),
        (Location.CONGO_DEMOCRATIC_REPUBLIC, "Y3"),
        (Location.COOK_ISLANDS, "G1"),
        (Location.COSTA_RICA, "G2"),
        (Location.COTE_DIVOIRE, "L7"),
        (Location.CROATIA, "1M"),
        (Location.CUBA, "G3"),
        (Location.CYPRUS, "G4"),
        (Location.CZECH_REPUBLIC, "2N"),
        (Location.DENMARK, "G7"),
        (Location.DJIBOUTI, "1G"),
        (Location.DOMINICA, "G9"),
        (Location.DOMINICAN_REPUBLIC, "D8"),
        (Location.ECUADOR, "H1"),
        (Location.EGYPT, "H2"),
        (Location.EL_SALVADOR, "H3"),
        (Location.EQUATORIAL_GUINEA, "H4"),
        (Location.ERITREA, "1J"),
        (Location.ESTONIA, "1H"),
        (Location.ETHIOPIA, "H5"),
        (Location.FALKLAND_ISLANDS, "H7"),
        (Location.FAROE_ISLANDS, "H6"),
        (Location.FIJI, "H8"),
        (Location.FINLAND, "H9"),
        (Location.FRANCE, "I0"),
        (Location.FRENCH_GUIANA, "I3"),
        (Location.FRENCH_POLYNESIA, "I4"),
        (Location.FRENCH_SOUTHERN_TERRITORIES, "2C"),
        (Location.GABON, "I5"),
        (Location.GAMBIA, "I6"),
        (Location.GEORGIA_REPUBLIC, "2Q"),
        (Location.GERMANY, "2M"),
        (Location.GHANA, "J0"),
        (Location.GIBRALTAR, "J1"),
        (Location.GREECE, "J3"),
        (Location.GREENLAND, "J4"),
        (Location.GRENADA, "J5"),
        (Location.GUADELOUPE, "J6"),
        (Location.GUAM, "GU"),
        (Location.GUATEMALA, "J8"),
        (Location.GUERNSEY, "Y7"),
        (Location.GUINEA, "J9"),
        (Location.GUINEA_BISSAU, "S0"),
        (Location.GUYANA, "K0"),
        (Location.HAITI, "K1"),
        (Location.HEARD_AND_MCDONALD_ISLANDS, "K4"),
        (Location.HOLY_SEE_VATICAN_CITY, "X4"),
        (Location.HONDURAS, "K2"),
        (Location.HONG_KONG, "K3"),
        (Location.HUNGARY, "K5"),
        (Location.ICELAND, "K6"),
        (Location.INDIA, "K7"),
        (Location.INDONESIA, "K8"),
        (Location.IRAN, "K9"),
        (Location.IRAQ, "L0"),
        (Location.IRELAND, "L2"),
        (Location.ISLE_OF_MAN, "Y8"),
        (Location.ISRAEL, "L3"),
        (Location.ITALY, "L6"),
        (Location.JAMAICA, "L8"),
        (Location.JAPAN, "M0"),
        (Location.JERSEY, "Y9"),
        (Location.JORDAN, "M2"),
        (Location.KAZAKHSTAN, "1P"),
        (Location.KENYA, "M3"),
        (Location.KIRIBATI, "J2"),
        (Location.NORTH_KOREA, "M4"),
        (Location.SOUTH_KOREA, "M5"),
        (Location.KUWAIT, "M6"),
        (Location.KYRGYZSTAN, "1N"),
        (Location.LAOS, "M7"),
        (Location.LATVIA, "1R"),
        (Location.LEBANON, "M8"),
        (Location.LESOTHO, "M9"),
        (Location.LIBERIA, "N0"),
        (Location.LIBYA, "N1"),
        (Location.LIECHTENSTEIN, "N2"),
        (Location.LITHUANIA, "1Q"),
        (Location.LUXEMBOURG, "N4"),
        (Location.MACAU, "N5"),
        (Location.MACEDONIA, "1U"),
        (Location.MADAGASCAR, "N6"),
        (Location.MALAWI, "N7"),
        (Location.MALAYSIA, "N8"),
        (Location.MALDIVES, "N9"),
        (Location.MALI, "O0"),
        (Location.MALTA, "O1"),
        (Location.MARSHALL_ISLANDS, "1T"),
        (Location.MARTINIQUE, "O2"),
        (Location.MAURITANIA, "O3"),
        (Location.MAURITIUS, "O4"),
        (Location.MAYOTTE, "2P"),
        (Location.MEXICO, "O5"),
        (Location.MICRONESIA, "1K"),
        (Location.MOLDOVA, "1S"),
        (Location.MONACO, "O9"),
        (Location.MONGOLIA, "P0"),
        (Location.MONTENEGRO, "Z5"),
        (Location.MONTSERRAT, "P1"),
        (Location.MOROCCO, "P2"),
        (Location.MOZAMBIQUE, "P3"),
        (Location.MYANMAR, "E1"),
        (Location.NAMIBIA, "T6"),
        (Location.NAURU, "P5"),
        (Location.NEPAL, "P6"),
        (Location.NETHERLANDS, "P7"),
        (Location.NETHERLANDS_ANTILLES, "P8"),
        (Location.NEW_CALEDONIA, "1W"),
        (Location.NEW_ZEALAND, "Q2"),
        (Location.NICARAGUA, "Q3"),
        (Location.NIGER, "Q4"),
        (Location.NIGERIA, "Q5"),
        (Location.NIUE, "Q6"),
        (Location.NORFOLK_ISLAND, "Q7"),
        (Location.NORTHERN_MARIANA_ISLANDS, "1V"),
        (Location.NORWAY, "Q8"),
        (Location.OMAN, "P4"),
        (Location.PAKISTAN, "R0"),
        (Location.PALAU, "1Y"),
        (Location.PALESTINIAN_TERRITORY, "1X"),
        (Location.PANAMA, "R1"),
        (Location.PAPUA_NEW_GUINEA, "R2"),
        (Location.PARAGUAY, "R4"),
        (Location.PERU, "R5"),
        (Location.PHILIPPINES, "R6"),
        (Location.PITCAIRN, "R8"),
        (Location.POLAND, "R9"),
        (Location.PORTUGAL, "S1"),
        (Location.PUERTO_RICO, "PR"),
        (Location.QATAR, "S3"),
        (Location.REUNION, "S4"),
        (Location.ROMANIA, "S5"),
        (Location.RUSSIAN_FEDERATION, "1Z"),
        (Location.RWANDA, "S6"),
        (Location.SAINT_BARTHELEMY, "Z0"),
        (Location.SAINT_HELENA, "U8"),
        (Location.SAINT_KITTS_AND_NEVIS, "U7"),
        (Location.SAINT_LUCIA, "U9"),
        (Location.SAINT_MARTIN, "Z1"),
        (Location.SAINT_PIERRE_AND_MIQUELON, "V0"),
        (Location.SAINT_VINCENT_AND_GRENADINES, "V1"),
        (Location.SAMOA, "Y0"),
        (Location.SAN_MARINO, "S8"),
        (Location.SAO_TOME_AND_PRINCIPE, "S9"),
        (Location.SAUDI_ARABIA, "T0"),
        (Location.SENEGAL, "T1"),
        (Location.SERBIA, "Z2"),
        (Location.SEYCHELLES, "T2"),
        (Location.SIERRA_LEONE, "T8"),
        (Location.SINGAPORE, "U0"),
        (Location.SLOVAKIA, "2B"),
        (Location.SLOVENIA, "2A"),
        (Location.SOLOMON_ISLANDS, "D7"),
        (Location.SOMALIA, "U1"),
        (Location.SOUTH_AFRICA, "T3"),
        (Location.SOUTH_GEORGIA_AND_SOUTH_SANDWICH_ISLANDS, "1L"),
        (Location.SPAIN, "U3"),
        (Location.SRI_LANKA, "F1"),
        (Location.SUDAN, "V2"),
        (Location.SURINAME, "V3"),
        (Location.SVALBARD_AND_JAN_MAYEN, "L9"),
        (Location.ESWATINI, "V6"),
        (Location.SWEDEN, "V7"),
        (Location.SWITZERLAND, "V8"),
        (Location.SYRIA, "V9"),
        (Location.TAIWAN, "F5"),
        (Location.TAJIKISTAN, "2D"),
        (Location.THAILAND, "W1"),
        (Location.TIMOR_LESTE, "Z3"),
        (Location.TOGO, "W2"),
        (Location.TOKELAU, "W3"),
        (Location.TONGA, "W4"),
        (Location.TRINIDAD_AND_TOBAGO, "W5"),
        (Location.TUNISIA, "W6"),
        (Location.TURKEY, "W8"),
        (Location.TURKMENISTAN, "2E"),
        (Location.TURKS_AND_CAICOS_ISLANDS, "W7"),
        (Location.TUVALU, "2G"),
        (Location.UGANDA, "W9"),
        (Location.UKRAINE, "2H"),
        (Location.UNITED_ARAB_EMIRATES, "C0"),
        (Location.UNITED_KINGDOM, "X0"),
        (Location.UNITED_STATES_MINOR_OUTLYING_ISLANDS, "2J"),
        (Location.URUGUAY, "X3"),
        (Location.UZBEKISTAN, "2K"),
        (Location.VANUATU, "2L"),
        (Location.VENEZUELA, "X5"),
        (Location.VIETNAM, "Q1"),
        (Location.BRITISH_VIRGIN_ISLANDS, "D8"),
        (Location.US_VIRGIN_ISLANDS, "VI"),
        (Location.WALLIS_AND_FUTUNA, "X8"),
        (Location.WESTERN_SAHARA, "Y1"),
        (Location.YEMEN, "T7"),
        (Location.ZAMBIA, "Y4"),
        (Location.ZIMBABWE, "Y5"),
        (Location.UNKNOWN, "XX"),
    ],
)
class TestPeoInAndIncIn:
    def test_should_correctly_generate_search_url_for_peo_in(
        self, abbreviation, expected_location_code
    ):
        # GIVEN
        expected_url = f"https://efts.sec.gov/LATEST/search-index?q=a&locationCode={expected_location_code}"

        # WHEN
        actual_url = url_generator.generate_search_url_for_kwargs(
            {"keywords": ["a"], "peo_in": abbreviation}
        )

        # THEN
        assert actual_url == expected_url

    def test_should_correctly_generate_search_url_for_inc_in(
        self, abbreviation, expected_location_code
    ):
        # GIVEN
        expected_url = f"https://efts.sec.gov/LATEST/search-index?q=a&locationType=incorporated&locationCode={expected_location_code}"

        # WHEN
        actual_url = url_generator.generate_search_url_for_kwargs(
            {"keywords": ["a"], "inc_in": abbreviation}
        )

        # THEN
        assert actual_url == expected_url


@pytest.mark.parametrize("key", ["peo_in", "inc_in"])
def test_should_raise_exception_if_location_code_invalid(key):
    # GIVEN
    expected_error_msg = (
        "Invalid location code. "
        "Please provide a valid 2-letter state abbreviation, "
        "3-letter country code, or 'XX' for unknown."
    )
    soviet_union = "SUN"
    test_kwargs = {"keywords": ["a"], key: soviet_union}

    # WHEN / THEN
    with pytest.raises(ValueError, match=expected_error_msg):
        url_generator.generate_search_url_for_kwargs(test_kwargs)


def test_should_raise_exception_if_both_peo_in_and_inc_in():
    # GIVEN
    expected_error_msg = (
        "Cannot specify both peo_in and inc_in. Please choose one or the other."
    )

    test_kwargs = {"keywords": ["a"], "peo_in": "CA", "inc_in": "CA"}

    # WHEN / THEN
    with pytest.raises(ValueError, match=expected_error_msg):
        url_generator.generate_search_url_for_kwargs(test_kwargs)
