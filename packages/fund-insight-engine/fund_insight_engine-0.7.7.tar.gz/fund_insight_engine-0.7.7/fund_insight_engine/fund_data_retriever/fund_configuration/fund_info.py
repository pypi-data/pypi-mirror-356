import pandas as pd
from mongodb_controller import COLLECTION_CONFIGURATION
from .pipeline import create_pipeline_for_fund_configuration

def fetch_data_fund_configuration(fund_code, date_ref=None):
    date_ref = date_ref if date_ref else sorted(COLLECTION_CONFIGURATION.distinct('date_ref'), reverse=True)[-1]
    pipeline = create_pipeline_for_fund_configuration(fund_code, date_ref)
    cursor = COLLECTION_CONFIGURATION.aggregate(pipeline=pipeline)
    data = list(cursor)[0]
    return data

def fetch_data_fund_info(fund_code, date_ref=None):
    configuration = fetch_data_fund_configuration(fund_code, date_ref)
    return configuration['data']['info']

def fetch_data_fund_fee(fund_code, date_ref=None):
    configuration = fetch_data_fund_configuration(fund_code, date_ref)
    return configuration['data']['fee']

def get_df_fund_info(fund_code, date_ref=None):
    data = fetch_data_fund_info(fund_code, date_ref)
    return (
        pd.DataFrame([data])
        .set_index('펀드코드')
        .T
    )

def get_df_fund_fee(fund_code, date_ref=None):
    data = fetch_data_fund_fee(fund_code, date_ref)
    return (
        pd.DataFrame(data)
        .set_index('판매사코드')
        .T    
    )