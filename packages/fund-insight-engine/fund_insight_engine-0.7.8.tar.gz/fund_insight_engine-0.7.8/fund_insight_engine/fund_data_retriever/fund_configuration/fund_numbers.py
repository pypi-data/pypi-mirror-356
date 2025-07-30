from mongodb_controller import COLLECTION_8186
from .pipeline import create_pipeline_for_fund_numbers

def fetch_data_fund_numbers(fund_code, date_ref=None):
    date_ref = date_ref if date_ref else sorted(COLLECTION_8186.distinct('일자'), reverse=True)[-1]
    pipeline = create_pipeline_for_fund_numbers(fund_code, date_ref)
    cursor = COLLECTION_8186.aggregate(pipeline=pipeline)
    data = list(cursor)[0]
    return data
