SUPPORTED_OUTPUT_EXTENSIONS = [".csv", ".jsonl", ".json"]
TEXT_SEARCH_BASE_URL = "https://www.sec.gov/edgar/search/#/"
TEXT_SEARCH_FILING_CATEGORIES_MAPPING = {
    "all_except_section_16": "form-cat0",
    "all_annual_quarterly_and_current_reports": "form-cat1",
    "all_section_16": "form-cat2",
    "beneficial_ownership_reports": "form-cat3",
    "exempt_offerings": "form-cat4",
    "registration_statements": "form-cat5",
    "filing_review_correspondence": "form-cat6",
    "sec_orders_and_notices": "form-cat7",
    "proxy_materials": "form-cat8",
    "tender_offers_and_going_private_tx": "form-cat9",
    "trust_indentures": "form-cat10",
}
TEXT_SEARCH_RESULTS_TABLE_XPATH = "/html/body/div[3]/div[2]/div[2]/table/tbody"
TEXT_SEARCH_SPLIT_BATCHES_NUMBER = 2
TEXT_SEARCH_CSV_FIELDS_NAMES = [
    "filing_type",
    "filed_at",
    "reporting_for",
    "entity_name",
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
