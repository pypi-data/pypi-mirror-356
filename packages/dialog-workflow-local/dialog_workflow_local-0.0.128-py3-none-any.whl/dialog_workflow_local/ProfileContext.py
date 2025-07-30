# from database_mysql_local.generic_crud import GenericCRUD
from logger_local.MetaLogger import MetaLogger
from variable_local.variables_local import VariablesLocal

from .Constants import DIALOG_WORKFLOW_CODE_LOGGER_OBJECT
from .utils import get_curr_state_id


class ProfileContext(metaclass=MetaLogger, object=DIALOG_WORKFLOW_CODE_LOGGER_OBJECT):
    # TODO We should consider to take ProfileContact to a separate package or merge it with UserContext
    def __init__(self, *, profile_id: int, curr_state_id: int = None) -> None:
        self.profile_id = profile_id
        self.chosen_poll_options = {}
        self.curr_state_id = curr_state_id or get_curr_state_id(profile_id)
        self.variables = VariablesLocal()
        self.groups = []

    def save_chosen_options(self, *, question_asked: str, variable_id: int,
                            chosen_numbers_list: list, list_of_options: list):
        """Saves the options chosen by the user in the multi_choice_poll action in a dict with the question as the key
            and a list of the options chosen as the value i.e: {<question asked> : [<chosen option 1>, <chosen option 2>, ...]}
            Also saves the chosen options in the database."""
        if not list_of_options:
            self.logger.error('list_of_options is empty', object={
                'question_asked': question_asked, 'variable_id': variable_id,
                'chosen_numbers_list': chosen_numbers_list, 'list_of_options': list_of_options})
            raise Exception('list_of_options is empty')
        self.chosen_poll_options[question_asked] = [
            list_of_options[chosen_option - 1] for chosen_option in chosen_numbers_list]
        variable_value_to_insert = question_asked + " "
        for chosen_option in self.chosen_poll_options[question_asked]:
            variable_value_to_insert = variable_value_to_insert + \
                str(chosen_option) + ", "
        self.variables.set_variable_value_by_variable_id(
            variable_id=variable_id, variable_value=variable_value_to_insert,
            profile_id=self.profile_id, state_id=self.curr_state_id)


class DialogWorkflowRecord:
    def __init__(self, record: dict) -> None:
        self.curr_state_id: int = record.get("state_id")
        self.parent_state_id: int = record.get("parent_state_id")
        self.workflow_action_id: int = record.get("workflow_action_id")
        self.lang_code = record.get("lang_code")
        self.parameter1 = record.get("parameter1")  # TODO: rename?
        self.variable1_id: int = record.get("variable1_id")
        self.result_logical = record.get("result_logical")
        self.result_figure_min: float = record.get("result_figure_min")
        self.result_figure_max: float = record.get("result_figure_max")
        self.next_state_id: int = record.get("next_state_id")
        self.no_feedback_milliseconds: float = record.get(
            "no_feedback_milliseconds")
        self.next_state_id_if_there_is_no_feedback: int = record.get(
            "next_state_id_if_there_is_no_feedback")
        self.message_template_id: int = record.get("message_template_id")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"
