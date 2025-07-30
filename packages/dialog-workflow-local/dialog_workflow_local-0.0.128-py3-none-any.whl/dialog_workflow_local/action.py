# import msvcrt
# import requests
# from AgeDetection import DetectAge
from database_mysql_local.connector import Connector  # TODO: use crud
from language_remote.lang_code import LangCode
from logger_local.MetaLogger import MetaLogger
from message_local.CompoundMessage import CompoundMessage
from message_local.Recipient import Recipient
from user_context_remote.user_context import UserContext
from variable_local.template import ReplaceFieldsWithValues
from variable_local.variables_local import VariablesLocal

from .Constants import (COMMUNICATION_TYPE, DIALOG_WORKFLOW_CODE_LOGGER_OBJECT,
                        CommunicationTypeEnum, WorkflowActionEnum, seperator)
from .ProfileContext import DialogWorkflowRecord, ProfileContext
from .utils import (Group, generic_menu, get_child_nodes_of_current_state,
                    get_curr_state_id, process_message,
                    update_profile_curr_state_in_db)


class Action(metaclass=MetaLogger, object=DIALOG_WORKFLOW_CODE_LOGGER_OBJECT):
    def __init__(self, *, incoming_message: str, profile_id: int,
                 lang_code: LangCode, profile_curr_state_id: int,
                 variables: VariablesLocal = None) -> None:
        self.incoming_message = incoming_message
        self.profile_id = profile_id
        self.lang_code = lang_code
        self.variables = variables or VariablesLocal()
        self.profile_curr_state_id = profile_curr_state_id
        self.accumulated_message = ""
        self.profile_context = ProfileContext(
            profile_id=self.profile_id, curr_state_id=profile_curr_state_id)
        self.record: DialogWorkflowRecord or None = None  # type: ignore
        self.got_response = False
        self.user_context = UserContext()

    def act(self, dialog_workflow_record: DialogWorkflowRecord, got_response: bool) -> dict:
        """This function applies the action of the relevant record with the profile's current state id.
        Params:
            1. dialog_workflow_record: The current record from the dialog workflow state table that is applied.
            2. got_response a bool indicator telling us if the user had sent back a response to the last outgoing message
               that we sent him from the same action or not. This will help understand if the action should
               apply the begging part of the action (i.e. to send a request to the user),
               or the second part of the action (i.e. got a response and now deal with it)

        Returns:
            1. True if the action resulted in a change of state, False otherwise
            2. The outgoing message json object that the user will recieve if the action needed to send a message to the user,
                or None if the action doesn't need to send a message to the user .

        Note : some of the actions are divided into 2 parts:
            1. The action before sendig the outgoing message to the user (i.e. got_response = false)
            2. The action after sending the outgoing message, and getting an incoming_message reply back (i.e. got_respone = true). """

        self.record = dialog_workflow_record
        self.got_response = got_response
        action = WorkflowActionEnum(self.record.workflow_action_id)
        self.logger.info(
            f"Applying action {action.name} ({action.value}) for profile_id {self.profile_id} in state_id {self.profile_curr_state_id}")
        if action == WorkflowActionEnum.LABEL_ACTION:
            selected_act = {"is_state_changed": False}
        elif action == WorkflowActionEnum.TEXT_MESSAGE_ACTION:
            selected_act = self.text_message_action()
        elif action == WorkflowActionEnum.QUESTION_ACTION:
            selected_act = self.question_action()
        elif action == WorkflowActionEnum.JUMP_ACTION:
            selected_act = self.jump_action()
        elif action == WorkflowActionEnum.SEND_REST_API_ACTION:
            selected_act = self.send_rest_api_action()
        elif action == WorkflowActionEnum.ASSIGN_VARIABLE_ACTION:
            selected_act = self.assign_variable_action()
        elif action == WorkflowActionEnum.INCREMENT_VARIABLE_ACTION:
            selected_act = self.increment_variable_action()
        elif action == WorkflowActionEnum.DECREMENT_VARIABLE_ACTION:
            selected_act = self.decrement_variable_action()
        elif action == WorkflowActionEnum.MENU_ACTION:
            selected_act = self.menu_action()
        elif action == WorkflowActionEnum.AGE_DETECTION:
            selected_act = self.age_detection()
        elif action == WorkflowActionEnum.MULTI_CHOICE_POLL:
            selected_act = self.multi_choice_poll()
        elif action == WorkflowActionEnum.PRESENT_CHILD_GROUPS_NAMES_BY_ID:
            selected_act = self.present_child_groups_names_by_id()
        elif action == WorkflowActionEnum.PRESENT_GROUPS_WITH_CERTAIN_TEXT:
            selected_act = self.present_groups_with_certain_text()
        elif action == WorkflowActionEnum.INSERT_MISSING_DATA:
            selected_act = self.insert_missing_data()
        elif action == WorkflowActionEnum.PRESENT_AND_CHOOSE_SCRIPT:
            selected_act = self.present_and_choose_script()
        elif action == WorkflowActionEnum.PRESENT_FORM:
            selected_act = self.present_form_action()
        elif action == WorkflowActionEnum.DISPLAY_MESSAGE_TEMPLATE:
            selected_act = self.display_message_template_action()
        else:
            raise ValueError(f"Action {action} is not supported")

        # TODO Please add support to question_schema i.e. ASK_QUESTION_ID
        return selected_act

    def text_message_action(self) -> dict:
        """Prints the paramter1 message after formatting:
        "Hello {First Name}, how are you {feeling|doing}?" --> "Hello Tal, how are you doing? """
        message = self.record.parameter1
        if not message:
            raise ValueError(f"Parameter1 is empty for record {self.record}")
        replace_fields_with_values_class = ReplaceFieldsWithValues(
            message=message, lang_code=self.lang_code, variables=self.variables)
        formatted_message = replace_fields_with_values_class.get_formatted_message(
            profile_id=self.profile_id)
        self.accumulated_message = self.accumulated_message + formatted_message + seperator
        outgoing_message = process_message(
            communication_type=COMMUNICATION_TYPE, action_type=WorkflowActionEnum.TEXT_MESSAGE_ACTION,
            message=self.accumulated_message)
        text_message_act = {"is_state_changed": False,
                            "outgoing_message": outgoing_message}
        return text_message_act

    # TODO Rename all those functions to question_workflow_action() - Add the word 'workflow'
    # TODO Use question.question_table
    # TODO send to the logger the question_id
    # TODO confirm we didn't ask this question in the period mention in question.question_table
    def question_action(self) -> dict:
        """Asks a question and waits for an answer from user on STDIN. If the user responded in a certain amount of time,
        then moves to next state, otherwise moves to a different state.
        Note: this function waits for input for a certain amount of time only if using console application.
              If using websocket we send a json message to the user and exit the code normally"""

        if not self.got_response:
            self.accumulated_message += self.record.parameter1 or ""
            outgoing_message = process_message(
                communication_type=COMMUNICATION_TYPE, action_type=WorkflowActionEnum.TEXT_MESSAGE_ACTION,
                message=self.accumulated_message)
            if COMMUNICATION_TYPE == CommunicationTypeEnum.WEBSOCKET:
                question_act = {
                    "outgoing_message": outgoing_message, "is_state_changed": False}
                return question_act
            else:
                self.accumulated_message = ""

            # waiting_time = self.record.no_feedback_milliseconds
            # start_time = time.monotonic()
            # input_str = None
            # while True:
            # if msvcrt.kbhit():
            # input_str = input().strip()
            # insert_profile_variable_value(self.profile_id, self.record.variable1_id, input_str, self.profile_curr_state_id)
            # break
            # elif time.monotonic() - start_time > waiting_time:
            # break
            input_str = input("Please insert your answer: ").strip()
            if input_str is None:
                self.profile_curr_state_id = self.record.next_state_id_if_there_is_no_feedback
                got_response = True
            else:
                got_response = False
            question_act = {"is_state_changed": got_response}
            return question_act
        else:
            self.variables.set_variable_value_by_variable_id(
                self.record.variable1_id, self.incoming_message, self.profile_id, self.profile_curr_state_id)
            question_act = {"is_state_changed": False}
            return question_act

    def jump_action(self) -> dict:
        """Jumps from one state to another."""
        self.profile_curr_state_id = int(self.record.parameter1)
        # TODO: do we also have to send channel_id and campaign_id?
        update_profile_curr_state_in_db(
            new_state=self.profile_curr_state_id, profile_id=self.profile_id)
        jump_action = {"is_state_changed": True}
        return jump_action

    @staticmethod
    def send_rest_api_action() -> dict:
        """Sends a REST API post"""
        # TODO: implament this function

        # api_url = self.record.parameter1
        # payload_variable_id = self.record.variable1_id
        # json_payload_string = self.variables.get_variable_value_by_variable_id(
        #             payload_variable_id, self.language, self.profile_id)
        # json_payload = json.loads(json_payload_string)
        # incoming_message = requests.post(api_url, json=json_payload)
        # incoming_message_string = json.dumps(incoming_message.json())
        # insert_profile_variable_value(self.profile_id, self.variable.get_variable_id("Post Result"), incoming_message_string, self.profile_curr_state_id)  # noqa
        api_post = {"is_state_changed": False}

        return api_post

    def assign_variable_action(self) -> dict:
        """Assigns a value to a given variable"""

        parameter_value = self.record.parameter1
        variable_id = self.record.variable1_id
        self.variables.set_variable_value_by_variable_id(
            variable_id, parameter_value, self.profile_id, self.profile_curr_state_id)
        assinged_variable_action = {"is_state_changed": self.got_response}
        return assinged_variable_action

    def increment_variable_action(self) -> dict:
        """Increments a value to a given variable by the amount of the given paramter1"""

        number_to_add = int(self.record.parameter1)
        variable_id = self.record.variable1_id
        current_variable_value = self.variables.get_variable_value_by_variable_id(
            variable_id, self.lang_code, self.profile_id)
        self.variables.set_variable_value_by_variable_id(variable_id, str(
            int(current_variable_value) + number_to_add), self.profile_id, self.profile_curr_state_id)
        incremented_variable_action = {"is_state_changed": self.got_response}
        return incremented_variable_action

    def decrement_variable_action(self) -> dict:
        """Increments a value to a given variable by the amount of the given paramter1"""

        if isinstance(self.record.parameter1, str) and not self.record.parameter1.isdigit():
            raise ValueError(
                f"Parameter1 must be a number (got {self.record.parameter1})")
        number_to_add = int(self.record.parameter1)
        variable_id = self.record.variable1_id
        current_variable_value = self.variables.get_variable_value_by_variable_id(
            variable_id, self.lang_code, self.profile_id)
        self.variables.set_variable_value_by_variable_id(variable_id, str(int(current_variable_value) - number_to_add),
                                                         self.profile_id, get_curr_state_id(self.profile_id))
        decremented_variable_action = {"is_state_changed": False}
        return decremented_variable_action

    # I have put this in remark right now because this action need to work with multiple profiles,
    # But right now this change makes it difficult to do that. Will work on it later.

    # def condition_action(self):
    #     cursor.execute("""SELECT * FROM dialog_workflow_state  WHERE parent_state_id = %s""", [record.curr_state_id])
    #     child_nodes = cursor.fetchall()
    #     """I am assuming that in these child records the varaible id must be the same id of the parent variable id,
    #     and the parameter1 value is the value of a profile_id from which I shall get the age"""
    #     for child in child_nodes:
    #         profile_id = child["parameter1"]
    #         child_age = (profiles_dict_class.get(profile_id)).get_variable_value_by_id(record.variable1_id)
    #         if child_age < record.result_figure_max and child_age > record.result_figure_min:
    #             profile_context.curr_state_id = child["next_state_id"]
    #             return True, None
    #     return False, None

    def menu_action(self) -> dict:
        """This action show a menu of options to the user for which he should choose one from it.
            the options we show are the records such that their parent id is the id of the current record.
            First part of the action is sending the user the options.
            Second part of the action is getting the chosen option (i.e. incoming_message) and dealing with it."""

        fields_to_select = ["parameter1", "next_state_id"]
        table_name = "dialog_workflow_state_view"
        values_from_where_to_select = (self.record.curr_state_id,)
        variables_from_where_to_select = ["parent_state_id"]
        child_nodes = get_child_nodes_of_current_state(
            fields_to_select, table_name, values_from_where_to_select, variables_from_where_to_select)
        self.record.parameter1 = self.record.parameter1 or ""
        # Adds the question and instructions to the accumulated_message to be sent to user.
        if not self.got_response:
            self.accumulated_message = self.accumulated_message + self.record.parameter1 + \
                f"{seperator}Please choose EXACTLY ONE option between 1-{len(child_nodes)}:{seperator}"
        is_state_changed, next_state_id, outgoing_message = self.generic_user_choice_action(
            record=self.record, accumulated_message=self.accumulated_message, child_nodes=child_nodes,
            choosed_exactly_one_option=True, got_response=self.got_response, chosen_numbers=self.incoming_message,
            profile_context=self.profile_context)
        # returns the outgoing message to send to the user.
        if outgoing_message is not None:
            menu_action_selected = {
                "is_state_changed": False, "outgoing_message": outgoing_message}
            return menu_action_selected
        self.profile_curr_state_id = next_state_id
        self.accumulated_message = ""
        menu_action_selected = {"is_state_changed": is_state_changed}

        return menu_action_selected

    @staticmethod
    def age_detection() -> dict:
        # TODO: implament this function

        #     """Action that recieves a path to a picture (for now the picture has to be stored in the folder)
        #         and returns the approximate age of the person in the picture.
        #         Stores the picture in database storage."""
        #     if not self.got_response:
        #         self.accumulated_message += "Please insert a path to the picture" + seperator
        #         outgoing_message = process_message(communication_type= COMMUNICATION_TYPE, action_type= action_enum.AGE_DETECTION, message= self.accumulated_message) # noqa
        #         if COMMUNICATION_TYPE == communication_type_enum.WEBSOCKET:
        #             return False, outgoing_message
        #         else:
        #             self.accumulated_message = ""
        #             self.incoming_message = input()
        #     age_range = DetectAge.detect(self.incoming_message)
        #     self.accumulated_message += f'The approximate age of the picture you have sent is: {age_range}{seperator}'
        #     insert_profile_variable_value(self.profile_id, self.record.variable1_id, age_range, self.profile_curr_state_id)
        #     store_age_detection_picture(age_range, self.profile_curr_state_id)
        age_detected = {"is_state_changed": False}

        return age_detected

    def multi_choice_poll(self) -> dict:
        """ Similar to Menu Action. If the user chose a single option we jump to next_state_id of the chosen option.
            Otherwise, we save the answers and jump to the next_state_id of the parent."""

        fields_to_select = ["parameter1", "next_state_id"]
        table_name = "dialog_workflow_state_view"
        values_from_where_to_select = (self.record.curr_state_id,)
        variables_from_where_to_select = ["parent_state_id"]
        child_nodes = get_child_nodes_of_current_state(
            fields_to_select, table_name, values_from_where_to_select, variables_from_where_to_select)
        self.record.parameter1 = self.record.parameter1 or ""
        # Adds the question and instructions to the accumulated_message to be sent to user.
        if not self.got_response:
            self.accumulated_message = self.accumulated_message + self.record.parameter1 + seperator + \
                                       f"Please select your desired choices, You may select any of the numbers between 1-{len(child_nodes)} with a comma seperator between each choice:{seperator}"  # noqa
        is_state_changed, next_state_id, outgoing_message = self.generic_user_choice_action(
            record=self.record, accumulated_message=self.accumulated_message, child_nodes=child_nodes,
            choosed_exactly_one_option=False, got_response=self.got_response, chosen_numbers=self.incoming_message,
            profile_context=self.profile_context)
        # returns the outgoing message to send to the user.
        if outgoing_message is not None:
            choises = {"is_state_changed": False,
                       "outgoing_message": outgoing_message}
        else:
            self.profile_curr_state_id = next_state_id
            choises = {"is_state_changed": is_state_changed}

        return choises

    def present_child_groups_names_by_id(self) -> dict:
        """Presents all the groups that their parent id is the given one. Does so recursively"""

        child_groups = Group(int(self.record.parameter1))
        self.accumulated_message = "Here are the interests:" + seperator
        groups = child_groups.get_child_group_names()
        for i in range(len(groups)):
            self.accumulated_message += groups[i] + seperator + str(i) + "\n"
        child_groups_names_by_id = {
            "is_state_changed": True, "outgoing_message": self.accumulated_message}
        return child_groups_names_by_id

    def present_groups_with_certain_text(self) -> dict:
        """Present all groups that their text contains the given text. (e.g: given text: 'sport' -> 'sports', 'walking sport'...).
            Saves the chosen options in profile context."""

        groups = self.get_groups_with_text(self.record.parameter1)
        groups_with_certain_text = {"is_state_changed": False}
        if not self.got_response:
            self.accumulated_message += "Please choose your desired interests. You may select more than one choice with a comma seperator." + seperator  # noqa
            for i, child in enumerate(groups):
                self.accumulated_message = self.accumulated_message + \
                    f'{i + 1}) {child["title"]}{seperator}'

            outgoing_message = process_message(
                communication_type=COMMUNICATION_TYPE,
                action_type=WorkflowActionEnum.PRESENT_GROUPS_WITH_CERTAIN_TEXT,
                message=self.accumulated_message)
            if COMMUNICATION_TYPE == CommunicationTypeEnum.WEBSOCKET:
                groups_with_certain_text = {
                    "is_state_changed": False, "outgoing_message": outgoing_message}
            else:
                self.accumulated_message = ""
                # TODO: chosen_numbers = input()
        else:
            chosen_numbers = self.incoming_message.split(',')
            chosen_numbers_list = [int(x) for x in chosen_numbers]
            self.profile_context.groups.extend(
                [groups[chosen_number] for chosen_number in chosen_numbers_list])

        return groups_with_certain_text

    def insert_missing_data(self) -> dict:
        """Asks the user for missing data (e.g. please insert your first name), and after getting a response,
            inserts the given value to the relevant table to fill the missing data.
            The record, field name, table and scehma in which the data should be inserted into are given in parameter1 as:
            <schema>,<table>,<field name>,<record id> (e.g. user,user_table,first_name,1)"""

        parameter1_list = self.record.parameter1.split(",")
        schema = parameter1_list[0]
        table = parameter1_list[1]
        field_name = parameter1_list[2]
        record_id = parameter1_list[3]
        if not self.got_response:
            self.accumulated_message += f"Please insert your {field_name}{seperator}"
            outgoing_message = process_message(
                communication_type=COMMUNICATION_TYPE, action_type=WorkflowActionEnum.TEXT_MESSAGE_ACTION,
                message=self.accumulated_message)
            if COMMUNICATION_TYPE == CommunicationTypeEnum.WEBSOCKET:
                missing_data = {"is_state_changed": False,
                                "outgoing_message": outgoing_message}

                return missing_data
            else:
                self.accumulated_message = ""
                self.incoming_message = input(self.accumulated_message + " ")
        else:
            try:
                connection = Connector.connect(schema)
                cursor = connection.cursor(dictionary=True, buffered=True)
                # cursor.execute(f"""USE {schema}""")
                cursor.execute(
                    f"""UPDATE {table} SET {field_name} = '{self.incoming_message}' WHERE (id= {record_id})""")
                # cursor.execute("""USE dialog_workflow""")
                connection.commit()
            except Exception as exception:  # If one of the arguments isn't valid
                self.logger.error("Invalid parameter1", object=exception)
        missing_data = {"is_state_changed": False}

        return missing_data

    def present_and_choose_script(self) -> dict:
        """Action for asking the user which workflo script he would like to run next and change the next state id according to his choice."""

        connection = Connector.connect('dialog_workflow')
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(
            """SELECT d.start_state_id, dml.title FROM dialog_workflow_script_view AS d JOIN dialog_workflow_script_ml_view AS dml on dml.dialog_workflow_script_id=d.dialog_workflow_script_id WHERE dml.lang_code = %s OR dml.lang_code IS NULL""",  # noqa
            (self.lang_code.value,))
        available_scripts_dict = cursor.fetchall()
        # TODO: prefer not null lang_code if exist
        available_scripts = [script["title"]
                             for script in available_scripts_dict]
        outgoing_message = "Please choose your desired script out of the following:" + seperator
        menu = generic_menu(options=available_scripts, got_response=self.got_response,
                            chosen_numbers=self.incoming_message,
                            choose_one_option=True, outgoing_message=outgoing_message)
        if COMMUNICATION_TYPE == CommunicationTypeEnum.WEBSOCKET and not self.got_response:
            present_and_choosed_script = {
                "is_state_changed": False, "outgoing_message": menu}
        else:
            self.profile_curr_state_id = available_scripts_dict[menu[0] -
                                                                1]["start_state_id"]
            present_and_choosed_script = {"is_state_changed": True}

        return present_and_choosed_script

    def present_form_action(self) -> dict:
        form_id = self.record.parameter1
        if not isinstance(form_id, int):
            if isinstance(form_id, str) and form_id.isdigit():
                form_id = int(form_id)
            else:
                raise ValueError(
                    f"parameter1 must be an integer (got {form_id})")
        save_additional_parameters = {"from_subsystem_id": 2,  # TODO do not use hard coded
                                      "channel_id": 14,
                                      "last_dialog_workflow_state_id": self.record.curr_state_id, }
        outgoing_messae_dict = CompoundMessage(
            form_id=form_id, save_additional_parameters=save_additional_parameters).get_compound_message_dict()
        form_actions = {"is_state_changed": False,
                        "outgoing_message": outgoing_messae_dict}
        return form_actions

    def generic_user_choice_action(self, *, record: DialogWorkflowRecord, accumulated_message: str, child_nodes: list,
                                   choosed_exactly_one_option: bool, got_response: bool, chosen_numbers: str,
                                   # type: ignore # TODO: return dict
                                   profile_context: ProfileContext) -> tuple[bool, int, str]:
        """Sends the user a question with a couple of answers. This function is generic and can let the user choose either
            exactly one option, or more than one. Each case is handeled differently.
            Returns:
                1. True if the users' next state should be changed to a child next state, False if there's no need to change it's state
                2. The next state id that the profile_context should be in, or None if the action didn't result in a change of state.
                3. The outging message to be sent to the user, or None if the message had already been sent."""
        # This is the first part of the action: sending the request to the user and waiting for an answer.
        is_state_changed = False
        if not got_response:
            for i, child in enumerate(child_nodes):
                accumulated_message = accumulated_message + \
                    f'{i + 1}) {child["parameter1"]}{seperator}'
            outgoing_message = process_message(communication_type=COMMUNICATION_TYPE,
                                               action_type=WorkflowActionEnum.TEXT_MESSAGE_ACTION,
                                               message=accumulated_message)
            if COMMUNICATION_TYPE == CommunicationTypeEnum.WEBSOCKET:
                next_state_id = record.next_state_id
                return is_state_changed, next_state_id, outgoing_message
            elif not chosen_numbers:
                chosen_numbers = input("Please choose your desired option:")

        # The user has to pick exactly one option
        if choosed_exactly_one_option and chosen_numbers.isdigit():
            if int(chosen_numbers) > len(child_nodes) or int(chosen_numbers) < 1:
                raise ValueError(
                    f"Invalid input: {chosen_numbers}, (expected an integer between 1 and {len(child_nodes)})")
            profile_next_state = (
                child_nodes[int(chosen_numbers) - 1])["next_state_id"]
            is_state_changed = True
            next_state_id = profile_next_state
        # In this case the user can choose more than one option:
        else:
            chosen_numbers = chosen_numbers.split(',')
            try:
                chosen_numbers_list = [int(x)
                                       for x in chosen_numbers if x.isdigit()]
                if not all(x.isdigit() for x in chosen_numbers):
                    self.logger.warning(
                        f"Ignored non-integers from: `{chosen_numbers}`, (expected a comma separated list of integers)")
            except ValueError:
                raise ValueError(
                    f"Invalid input: {chosen_numbers}, (expected an integer or a comma separated list of integers)")

            # If he chooses more than one, we store the chosen options and jump to the next_state_id of the parent.
            list_of_options = [option["parameter1"] for option in child_nodes]
            profile_context.save_chosen_options(
                question_asked=record.parameter1, variable_id=record.variable1_id,
                chosen_numbers_list=chosen_numbers_list, list_of_options=list_of_options)
            next_state_id = record.next_state_id

        outgoing_message = None
        return is_state_changed, next_state_id, outgoing_message

    def display_message_template_action(self) -> dict:
        # call compound message
        if not self.record.message_template_id:
            raise ValueError(
                f"message_template_id is empty for record {self.record}")
        recipient = Recipient(profile_id=self.profile_id, preferred_lang_code_str=self.lang_code.value,
                              user_id=self.user_context.get_effective_user_id(),
                              first_name=self.user_context.get_real_name())

        outgoing_message = CompoundMessage(message_template_id=self.record.message_template_id,
                                           recipients=[recipient]).get_compound_message_dict()
        display_message_template = {
            "is_state_changed": False, "outgoing_message": outgoing_message}
        return display_message_template

    @staticmethod  # TODO move to another repository
    def get_groups_with_text(text: str) -> list:
        connection = Connector.connect('group')
        cursor = connection.cursor(dictionary=True, buffered=True)
        # cursor.execute("""USE `group`""")
        cursor.execute(
            f"""SELECT title, group_id FROM group_ml_table WHERE title LIKE '%{text}%'""")
        groups_with_text = cursor.fetchall()

        return groups_with_text
