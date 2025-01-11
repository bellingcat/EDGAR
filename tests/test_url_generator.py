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
        ("AL", "AL"),  # Alabama
        ("AK", "AK"),  # Alaska
        ("AZ", "AZ"),  # Arizona
        ("AR", "AR"),  # Arkansas
        ("CA", "CA"),  # California
        ("CO", "CO"),  # Colorado
        ("CT", "CT"),  # Connecticut
        ("DE", "DE"),  # Delaware
        ("DC", "DC"),  # District of Columbia
        ("FL", "FL"),  # Florida
        ("GA", "GA"),  # Georgia
        ("HI", "HI"),  # Hawaii
        ("ID", "ID"),  # Idaho
        ("IL", "IL"),  # Illinois
        ("IN", "IN"),  # Indiana
        ("IA", "IA"),  # Iowa
        ("KS", "KS"),  # Kansas
        ("KY", "KY"),  # Kentucky
        ("LA", "LA"),  # Louisiana
        ("ME", "ME"),  # Maine
        ("MD", "MD"),  # Maryland
        ("MA", "MA"),  # Massachusetts
        ("MI", "MI"),  # Michigan
        ("MN", "MN"),  # Minnesota
        ("MS", "MS"),  # Mississippi
        ("MO", "MO"),  # Missouri
        ("MT", "MT"),  # Montana
        ("NE", "NE"),  # Nebraska
        ("NV", "NV"),  # Nevada
        ("NH", "NH"),  # New Hampshire
        ("NJ", "NJ"),  # New Jersey
        ("NM", "NM"),  # New Mexico
        ("NY", "NY"),  # New York
        ("NC", "NC"),  # North Carolina
        ("ND", "ND"),  # North Dakota
        ("OH", "OH"),  # Ohio
        ("OK", "OK"),  # Oklahoma
        ("OR", "OR"),  # Oregon
        ("PA", "PA"),  # Pennsylvania
        ("RI", "RI"),  # Rhode Island
        ("SC", "SC"),  # South Carolina
        ("SD", "SD"),  # South Dakota
        ("TN", "TN"),  # Tennessee
        ("TX", "TX"),  # Texas
        ("UT", "UT"),  # Utah
        ("VT", "VT"),  # Vermont
        ("VA", "VA"),  # Virginia
        ("WA", "WA"),  # Washington
        ("WV", "WV"),  # West Virginia
        ("WI", "WI"),  # Wisconsin
        ("WY", "WY"),  # Wyoming
        # Canadian Provinces - P.E.O. in to use internationally approved alpha codes (ISO 3166-2)
        ("AB", "A0"),  # Alberta
        ("BC", "A1"),  # British Columbia
        ("CAN", "Z4"),  # Canada (Federal Level)
        ("MB", "A2"),  # Manitoba
        ("NB", "A3"),  # New Brunswick
        ("NL", "A4"),  # Newfoundland and Labrador
        ("NS", "A5"),  # Nova Scotia
        ("ON", "A6"),  # Ontario
        ("PE", "A7"),  # Prince Edward Island
        ("QC", "A8"),  # Quebec
        ("SK", "A9"),  # Saskatchewan
        ("YT", "B0"),  # Yukon
        # Other Countries - All use internationally approved 3-letter alpha codes (ISO 3166-1)
        ("AFG", "B2"),  # Afghanistan
        ("ALA", "Y6"),  # Aland Islands
        ("ALB", "B3"),  # Albania
        ("DZA", "B4"),  # Algeria
        ("ASM", "B5"),  # American Samoa
        ("AND", "B6"),  # Andorra
        ("AGO", "B7"),  # Angola
        ("AIA", "1A"),  # Anguilla
        ("ATA", "B8"),  # Antarctica
        ("ATG", "B9"),  # Antigua and Barbuda
        ("ARG", "C1"),  # Argentina
        ("ARM", "1B"),  # Armenia
        ("ABW", "1C"),  # Aruba
        ("AUS", "C3"),  # Australia
        ("AUT", "C4"),  # Austria
        ("AZE", "1D"),  # Azerbaijan
        ("BHS", "C5"),  # Bahamas
        ("BHR", "C6"),  # Bahrain
        ("BGD", "C7"),  # Bangladesh
        ("BRB", "C8"),  # Barbados
        ("BLR", "1F"),  # Belarus
        ("BEL", "C9"),  # Belgium
        ("BLZ", "D1"),  # Belize
        ("BEN", "G6"),  # Benin
        ("BMU", "D0"),  # Bermuda
        ("BTN", "D2"),  # Bhutan
        ("BOL", "D3"),  # Bolivia
        ("BIH", "1E"),  # Bosnia and Herzegovina
        ("BWA", "B1"),  # Botswana
        ("BVT", "D4"),  # Bouvet Island
        ("BRA", "D5"),  # Brazil
        ("IOT", "D6"),  # British Indian Ocean Territory
        ("BRN", "D9"),  # Brunei Darussalam
        ("BGR", "E0"),  # Bulgaria
        ("BFA", "X2"),  # Burkina Faso
        ("BDI", "E2"),  # Burundi
        ("KHM", "E3"),  # Cambodia
        ("CMR", "E4"),  # Cameroon
        ("CPV", "E8"),  # Cape Verde
        ("CYM", "E9"),  # Cayman Islands
        ("CAF", "F0"),  # Central African Republic
        ("TCD", "F2"),  # Chad
        ("CHL", "F3"),  # Chile
        ("CHN", "F4"),  # China
        ("CXR", "F6"),  # Christmas Island
        ("CCK", "F7"),  # Cocos (Keeling) Islands
        ("COL", "F8"),  # Colombia
        ("COM", "F9"),  # Comoros
        ("COG", "G0"),  # Congo
        ("COD", "Y3"),  # Congo, Democratic Republic of the
        ("COK", "G1"),  # Cook Islands
        ("CRI", "G2"),  # Costa Rica
        ("CIV", "L7"),  # Cote d'Ivoire
        ("HRV", "1M"),  # Croatia
        ("CUB", "G3"),  # Cuba
        ("CYP", "G4"),  # Cyprus
        ("CZE", "2N"),  # Czech Republic
        ("DNK", "G7"),  # Denmark
        ("DJI", "1G"),  # Djibouti
        ("DMA", "G9"),  # Dominica
        ("DOM", "D8"),  # Dominican Republic
        ("ECU", "H1"),  # Ecuador
        ("EGY", "H2"),  # Egypt
        ("SLV", "H3"),  # El Salvador
        ("GNQ", "H4"),  # Equatorial Guinea
        ("ERI", "1J"),  # Eritrea
        ("EST", "1H"),  # Estonia
        ("ETH", "H5"),  # Ethiopia
        ("FLK", "H7"),  # Falkland Islands (Malvinas)
        ("FRO", "H6"),  # Faroe Islands
        ("FJI", "H8"),  # Fiji
        ("FIN", "H9"),  # Finland
        ("FRA", "I0"),  # France
        ("GUF", "I3"),  # French Guiana
        ("PYF", "I4"),  # French Polynesia
        ("ATF", "2C"),  # French Southern Territories
        ("GAB", "I5"),  # Gabon
        ("GMB", "I6"),  # Gambia
        ("GEO", "2Q"),  # Georgia
        ("DEU", "2M"),  # Germany
        ("GHA", "J0"),  # Ghana
        ("GIB", "J1"),  # Gibraltar
        ("GRC", "J3"),  # Greece
        ("GRL", "J4"),  # Greenland
        ("GRD", "J5"),  # Grenada
        ("GLP", "J6"),  # Guadeloupe
        ("GUM", "GU"),  # Guam
        ("GTM", "J8"),  # Guatemala
        ("GGY", "Y7"),  # Guernsey
        ("GIN", "J9"),  # Guinea
        ("GNB", "S0"),  # Guinea-Bissau
        ("GUY", "K0"),  # Guyana
        ("HTI", "K1"),  # Haiti
        ("HMD", "K4"),  # Heard Island and McDonald Islands
        ("VAT", "X4"),  # Holy See (Vatican City State)
        ("HND", "K2"),  # Honduras
        ("HKG", "K3"),  # Hong Kong
        ("HUN", "K5"),  # Hungary
        ("ISL", "K6"),  # Iceland
        ("IND", "K7"),  # India
        ("IDN", "K8"),  # Indonesia
        ("IRN", "K9"),  # Iran
        ("IRQ", "L0"),  # Iraq
        ("IRL", "L2"),  # Ireland
        ("IMN", "Y8"),  # Isle of Man
        ("ISR", "L3"),  # Israel
        ("ITA", "L6"),  # Italy
        ("JAM", "L8"),  # Jamaica
        ("JPN", "M0"),  # Japan
        ("JEY", "Y9"),  # Jersey
        ("JOR", "M2"),  # Jordan
        ("KAZ", "1P"),  # Kazakhstan
        ("KEN", "M3"),  # Kenya
        ("KIR", "J2"),  # Kiribati
        ("PRK", "M4"),  # Korea, Democratic People's Republic of
        ("KOR", "M5"),  # Korea, Republic of
        ("KWT", "M6"),  # Kuwait
        ("KGZ", "1N"),  # Kyrgyzstan
        ("LAO", "M7"),  # Lao People's Democratic Republic
        ("LVA", "1R"),  # Latvia
        ("LBN", "M8"),  # Lebanon
        ("LSO", "M9"),  # Lesotho
        ("LBR", "N0"),  # Liberia
        ("LBY", "N1"),  # Libya
        ("LIE", "N2"),  # Liechtenstein
        ("LTU", "1Q"),  # Lithuania
        ("LUX", "N4"),  # Luxembourg
        ("MAC", "N5"),  # Macao
        ("MKD", "1U"),  # Macedonia
        ("MDG", "N6"),  # Madagascar
        ("MWI", "N7"),  # Malawi
        ("MYS", "N8"),  # Malaysia
        ("MDV", "N9"),  # Maldives
        ("MLI", "O0"),  # Mali
        ("MLT", "O1"),  # Malta
        ("MHL", "1T"),  # Marshall Islands
        ("MTQ", "O2"),  # Martinique
        ("MRT", "O3"),  # Mauritania
        ("MUS", "O4"),  # Mauritius
        ("MYT", "2P"),  # Mayotte
        ("MEX", "O5"),  # Mexico
        ("FSM", "1K"),  # Micronesia, Federated States of
        ("MDA", "1S"),  # Moldova
        ("MCO", "O9"),  # Monaco
        ("MNG", "P0"),  # Mongolia
        ("MNE", "Z5"),  # Montenegro
        ("MSR", "P1"),  # Montserrat
        ("MAR", "P2"),  # Morocco
        ("MOZ", "P3"),  # Mozambique
        ("MMR", "E1"),  # Myanmar
        ("NAM", "T6"),  # Namibia
        ("NRU", "P5"),  # Nauru
        ("NPL", "P6"),  # Nepal
        ("NLD", "P7"),  # Netherlands
        ("ANT", "P8"),  # Netherlands Antilles
        ("NCL", "1W"),  # New Caledonia
        ("NZL", "Q2"),  # New Zealand
        ("NIC", "Q3"),  # Nicaragua
        ("NER", "Q4"),  # Niger
        ("NGA", "Q5"),  # Nigeria
        ("NIU", "Q6"),  # Niue
        ("NFK", "Q7"),  # Norfolk Island
        ("MNP", "1V"),  # Northern Mariana Islands
        ("NOR", "Q8"),  # Norway
        ("OMN", "P4"),  # Oman
        ("PAK", "R0"),  # Pakistan
        ("PLW", "1Y"),  # Palau
        ("PSE", "1X"),  # Palestinian Territory
        ("PAN", "R1"),  # Panama
        ("PNG", "R2"),  # Papua New Guinea
        ("PRY", "R4"),  # Paraguay
        ("PER", "R5"),  # Peru
        ("PHL", "R6"),  # Philippines
        ("PCN", "R8"),  # Pitcairn
        ("POL", "R9"),  # Poland
        ("PRT", "S1"),  # Portugal
        ("PRI", "PR"),  # Puerto Rico
        ("QAT", "S3"),  # Qatar
        ("REU", "S4"),  # Reunion
        ("ROU", "S5"),  # Romania
        ("RUS", "1Z"),  # Russian Federation
        ("RWA", "S6"),  # Rwanda
        ("BLM", "Z0"),  # Saint Barthelemy
        ("SHN", "U8"),  # Saint Helena
        ("KNA", "U7"),  # Saint Kitts and Nevis
        ("LCA", "U9"),  # Saint Lucia
        ("MAF", "Z1"),  # Saint Martin
        ("SPM", "V0"),  # Saint Pierre and Miquelon
        ("VCT", "V1"),  # Saint Vincent and the Grenadines
        ("WSM", "Y0"),  # Samoa
        ("SMR", "S8"),  # San Marino
        ("STP", "S9"),  # Sao Tome and Principe
        ("SAU", "T0"),  # Saudi Arabia
        ("SEN", "T1"),  # Senegal
        ("SRB", "Z2"),  # Serbia
        ("SYC", "T2"),  # Seychelles
        ("SLE", "T8"),  # Sierra Leone
        ("SGP", "U0"),  # Singapore
        ("SVK", "2B"),  # Slovakia
        ("SVN", "2A"),  # Slovenia
        ("SLB", "D7"),  # Solomon Islands
        ("SOM", "U1"),  # Somalia
        ("ZAF", "T3"),  # South Africa
        ("SGS", "1L"),  # South Georgia and the South Sandwich Islands
        ("ESP", "U3"),  # Spain
        ("LKA", "F1"),  # Sri Lanka
        ("SDN", "V2"),  # Sudan
        ("SUR", "V3"),  # Suriname
        ("SJM", "L9"),  # Svalbard and Jan Mayen
        ("SWZ", "V6"),  # Kingdom of Eswatini (Formerly Swaziland)
        ("SWE", "V7"),  # Sweden
        ("CHE", "V8"),  # Switzerland
        ("SYR", "V9"),  # Syrian Arab Republic (Syria)
        ("TWN", "F5"),  # Taiwan
        ("TJK", "2D"),  # Tajikistan
        ("THA", "W1"),  # Thailand
        ("TLS", "Z3"),  # Timor-Leste
        ("TGO", "W2"),  # Togo
        ("TKL", "W3"),  # Tokelau
        ("TON", "W4"),  # Tonga
        ("TTO", "W5"),  # Trinidad and Tobago
        ("TUN", "W6"),  # Tunisia
        ("TUR", "W8"),  # Turkey
        ("TKM", "2E"),  # Turkmenistan
        ("TCA", "W7"),  # Turks and Caicos Islands
        ("TUV", "2G"),  # Tuvalu
        ("UGA", "W9"),  # Uganda
        ("UKR", "2H"),  # Ukraine
        ("ARE", "C0"),  # United Arab Emirates
        ("GBR", "X0"),  # United Kingdom
        ("UMI", "2J"),  # United States Minor Outlying Islands
        ("URY", "X3"),  # Uruguay
        ("UZB", "2K"),  # Uzbekistan
        ("VUT", "2L"),  # Vanuatu
        ("VEN", "X5"),  # Venezuela
        ("VNM", "Q1"),  # Vietnam
        ("VGB", "D8"),  # British Virgin Islands
        ("VIR", "VI"),  # U.S. Virgin Islands
        ("WLF", "X8"),  # Wallis and Futuna
        ("ESH", "Y1"),  # Western Sahara
        ("YEM", "T7"),  # Yemen
        ("ZMB", "Y4"),  # Zambia
        ("ZWE", "Y5"),  # Zimbabwe
        ("XX", "XX"),  # Unknown
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
