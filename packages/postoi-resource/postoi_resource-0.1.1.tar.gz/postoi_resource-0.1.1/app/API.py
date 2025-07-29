from .Loader    import Loader
from .Config    import Config

class API():
    def init(self):
        pass

    def Load(self):
        config = Config()
        loader = Loader()
        loader.load(
            config.AIRTABLE_API_KEY, 
            config.AIRTABLE_BASE_ID,
            config.AIRTABLE_STATES_TABLE_ID,
            config.AIRTABLE_STATES_TABLE_MAIN_VIEW_ID,
            config.AIRTABLE_TRANSITIONS_TABLE_ID,
            config.AIRTABLE_TRANSITION_TABLE_MAIN_VIEW_ID,
            config.AIRTABLE_FORMS_TABLE_ID,
            config.AIRTABLE_FORMS_TABLE_MAIN_VIEW_ID,
            config.AIRTABLE_CONFIG_TABLE_ID,
            config.AIRTABLE_CONFIG_TABLE_MAIN_VIEW_ID
        )

        return {
            'graph'         : loader.graph,
            'forms'         : loader.forms,
            'docs'          : loader.docs,
            'errors'        : loader.errors,
        }

