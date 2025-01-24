import enum

from typing_extensions import Literal

SUPPORTED_OUTPUT_EXTENSIONS = [".csv", ".jsonl", ".json"]
TEXT_SEARCH_BASE_URL = "https://efts.sec.gov/LATEST/search-index?"
TEXT_SEARCH_SPLIT_BATCHES_NUMBER = 2
TEXT_SEARCH_CSV_FIELDS_NAMES = [
    "root_form",
    "form_name",
    "filed_at",
    "reporting_for",
    "entity_name",
    "ticker",
    "company_cik",
    "company_cik_trimmed",
    "place_of_business",
    "incorporated_location",
    "file_num",
    "film_num",
    "file_num_search_url",
    "filing_details_url",
    "filing_document_url",
]
RSS_FEED_CSV_FIELDS_NAMES = [
    "company_name",
    "cik",
    "trimmed_cik",
    "ticker",
    "published_date",
    "title",
    "link",
    "description",
    "form",
    "filing_date",
    "file_number",
    "accession_number",
    "acceptance_date",
    "period",
    "assistant_director",
    "assigned_sic",
    "fiscal_year_end",
    "xbrl_files",
]

"""All mappings below are from the SEC EDGAR website's search form.
The keys are the values that the CLI uses, and the values are those
that the search form uses. All values are shown in the order they
appear in the SEC EDGAR search drop down."""


class Location(str, enum.Enum):
    # US States
    ALABAMA = "AL"
    ALASKA = "AK"
    ARIZONA = "AZ"
    ARKANSAS = "AR"
    CALIFORNIA = "CA"
    COLORADO = "CO"
    CONNECTICUT = "CT"
    DELAWARE = "DE"
    DISTRICT_OF_COLUMBIA = "DC"
    FLORIDA = "FL"
    GEORGIA = "GA"
    HAWAII = "HI"
    IDAHO = "ID"
    ILLINOIS = "IL"
    INDIANA = "IN"
    IOWA = "IA"
    KANSAS = "KS"
    KENTUCKY = "KY"
    LOUISIANA = "LA"
    MAINE = "ME"
    MARYLAND = "MD"
    MASSACHUSETTS = "MA"
    MICHIGAN = "MI"
    MINNESOTA = "MN"
    MISSISSIPPI = "MS"
    MISSOURI = "MO"
    MONTANA = "MT"
    NEBRASKA = "NE"
    NEVADA = "NV"
    NEW_HAMPSHIRE = "NH"
    NEW_JERSEY = "NJ"
    NEW_MEXICO = "NM"
    NEW_YORK = "NY"
    NORTH_CAROLINA = "NC"
    NORTH_DAKOTA = "ND"
    OHIO = "OH"
    OKLAHOMA = "OK"
    OREGON = "OR"
    PENNSYLVANIA = "PA"
    RHODE_ISLAND = "RI"
    SOUTH_CAROLINA = "SC"
    SOUTH_DAKOTA = "SD"
    TENNESSEE = "TN"
    TEXAS = "TX"
    UTAH = "UT"
    VERMONT = "VT"
    VIRGINIA = "VA"
    WASHINGTON = "WA"
    WEST_VIRGINIA = "WV"
    WISCONSIN = "WI"
    WYOMING = "WY"

    # Canadian Provinces
    ALBERTA = "AB"
    BRITISH_COLUMBIA = "BC"
    CANADA = "CAN"
    MANITOBA = "MB"
    NEW_BRUNSWICK = "NB"
    NEWFOUNDLAND_AND_LABRADOR = "NL"
    NOVA_SCOTIA = "NS"
    ONTARIO = "ON"
    PRINCE_EDWARD_ISLAND = "PE"
    QUEBEC = "QC"
    SASKATCHEWAN = "SK"
    YUKON = "YT"

    # Countries
    AFGHANISTAN = "AFG"
    ALAND_ISLANDS = "ALA"
    ALBANIA = "ALB"
    ALGERIA = "DZA"
    AMERICAN_SAMOA = "ASM"
    ANDORRA = "AND"
    ANGOLA = "AGO"
    ANGUILLA = "AIA"
    ANTARCTICA = "ATA"
    ANTIGUA_AND_BARBUDA = "ATG"
    ARGENTINA = "ARG"
    ARMENIA = "ARM"
    ARUBA = "ABW"
    AUSTRALIA = "AUS"
    AUSTRIA = "AUT"
    AZERBAIJAN = "AZE"
    BAHAMAS = "BHS"
    BAHRAIN = "BHR"
    BANGLADESH = "BGD"
    BARBADOS = "BRB"
    BELARUS = "BLR"
    BELGIUM = "BEL"
    BELIZE = "BLZ"
    BENIN = "BEN"
    BERMUDA = "BMU"
    BHUTAN = "BTN"
    BOLIVIA = "BOL"
    BOSNIA_AND_HERZEGOVINA = "BIH"
    BOTSWANA = "BWA"
    BOUVET_ISLAND = "BVT"
    BRAZIL = "BRA"
    BRITISH_INDIAN_OCEAN_TERRITORY = "IOT"
    BRUNEI_DARUSSALAM = "BRN"
    BULGARIA = "BGR"
    BURKINA_FASO = "BFA"
    BURUNDI = "BDI"
    CAMBODIA = "KHM"
    CAMEROON = "CMR"
    CAPE_VERDE = "CPV"
    CAYMAN_ISLANDS = "CYM"
    CENTRAL_AFRICAN_REPUBLIC = "CAF"
    CHAD = "TCD"
    CHILE = "CHL"
    CHINA = "CHN"
    CHRISTMAS_ISLAND = "CXR"
    COCOS_KEELING_ISLANDS = "CCK"
    COLOMBIA = "COL"
    COMOROS = "COM"
    CONGO = "COG"
    CONGO_DEMOCRATIC_REPUBLIC = "COD"
    COOK_ISLANDS = "COK"
    COSTA_RICA = "CRI"
    COTE_DIVOIRE = "CIV"
    CROATIA = "HRV"
    CUBA = "CUB"
    CYPRUS = "CYP"
    CZECH_REPUBLIC = "CZE"
    DENMARK = "DNK"
    DJIBOUTI = "DJI"
    DOMINICA = "DMA"
    DOMINICAN_REPUBLIC = "DOM"
    ECUADOR = "ECU"
    EGYPT = "EGY"
    EL_SALVADOR = "SLV"
    EQUATORIAL_GUINEA = "GNQ"
    ERITREA = "ERI"
    ESTONIA = "EST"
    ETHIOPIA = "ETH"
    FALKLAND_ISLANDS = "FLK"
    FAROE_ISLANDS = "FRO"
    FIJI = "FJI"
    FINLAND = "FIN"
    FRANCE = "FRA"
    FRENCH_GUIANA = "GUF"
    FRENCH_POLYNESIA = "PYF"
    FRENCH_SOUTHERN_TERRITORIES = "ATF"
    GABON = "GAB"
    GAMBIA = "GMB"
    GEORGIA_REPUBLIC = "GEO"
    GERMANY = "DEU"
    GHANA = "GHA"
    GIBRALTAR = "GIB"
    GREECE = "GRC"
    GREENLAND = "GRL"
    GRENADA = "GRD"
    GUADELOUPE = "GLP"
    GUAM = "GUM"
    GUATEMALA = "GTM"
    GUERNSEY = "GGY"
    GUINEA = "GIN"
    GUINEA_BISSAU = "GNB"
    GUYANA = "GUY"
    HAITI = "HTI"
    HEARD_AND_MCDONALD_ISLANDS = "HMD"
    HOLY_SEE_VATICAN_CITY = "VAT"
    HONDURAS = "HND"
    HONG_KONG = "HKG"
    HUNGARY = "HUN"
    ICELAND = "ISL"
    INDIA = "IND"
    INDONESIA = "IDN"
    IRAN = "IRN"
    IRAQ = "IRQ"
    IRELAND = "IRL"
    ISLE_OF_MAN = "IMN"
    ISRAEL = "ISR"
    ITALY = "ITA"
    JAMAICA = "JAM"
    JAPAN = "JPN"
    JERSEY = "JEY"
    JORDAN = "JOR"
    KAZAKHSTAN = "KAZ"
    KENYA = "KEN"
    KIRIBATI = "KIR"
    NORTH_KOREA = "PRK"
    SOUTH_KOREA = "KOR"
    KUWAIT = "KWT"
    KYRGYZSTAN = "KGZ"
    LAOS = "LAO"
    LATVIA = "LVA"
    LEBANON = "LBN"
    LESOTHO = "LSO"
    LIBERIA = "LBR"
    LIBYA = "LBY"
    LIECHTENSTEIN = "LIE"
    LITHUANIA = "LTU"
    LUXEMBOURG = "LUX"
    MACAU = "MAC"
    MACEDONIA = "MKD"
    MADAGASCAR = "MDG"
    MALAWI = "MWI"
    MALAYSIA = "MYS"
    MALDIVES = "MDV"
    MALI = "MLI"
    MALTA = "MLT"
    MARSHALL_ISLANDS = "MHL"
    MARTINIQUE = "MTQ"
    MAURITANIA = "MRT"
    MAURITIUS = "MUS"
    MAYOTTE = "MYT"
    MEXICO = "MEX"
    MICRONESIA = "FSM"
    MOLDOVA = "MDA"
    MONACO = "MCO"
    MONGOLIA = "MNG"
    MONTENEGRO = "MNE"
    MONTSERRAT = "MSR"
    MOROCCO = "MAR"
    MOZAMBIQUE = "MOZ"
    MYANMAR = "MMR"
    NAMIBIA = "NAM"
    NAURU = "NRU"
    NEPAL = "NPL"
    NETHERLANDS = "NLD"
    NETHERLANDS_ANTILLES = "ANT"
    NEW_CALEDONIA = "NCL"
    NEW_ZEALAND = "NZL"
    NICARAGUA = "NIC"
    NIGER = "NER"
    NIGERIA = "NGA"
    NIUE = "NIU"
    NORFOLK_ISLAND = "NFK"
    NORTHERN_MARIANA_ISLANDS = "MNP"
    NORWAY = "NOR"
    OMAN = "OMN"
    PAKISTAN = "PAK"
    PALAU = "PLW"
    PALESTINIAN_TERRITORY = "PSE"
    PANAMA = "PAN"
    PAPUA_NEW_GUINEA = "PNG"
    PARAGUAY = "PRY"
    PERU = "PER"
    PHILIPPINES = "PHL"
    PITCAIRN = "PCN"
    POLAND = "POL"
    PORTUGAL = "PRT"
    PUERTO_RICO = "PRI"
    QATAR = "QAT"
    REUNION = "REU"
    ROMANIA = "ROU"
    RUSSIAN_FEDERATION = "RUS"
    RWANDA = "RWA"
    SAINT_BARTHELEMY = "BLM"
    SAINT_HELENA = "SHN"
    SAINT_KITTS_AND_NEVIS = "KNA"
    SAINT_LUCIA = "LCA"
    SAINT_MARTIN = "MAF"
    SAINT_PIERRE_AND_MIQUELON = "SPM"
    SAINT_VINCENT_AND_GRENADINES = "VCT"
    SAMOA = "WSM"
    SAN_MARINO = "SMR"
    SAO_TOME_AND_PRINCIPE = "STP"
    SAUDI_ARABIA = "SAU"
    SENEGAL = "SEN"
    SERBIA = "SRB"
    SEYCHELLES = "SYC"
    SIERRA_LEONE = "SLE"
    SINGAPORE = "SGP"
    SLOVAKIA = "SVK"
    SLOVENIA = "SVN"
    SOLOMON_ISLANDS = "SLB"
    SOMALIA = "SOM"
    SOUTH_AFRICA = "ZAF"
    SOUTH_GEORGIA_AND_SOUTH_SANDWICH_ISLANDS = "SGS"
    SPAIN = "ESP"
    SRI_LANKA = "LKA"
    SUDAN = "SDN"
    SURINAME = "SUR"
    SVALBARD_AND_JAN_MAYEN = "SJM"
    ESWATINI = "SWZ"  # Formerly Swaziland
    SWEDEN = "SWE"
    SWITZERLAND = "CHE"
    SYRIA = "SYR"
    TAIWAN = "TWN"
    TAJIKISTAN = "TJK"
    THAILAND = "THA"
    TIMOR_LESTE = "TLS"
    TOGO = "TGO"
    TOKELAU = "TKL"
    TONGA = "TON"
    TRINIDAD_AND_TOBAGO = "TTO"
    TUNISIA = "TUN"
    TURKEY = "TUR"
    TURKMENISTAN = "TKM"
    TURKS_AND_CAICOS_ISLANDS = "TCA"
    TUVALU = "TUV"
    UGANDA = "UGA"
    UKRAINE = "UKR"
    UNITED_ARAB_EMIRATES = "ARE"
    UNITED_KINGDOM = "GBR"
    UNITED_STATES_MINOR_OUTLYING_ISLANDS = "UMI"
    URUGUAY = "URY"
    UZBEKISTAN = "UZB"
    VANUATU = "VUT"
    VENEZUELA = "VEN"
    VIETNAM = "VNM"
    BRITISH_VIRGIN_ISLANDS = "VGB"
    US_VIRGIN_ISLANDS = "VIR"
    WALLIS_AND_FUTUNA = "WLF"
    WESTERN_SAHARA = "ESH"
    YEMEN = "YEM"
    ZAMBIA = "ZMB"
    ZIMBABWE = "ZWE"
    UNKNOWN = "XX"


PEO_IN_AND_INC_IN_TO_SEC_FORM_ID = {
    # US States
    Location.ALABAMA: "AL",
    Location.ALASKA: "AK",
    Location.ARIZONA: "AZ",
    Location.ARKANSAS: "AR",
    Location.CALIFORNIA: "CA",
    Location.COLORADO: "CO",
    Location.CONNECTICUT: "CT",
    Location.DELAWARE: "DE",
    Location.DISTRICT_OF_COLUMBIA: "DC",
    Location.FLORIDA: "FL",
    Location.GEORGIA: "GA",
    Location.HAWAII: "HI",
    Location.IDAHO: "ID",
    Location.ILLINOIS: "IL",
    Location.INDIANA: "IN",
    Location.IOWA: "IA",
    Location.KANSAS: "KS",
    Location.KENTUCKY: "KY",
    Location.LOUISIANA: "LA",
    Location.MAINE: "ME",
    Location.MARYLAND: "MD",
    Location.MASSACHUSETTS: "MA",
    Location.MICHIGAN: "MI",
    Location.MINNESOTA: "MN",
    Location.MISSISSIPPI: "MS",
    Location.MISSOURI: "MO",
    Location.MONTANA: "MT",
    Location.NEBRASKA: "NE",
    Location.NEVADA: "NV",
    Location.NEW_HAMPSHIRE: "NH",
    Location.NEW_JERSEY: "NJ",
    Location.NEW_MEXICO: "NM",
    Location.NEW_YORK: "NY",
    Location.NORTH_CAROLINA: "NC",
    Location.NORTH_DAKOTA: "ND",
    Location.OHIO: "OH",
    Location.OKLAHOMA: "OK",
    Location.OREGON: "OR",
    Location.PENNSYLVANIA: "PA",
    Location.RHODE_ISLAND: "RI",
    Location.SOUTH_CAROLINA: "SC",
    Location.SOUTH_DAKOTA: "SD",
    Location.TENNESSEE: "TN",
    Location.TEXAS: "TX",
    Location.UTAH: "UT",
    Location.VERMONT: "VT",
    Location.VIRGINIA: "VA",
    Location.WASHINGTON: "WA",
    Location.WEST_VIRGINIA: "WV",
    Location.WISCONSIN: "WI",
    Location.WYOMING: "WY",
    # Canadian Provinces
    Location.ALBERTA: "A0",
    Location.BRITISH_COLUMBIA: "A1",
    Location.CANADA: "Z4",  # Canada (Federal Level)
    Location.MANITOBA: "A2",
    Location.NEW_BRUNSWICK: "A3",
    Location.NEWFOUNDLAND_AND_LABRADOR: "A4",
    Location.NOVA_SCOTIA: "A5",
    Location.ONTARIO: "A6",
    Location.PRINCE_EDWARD_ISLAND: "A7",
    Location.QUEBEC: "A8",
    Location.SASKATCHEWAN: "A9",
    Location.YUKON: "B0",
    # Countries
    Location.AFGHANISTAN: "B2",
    Location.ALAND_ISLANDS: "Y6",
    Location.ALBANIA: "B3",
    Location.ALGERIA: "B4",
    Location.AMERICAN_SAMOA: "B5",
    Location.ANDORRA: "B6",
    Location.ANGOLA: "B7",
    Location.ANGUILLA: "1A",
    Location.ANTARCTICA: "B8",
    Location.ANTIGUA_AND_BARBUDA: "B9",
    Location.ARGENTINA: "C1",
    Location.ARMENIA: "1B",
    Location.ARUBA: "1C",
    Location.AUSTRALIA: "C3",
    Location.AUSTRIA: "C4",
    Location.AZERBAIJAN: "1D",
    Location.BAHAMAS: "C5",
    Location.BAHRAIN: "C6",
    Location.BANGLADESH: "C7",
    Location.BARBADOS: "C8",
    Location.BELARUS: "1F",
    Location.BELGIUM: "C9",
    Location.BELIZE: "D1",
    Location.BENIN: "G6",
    Location.BERMUDA: "D0",
    Location.BHUTAN: "D2",
    Location.BOLIVIA: "D3",
    Location.BOSNIA_AND_HERZEGOVINA: "1E",
    Location.BOTSWANA: "B1",
    Location.BOUVET_ISLAND: "D4",
    Location.BRAZIL: "D5",
    Location.BRITISH_INDIAN_OCEAN_TERRITORY: "D6",
    Location.BRUNEI_DARUSSALAM: "D9",
    Location.BULGARIA: "E0",
    Location.BURKINA_FASO: "X2",
    Location.BURUNDI: "E2",
    Location.CAMBODIA: "E3",
    Location.CAMEROON: "E4",
    Location.CAPE_VERDE: "E8",
    Location.CAYMAN_ISLANDS: "E9",
    Location.CENTRAL_AFRICAN_REPUBLIC: "F0",
    Location.CHAD: "F2",
    Location.CHILE: "F3",
    Location.CHINA: "F4",
    Location.CHRISTMAS_ISLAND: "F6",
    Location.COCOS_KEELING_ISLANDS: "F7",
    Location.COLOMBIA: "F8",
    Location.COMOROS: "F9",
    Location.CONGO: "G0",
    Location.CONGO_DEMOCRATIC_REPUBLIC: "Y3",
    Location.COOK_ISLANDS: "G1",
    Location.COSTA_RICA: "G2",
    Location.COTE_DIVOIRE: "L7",
    Location.CROATIA: "1M",
    Location.CUBA: "G3",
    Location.CYPRUS: "G4",
    Location.CZECH_REPUBLIC: "2N",
    Location.DENMARK: "G7",
    Location.DJIBOUTI: "1G",
    Location.DOMINICA: "G9",
    Location.DOMINICAN_REPUBLIC: "D8",
    Location.ECUADOR: "H1",
    Location.EGYPT: "H2",
    Location.EL_SALVADOR: "H3",
    Location.EQUATORIAL_GUINEA: "H4",
    Location.ERITREA: "1J",
    Location.ESTONIA: "1H",
    Location.ETHIOPIA: "H5",
    Location.FALKLAND_ISLANDS: "H7",
    Location.FAROE_ISLANDS: "H6",
    Location.FIJI: "H8",
    Location.FINLAND: "H9",
    Location.FRANCE: "I0",
    Location.FRENCH_GUIANA: "I3",
    Location.FRENCH_POLYNESIA: "I4",
    Location.FRENCH_SOUTHERN_TERRITORIES: "2C",
    Location.GABON: "I5",
    Location.GAMBIA: "I6",
    Location.GEORGIA_REPUBLIC: "2Q",
    Location.GERMANY: "2M",
    Location.GHANA: "J0",
    Location.GIBRALTAR: "J1",
    Location.GREECE: "J3",
    Location.GREENLAND: "J4",
    Location.GRENADA: "J5",
    Location.GUADELOUPE: "J6",
    Location.GUAM: "GU",
    Location.GUATEMALA: "J8",
    Location.GUERNSEY: "Y7",
    Location.GUINEA: "J9",
    Location.GUINEA_BISSAU: "S0",
    Location.GUYANA: "K0",
    Location.HAITI: "K1",
    Location.HEARD_AND_MCDONALD_ISLANDS: "K4",
    Location.HOLY_SEE_VATICAN_CITY: "X4",
    Location.HONDURAS: "K2",
    Location.HONG_KONG: "K3",
    Location.HUNGARY: "K5",
    Location.ICELAND: "K6",
    Location.INDIA: "K7",
    Location.INDONESIA: "K8",
    Location.IRAN: "K9",
    Location.IRAQ: "L0",
    Location.IRELAND: "L2",
    Location.ISLE_OF_MAN: "Y8",
    Location.ISRAEL: "L3",
    Location.ITALY: "L6",
    Location.JAMAICA: "L8",
    Location.JAPAN: "M0",
    Location.JERSEY: "Y9",
    Location.JORDAN: "M2",
    Location.KAZAKHSTAN: "1P",
    Location.KENYA: "M3",
    Location.KIRIBATI: "J2",
    Location.NORTH_KOREA: "M4",
    Location.SOUTH_KOREA: "M5",
    Location.KUWAIT: "M6",
    Location.KYRGYZSTAN: "1N",
    Location.LAOS: "M7",
    Location.LATVIA: "1R",
    Location.LEBANON: "M8",
    Location.LESOTHO: "M9",
    Location.LIBERIA: "N0",
    Location.LIBYA: "N1",
    Location.LIECHTENSTEIN: "N2",
    Location.LITHUANIA: "1Q",
    Location.LUXEMBOURG: "N4",
    Location.MACAU: "N5",
    Location.MACEDONIA: "1U",
    Location.MADAGASCAR: "N6",
    Location.MALAWI: "N7",
    Location.MALAYSIA: "N8",
    Location.MALDIVES: "N9",
    Location.MALI: "O0",
    Location.MALTA: "O1",
    Location.MARSHALL_ISLANDS: "1T",
    Location.MARTINIQUE: "O2",
    Location.MAURITANIA: "O3",
    Location.MAURITIUS: "O4",
    Location.MAYOTTE: "2P",
    Location.MEXICO: "O5",
    Location.MICRONESIA: "1K",
    Location.MOLDOVA: "1S",
    Location.MONACO: "O9",
    Location.MONGOLIA: "P0",
    Location.MONTENEGRO: "Z5",
    Location.MONTSERRAT: "P1",
    Location.MOROCCO: "P2",
    Location.MOZAMBIQUE: "P3",
    Location.MYANMAR: "E1",
    Location.NAMIBIA: "T6",
    Location.NAURU: "P5",
    Location.NEPAL: "P6",
    Location.NETHERLANDS: "P7",
    Location.NETHERLANDS_ANTILLES: "P8",
    Location.NEW_CALEDONIA: "1W",
    Location.NEW_ZEALAND: "Q2",
    Location.NICARAGUA: "Q3",
    Location.NIGER: "Q4",
    Location.NIGERIA: "Q5",
    Location.NIUE: "Q6",
    Location.NORFOLK_ISLAND: "Q7",
    Location.NORTHERN_MARIANA_ISLANDS: "1V",
    Location.NORWAY: "Q8",
    Location.OMAN: "P4",
    Location.PAKISTAN: "R0",
    Location.PALAU: "1Y",
    Location.PALESTINIAN_TERRITORY: "1X",
    Location.PANAMA: "R1",
    Location.PAPUA_NEW_GUINEA: "R2",
    Location.PARAGUAY: "R4",
    Location.PERU: "R5",
    Location.PHILIPPINES: "R6",
    Location.PITCAIRN: "R8",
    Location.POLAND: "R9",
    Location.PORTUGAL: "S1",
    Location.PUERTO_RICO: "PR",
    Location.QATAR: "S3",
    Location.REUNION: "S4",
    Location.ROMANIA: "S5",
    Location.RUSSIAN_FEDERATION: "1Z",
    Location.RWANDA: "S6",
    Location.SAINT_BARTHELEMY: "Z0",
    Location.SAINT_HELENA: "U8",
    Location.SAINT_KITTS_AND_NEVIS: "U7",
    Location.SAINT_LUCIA: "U9",
    Location.SAINT_MARTIN: "Z1",
    Location.SAINT_PIERRE_AND_MIQUELON: "V0",
    Location.SAINT_VINCENT_AND_GRENADINES: "V1",
    Location.SAMOA: "Y0",
    Location.SAN_MARINO: "S8",
    Location.SAO_TOME_AND_PRINCIPE: "S9",
    Location.SAUDI_ARABIA: "T0",
    Location.SENEGAL: "T1",
    Location.SERBIA: "Z2",
    Location.SEYCHELLES: "T2",
    Location.SIERRA_LEONE: "T8",
    Location.SINGAPORE: "U0",
    Location.SLOVAKIA: "2B",
    Location.SLOVENIA: "2A",
    Location.SOLOMON_ISLANDS: "D7",
    Location.SOMALIA: "U1",
    Location.SOUTH_AFRICA: "T3",
    Location.SOUTH_GEORGIA_AND_SOUTH_SANDWICH_ISLANDS: "1L",
    Location.SPAIN: "U3",
    Location.SRI_LANKA: "F1",
    Location.SUDAN: "V2",
    Location.SURINAME: "V3",
    Location.SVALBARD_AND_JAN_MAYEN: "L9",
    Location.ESWATINI: "V6",
    Location.SWEDEN: "V7",
    Location.SWITZERLAND: "V8",
    Location.SYRIA: "V9",
    Location.TAIWAN: "F5",
    Location.TAJIKISTAN: "2D",
    Location.THAILAND: "W1",
    Location.TIMOR_LESTE: "Z3",
    Location.TOGO: "W2",
    Location.TOKELAU: "W3",
    Location.TONGA: "W4",
    Location.TRINIDAD_AND_TOBAGO: "W5",
    Location.TUNISIA: "W6",
    Location.TURKEY: "W8",
    Location.TURKMENISTAN: "2E",
    Location.TURKS_AND_CAICOS_ISLANDS: "W7",
    Location.TUVALU: "2G",
    Location.UGANDA: "W9",
    Location.UKRAINE: "2H",
    Location.UNITED_ARAB_EMIRATES: "C0",
    Location.UNITED_KINGDOM: "X0",
    Location.UNITED_STATES_MINOR_OUTLYING_ISLANDS: "2J",
    Location.URUGUAY: "X3",
    Location.UZBEKISTAN: "2K",
    Location.VANUATU: "2L",
    Location.VENEZUELA: "X5",
    Location.VIETNAM: "Q1",
    Location.BRITISH_VIRGIN_ISLANDS: "D8",
    Location.US_VIRGIN_ISLANDS: "VI",
    Location.WALLIS_AND_FUTUNA: "X8",
    Location.WESTERN_SAHARA: "Y1",
    Location.YEMEN: "T7",
    Location.ZAMBIA: "Y4",
    Location.ZIMBABWE: "Y5",
    Location.UNKNOWN: "XX",
}

TEXT_SEARCH_LOCATIONS_MAPPING = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District of Columbia",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "X1": "United States",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
    "A0": "Alberta, Canada",
    "A1": "British Columbia, Canada",
    "Z4": "Canada (Federal Level)",
    "A2": "Manitoba, Canada",
    "A3": "New Brunswick, Canada",
    "A4": "Newfoundland, Canada",
    "A5": "Nova Scotia, Canada",
    "A6": "Ontario, Canada",
    "A7": "Prince Edward Island, Canada",
    "A8": "Quebec, Canada",
    "A9": "Saskatchewan, Canada",
    "B0": "Yukon, Canada",
    "B2": "Afghanistan",
    "Y6": "Aland Islands",
    "B3": "Albania",
    "B4": "Algeria",
    "B5": "American Samoa",
    "B6": "Andorra",
    "B7": "Angola",
    "1A": "Anguilla",
    "B8": "Antarctica",
    "B9": "Antigua and Barbuda",
    "C1": "Argentina",
    "1B": "Armenia",
    "1C": "Aruba",
    "C3": "Australia",
    "C4": "Austria",
    "1D": "Azerbaijan",
    "C5": "Bahamas",
    "C6": "Bahrain",
    "C7": "Bangladesh",
    "C8": "Barbados",
    "1F": "Belarus",
    "C9": "Belgium",
    "D1": "Belize",
    "G6": "Benin",
    "D0": "Bermuda",
    "D2": "Bhutan",
    "D3": "Bolivia",
    "1E": "Bosnia and Herzegovina",
    "B1": "Botswana",
    "D4": "Bouvet Island",
    "D5": "Brazil",
    "D6": "British Indian Ocean Territory",
    "D9": "Brunei Darussalam",
    "E0": "Bulgaria",
    "X2": "Burkina Faso",
    "E2": "Burundi",
    "E3": "Cambodia",
    "E4": "Cameroon",
    "E8": "Cape Verde",
    "E9": "Cayman Islands",
    "F0": "Central African Republic",
    "F2": "Chad",
    "F3": "Chile",
    "F4": "China",
    "F6": "Christmas Island",
    "F7": "Cocos (Keeling) Islands",
    "F8": "Colombia",
    "F9": "Comoros",
    "G0": "Congo",
    "Y3": "Congo, the Democratic Republic of the",
    "G1": "Cook Islands",
    "G2": "Costa Rica",
    "L7": "Cote D'ivoire ",
    "1M": "Croatia",
    "G3": "Cuba",
    "G4": "Cyprus",
    "2N": "Czech Republic",
    "G7": "Denmark",
    "1G": "Djibouti",
    "G9": "Dominica",
    "G8": "Dominican Republic",
    "H1": "Ecuador",
    "H2": "Egypt",
    "H3": "El Salvador",
    "H4": "Equatorial Guinea",
    "1J": "Eritrea",
    "1H": "Estonia",
    "H5": "Ethiopia",
    "H7": "Falkland Islands (Malvinas)",
    "H6": "Faroe Islands",
    "H8": "Fiji",
    "H9": "Finland",
    "I0": "France",
    "I3": "French Guiana",
    "I4": "French Polynesia",
    "2C": "French Southern Territories",
    "I5": "Gabon",
    "I6": "Gambia",
    "2Q": "Georgia (country)",
    "2M": "Germany",
    "J0": "Ghana",
    "J1": "Gibraltar",
    "J3": "Greece",
    "J4": "Greenland",
    "J5": "Grenada",
    "J6": "Guadeloupe",
    "GU": "Guam",
    "J8": "Guatemala",
    "Y7": "Guernsey",
    "J9": "Guinea",
    "S0": "Guinea-bissau",
    "K0": "Guyana",
    "K1": "Haiti",
    "K4": "Heard Island and Mcdonald Islands",
    "X4": "Holy See (Vatican City State)",
    "K2": "Honduras",
    "K3": "Hong Kong",
    "K5": "Hungary",
    "K6": "Iceland",
    "K7": "India",
    "K8": "Indonesia",
    "K9": "Iran, Islamic Republic of",
    "L0": "Iraq",
    "L2": "Ireland",
    "Y8": "Isle of Man",
    "L3": "Israel",
    "L6": "Italy",
    "L8": "Jamaica",
    "M0": "Japan",
    "Y9": "Jersey",
    "M2": "Jordan",
    "1P": "Kazakhstan",
    "M3": "Kenya",
    "J2": "Kiribati",
    "M4": "Korea, Democratic People's Republic of ",
    "M5": "Korea, Republic of",
    "M6": "Kuwait",
    "1N": "Kyrgyzstan",
    "M7": "Lao People's Democratic Republic ",
    "1R": "Latvia",
    "M8": "Lebanon",
    "M9": "Lesotho",
    "N0": "Liberia",
    "N1": "Libyan Arab Jamahiriya",
    "N2": "Liechtenstein",
    "1Q": "Lithuania",
    "N4": "Luxembourg",
    "N5": "Macau",
    "1U": "Macedonia, the Former Yugoslav Republic of",
    "N6": "Madagascar",
    "N7": "Malawi",
    "N8": "Malaysia",
    "N9": "Maldives",
    "O0": "Mali",
    "O1": "Malta",
    "1T": "Marshall Islands",
    "O2": "Martinique",
    "O3": "Mauritania",
    "O4": "Mauritius",
    "2P": "Mayotte",
    "O5": "Mexico",
    "1K": "Micronesia, Federated States of",
    "1S": "Moldova, Republic of",
    "O9": "Monaco",
    "P0": "Mongolia",
    "Z5": "Montenegro",
    "P1": "Montserrat",
    "P2": "Morocco",
    "P3": "Mozambique",
    "E1": "Myanmar",
    "T6": "Namibia",
    "P5": "Nauru",
    "P6": "Nepal",
    "P7": "Netherlands",
    "P8": "Netherlands Antilles",
    "1W": "New Caledonia",
    "Q2": "New Zealand",
    "Q3": "Nicaragua",
    "Q4": "Niger",
    "Q5": "Nigeria",
    "Q6": "Niue",
    "Q7": "Norfolk Island",
    "1V": "Northern Mariana Islands",
    "Q8": "Norway",
    "P4": "Oman",
    "R0": "Pakistan",
    "1Y": "Palau",
    "1X": "Palestinian Territory, Occupied",
    "R1": "Panama",
    "R2": "Papua New Guinea",
    "R4": "Paraguay",
    "R5": "Peru",
    "R6": "Philippines",
    "R8": "Pitcairn",
    "R9": "Poland",
    "S1": "Portugal",
    "PR": "Puerto Rico",
    "S3": "Qatar",
    "S4": "Reunion",
    "S5": "Romania",
    "1Z": "Russian Federation",
    "S6": "Rwanda",
    "Z0": "Saint Barthelemy",
    "U8": "Saint Helena",
    "U7": "Saint Kitts and Nevis",
    "U9": "Saint Lucia",
    "Z1": "Saint Martin",
    "V0": "Saint Pierre and Miquelon",
    "V1": "Saint Vincent and the Grenadines",
    "Y0": "Samoa",
    "S8": "San Marino",
    "S9": "Sao Tome and Principe",
    "T0": "Saudi Arabia",
    "T1": "Senegal",
    "Z2": "Serbia",
    "T2": "Seychelles",
    "T8": "Sierra Leone",
    "U0": "Singapore",
    "2B": "Slovakia",
    "2A": "Slovenia",
    "D7": "Solomon Islands",
    "U1": "Somalia",
    "T3": "South Africa",
    "1L": "South Georgia and the South Sandwich Islands",
    "U3": "Spain",
    "F1": "Sri Lanka",
    "V2": "Sudan",
    "V3": "Suriname",
    "L9": "Svalbard and Jan Mayen",
    "V6": "Swaziland",
    "V7": "Sweden",
    "V8": "Switzerland",
    "V9": "Syrian Arab Republic",
    "F5": "Taiwan, Province of China",
    "2D": "Tajikistan",
    "W0": "Tanzania, United Republic of",
    "W1": "Thailand",
    "Z3": "Timor-leste",
    "W2": "Togo",
    "W3": "Tokelau",
    "W4": "Tonga",
    "W5": "Trinidad and Tobago",
    "W6": "Tunisia",
    "W8": "Turkey",
    "2E": "Turkmenistan",
    "W7": "Turks and Caicos Islands",
    "2G": "Tuvalu",
    "W9": "Uganda",
    "2H": "Ukraine",
    "C0": "United Arab Emirates",
    "X0": "United Kingdom",
    "2J": "United States Minor Outlying Islands",
    "X3": "Uruguay",
    "2K": "Uzbekistan",
    "2L": "Vanuatu",
    "X5": "Venezuela",
    "Q1": "Viet Nam",
    "D8": "Virgin Islands, British",
    "VI": "Virgin Islands, U.s.",
    "X8": "Wallis and Futuna",
    "U5": "Western Sahara",
    "T7": "Yemen",
    "Y4": "Zambia",
    "Y5": "Zimbabwe",
    "XX": "Unknown",
}

TEXT_SEARCH_FORM_MAPPING = {
    "4": {
        "description": "Statement of changes in beneficial ownership of securities",
        "title": "Insider trading report",
    },
    "8-K": {"description": "Current report", "title": "Current report"},
    "SC 13G": {
        "description": "Schedule filed to report acquisition of beneficial ownership of 5% or more of a class of equity securities by passive investors and certain institutions",
        "title": "Beneficial ownership report",
    },
    "D": {
        "description": "Notice of sales of securities on Form D (Regulation D)",
        "title": "Notice of sales of unregistered securities",
    },
    "3": {
        "description": "Initial statement of beneficial ownership of securities",
        "title": "Initial insider holdings report",
    },
    "10-Q": {
        "description": "Quarterly report pursuant to Section 13 or 15(d)",
        "title": "Quarterly report",
    },
    "424B2": {"description": "", "title": "Prospectus"},
    "6-K": {
        "description": "Current report of foreign issuer pursuant to Rules 13a-16 and 15d-16",
        "title": "Current report",
    },
    "497": {
        "description": "Definitive materials filed under paragraph (a), (b), (c), (d), (e) or (f) of Securities Act Rule 497",
        "title": "Prospectus",
    },
    "497K": {
        "description": "Summary prospectuses for open-end management investment companies registered on Form N-1A filed pursuant to Securities Act Rule 497(k)",
        "title": "Summary prospectus",
    },
    "13F-HR": {
        "description": "Further understand that each of 13F-HR, 13F-NT, and amendments thereto are mandatory electronic filings (hardship exemption exists to submit in paper; never used to the knowledge of IM staff);",
        "title": "Institutional investment manager holdings report",
    },
    "CORRESP": {"description": "", "title": "Correspondence"},
    "424B3": {"description": "", "title": "Prospectus"},
    "UPLOAD": {"description": "Upload Submission", "title": "Correspondence"},
    "SC 13D": {
        "description": "Schedule filed to report acquisition of beneficial ownership of 5% or more of a class of equity securities",
        "title": "Beneficial ownership report",
    },
    "FWP": {
        "description": "Filing under Securities Act Rule 163/433 of free writing prospectuses.",
        "title": "Prospectus",
    },
    "10-K": {
        "description": "Annual report pursuant to Section 13 or 15(d)",
        "title": "Annual report",
    },
    "EFFECT": {
        "description": "Effectiveness filing by commission order",
        "title": "SEC order",
    },
    "S-4": {
        "description": "Registration statement for securities to be issued in business combination transactions",
        "title": "Registration statement - business combination",
    },
    "485BPOS": {
        "description": "Post-effective amendment filed pursuant to Securities Act Rule 485(b) (this filing cannot be submitted as a 1940 Act only filing)",
        "title": "Prospectus materials",
    },
    "5": {
        "description": "Annual statement of changes in beneficial ownership of securities",
        "title": "Annual insider trading report",
    },
    "24F-2NT": {
        "description": "Rule 24f-2 notice filed on Form 24F-2",
        "title": "Annual notice of securities sold",
    },
    "N-Q": {
        "description": "Quarterly Schedule of Portfolio Holdings of Registered Management Investment Company filed on Form N-Q",
        "title": "Quarterly portolio holdings schedule",
    },
    "424B5": {"description": "", "title": "Prospectus"},
    "DEF 14A": {
        "description": "Proxy Statement Pursuant to Section 14(a) of the Securities Exchange Act of 1934",
        "title": "Proxy statement",
    },
    "13F-NT": {
        "description": "Further understand that each of 13F-HR, 13F-NT, and amendments thereto are mandatory electronic filings (hardship exemption exists to submit in paper; never used to the knowledge of IM staff);",
        "title": "Institutional investment manager notice",
    },
    "497J": {
        "description": "Certification of no change in definitive materials under paragraph (j) of Securities Act Rule 497",
        "title": "Prospectus materials",
    },
    "10-D": {
        "description": "Asset-Backed Issuer Distribution Report Pursuant to Section 13 or 15(d) of the Securities Exchange Act of 1934",
        "title": "Distribution report",
    },
    "DEFA14A": {
        "description": "Proxy Statement Pursuant to Section 14(a) of the Securities Exchange Act of 1934",
        "title": "Proxy materials",
    },
    "425": {
        "description": "Filing under Securities Act Rule 425 of certain prospectuses and communications in connection with business combination transactions.",
        "title": "Prospectus/communication re business combination",
    },
    "X-17A-5": {
        "description": "Annual audit report by brokers or dealers. To provide the Commission with audited statements of financial condition, income, and cash flows, and other financial materials.",
        "title": "",
    },
    "N-MFP": {
        "description": "Monthly Schedule of Portfolio Holdings of Money Market Funds on Form N-MFP",
        "title": "Monthly portfolio holdings schedule",
    },
    "S-1": {
        "description": "General form of registration statement for all companies including face-amount certificate companies",
        "title": "Registration statement",
    },
    "40-17G": {
        "description": "Fidelity bond filed pursuant to Rule 17g-1(g)(1) of the Investment Company Act of 1940.",
        "title": "",
    },
    "N-CSR": {
        "description": "Certified annual shareholder report of registered management investment companies filed on Form N-CSR",
        "title": "Annual shareholder report",
    },
    "N-CSRS": {
        "description": "Certified semi-annual shareholder report of registered management investment companies filed on Form N-CSR",
        "title": "Semi-annual shareholder report",
    },
    "N-PX": {
        "description": "Annual Report of Proxy Voting Record of Registered Management Investment Companies filed on Form N-PX",
        "title": "Annual proxy voting report",
    },
    "NSAR-B": {
        "description": "Annual report for management companies filed on Form N-SAR",
        "title": "",
    },
    "NSAR-A": {
        "description": "Semi-annual report for management companies filed on Form N-SAR",
        "title": "",
    },
    "NT 10-Q": {"description": "", "title": "Late filing notice"},
    "S-3ASR": {
        "description": "Automatic shelf registration statement of securities of well-known seasoned issuers",
        "title": "Registration statement",
    },
    "40-APP": {
        "description": "Application for an order of exemptive or other relief filed under the Investment Company Act of 1940",
        "title": "",
    },
    "S-3": {
        "description": "Registration statement for specified transactions by certain issuers including face-amount certificate companies",
        "title": "Registration statement",
    },
    "S-8": {
        "description": "Initial registration statement for securities to be offered to employees pursuant to employee benefit plans",
        "title": "Registration statement",
    },
    "19B-4E": {"description": "", "title": ""},
    "POSASR": {
        "description": "Post-effective amendment to an automatic shelf registration statement of Form S-3ASR or Form F-3ASR",
        "title": "Post-effective amendment",
    },
    "S-8 POS": {
        "description": "Post-effective amendment to a S-8 registration statement",
        "title": "Post-effective amendment",
    },
    "S-6": {
        "description": "Initial registration statement filed on Form S-6 for unit investment trusts",
        "title": "",
    },
    "FOCUSN": {"description": "", "title": ""},
    "485BXT": {
        "description": "Post-effective amendment filed pursuant to Securities Act Rule 485(b)(1)(iii) to designate a new effective date for a post-effective amendment previously filed pursuant to Securities Act Rule 485(a) (this filing cannot be submitted as a 1940 Act only fili",
        "title": "",
    },
    "POS AM": {
        "description": "Post-effective amendment to a registration statement that is not immediately effective upon filing",
        "title": "Post-effective amendment",
    },
    "N-MFP2": {
        "description": "Monthly Schedule of Portfolio Holdings of Money Market Funds on Form N-MFP",
        "title": "Monthly portfolio holdings schedule",
    },
    "MA-I": {
        "description": "Information Regarding Natural Persons Who Engage in Municipal Advisory Activities",
        "title": "",
    },
    "11-K": {
        "description": "Annual reports of employee stock purchase, savings and similar plans pursuant to Section 15(d)",
        "title": "Annual report",
    },
    "485APOS": {
        "description": "Post-effective amendment filed pursuant to Securities Act Rule 485(a) (this filing cannot be submitted as a 1940 Act only filing)",
        "title": "Prospectus materials",
    },
    "25-NSE": {"description": "", "title": ""},
    "NT 10-K": {"description": "", "title": "Late filing notice"},
    "CT ORDER": {"description": "", "title": "Confidential order"},
    "ARS": {
        "description": "Annual report to security holders. ",
        "title": "Annual report",
    },
    "SC TO-I": {
        "description": "Issuer tender offer statement",
        "title": "Tender offer statement",
    },
    "ABS-15G": {"description": "Asset-Backed Securitizer Report", "title": ""},
    "PRE 14A": {
        "description": "Proxy Statement Pursuant to Section 14(a) of the Securities Exchange Act of 1934",
        "title": "Proxy statement (preliminary)",
    },
    "SC TO-T": {
        "description": "Third party tender offer statement",
        "title": "Tender offer statement",
    },
    "DFAN14A": {
        "description": "Definitive additional proxy soliciting materials filed by non-management including Rule 14(a)(12) material.",
        "title": "Proxy soliciting materials",
    },
    "487": {
        "description": "Pre-effective pricing amendments filed pursuant to Securities Act Rule 487",
        "title": "",
    },
    "8-A12B": {"description": "", "title": "Registration statement"},
    "20-F": {
        "description": "Registration statement under Section 12 of the Securities Exchange Act of 1934 or an annual or transition report filed under Section 13(a) or 15(d) of the Exchange Act for a  foreign private issuer.",
        "title": "Annual report - foreign issuer",
    },
    "F-6EF": {
        "description": "Auto effective registration statement for American Depositary Receipts representing securities of certain foreign private issuers",
        "title": "Registration statement",
    },
    "40-17F2": {
        "description": "Initial certificate of accounting of securities and similar investments in the custody of management investment companies filed pursuant to Rule 17f-2 of the Investment Company Act of 1940 filed on Form N-17F-2",
        "title": "",
    },
    "SD": {
        "description": "Specialized Disclosure Report",
        "title": "Specialized disclosure",
    },
    "144": {
        "description": "Filing for proposed sale of securities under Rule 144.",
        "title": "Sale of securities",
    },
    "NSAR-U": {
        "description": "Annual report for unit investment trusts filed on Form N-SAR",
        "title": "",
    },
    "ABS-EE": {
        "description": "Form for Submission of Electronic Exhibits in Asset-Backed Securities Offerings",
        "title": "",
    },
    "DEF 14C": {
        "description": "Information Statement Pursuant to Section 14(c) of the Securities Exchange Act of 1934",
        "title": "Information statement",
    },
    "15-15D": {"description": "", "title": "Suspension notice"},
    "SC 14D9": {
        "description": "Tender offer solicitation / recommendation statements filed under Rule 14-d9",
        "title": "Recommendation statement",
    },
    "RW": {"description": "Registration Withdrawal Request", "title": "Withdrawal"},
    "F-3": {
        "description": "Registration statement for specified transactions by certain foreign private issuers",
        "title": "Registration statement",
    },
    "F-4": {
        "description": "Registration statement for securities issued by foreign private issuers in certain business combination transactions",
        "title": "Registration statement",
    },
    "DRS": {"description": "", "title": "Draft registration statement"},
    "N-30B-2": {
        "description": "Periodic and interim reports mailed to investment company shareholders (other than annual and semi-annual reports mailed to shareholders pursuant to Rule 30e-1)",
        "title": "Shareholder reports",
    },
    "T-3": {
        "description": "Initial application for qualification of trust indentures",
        "title": "",
    },
    "REVOKED": {"description": "", "title": ""},
    "N-30D": {
        "description": "Initial annual and semi-annual reports mailed to investment company shareholders pursuant to Rule 30e-1 (other than those required to be submitted as part of Form N-CSR)",
        "title": "",
    },
    "N-2": {
        "description": "Filing of a registration statement on Form N-2 for closed-end investment companies",
        "title": "",
    },
    "PRE 14C": {
        "description": "Information Statement Pursuant to Section 14(c) of the Securities Exchange Act of 1934",
        "title": "Information statement (preliminary)",
    },
    "424B4": {"description": "", "title": "Prospectus"},
    "15-12G": {"description": "", "title": "Termination notice"},
    "NO ACT": {"description": "", "title": ""},
    "TA-2": {
        "description": "Annual report of transfer agent activities filed pursuant to the Securities Exchange Act of 1934. IN contains information necessary to monitor transfer agent registration",
        "title": "",
    },
    "N-CEN": {
        "description": "Form N-CEN will require annual reporting of certain census-type information in a structured XML format. Form N-CEN will replace Form N-SAR.  The compliance date for Form N-CEN filers – regardless of asset size – is June 1, 2018.",
        "title": "Annual report",
    },
    "N-MFP1": {
        "description": "Monthly Schedule of Portfolio Holdings of Money Market Funds on Form N-MFP",
        "title": "Monthly portfolio holdings schedule",
    },
    "SUPPL": {
        "description": "Voluntary supplemental material filed pursuant to Section 11(a) of the Securities Act of 1933 by foreign issuers",
        "title": "",
    },
    "C": {"description": "Offering Statement", "title": "Offering statement"},
    "SC TO-C": {
        "description": "Written communication relating to an issuer or third party tender offer",
        "title": "Tender offer communication",
    },
    "10-12G": {"description": "", "title": "Registration statement"},
    "POS EX": {
        "description": "Post-effective amendment filed solely to add exhibits to a registration statement",
        "title": "",
    },
    "F-6 POS": {
        "description": "Post-effective amendment to a F-6EF registration",
        "title": "Post-effective amendment",
    },
    "SC 13E3": {
        "description": "Schedule filed to report going private transactions",
        "title": "Going private transaction",
    },
    "40-24B2": {
        "description": "Filing of sales literature pursuant to Rule 24b-2 under the Investment Company Act of 1940.",
        "title": "",
    },
    "CERTNYS": {"description": "", "title": ""},
    "F-1": {
        "description": "Registration statement for certain foreign private issuers",
        "title": "Registration statement",
    },
    "NPORT-EX": {
        "description": "Portfolio holdings exhibit",
        "title": "Quarterly portfolio holdings schedule",
    },
    "NPORT-P": {"description": "", "title": ""},
    "NT NPORT-P": {"description": "", "title": ""},
    "NPORT-NP": {"description": "", "title": ""},
    "IRANNOTICE": {
        "description": "Notice of Iran-related disclosure filed pursuant to Section 13(r)(3) of the Exchange Act",
        "title": "",
    },
    "PRER14A": {
        "description": "Proxy Statement Pursuant to Section 14(a) of the Securities Exchange Act of 1934",
        "title": "Proxy statement (preliminary)",
    },
    "1-A": {
        "description": "REGULATION A OFFERING STATEMENT UNDER THE SECURITIES ACT OF 1933",
        "title": "Offering statement",
    },
    "15-12B": {"description": "", "title": "Termination notice"},
    "497AD": {
        "description": "Filing by certain investment companies of Securities Act Rule 482 advertising in accordance with Securities Act Rule 497 and the Note to Rule 482(c).  ",
        "title": "",
    },
    "N-8F": {
        "description": "Application for deregistration made on Form N-8F",
        "title": "",
    },
    "PX14A6G": {"description": "", "title": ""},
    "POS AMI": {
        "description": "Amendment (for filings made under the1940 Act only)",
        "title": "",
    },
    "CB": {
        "description": "Notification form filed in connection with certain tender offers, business combinations and rights offerings, in which the subject company is a foreign private issuer of which less than 10% of its securities are held by U.S. persons.",
        "title": "",
    },
    "N-14": {
        "description": "Initial registration statement filed on Form N-14 for open-end investment company, including those filed with automatic effectiveness under Rule 488 (business combinations).",
        "title": "",
    },
    "F-6": {
        "description": "Registration statement for American Depositary Receipts representing securities of certain foreign private issuers",
        "title": "Registration statement (foreign issuer)",
    },
    "DRSLTR": {
        "description": "Correspondence Submission of a DRS filer. Correspondence is not publicly disseminated immediately. The SEC staff may publicly release all or portions of these documents.",
        "title": "",
    },
    "305B2": {
        "description": "Application for designation of a new trustee under the Trust Indenture Act",
        "title": "",
    },
    "CERTNAS": {"description": "", "title": ""},
    "424B7": {"description": "", "title": "Prospectus"},
    "DEFM14A": {
        "description": "Proxy Statement Pursuant to Section 14(a) of the Securities Exchange Act of 1934",
        "title": "Proxy statement (business combination)",
    },
    "MA": {
        "description": "Application For Municipal Advisor Registration",
        "title": "",
    },
    "S-11": {
        "description": "Registration statement for securities to be issued by real estate companies",
        "title": "Registration statement",
    },
    "AW": {
        "description": "Withdrawal of amendment to a registration statement filed under the Securities Act",
        "title": "Withdrawal",
    },
    "TA-1": {
        "description": "Application for registration as a transfer agent filed pursuant to the Securities Exchange Act of 1934. It contains information necessary to consider the Transfer Agent registration",
        "title": "",
    },
    "F-X": {
        "description": "For appointment of agent for service of process by issuers registering securities (if filed on Form F-8, F-9, F-10 or F-80, or registering securities or filing periodic reports on Form 40-F, or by any person filing certain tender offer documents, or by an",
        "title": "",
    },
    "8-A12G": {"description": "", "title": "Registration statement"},
    "DEFR14A": {
        "description": "Proxy Statement Pursuant to Section 14(a) of the Securities Exchange Act of 1934",
        "title": "Proxy statement",
    },
    "18-K": {
        "description": "Annual report for foreign governments and political subdivisions",
        "title": "Annual report",
    },
    "N-8F ORDR": {"description": "N-8F Order", "title": ""},
    "40-F": {
        "description": "Registration Statement Pursuant to Section 12 of the Securities Exchange Act of 1934 or Annual Report pursuant to Section 13(a) or 15(d) of the Securities Exchange Act of 1934",
        "title": "Registration statement",
    },
    "MA-A": {
        "description": "Annual Update of Municipal Advisor Registration",
        "title": "",
    },
    "PREC14A": {
        "description": "Proxy Statement Pursuant to Section 14(a) of the Securities Exchange Act of 1934",
        "title": "Proxy statement (preliminary)",
    },
    "N-8F NTC": {"description": "N-8F Notice", "title": ""},
    "POS 8C": {
        "description": "Post-effective amendment filed under the 1933 Act only or under both the 1933 and 1940 Acts pursuant to Section 8(c) of the 1933 Act by closed-end investment companies (this filing cannot be submitted as a 1940 Act only filing)",
        "title": "",
    },
    "PREM14A": {
        "description": "Proxy Statement Pursuant to Section 14(a) of the Securities Exchange Act of 1934",
        "title": "Proxy statement (preliminary)",
    },
    "PRRN14A": {
        "description": "Proxy Statement Pursuant to Section 14(a) of the Securities Exchange Act of 1934",
        "title": "Proxy statement (preliminary)",
    },
    "N-4": {
        "description": "Initial registration statement on Form N-4 for separate accounts (unit investment trusts)",
        "title": "",
    },
    "N-8A": {
        "description": "Initial notification of registration under section 8(a) filed on Form N-8A",
        "title": "",
    },
    "424H": {"description": "", "title": ""},
    "N-1A": {
        "description": "Initial registration statement including amendments for open-end management investment companies",
        "title": "",
    },
    "CERT": {"description": "", "title": ""},
    "F-3ASR": {
        "description": "Automatic shelf registration statement of securities of well-known seasoned issuers",
        "title": "Registration statement",
    },
    "1": {"description": "", "title": ""},
    "DEFC14A": {
        "description": "Proxy Statement Pursuant to Section 14(a) of the Securities Exchange Act of 1934",
        "title": "Proxy statement",
    },
    "424B1": {"description": "", "title": "Prospectus"},
    "10-12B": {"description": "", "title": "Registration statement"},
    "SC14D9C": {
        "description": "Written communication by the subject company relating to a third party tender offer",
        "title": "Tender offer communication",
    },
    "F-10": {
        "description": "Registration statement for securities of certain Canadian issuers under the Securities Act of 1933",
        "title": "Registration statement",
    },
    "APP NTC": {"description": "40-APP Notice", "title": ""},
    "N-23C3A": {"description": "", "title": ""},
    "40-OIP": {
        "description": "Application for an order of exemptive or other relief filed under the Investment Company Act of 1940",
        "title": "",
    },
    "25": {
        "description": "Notification of removal from listing and/or registration from a national securities exchange",
        "title": "Notice of listing removal",
    },
    "APP ORDR": {"description": "40-APP Order", "title": ""},
    "APP WD": {
        "description": "Withdrawal of an application for exemptive or other relief from the federal securities laws",
        "title": "",
    },
    "PRER14C": {
        "description": "Information Statement Pursuant to Section 14(c) of the Securities Exchange Act of 1934",
        "title": "Proxy statement (preliminary)",
    },
    "424B8": {"description": "", "title": "Prospectus"},
    "253G2": {"description": "", "title": ""},
    "1-U": {
        "description": "Current Report Pursuant to Regulation A",
        "title": "Current report",
    },
    "SC 14F1": {
        "description": "Statement regarding change in majority of directors pursuant to Rule 14f-1",
        "title": "Change in board majority",
    },
    "C-U": {"description": "Progress Update", "title": "Progess update"},
    "N-23C-2": {
        "description": "Notice by closed-end investment companies of intention to call or redeem their own securities under Investment Company Act Rule 23c-2",
        "title": "",
    },
    "S-1MEF": {
        "description": "A new registration statement filed under Rule 462(b) to add securities to a prior related effective registration statement filed on Form S-1",
        "title": "Registration statement",
    },
    "NT 20-F": {"description": "", "title": "Late filing notice"},
    "QUALIF": {"description": "", "title": "Qualification"},
    "C-AR": {"description": "Annual Report", "title": "Annual report"},
    "DEL AM": {
        "description": "Separately filed delaying amendment under Securities Act Rule 473 to delay effectiveness of a 1933 Act registration statement",
        "title": "Delaying amendment",
    },
    "1-A POS": {"description": "", "title": "Post-qualification amendment"},
    "NTN 10Q": {"description": "", "title": ""},
    "ADV-NR": {"description": "", "title": ""},
    "SF-3": {
        "description": "Shelf registration statement for qualified offerings of asset-backed securities",
        "title": "Registration statement",
    },
    "486BPOS": {
        "description": "Post-effective amendment to filing filed pursuant to Securities Act Rule 486(b)",
        "title": "",
    },
    "40-6B": {
        "description": "Application under the Investment Company Act of 1940 by an employees securities company",
        "title": "",
    },
    "CERTARCA": {"description": "", "title": ""},
    "10-KT": {"description": "", "title": "Transition report"},
    "NTN 10K": {"description": "", "title": ""},
    "DSTRBRPT": {
        "description": "Distribution of primary obligations Development Bank report",
        "title": "",
    },
    "40-17F1": {
        "description": "Initial certificate of accounting of securities and similar investments in the custody of management investment companies filed pursuant to Rule 17f-1 of the Investment Company Act of 1940 filed on Form N-17F-1",
        "title": "",
    },
    "N-14 8C": {
        "description": "Initial registration statement filed on Form N-14 by closed-end investment company (business combinations)",
        "title": "",
    },
    "ADV-E": {"description": "", "title": ""},
    "S-3MEF": {
        "description": "A new registration statement filed under Rule 462(b) to add securities to a prior related effective registration statement filed on Form S-3",
        "title": "Registration statement",
    },
    "40-33": {
        "description": "Copies of all stockholder derivative actions filed with a court against an investment company or an affiliate thereof pursuant to Section 33 of the Investment Company Act of 1940. ",
        "title": "",
    },
    "N-18F1": {
        "description": "Initial notification of election pursuant to Rule 18f-1 filed on Form N-18F-1 [under the Investment Company Act of 1940 by a registered open-end investment company].",
        "title": "",
    },
    "N-6": {
        "description": "Initial registration statement filed on Form N-6 for separate accounts (unit investment trusts)",
        "title": "",
    },
    "SE": {"description": "", "title": ""},
    "S-B": {
        "description": "Registration statement for securities of foreign governments and subdivisions thereof under the Securities Act of 1933 (Schedule b)",
        "title": "Registration statement",
    },
    "MA-W": {
        "description": "Notice of Withdrawal From Registration as a Municipal Advisor",
        "title": "",
    },
    "F-N": {
        "description": "Notification of the appointment of an agent for service by certain foreign institutions.",
        "title": "",
    },
    "DOS": {"description": "Persons who", "title": ""},
    "1-K": {"description": "Regulation A Annual Report", "title": "Annual report"},
    "1-SA": {
        "description": "SEMIANNUAL REPORT PURSUANT TO REGULATION A or SPECIAL FINANCIAL REPORT PURSUANT TO REGULATION A",
        "title": "Semiannual report",
    },
    "CFPORTAL": {
        "description": "It contains information to consider registration as a crowdfunding portal",
        "title": "",
    },
    "NT N-MFP": {
        "description": "EDGAR generated form type for late filing of  Monthly Schedule of Portfolio Holdings of Money Market Funds on Form N-MFP",
        "title": "",
    },
    "S-3D": {
        "description": "Automatically effective registration statement for securities issued pursuant to dividend or interest reinvestment plans",
        "title": "Registration statement",
    },
    "S-3DPOS": {
        "description": "Post-effective amendment to a S-3D registration statement",
        "title": "Post-effective amendment",
    },
    "MSD": {"description": "", "title": ""},
    "13FCONP": {"description": "", "title": ""},
    "NT 11-K": {"description": "", "title": "Late filing notice"},
    "20FR12G": {"description": "", "title": ""},
    "8-K12B": {"description": "", "title": ""},
    "NSAR-BT": {
        "description": "Transitional annual report filed on Form N-SAR",
        "title": "",
    },
    "TA-W": {
        "description": "Notice of withdrawal from registration as transfer agent filed pursuant to the Securities Exchange Act of 1934. IN contains information necessary to consider the Transfer Agent registration withdrawal",
        "title": "",
    },
    "RW WD": {
        "description": "Withdrawal of a request for withdrawal of a registration statement",
        "title": "Withdrawal",
    },
    "NT-NSAR": {
        "description": "Notice under Exchange Act Rule 12b-25 of inability to timely file Form N-SAR",
        "title": "",
    },
    "PREM14C": {
        "description": "Information Statement Pursuant to Section 14(c) of the Securities Exchange Act of 1934",
        "title": "Information statement (preliminary)",
    },
    "PREN14A": {
        "description": "Proxy Statement Pursuant to Section 14(a) of the Securities Exchange Act of 1934",
        "title": "Proxy statement (preliminary)",
    },
    "OIP NTC": {"description": "40-OIP Notice", "title": ""},
    "DEFA14C": {
        "description": "Information Statement Pursuant to Section 14(c) of the Securities Exchange Act of 1934",
        "title": "Information statement materials",
    },
    "DFRN14A": {
        "description": "Revised definitive proxy statement filed by non-management",
        "title": "Proxy statement",
    },
    "N-6F": {
        "description": "Notice of intent by business development companies to elect to be subject to Sections 55 through 65 of the 1940 Act filed on Form N-6F",
        "title": "",
    },
    "OIP ORDR": {"description": "40-OIP Order", "title": ""},
    "C-W": {"description": "Offering Statement Withdrawal", "title": "Withdrawal"},
    "CERTPAC": {"description": "", "title": ""},
    "8-K12G3": {"description": "", "title": ""},
    "SC14D1F": {
        "description": "Third party tender offer statement filed pursuant to Rule 14d-1(b) by foreign issuers",
        "title": "Tender offer statement",
    },
    "DEFN14A": {
        "description": "Proxy Statement Pursuant to Section 14(a) of the Securities Exchange Act of 1934",
        "title": "Proxy statement",
    },
    "DEFM14C": {
        "description": "Information Statement Pursuant to Section 14(c) of the Securities Exchange Act of 1934",
        "title": "Information statement",
    },
    "1-A-W": {"description": "", "title": "Withdrawal"},
    "DEFR14C": {
        "description": "Information Statement Pursuant to Section 14(c) of the Securities Exchange Act of 1934",
        "title": "Information statement",
    },
    "G-FIN": {"description": "", "title": ""},
    "NRSRO-UPD": {
        "description": "Form NRSRO – Update of Registration for Nationally Recognized Statistical Rating Organizations",
        "title": "",
    },
    "NT-NCSR": {
        "description": "Notice under Exchange Act Rule 12b-25 of inability to timely file Form N-CSR (annual or semi-annual report)",
        "title": "",
    },
    "15F-12G": {"description": "", "title": "Termination notice"},
    "20FR12B": {"description": "", "title": "Registration statement"},
    "SEC STAFF ACTION": {"description": "", "title": ""},
    "DOSLTR": {"description": "", "title": ""},
    "40FR12B": {
        "description": "Registration of a class of securities of certain Canadian issuers pursuant to Section 12(b) of the 1934 Act",
        "title": "Registration statement",
    },
    "F-1MEF": {
        "description": "A new registration statement filed under Rule 462(b) to add securities to a prior related effective registration statement filed on Form F-1",
        "title": "Registration statement",
    },
    "N-54A": {
        "description": "Notification of election by business development companies to be subject to the provisions of sections 55 through 65 of the Investment Company Act",
        "title": "",
    },
    "15F-15D": {"description": "", "title": "Suspension notice"},
    "NT N-CEN": {"description": "", "title": ""},
    "15F-12B": {"description": "", "title": "Termination notice"},
    "486APOS": {
        "description": "Post-effective amendment to filing filed pursuant to Securities Act Rule 486(a)",
        "title": "",
    },
    "F-9": {
        "description": "Registration of securities of certain investment grade debt or investment grade preferred securities of certain Canadian issuers under the Securities Act of 1933",
        "title": "",
    },
    "QRTLYRPT": {
        "description": "Periodic Development Bank filing, submitted quarterly",
        "title": "",
    },
    "40-8B25": {
        "description": "Filing by investment company of application under Investment Company Act Rule 8b-25(a) requesting extension of time for filing certain information, document or report",
        "title": "",
    },
    "NT N-MFP2": {"description": "", "title": ""},
    "1-Z": {"description": "Exit Report Under Regulation A", "title": "Exit report"},
    "N-2MEF": {
        "description": "A new registration statement on Form N-2 filed under the Securities Act Rule 462(b) by closed-end investment companies to register up to an additional 20% of securities for an offering that was registered on Form N-2",
        "title": "",
    },
    "TACO": {"description": "", "title": ""},
    "CERTCBO": {"description": "", "title": ""},
    "10-QT": {"description": "", "title": "Transition report"},
    "CERTBATS": {"description": "", "title": ""},
    "S-4 POS": {
        "description": "Post-effective amendment to a S-4EF registration statement",
        "title": "Post-effective amendment",
    },
    "N-23C3B": {
        "description": "Notification of  discretionary repurchase offer [by registered closed-end investment companies or business development companies] pursuant Rule 23c-3(c) only",
        "title": "",
    },
    "40-206A": {"description": "", "title": ""},
    "NRSRO-CE": {
        "description": "Form NRSRO – Annual Certification for Nationally Recognized Statistical Rating Organizations",
        "title": "",
    },
    "APP WDG": {"description": "", "title": ""},
    "STOP ORDER": {"description": "", "title": ""},
    "424A": {"description": "", "title": "Prospectus"},
    "ANNLRPT": {
        "description": "Periodic Development Bank filing, submitted annually",
        "title": "",
    },
    "N-CR": {
        "description": "Current Report of Money Market Fund Material Events",
        "title": "",
    },
    "PX14A6N": {"description": "", "title": ""},
    "SEC STAFF LETTER": {"description": "", "title": ""},
    "N-54C": {
        "description": "Notification of withdrawal by business development companies of notification of election by business development companies to be subject to the provisions of sections 55 through 65 of the Investment Company Act",
        "title": "",
    },
    "NT-NCEN": {"description": "", "title": ""},
    "POS462B": {
        "description": "Post-effective amendment to Securities Act Rule 462(b) registration statement",
        "title": "Post-effective amendment",
    },
    "C-TR": {"description": "Termination of Reporting", "title": "Termination"},
    "2-A": {"description": "", "title": ""},
    "S-4MEF": {
        "description": "A new registration statement filed under Rule 462(b) to add securities to a prior related effective registration statement filed on Form S-4",
        "title": "Registration statement",
    },
    "ADV-H-T": {"description": "", "title": ""},
    "F-3D": {
        "description": "Registration statement for dividend or interest reinvestment plan securities of foreign private issuers",
        "title": "Registration statement",
    },
    "AW WD": {
        "description": "Withdrawal of a request for withdrawal of an amendment to a registration statement",
        "title": "Withdrawal",
    },
    "6B NTC": {"description": "40-6B Notice", "title": ""},
    "8-M": {"description": "", "title": ""},
    "NT N-MFP1": {"description": "", "title": ""},
    "N-8B-2": {
        "description": "Initial registration statement for unit investment trusts filed on Form N-8B-2",
        "title": "",
    },
    "REG-NR": {"description": "", "title": ""},
    "497H2": {
        "description": "Filings made pursuant to Securities Act Rule 497(h)(2)",
        "title": "",
    },
    "F-7": {
        "description": "Registration statement for securities of certain Canadian issuers offered for cash upon the exercise of rights granted to existing security holders under the Securities Act of 1933",
        "title": "Registration statement",
    },
    "S-11MEF": {
        "description": "A new registration statement filed under Rule 462(b) to add securities to a prior related effective registration statement filed on Form S-11",
        "title": "Registration statement",
    },
    "253G1": {"description": "", "title": "Disclosure"},
    "6B ORDR": {"description": "40-6B Order", "title": ""},
    "F-80": {
        "description": "Registration of securities of certain Canadian issuers to be issued in exchange offers or a business combination under the Securities Act of 1933",
        "title": "Registration statement",
    },
    "40-202A": {"description": "", "title": ""},
    "SC 14N": {
        "description": "Information to be included in statements filed pursuant to §240.14n-1 and amendments thereto filed pursuant to §240.14n-2.",
        "title": "",
    },
    "F-10POS": {
        "description": "Post-effective amendment to a F-10EF registration",
        "title": "Post-effective amendment",
    },
    "MSDW": {"description": "", "title": ""},
    "NSAR-AT": {
        "description": "Transitional semi-annual report filed on Form N-SAR",
        "title": "",
    },
    "SC14D9F": {
        "description": "Solicitation/recommendation statement pursuant to Section 14(d)(4) of the Securities Exchange Act of 1934 and Rules 14d-1(b) and 14e-2(c) by foreign issuers",
        "title": "Recommendation statement",
    },
    "486BXT": {"description": "", "title": ""},
    "F-8": {
        "description": "Registration statement for securities of certain Canadian issuers to be issued in exchange offers or a business combination under the Securities Act of 1933",
        "title": "Registration statement",
    },
    "PREC14C": {
        "description": "Proxy Statement Pursuant to Section 14(a) of the Securities Exchange Act of 1934",
        "title": "Information statement (preliminary)",
    },
    "MSDCO": {"description": "", "title": ""},
    "TTW": {"description": "", "title": ""},
    "WDL-REQ": {"description": "", "title": ""},
    "G-405": {"description": "", "title": ""},
    "NTFNCSR": {"description": "", "title": ""},
    "SF-1": {
        "description": "General form of registration statement for all issuers of asset-backed securities",
        "title": "Registration statement",
    },
    "G-405N": {"description": "", "title": ""},
    "F-80POS": {
        "description": "Post-effective amendment to a F-80 registration",
        "title": "Post-effective amendment",
    },
    "F-3MEF": {
        "description": "A new registration statement filed under Rule 462(b) to add securities to a prior related effective registration statement filed on Form F-3",
        "title": "Registration statement",
    },
    "SP 15D2": {
        "description": "Special Financial Report filed under Rule 15d-2",
        "title": "Special financial report",
    },
    "11-KT": {"description": "", "title": "Transition report"},
    "40-17GCS": {
        "description": "Filings of claim or settlement pursuant to rule 17g-1(g)(1)(2) or (3) of the Investment Company Act of 1940.",
        "title": "",
    },
    "40FR12G": {
        "description": "Registration of a class of securities of certain Canadian issuers pursuant to Section 12(g) of the 1934 Act",
        "title": "Registration statement",
    },
    "F-3DPOS": {
        "description": "Post-Effective amendment to a F-3D registration",
        "title": "Post-effective amendment",
    },
    "F-4 POS": {
        "description": "Post-Effective amendment to an F-4EF registration",
        "title": "Post-effective amendment",
    },
    "NTFNSAR": {"description": "", "title": ""},
    "1-E": {
        "description": "Notification under Regulation E by small business investment companies and business development companies",
        "title": "",
    },
    "40-8F-2": {
        "description": "Initial application for deregistration pursuant to Investment Company Act Rule 0-2",
        "title": "",
    },
    "8-K15D5": {"description": "", "title": ""},
    "G-FINW": {"description": "", "title": ""},
    "NTFNCEN": {"description": "", "title": ""},
    "2-AF": {"description": "", "title": ""},
    "N-23C3C": {
        "description": "Notification of periodic repurchase offer under paragraph (b) of Rule 23c-3 and a discretionary repurchase offer under paragraph (c) of Rule 23c-3. [by registered closed-end investment companies or business development companies] pursuant to Rule 23c-3(b)",
        "title": "",
    },
    "NTN 20F": {"description": "", "title": ""},
    "SC13E4F": {
        "description": "Issuer tender offer statement filed pursuant to Rule 13(e)(4) by foreign issuers",
        "title": "Tender offer statement",
    },
    "F-8 POS": {
        "description": "Post-effective amendment to a F-8 registration",
        "title": "Post-effective amendment",
    },
    "NT NPORT-EX": {"description": "", "title": ""},
    "TH": {"description": "", "title": ""},
    "ADN-MTL": {"description": "", "title": ""},
    "CFPORTAL-W": {"description": "", "title": ""},
    "DEFC14C": {
        "description": "Information Statement Pursuant to Section 14(c) of the Securities Exchange Act of 1934",
        "title": "Information statement",
    },
    "SC 13E1": {
        "description": "Schedule 13-E1 statement of issuer required by Rule 13e-1",
        "title": "Purchase of securities",
    },
    "SDR": {
        "description": "Swap Data Repository (in Edgar now). It contains information necessary to consider registration as a swap data repository",
        "title": "",
    },
    "2-E": {
        "description": "Report of sales of securities by small business investment companies and business development companies pursuant to Rule 609 (Regulation E) Securities Act of 1933",
        "title": "",
    },
    "9-M": {"description": "", "title": ""},
    "S-BMEF": {
        "description": "A new registration statement filed under Rule 462(b) to add securities to a prior related effective registration statement filed on Form S-B",
        "title": "Registration statement",
    },
    "253G3": {"description": "", "title": "Disclosure"},
    "34-12H": {"description": "", "title": ""},
    "F-7 POS": {
        "description": "Post-effective amendment to a F-7 registration",
        "title": "Post-effective amendment",
    },
    "N-5": {
        "description": "Initial registration statement on Form N-5 for small business investment companies",
        "title": "",
    },
    "POS462C": {
        "description": "Post-effective amendment to a registration statement filed under Securities Act Rule 462(c)",
        "title": "Post-effective amendment",
    },
    "8F-2 NTC": {"description": "40-8F-2 Notice", "title": ""},
    "ATS-N-C": {"description": "", "title": ""},
    "C-AR-W": {"description": "", "title": "Withdrawal"},
    "C-U-W": {"description": "Broker-Dealer Withdrawal", "title": "Withdrawal"},
    "F-10EF": {
        "description": "Auto effective registration statement for securities of certain Canadian issuers under the Securities Act of 1933",
        "title": "Registration statement",
    },
    "F-4MEF": {
        "description": "A new registration statement filed under Rule 462(b) to add securities to a prior related effective registration statement filed on Form F-4",
        "title": "Registration statement",
    },
    "F-9 POS": {
        "description": "Post-effective amendment to a F-9EF registration",
        "title": "",
    },
    "NT 10-D": {"description": "", "title": "Late filing notice"},
    "NTN 10D": {"description": "", "title": ""},
    "S-20": {
        "description": "Registration statement for standardized options",
        "title": "Registration statement",
    },
    "SL": {"description": "", "title": ""},
    "UNDER": {"description": "Initial undertaking to file reports", "title": ""},
    "1-E AD": {"description": "", "title": "Sales materials"},
    "1-Z-W": {"description": "", "title": "Withdrawal"},
    "18-12B": {"description": "", "title": "Registration statement"},
    "8F-2 ORDR": {"description": "40-8F-2 Order", "title": ""},
    "ADV-H-C": {"description": "", "title": ""},
    "N-14MEF": {
        "description": "A new registration statement filed on Form N-14 by closed end investment companies filed under Securities Act Rule 462(b) of up to an additional 20% of securities for an offering that was registered on Form N-14",
        "title": "",
    },
    "SEC ACTION": {"description": "", "title": ""},
    "253G4": {"description": "", "title": "Disclosure"},
    "40-203A": {"description": "", "title": ""},
    "ATS-N": {"description": "", "title": ""},
    "ATS-N/UA": {"description": "", "title": ""},
    "C-TR-W": {
        "description": "Termination of Reporting Withdrawal",
        "title": "Withdrawal",
    },
    "N-1": {
        "description": "Initial registration statement filed on Form N-1 for open-end management investment companies",
        "title": "",
    },
    "S-4EF": {
        "description": "Auto effective registration statement for securities issued in connection with the formation of a bank or savings and loan holding company in compliance with General Instruction G",
        "title": "Registration statement",
    },
    "SBSE": {
        "description": "Application for Registration of Security-based Swap Dealers and Major Security-based Swap Participants",
        "title": "SBSE Registration",
    },
    "SBSE-A": {
        "description": "Application for Registration of Security-based Swap Dealers and Major Security-based Swap Participants that are Registered or Registering with the Commodity Futures Trading Commission as a Swap Dealer or Major Swap Participant",
        "title": "SBSE Registration for Commodity Futures Trading Commission registrants",
    },
    "SBSE-BD": {
        "description": "Application for Registration of Security-based Swap Dealers and Major Security-based Swap Participants that are Registered Broker-dealers",
        "title": "SBSE Registration for Broker-Dealers",
    },
    "SBSE-C": {
        "description": "Certifications for Registration of Security-based Swap Dealers and Major Security-based Participants",
        "title": "SBSE Registration Certification",
    },
    "SBSE-W": {
        "description": "Request for Withdrawal from Registration as a Security-based Swap Dealer or Major Security-based Swap Participant",
        "title": "SBSE Registration Withdrawal",
    },
    "N-2ASR": {"description": "", "title": ""},
    "N-2 POSASR": {"description": "", "title": ""},
    "497VPI": {
        "description": "Initial summary prospectus for variable contracts filed pursuant to Securities Act Rule 497(k)",
        "title": "",
    },
    "497VPU": {
        "description": "Updating summary prospectus for variable contracts filed pursuant to Securities Act Rule 497(k)",
        "title": "",
    },
    "N-VP": {
        "description": "",
        "title": "Notice documents for certain variable contracts",
    },
    "N-VPFS": {
        "description": "",
        "title": "Financial statements for certain variable contracts",
    },
}


class DateRange(str, enum.Enum):
    all = "all"
    ten_years = "10y"
    five_years = "5y"
    one_year = "1y"
    thirty_days = "30d"


class FilingCategory(str, enum.Enum):
    all_annual_quarterly_and_current_reports = (
        "all_annual_quarterly_and_current_reports"
    )
    all_section_16 = "all_section_16"
    beneficial_ownership_reports = "beneficial_ownership_reports"
    exempt_offerings = "exempt_offerings"
    registration_statements = "registration_statements"
    filing_review_correspondence = "filing_review_correspondence"
    sec_orders_and_notices = "sec_orders_and_notices"
    proxy_materials = "proxy_materials"
    tender_offers_and_going_private_tx = "tender_offers_and_going_private_tx"
    trust_indentures = "trust_indentures"


TEXT_SEARCH_CATEGORY_FORM_GROUPINGS = {
    #    "Exclude insider equity awards, transactions, and ownership (Section 16 Reports)": ["-3","-4","-5"], # todo: work out how to exclude these
    FilingCategory.all_annual_quarterly_and_current_reports: [
        "1-K",
        "1-SA",
        "1-U",
        "1-Z",
        "1-Z-W",
        "10-D",
        "10-K",
        "10-KT",
        "10-Q",
        "10-QT",
        "11-K",
        "11-KT",
        "13F-HR",
        "13F-NT",
        "15-12B",
        "15-12G",
        "15-15D",
        "15F-12B",
        "15F-12G",
        "15F-15D",
        "18-K",
        "20-F",
        "24F-2NT",
        "25",
        "25-NSE",
        "40-17F2",
        "40-17G",
        "40-F",
        "6-K",
        "8-K",
        "8-K12G3",
        "8-K15D5",
        "ABS-15G",
        "ABS-EE",
        "ANNLRPT",
        "DSTRBRPT",
        "IRANNOTICE",
        "N-30B-2",
        "N-30D",
        "N-CEN",
        "N-CSR",
        "N-CSRS",
        "N-MFP",
        "N-MFP1",
        "N-MFP2",
        "N-PX",
        "N-Q",
        "NPORT-EX",
        "NSAR-A",
        "NSAR-B",
        "NSAR-U",
        "NT 10-D",
        "NT 10-K",
        "NT 10-Q",
        "NT 11-K",
        "NT 20-F",
        "QRTLYRPT",
        "SD",
        "SP 15D2",
    ],
    FilingCategory.all_section_16: [
        "3",
        "4",
        "5",
    ],
    FilingCategory.beneficial_ownership_reports: ["SC 13D", "SC 13G", "SC14D1F"],
    FilingCategory.exempt_offerings: [
        "1-A",
        "1-A POS",
        "1-A-W",
        "253G1",
        "253G2",
        "253G3",
        "253G4",
        "C",
        "D",
        "DOS",
    ],
    FilingCategory.registration_statements: [
        "10-12B",
        "10-12G",
        "18-12B",
        "20FR12B",
        "20FR12G",
        "40-24B2",
        "40FR12B",
        "40FR12G",
        "424A",
        "424B1",
        "424B2",
        "424B3",
        "424B4",
        "424B5",
        "424B7",
        "424B8",
        "424H",
        "425",
        "485APOS",
        "485BPOS",
        "485BXT",
        "487",
        "497",
        "497J",
        "497K",
        "8-A12B",
        "8-A12G",
        "AW",
        "AW WD",
        "DEL AM",
        "DRS",
        "F-1",
        "F-10",
        "F-10EF",
        "F-10POS",
        "F-3",
        "F-3ASR",
        "F-3D",
        "F-3DPOS",
        "F-3MEF",
        "F-4",
        "F-4 POS",
        "F-4MEF",
        "F-6",
        "F-6 POS",
        "F-6EF",
        "F-7",
        "F-7 POS",
        "F-8",
        "F-8 POS",
        "F-80",
        "F-80POS",
        "F-9",
        "F-9 POS",
        "F-N",
        "F-X",
        "FWP",
        "N-2",
        "POS AM",
        "POS EX",
        "POS462B",
        "POS462C",
        "POSASR",
        "RW",
        "RW WD",
        "S-1",
        "S-11",
        "S-11MEF",
        "S-1MEF",
        "S-20",
        "S-3",
        "S-3ASR",
        "S-3D",
        "S-3DPOS",
        "S-3MEF",
        "S-4",
        "S-4 POS",
        "S-4EF",
        "S-4MEF",
        "S-6",
        "S-8",
        "S-8 POS",
        "S-B",
        "S-BMEF",
        "SF-1",
        "SF-3",
        "SUPPL",
        "UNDER",
    ],
    FilingCategory.filing_review_correspondence: [
        "CORRESP",
        "DOSLTR",
        "DRSLTR",
        "UPLOAD",
    ],
    FilingCategory.sec_orders_and_notices: [
        "40-APP",
        "CT ORDER",
        "EFFECT",
        "QUALIF",
        "REVOKED",
    ],
    FilingCategory.proxy_materials: [
        "ARS",
        "DEF 14A",
        "DEF 14C",
        "DEFA14A",
        "DEFA14C",
        "DEFC14A",
        "DEFC14C",
        "DEFM14A",
        "DEFM14C",
        "DEFN14A",
        "DEFR14A",
        "DEFR14C",
        "DFAN14A",
        "DFRN14A",
        "PRE 14A",
        "PRE 14C",
        "PREC14A",
        "PREC14C",
        "PREM14A",
        "PREM14C",
        "PREN14A",
        "PRER14A",
        "PRER14C",
        "PRRN14A",
        "PX14A6G",
        "PX14A6N",
        "SC 14N",
    ],
    FilingCategory.tender_offers_and_going_private_tx: [
        "CB",
        "SC 13E1",
        "SC 13E3",
        "SC 14D9",
        "SC 14F1",
        "SC TO-C",
        "SC TO-I",
        "SC TO-T",
        "SC13E4F",
        "SC14D9C",
        "SC14D9F",
    ],
    FilingCategory.trust_indentures: ["305B2", "T-3"],
}
# These are the verbose descriptions of the categories that are used in the CLI,
TEXT_SEARCH_FILING_VS_MAPPING_CATEGORIES_MAPPING = {
    "all_annual_quarterly_and_current_reports": "All annual, quarterly, and current reports",
    "all_section_16": "Insider equity awards, transactions, and ownership (Section 16 Reports)",
    "beneficial_ownership_reports": "Beneficial ownership reports",
    "exempt_offerings": "Exempt offerings",
    "registration_statements": "Registration statements and prospectuses",
    "filing_review_correspondence": "Filing review correspondence",
    "sec_orders_and_notices": "SEC orders and notices",
    "proxy_materials": "Proxy materials",
    "tender_offers_and_going_private_tx": "Tender offers and going private transactions",
    "trust_indentures": "Trust indenture filings",
}

FilingCategoryLiteral = Literal[
    "all",
    "custom",
    "all_except_section_16",
    "all_annual_quarterly_and_current_reports",
    "all_section_16",
    "beneficial_ownership_reports",
    "exempt_offerings",
    "registration_statements",
    "filing_review_correspondence",
    "sec_orders_and_notices",
    "proxy_materials",
    "tender_offers_and_going_private_tx",
    "trust_indentures",
]

DateRangeLiteral = Literal["all", "10y", "5y", "1y", "30d", "custom"]

LocationLiteral = Literal[
    "AL",  # Alabama
    "AK",  # Alaska
    "AZ",  # Arizona
    "AR",  # Arkansas
    "CA",  # California
    "CO",  # Colorado
    "CT",  # Connecticut
    "DE",  # Delaware
    "DC",  # District of Columbia
    "FL",  # Florida
    "GA",  # Georgia
    "HI",  # Hawaii
    "ID",  # Idaho
    "IL",  # Illinois
    "IN",  # Indiana
    "IA",  # Iowa
    "KS",  # Kansas
    "KY",  # Kentucky
    "LA",  # Louisiana
    "ME",  # Maine
    "MD",  # Maryland
    "MA",  # Massachusetts
    "MI",  # Michigan
    "MN",  # Minnesota
    "MS",  # Mississippi
    "MO",  # Missouri
    "MT",  # Montana
    "NE",  # Nebraska
    "NV",  # Nevada
    "NH",  # New Hampshire
    "NJ",  # New Jersey
    "NM",  # New Mexico
    "NY",  # New York
    "NC",  # North Carolina
    "ND",  # North Dakota
    "OH",  # Ohio
    "OK",  # Oklahoma
    "OR",  # Oregon
    "PA",  # Pennsylvania
    "RI",  # Rhode Island
    "SC",  # South Carolina
    "SD",  # South Dakota
    "TN",  # Tennessee
    "TX",  # Texas
    "UT",  # Utah
    "VT",  # Vermont
    "VA",  # Virginia
    "WA",  # Washington
    "WV",  # West Virginia
    "WI",  # Wisconsin
    "WY",  # Wyoming
    "AB",  # Alberta
    "BC",  # British Columbia
    "CAN",  # Canada
    "MB",  # Manitoba
    "NB",  # New Brunswick
    "NL",  # Newfoundland and Labrador
    "NS",  # Nova Scotia
    "ON",  # Ontario
    "PE",  # Prince Edward Island
    "QC",  # Quebec
    "SK",  # Saskatchewan
    "YT",  # Yukon
    "AFG",  # Afghanistan
    "ALA",  # Åland Islands
    "ALB",  # Albania
    "DZA",  # Algeria
    "ASM",  # American Samoa
    "AND",  # Andorra
    "AGO",  # Angola
    "AIA",  # Anguilla
    "ATA",  # Antarctica
    "ATG",  # Antigua and Barbuda
    "ARG",  # Argentina
    "ARM",  # Armenia
    "ABW",  # Aruba
    "AUS",  # Australia
    "AUT",  # Austria
    "AZE",  # Azerbaijan
    "BHS",  # Bahamas
    "BHR",  # Bahrain
    "BGD",  # Bangladesh
    "BRB",  # Barbados
    "BLR",  # Belarus
    "BEL",  # Belgium
    "BLZ",  # Belize
    "BEN",  # Benin
    "BMU",  # Bermuda
    "BTN",  # Bhutan
    "BOL",  # Bolivia
    "BIH",  # Bosnia and Herzegovina
    "BWA",  # Botswana
    "BVT",  # Bouvet Island
    "BRA",  # Brazil
    "IOT",  # British Indian Ocean Territory
    "BRN",  # Brunei Darussalam
    "BGR",  # Bulgaria
    "BFA",  # Burkina Faso
    "BDI",  # Burundi
    "KHM",  # Cambodia
    "CMR",  # Cameroon
    "CPV",  # Cape Verde
    "CYM",  # Cayman Islands
    "CAF",  # Central African Republic
    "TCD",  # Chad
    "CHL",  # Chile
    "CHN",  # China
    "CXR",  # Christmas Island
    "CCK",  # Cocos (Keeling) Islands
    "COL",  # Colombia
    "COM",  # Comoros
    "COG",  # Congo
    "COD",  # Congo, the Democratic Republic of the
    "COK",  # Cook Islands
    "CRI",  # Costa Rica
    "CIV",  # Côte d'Ivoire
    "HRV",  # Croatia
    "CUB",  # Cuba
    "CYP",  # Cyprus
    "CZE",  # Czech Republic
    "DNK",  # Denmark
    "DJI",  # Djibouti
    "DMA",  # Dominica
    "DOM",  # Dominican Republic
    "ECU",  # Ecuador
    "EGY",  # Egypt
    "SLV",  # El Salvador
    "GNQ",  # Equatorial Guinea
    "ERI",  # Eritrea
    "EST",  # Estonia
    "ETH",  # Ethiopia
    "FLK",  # Falkland Islands (Malvinas)
    "FRO",  # Faroe Islands
    "FJI",  # Fiji
    "FIN",  # Finland
    "FRA",  # France
    "GUF",  # French Guiana
    "PYF",  # French Polynesia
    "ATF",  # French Southern Territories
    "GAB",  # Gabon
    "GMB",  # Gambia
    "GEO",  # Georgia
    "DEU",  # Germany
    "GHA",  # Ghana
    "GIB",  # Gibraltar
    "GRC",  # Greece
    "GRL",  # Greenland
    "GRD",  # Grenada
    "GLP",  # Guadeloupe
    "GUM",  # Guam
    "GTM",  # Guatemala
    "GGY",  # Guernsey
    "GIN",  # Guinea
    "GNB",  # Guinea-Bissau
    "GUY",  # Guyana
    "HTI",  # Haiti
    "HMD",  # Heard Island and McDonald Islands
    "VAT",  # Holy See (Vatican City State)
    "HND",  # Honduras
    "HKG",  # Hong Kong
    "HUN",  # Hungary
    "ISL",  # Iceland
    "IND",  # India
    "IDN",  # Indonesia
    "IRN",  # Iran, Islamic Republic of
    "IRQ",  # Iraq
    "IRL",  # Ireland
    "IMN",  # Isle of Man
    "ISR",  # Israel
    "ITA",  # Italy
    "JAM",  # Jamaica
    "JPN",  # Japan
    "JEY",  # Jersey
    "JOR",  # Jordan
    "KAZ",  # Kazakhstan
    "KEN",  # Kenya
    "KIR",  # Kiribati
    "PRK",  # Korea, Democratic People's Republic of
    "KOR",  # Korea, Republic of
    "KWT",  # Kuwait
    "KGZ",  # Kyrgyzstan
    "LAO",  # Lao People's Democratic Republic
    "LVA",  # Latvia
    "LBN",  # Lebanon
    "LSO",  # Lesotho
    "LBR",  # Liberia
    "LBY",  # Libya
    "LIE",  # Liechtenstein
    "LTU",  # Lithuania
    "LUX",  # Luxembourg
    "MAC",  # Macao
    "MKD",  # Macedonia, the former Yugoslav Republic of
    "MDG",  # Madagascar
    "MWI",  # Malawi
    "MYS",  # Malaysia
    "MDV",  # Maldives
    "MLI",  # Mali
    "MLT",  # Malta
    "MHL",  # Marshall Islands
    "MTQ",  # Martinique
    "MRT",  # Mauritania
    "MUS",  # Mauritius
    "MYT",  # Mayotte
    "MEX",  # Mexico
    "FSM",  # Micronesia, Federated States of
    "MDA",  # Moldova, Republic of
    "MCO",  # Monaco
    "MNG",  # Mongolia
    "MNE",  # Montenegro
    "MSR",  # Montserrat
    "MAR",  # Morocco
    "MOZ",  # Mozambique
    "MMR",  # Myanmar
    "NAM",  # Namibia
    "NRU",  # Nauru
    "NPL",  # Nepal
    "NLD",  # Netherlands
    "ANT",  # Netherlands Antilles
    "NCL",  # New Caledonia
    "NZL",  # New Zealand
    "NIC",  # Nicaragua
    "NER",  # Niger
    "NGA",  # Nigeria
    "NIU",  # Niue
    "NFK",  # Norfolk Island
    "MNP",  # Northern Mariana Islands
    "NOR",  # Norway
    "OMN",  # Oman
    "PAK",  # Pakistan
    "PLW",  # Palau
    "PSE",  # Palestine, State of
    "PAN",  # Panama
    "PNG",  # Papua New Guinea
    "PRY",  # Paraguay
    "PER",  # Peru
    "PHL",  # Philippines
    "PCN",  # Pitcairn
    "POL",  # Poland
    "PRT",  # Portugal
    "PRI",  # Puerto Rico
    "QAT",  # Qatar
    "REU",  # Réunion
    "ROU",  # Romania
    "RUS",  # Russian Federation
    "RWA",  # Rwanda
    "BLM",  # Saint Barthélemy
    "SHN",  # Saint Helena, Ascension and Tristan da Cunha
    "KNA",  # Saint Kitts and Nevis
    "LCA",  # Saint Lucia
    "MAF",  # Saint Martin (French part)
    "SPM",  # Saint Pierre and Miquelon
    "VCT",  # Saint Vincent and the Grenadines
    "WSM",  # Samoa
    "SMR",  # San Marino
    "STP",  # Sao Tome and Principe
    "SAU",  # Saudi Arabia
    "SEN",  # Senegal
    "SRB",  # Serbia
    "SYC",  # Seychelles
    "SLE",  # Sierra Leone
    "SGP",  # Singapore
    "SVK",  # Slovakia
    "SVN",  # Slovenia
    "SLB",  # Solomon Islands
    "SOM",  # Somalia
    "ZAF",  # South Africa
    "SGS",  # South Georgia and the South Sandwich Islands
    "ESP",  # Spain
    "LKA",  # Sri Lanka
    "SDN",  # Sudan
    "SUR",  # Suriname
    "SJM",  # Svalbard and Jan Mayen
    "SWZ",  # Swaziland
    "SWE",  # Sweden
    "CHE",  # Switzerland
    "SYR",  # Syrian Arab Republic
    "TWN",  # Taiwan, Province of China
    "TJK",  # Tajikistan
    "THA",  # Thailand
    "TLS",  # Timor-Leste
    "TGO",  # Togo
    "TKL",  # Tokelau
    "TON",  # Tonga
    "TTO",  # Trinidad and Tobago
    "TUN",  # Tunisia
    "TUR",  # Turkey
    "TKM",  # Turkmenistan
    "TCA",  # Turks and Caicos Islands
    "TUV",  # Tuvalu
    "UGA",  # Uganda
    "UKR",  # Ukraine
    "ARE",  # United Arab Emirates
    "GBR",  # United Kingdom
    "UMI",  # United States Minor Outlying Islands
    "URY",  # Uruguay
    "UZB",  # Uzbekistan
    "VUT",  # Vanuatu
    "VEN",  # Venezuela, Bolivarian Republic of
    "VNM",  # Viet Nam
    "VGB",  # Virgin Islands, British
    "VIR",  # Virgin Islands, U.S.
    "WLF",  # Wallis and Futuna
    "ESH",  # Western Sahara
    "YEM",  # Yemen
    "ZMB",  # Zambia
    "ZWE",  # Zimbabwe
    "XX",  # Unknown
]

FilingLiteral = Literal[
    "1-A POS",  # Post-qualification amendment (Regulation A)
    "1-A-W",  # Withdrawal of Regulation A offering statement
    "1-A",  # Regulation A offering statement
    "1-E AD",  # Sales material filed under Regulation E
    "1-K",  # Annual report (Regulation A)
    "1-SA",  # Semiannual report (Regulation A)
    "1-U",  # Current report (Regulation A)
    "1-Z-W",  # Withdrawal of Regulation A exit report
    "1-Z",  # Exit report under Regulation A
    "1",  #
    "10-12B",  # Registration statement
    "10-12G",  # Registration statement
    "10-D",  # Distribution report
    "10-K",  # Annual report
    "10-KT",  # Transition report (10-K)
    "10-Q",  # Quarterly report
    "10-QT",  # Transition report (10-Q)
    "11-K",  # Annual report (employee stock purchase, savings and similar plans)
    "13F-HR",  # Institutional investment manager holdings report
    "13F-NT",  # Institutional investment manager notice
    "13FCONP",  #
    "144",  # Notice of proposed sale of securities
    "15-12B",  # Termination of registration
    "15-12G",  # Termination of registration
    "15-15D",  # Suspension notice
    "15F-12B",  # Termination of registration of a class of securities of a foreign private issuer
    "15F-12G",  # Termination of registration of a foreign private issuer
    "15F-15D",  # Suspension of duty to file reports by a foreign private issuer
    "18-12B",  # Initial registration of foreign governments or political subdivisions under 12(b)
    "18-K",  # Annual report for foreign governments and political subdivisions
    "19B-4E",  #
    "2-A",  # Small company offering registration form
    "20-F",  # Annual report (foreign private issuer)
    "20FR12B",  # Registration of a class of securities of a foreign private issuer
    "20FR12G",  #
    "24F-2NT",  # Annual notice of securities sold
    "25-NSE",  #
    "25",  # Notice of removal from listing and/or registration
    "253G1",  # Prospectus previously omitted in reliance on Rule 430A
    "253G2",  #
    "253G4",  # Prospectus previously omitted in reliance on Rule 430D
    "3",  # Initial insider holdings report
    "305B2",  # Application for designation of new trustee
    "4",  # Statement of changes in beneficial ownership of securities
    "40-17F1",  # Initial certificate of accounting of securities and similar investments (investment companies)
    "40-17F2",  # Initial certificate of accounting (investment companies)
    "40-17G",  # Fidelity bond for investment companies
    "40-202A",  # Application for exemption under the Investment Advisers Act
    "40-203A",  # Application for exemption under the Investment Advisers Act
    "40-206A",  # Application for exemption under the Investment Advisers Act
    "40-24B2",  # Filing of sales literature (investment companies)
    "40-33",  # Copies of all stockholder derivative actions (investment companies)
    "40-6B",  # Application under the Investment Company Act by an employees' securities company
    "40-8B25",  # Request for extension of time by an investment company
    "40-APP",  # Application for exemptive relief (investment companies)
    "40-F",  # Registration statement (certain Canadian issuers)
    "40-OIP",  # Application for exemptive relief (investment companies)
    "40FR12B",  # Registration of a class of securities of certain Canadian issuers
    "424A",  # Prospectus filed under Rule 424(a)
    "424B1",  # Prospectus
    "424B2",  # Prospectus
    "424B3",  # Prospectus
    "424B4",  # Prospectus
    "424B5",  # Prospectus
    "424B7",  # Prospectus
    "424B8",  # Prospectus
    "424H",  #
    "425",  # Prospectus/communication re business combination
    "485APOS",  # Prospectus materials
    "485BPOS",  # Prospectus materials
    "485BXT",  # Post-effective amendment to extend effective date
    "486APOS",  # Post-effective amendment filed pursuant to Rule 486(a)
    "486BPOS",  # Post-effective amendment filed pursuant to Rule 486(b)
    "486BXT",  # Post-effective amendment under Rule 486(b)(1)(iii) to extend effective date
    "487",  # Pre-effective pricing amendment
    "497",  # Definitive materials for investment companies
    "497AD",  # Filing of Rule 482 advertising
    "497H2",  # Filings under Rule 497(h)(2)
    "497J",  # Prospectus materials
    "497K",  # Summary prospectus for open-end management investment companies
    "497VPI",  # Initial summary prospectus for variable contracts under Rule 497(k)
    "497VPU",  # Updating summary prospectus for variable contracts under Rule 497(k)
    "5",  # Annual insider trading report
    "6-K",  # Current report (foreign issuer)
    "6B NTC",  # Notice of application by employees' securities company under Investment Company Act
    "6B ORDR",  # Order approving application by employees' securities company
    "8-A12B",  # Registration statement
    "8-A12G",  # Registration statement
    "8-K",  # Current report
    "8-K12B",  #
    "8-K12G3",  #
    "8-M",  # Modified current report
    "8F-2 NTC",  # Notice of termination of registration of certain investment companies
    "8F-2 ORDR",  # Order terminating registration of certain investment companies
    "ABS-15G",  # Asset-Backed Securitizer Report
    "ABS-EE",  # Form for electronic exhibits in asset-backed securities offerings
    "ADV-E",  #
    "ADV-H-C",  # Continuing hardship exemption request for Form ADV
    "ADV-H-T",  # Temporary hardship exemption request for Form ADV
    "ADV-NR",  #
    "ANNLRPT",  # Annual report by development banks
    "APP NTC",  # 40-APP Notice
    "APP ORDR",  # 40-APP Order
    "APP WD",  # Withdrawal of application for exemptive relief
    "APP WDG",  # Withdrawal of application for exemptive relief from Investment Company Act
    "ARS",  # Annual report to security holders
    "ATS-N-C",  # Cessation of operations report for NMS Stock ATS
    "ATS-N",  # Initial operation report, amendment, or cessation report for NMS Stock ATS
    "ATS-N/UA",  # Amendment to initial operation report for NMS Stock ATS
    "AW WD",  # Withdrawal of request to withdraw amendment to registration statement
    "AW",  # Withdrawal of amendment to a registration statement
    "C-AR-W",  # Withdrawal of Regulation A annual report
    "C-AR",  # Annual report (Regulation A)
    "C-TR-W",  # Withdrawal of Regulation C termination of reporting
    "C-TR",  # Termination of Regulation C offering
    "C-U-W",  # Withdrawal of Regulation A periodic report
    "C-U",  # Progress update (Regulation A)
    "C-W",  # Offering statement withdrawal
    "C",  # Offering statement
    "CB",  # Notification form for certain tender offers (foreign private issuer)
    "CERT",  #
    "CERTARCA",  #
    "CERTBATS",  #
    "CERTCBO",  #
    "CERTNAS",  #
    "CERTNYS",  #
    "CERTPAC",  #
    "CFPORTAL",  # Application for registration as funding portal
    "CORRESP",  # Correspondence
    "CT ORDER",  # Confidential order
    "D",  # Notice of sales of unregistered securities
    "DEF 14A",  # Proxy statement
    "DEF 14C",  # Information statement
    "DEFA14A",  # Proxy materials
    "DEFA14C",  # Additional definitive proxy soliciting materials
    "DEFC14A",  # Definitive proxy statement to contested solicitations
    "DEFM14A",  # Definitive proxy statement (merger or acquisition)
    "DEFM14C",  # Definitive information statement relating to merger or acquisition
    "DEFN14A",  # Definitive proxy statement - non-management
    "DEFR14A",  # Revised definitive proxy statement
    "DEFR14C",  # Revised definitive information statement
    "DEL AM",  # Delaying amendment
    "DFAN14A",  # Proxy soliciting materials (non-management)
    "DFRN14A",  # Revised definitive proxy statement (non-management)
    "DOS",  #
    "DOSLTR",  #
    "DRS",  # Draft registration statement
    "DRSLTR",  # Correspondence related to draft registration statement
    "DSTRBRPT",  # Distribution of primary obligations development bank report
    "EFFECT",  # SEC order
    "F-1",  # Registration statement for certain foreign private issuers
    "F-10",  # Registration statement (certain Canadian issuers)
    "F-10EF",  # Auto effective registration statement for certain Canadian issuers
    "F-10POS",  # Post-effective amendment to F-10 registration
    "F-1MEF",  # Registration statement under Rule 462(b)
    "F-3",  # Registration statement (certain foreign private issuers)
    "F-3ASR",  # Automatic shelf registration statement (foreign private issuers)
    "F-3D",  # Registration for dividend or interest reinvestment plan by foreign issuers
    "F-4",  # Registration statement (business combinations - foreign private issuers)
    "F-4MEF",  # Registration statement under Rule 462(b) related to Form F-4
    "F-6 POS",  # Post-effective amendment to F-6EF registration
    "F-6",  # Registration statement (American Depositary Receipts - foreign private issuer)
    "F-6EF",  # Registration statement (American Depositary Receipts)
    "F-7 POS",  # Post-effective amendment to F-7 registration
    "F-7",  # Registration of certain Canadian issuers for rights offerings
    "F-8",  # Registration of certain Canadian issuers for exchange offers or business combinations
    "F-80",  # Registration of certain Canadian issuers for exchange offers or business combinations
    "F-80POS",  # Post-effective amendment to F-80 registration
    "F-9 POS",  # Post-effective amendment to F-9 registration
    "F-9",  # Registration of certain investment grade debt or investment grade preferred securities of certain Canadian issuers
    "F-N",  # Appointment of agent for service by foreign institutions
    "F-X",  # Appointment of agent for service of process
    "FOCUSN",  #
    "FWP",  # Free writing prospectus
    "G-FIN",  #
    "IRANNOTICE",  # Notice of Iran-related disclosure
    "MA-A",  # Annual update of municipal advisor registration
    "MA-I",  # Municipal advisor registration
    "MA-W",  # Notice of withdrawal from registration as a municipal advisor
    "MA",  # Municipal advisor registration
    "MSD",  #
    "MSDW",  # Withdrawal of application for exemptive relief
    "N-1",  # Registration statement for open-end management investment companies
    "N-14 8C",  # Registration statement by closed-end investment company (business combinations)
    "N-14",  # Registration statement (open-end investment company - business combinations)
    "N-14MEF",  # Registration statement under Rule 462(b) related to Form N-14
    "N-18F1",  # Initial notification of election (open-end investment companies)
    "N-1A",  # Registration statement (open-end management investment companies)
    "N-2 POSASR",  # Post-effective amendment to automatic shelf registration on Form N-2
    "N-2",  # Registration statement (closed-end investment companies)
    "N-23C-2",  # Notice of intention to redeem securities (closed-end investment companies)
    "N-23C3A",  #
    "N-23C3B",  # Notification of discretionary repurchase offer by closed-end funds or BDCs
    "N-2ASR",  # Automatic shelf registration statement of WKSIs
    "N-2MEF",  # Registration statement under Rule 462(b) by closed-end investment companies
    "N-30B-2",  # Periodic and interim reports (investment companies)
    "N-30D",  # Annual and semi-annual reports (investment companies)
    "N-4",  # Registration statement (separate accounts - unit investment trusts)
    "N-5",  # Registration statement for SBICs
    "N-54A",  # Notification of election by business development companies
    "N-54C",  # Withdrawal of BDC election
    "N-6",  # Registration statement (separate accounts - unit investment trusts)
    "N-6F",  # Notice of intent by business development companies to elect to be regulated
    "N-8A",  # Initial notification of registration (investment companies)
    "N-8B-2",  # Initial registration statement for UITs on Form N-8B-2
    "N-8F NTC",  # N-8F Notice
    "N-8F ORDR",  # N-8F Order
    "N-8F",  # Application for deregistration (investment companies)
    "N-CEN",  # Annual report for investment companies
    "N-CR",  # Current report of money market fund material events
    "N-CSR",  # Annual shareholder report
    "N-CSRS",  # Semi-annual shareholder report
    "N-MFP",  # Monthly portfolio holdings schedule
    "N-MFP1",  # Monthly portfolio holdings schedule
    "N-MFP2",  # Monthly portfolio holdings schedule
    "N-PX",  # Annual proxy voting report
    "N-Q",  # Quarterly portolio holdings schedule
    "N-VP",  # Certification of no change in definitive materials under Rule 497(j)
    "N-VPFS",  # Designation of new effective date for post-effective amendment under Rule 486(a)
    "NO ACT",  #
    "NPORT-EX",  # Portfolio holdings exhibit
    "NPORT-NP",  #
    "NPORT-P",  #
    "NRSRO-CE",  # Annual certification for NRSROs
    "NRSRO-UPD",  # Form NRSRO – Update of Registration for Nationally Recognized Statistical Rating Organizations
    "NSAR-A",  # Semi-annual report for management companies
    "NSAR-AT",  # Transitional semi-annual report on Form N-SAR
    "NSAR-B",  # Annual report for management companies
    "NSAR-BT",  # Transitional annual report (Form N-SAR)
    "NSAR-U",  # Annual report for unit investment trusts
    "NT 10-D",  # Late filing notice for Form 10-D
    "NT 10-K",  # Late filing notice (10-K)
    "NT 10-Q",  # Late filing notice (10-Q)
    "NT 11-K",  # Late filing notice (11-K)
    "NT 20-F",  # Late filing notice (20-F)
    "NT N-CEN",  #
    "NT N-MFP",  # Late filing notice (Form N-MFP)
    "NT N-MFP1",  # Late filing notice for Form N-MFP1
    "NT N-MFP2",  #
    "NT NPORT-P",  #
    "NT-NCEN",  # Late filing notice for Form N-CEN
    "NT-NCSR",  # Late filing notice (Form N-CSR)
    "NT-NSAR",  # Late filing notice (Form N-SAR)
    "NTN 10D",  # Late filing notice for Form 10-D
    "NTN 10K",  #
    "NTN 10Q",  #
    "OIP NTC",  # 40-OIP Notice
    "OIP ORDR",  # 40-OIP Order
    "POS 8C",  # Post-effective amendment filed under the 1933 Act only or under both the 1933 and 1940 Acts
    "POS AM",  # Post-effective amendment
    "POS AMI",  # Post-effective amendment (1940 Act only)
    "POS EX",  # Post-effective amendment to add exhibits
    "POS462B",  # Post-effective amendment to Rule 462(b) registration statement
    "POS462C",  # Post-effective amendment to Rule 462(c) registration statement
    "POSASR",  # Post-effective amendment to automatic shelf registration
    "PRE 14A",  # Preliminary proxy statement
    "PRE 14C",  # Preliminary information statement
    "PREC14A",  # Preliminary proxy statement in contested solicitations
    "PREM14A",  # Preliminary proxy statement relating to merger or acquisition
    "PREM14C",  # Preliminary information statement relating to merger or acquisition
    "PREN14A",  # Preliminary proxy statement - non-management
    "PRER14A",  # Preliminary revised proxy statement
    "PRER14C",  # Preliminary information statement
    "PRRN14A",  # Revised preliminary proxy statement
    "PX14A6G",  #
    "PX14A6N",  # Notice of exempt solicitation
    "QRTLYRPT",  # Periodic development bank filing, submitted quarterly
    "QUALIF",  #
    "REG-NR",  # Non-resident registration
    "REVOKED",  #
    "RW WD",  # Withdrawal of a request for withdrawal of a registration statement
    "RW",  # Registration withdrawal request
    "S-1",  # Registration statement
    "S-11",  # Registration statement (real estate companies)
    "S-11MEF",  # Registration statement under Rule 462(b) related to Form S-11
    "S-1MEF",  # Registration statement under Rule 462(b)
    "S-20",  # Registration statement for standardized options
    "S-3",  # Registration statement (certain issuers)
    "S-3ASR",  # Automatic shelf registration statement
    "S-3D",  # Registration statement (dividend or interest reinvestment plan)
    "S-3DPOS",  # Post-effective amendment to S-3D registration statement
    "S-3MEF",  # Registration statement under Rule 462(b)
    "S-4 POS",  # Post-effective amendment to S-4EF registration statement
    "S-4",  # Registration statement - business combination
    "S-4EF",  # Auto effective registration statement related to bank/S&L holding company formation
    "S-4MEF",  # Registration statement under Rule 462(b) related to Form S-4
    "S-6",  # Registration statement for unit investment trusts
    "S-8 POS",  # Post-effective amendment to S-8 registration
    "S-8",  # Registration statement (employee benefit plans)
    "S-B",  # Registration statement (foreign governments and subdivisions)
    "SBSE-A",  # Application for registration of security-based swap dealers and participants (CFTC)
    "SBSE-BD",  # Application for registration of security-based swap dealers and participants (broker-dealers)
    "SBSE-C",  # Certifications for registration of security-based swap dealers and participants
    "SBSE-W",  # Withdrawal of registration as a security-based swap dealer or participant
    "SBSE",  # Application for registration of security-based swap dealers and participants
    "SC 13D",  # Beneficial ownership report (active investors)
    "SC 13E3",  # Going private transaction statement
    "SC 13G",  # Beneficial ownership report (passive investors)
    "SC 14D9",  # Recommendation statement (tender offers)
    "SC 14F1",  # Change in majority of directors
    "SC 14N",  # Information filed under §240.14n-1 and amendments under §240.14n-2
    "SC TO-C",  # Written communication relating to tender offer
    "SC TO-I",  # Issuer tender offer statement
    "SC TO-T",  # Third party tender offer statement
    "SC14D1F",  # Third party tender offer statement (foreign issuer)
    "SC14D9C",  # Written communication by the subject company relating to a third party tender offer
    "SC14D9F",  # Solicitation/recommendation statement by foreign issuers under 14(d)(4)
    "SD",  # Specialized disclosure report
    "SE",  #
    "SEC ACTION",  # Commission opinion, order, or consent to withdraw registration statement
    "SEC STAFF ACTION",  #
    "SEC STAFF LETTER",  # SEC staff correspondence
    "SF-3",  # Registration statement (asset-backed securities)
    "SL",  # Prospectus filed under Rule 424(b)(2) or (b)(3)
    "STOP ORDER",  # Stop order on a registration statement
    "SUPPL",  # Voluntary supplemental material (foreign issuers)
    "T-3",  # Application for qualification of trust indentures
    "TA-1",  # Application for registration as a transfer agent
    "TA-2",  # Annual report of transfer agent activities
    "TA-W",  # Notice of withdrawal from registration as transfer agent
    "TACO",  #
    "UNDER",  # Initial undertaking to file reports
    "UPLOAD",  # Correspondence
    "X-17A-5",  # Annual audit report by brokers or dealers
]
