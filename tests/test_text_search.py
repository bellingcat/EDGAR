import urllib.parse
from datetime import date
from edgar_tool.cli import EdgarTextSearcher

def decode_url(query_string):
    """
    Parses the query string anf extracts and sorts the 'forms' 
    parameter from a query string, then reconstructs the entire 
    query string with the sorted 'forms' parameter.

    This is necessary because raw forms can be order agnostic and
    URL strings cannot be compared directly due to encoding differences.

    Args:
        query_string (str): The query string to parse and modify.

    Returns:
        str: The query string with the 'forms' parameter sorted and the rest of the parameters unchanged.
    """
    parsed_query = urllib.parse.parse_qs(query_string)
    forms = parsed_query.get('forms', [''])[0]
    sorted_forms = ','.join(sorted(forms.split(',')))

    # Reconstruct the query string with the sorted 'forms' parameter
    parsed_query['forms'] = sorted_forms
    return urllib.parse.urlencode(parsed_query, doseq=True)

def test_generate_request_args():
    """
    Tests `EdgarTextSearcher._generate_request_args` to ensure it produces
    the correct query string, with 'forms' parameters being order-agnostic.
    """
    # ARRANGE & ACT
    result = EdgarTextSearcher._generate_request_args(
        keywords=['Tsunami', 'Hazards'],
        entity_id='0001030717',
        filing_form="All annual, quarterly, and current reports",
        single_forms=['8-K'],
        start_date=date(2019, 6, 1),
        end_date=date(2024, 1, 1),
        peo_in=None,
        inc_in="NY,OH"
    )

    expected = (
        'q=Tsunami+Hazards&dateRange=custom&startdt=2019-06-01&enddt=2024-01-01'
        '&locationCodes=NY,OH&locationType=incorporated&entityName=0001030717'
        '&forms=15-12B,1-K,40-F,24F-2NT,N-30B-2,NT+10-D,ABS-15G,20-F,1-Z,15-15D'
        ',6-K,13F-NT,N-MFP1,10-QT,QRTLYRPT,11-KT,15-12G,DSTRBRPT,NSAR-B,25-NSE'
        ',ABS-EE,N-30D,N-MFP2,ANNLRPT,N-PX,25,NPORT-EX,SP+15D2,NT+20-F,1-SA'
        ',NSAR-A,1-U,13F-HR,8-K12G3,N-CSR,SD,NT+11-K,N-Q,40-17F2,8-K15D5'
        ',NT+10-K,10-KT,NSAR-U,NT+10-Q,10-D,15F-15D,10-K,N-CSRS,10-Q,18-K'
        ',IRANNOTICE,1-Z-W,15F-12G,11-K,N-CEN,15F-12B,N-MFP,8-K,40-17G'
    )

    # ASSERT
    assert decode_url(result) == decode_url(expected)
