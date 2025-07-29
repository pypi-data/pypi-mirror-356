from pyairtable  import Table
from typing      import (
    Dict, 
    Tuple,
    Optional,
)
from ..Types     import (
    State, 
    StateType, 
    StateBehavior, 
    Transition, 
    TransitionType, 
    Form, 
    FormType, 
    Doc, 
    ID_TYPE
)
from ..Graph     import (
    Graph,
)
from ..Exceptions import (
    UnknownFormType, 
    TableIsEmpty,
)
from .Models     import (
    StateFieldsConsts, 
    StateBehaviorConsts, 
    TransitionFieldConsts, 
    TransitionTypesConsts, 
    FormFieldConsts, 
    DocFieldConsts
)
from .Errors    import (
    Errors,
)


class Loader():
    def __init__(self):
        self.states_records         = list()
        self.transitions_records    = list()
        self.forms_records          = list()
        self.config_records         = list()
        self.states_external        = list()

        self.forms : Dict[ID_TYPE, Form] = dict()
        self.docs  : Dict[ID_TYPE, Doc]  = dict()
        self.errors: List[Tuple[str, Optional]] = list()

        self.graph                  = Graph()

    def load(self,
             AIRTABLE_API_KEY, 
             AIRTABLE_BASE_ID,
             AIRTABLE_STATES_TABLE_ID,
             AIRTABLE_STATES_TABLE_MAIN_VIEW_ID,
             AIRTABLE_TRANSITIONS_TABLE_ID,
             AIRTABLE_TRANSITION_TABLE_MAIN_VIEW_ID,
             AIRTABLE_FORMS_TABLE_ID,
             AIRTABLE_FORMS_TABLE_MAIN_VIEW_ID,
             AIRTABLE_CONFIG_TABLE_ID,
             AIRTABLE_CONFIG_TABLE_MAIN_VIEW_ID
        ):
        self.load_tables(
            AIRTABLE_API_KEY, 
            AIRTABLE_BASE_ID,
            AIRTABLE_STATES_TABLE_ID,
            AIRTABLE_STATES_TABLE_MAIN_VIEW_ID,
            AIRTABLE_TRANSITIONS_TABLE_ID,
            AIRTABLE_TRANSITION_TABLE_MAIN_VIEW_ID,
            AIRTABLE_FORMS_TABLE_ID,
            AIRTABLE_FORMS_TABLE_MAIN_VIEW_ID,
            AIRTABLE_CONFIG_TABLE_ID,
            AIRTABLE_CONFIG_TABLE_MAIN_VIEW_ID
        ) 

        s = self.process_states_records()
        t = self.process_transitions_records()
        f = self.process_forms_records()
        c = self.process_config_records()

        self.connect_states_with_forms(s, f)

        for ext in self.states_external:
            ext_data = ext['external_table_data']
            loader = Loader()
            loader.load(AIRTABLE_API_KEY, *ext_data.splitlines())

            self.graph.AttachAnotherGraph(loader.graph, ext)
            self.forms.update(loader.forms)
            self.docs.update(loader.docs)
            self.errors.extend(loader.errors)

        self.errors.extend(self.graph.errors)
        
    
    def load_tables(
            self,
            AIRTABLE_API_KEY, 
            AIRTABLE_BASE_ID,
            AIRTABLE_STATES_TABLE_ID,
            AIRTABLE_STATES_TABLE_MAIN_VIEW_ID,
            AIRTABLE_TRANSITIONS_TABLE_ID,
            AIRTABLE_TRANSITION_TABLE_MAIN_VIEW_ID,
            AIRTABLE_FORMS_TABLE_ID,
            AIRTABLE_FORMS_TABLE_MAIN_VIEW_ID,
            AIRTABLE_CONFIG_TABLE_ID,
            AIRTABLE_CONFIG_TABLE_MAIN_VIEW_ID):
        states_table        = Table(AIRTABLE_API_KEY, 
                                    AIRTABLE_BASE_ID,
                                    AIRTABLE_STATES_TABLE_ID)
        self.states_records = states_table.all( 
            view=AIRTABLE_STATES_TABLE_MAIN_VIEW_ID)
        if len(self.states_records) == 0:
            self.errors.append((Errors.STATES_TABLE_EMPTY, ))
            #raise TableIsEmpty('States')

        transitions_table   = Table(AIRTABLE_API_KEY, 
                                    AIRTABLE_BASE_ID,
                                    AIRTABLE_TRANSITIONS_TABLE_ID)
        self.transitions_records = transitions_table.all( 
            view=AIRTABLE_TRANSITION_TABLE_MAIN_VIEW_ID)
        if len(self.transitions_records) == 0:
            self.errors.append((Errors.TRANSITIONS_TABLE_EMPTY, ))
            #raise TableIsEmpty('Transitions')

        forms_table         = Table(AIRTABLE_API_KEY, 
                                    AIRTABLE_BASE_ID,
                                    AIRTABLE_FORMS_TABLE_ID,
                                )
        self.forms_records  = forms_table.all(
            view=AIRTABLE_FORMS_TABLE_MAIN_VIEW_ID)
        if len(self.forms_records) == 0:
            self.errors.append((Errors.FORMS_TABLE_EMPTY, ))
            #raise TableIsEmpty('Forms')
    
        config_table        = Table(AIRTABLE_API_KEY, 
                                    AIRTABLE_BASE_ID,
                                    AIRTABLE_CONFIG_TABLE_ID,
                                )
        self.config_records = config_table.all(
            view=AIRTABLE_CONFIG_TABLE_MAIN_VIEW_ID)
        if len(self.config_records) == 0:
            self.errors.append((Errors.CONFIG_TABLE_EMPTY, ))
            #raise TableIsEmpty('Config')

    def process_states_records(self):
        for record in self.states_records:
            fields = record['fields']
            state : State = {
                'id'        : record['id'],
                'name'      : fields.get(
                        StateFieldsConsts.NAME, 'NO NAME'),
                'type'      : StateType.UNKNOWN,
                'behavior'  : StateBehavior.UNKNOWN,
                'is_start'  : False,
                'is_end'    : False,
                'forms_ids' : list(), 
                'in_transitions_ids' : [
                    a_id for a_id in fields.get( 
                        StateFieldsConsts.IN_TRANSITIONS, list() )],
                'out_transitions_ids' : [
                    a_id for a_id in fields.get( 
                        StateFieldsConsts.OUT_TRANSITIONS, list() )],
                'external_table_data'   : fields.get( 
                        StateFieldsConsts.EXTERANL_TABLE_DATA, '' ),
            }

            if   len(state['in_transitions_ids'])  == 0 and\
                 len(state['out_transitions_ids']) == 0:
                state['type'] = StateType.ALWAYS_OPEN
            elif len(state['in_transitions_ids'])  == 0:
                state['type'] = StateType.START
            elif len(state['out_transitions_ids']) == 0:
                state['type'] = StateType.END
            else:
                state['type'] = StateType.REGULAR
           
            cond = fields.get(
                StateFieldsConsts.BEHAVIOR)
            match cond:
                case StateBehaviorConsts.FORM:
                    state['behavior']=StateBehavior.FORM
                case StateBehaviorConsts.INPUT_CHECK:
                    state['behavior']=StateBehavior.INPUT_CHECK
                case StateBehaviorConsts.EXTERNAL:
                    state['behavior']=StateBehavior.EXTERNAL
                    self.states_external.append(state)
                case _:
                    self.errors.append( (Errors.STATE_NO_BEHAVIOR, state['name']) )
                    #raise RuntimeError(f"State {state['name']} does not have a behavior set")
           
            self.graph.AddState(state)
        return self.graph.states


    def process_transitions_records(self):
        transitions : Dict[ID_TYPE, Transition] = dict()
        for record in self.transitions_records:
            fields = record['fields']

            transition : Transition = {
                    'id' : record['id'],
                    'name' : fields.get(
                        TransitionFieldConsts.NAME, 'NO NAME'),
                    'type': TransitionType.UNKNOWN,
                    'source_id' : fields.get(
                        TransitionFieldConsts.SOURCE, [None,])[0],
                    'target_id' : fields.get(
                        TransitionFieldConsts.TARGET, [None,])[0],
                    'form_elem_ids' : fields.get(
                        TransitionFieldConsts.FORM_CONDITIONS, list()),
            }

            cond = fields.get(
                TransitionFieldConsts.TRANSITION_CONDITION)
            match cond:
                case TransitionTypesConsts.CONDITIONAL:
                    transition['type']=TransitionType.CONDITIONAL
                case TransitionTypesConsts.UNCONDITIONAL:
                    transition['type']=TransitionType.UNCONDITIONAL
                case TransitionTypesConsts.STRICT:
                    transition['type']=TransitionType.STRICT
                case _:
                    self.errors.append( (Errors.TRANSITION_NO_BEHAVIOR, transition['name']) )
                    #raise RuntimeError(f"Transition {transition['name']} does not have a condition set")

            self.graph.AddTransition(transition)
        return self.graph.transitions


    def process_forms_records(self):
        for record in self.forms_records:
            fields = record['fields']
            form : Form = {
                'id'        : record['id'],
                'name'      : fields.get(
                    FormFieldConsts.NAME, "NO NAME"),
                'type'      : FormType.UNKNOWN,
                'text'      : fields.get(
                    FormFieldConsts.TEXT, "NO TEXT"),
                'state_id'  : fields.get(
                    FormFieldConsts.STATE_ID, None),
                'tags'      : fields.get(
                    FormFieldConsts.TAGS, ''),
            }

            t = record['fields'].get(FormFieldConsts.TYPE, None)
            for ft in FormType:
                if ft.value == t:
                    form['type'] = ft
                    break
            if form['type'] == FormType.UNKNOWN:
                    self.errors.append( (Errors.FORM_TYPE_UNKNOWN, form['name']) )

            if form['state_id']:
                form['state_id'] = form['state_id'][0]

            self.forms[form['id']] = form
        return self.forms


    def process_config_records(self):
        for record in self.config_records:
            fields = record['fields']
            doc : Doc = {
                'id'        : record['id'],
                'name'      : fields[DocFieldConsts.NAME],
                'tag'       : fields[DocFieldConsts.TAG],
            }
            
            self.docs[doc['id']] = doc
        return self.docs


    def connect_states_with_forms(self, states: Dict, forms: Dict):
        for form in forms.values():
            state = states.get(form['state_id'], None)
            if state:
                state['forms_ids'].append(form['id'])

