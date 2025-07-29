import os
from dotenv import load_dotenv


class Config():
    def __init__(self):
        load_dotenv()

        self.AIRTABLE_API_KEY                       =\
            os.getenv('AIRTABLE_API_KEY')
        self.AIRTABLE_BASE_ID                       =\
            os.getenv('AIRTABLE_BASE_ID')
        self.AIRTABLE_STATES_TABLE_ID               =\
            os.getenv('AIRTABLE_STATES_TABLE_ID')
        self.AIRTABLE_STATES_TABLE_MAIN_VIEW_ID     =\
            os.getenv('AIRTABLE_STATES_TABLE_MAIN_VIEW_ID')
        self.AIRTABLE_TRANSITIONS_TABLE_ID          =\
            os.getenv('AIRTABLE_TRANSITIONS_TABLE_ID')
        self.AIRTABLE_TRANSITION_TABLE_MAIN_VIEW_ID =\
            os.getenv('AIRTABLE_TRANSITION_TABLE_MAIN_VIEW_ID')
        self.AIRTABLE_FORMS_TABLE_ID                =\
            os.getenv('AIRTABLE_FORMS_TABLE_ID')
        self.AIRTABLE_FORMS_TABLE_MAIN_VIEW_ID      =\
            os.getenv('AIRTABLE_FORMS_TABLE_MAIN_VIEW_ID')
        self.AIRTABLE_CONFIG_TABLE_ID               =\
            os.getenv('AIRTABLE_CONFIG_TABLE_ID')
        self.AIRTABLE_CONFIG_TABLE_MAIN_VIEW_ID     =\
            os.getenv('AIRTABLE_CONFIG_TABLE_MAIN_VIEW_ID')

config = Config()

def get() -> Config:
    return config

