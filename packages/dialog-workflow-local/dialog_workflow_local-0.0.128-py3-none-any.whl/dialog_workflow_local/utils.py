import json

from database_mysql_local.connector import Connector
from database_mysql_local.generic_crud import GenericCRUD
from logger_local.LoggerLocal import Logger
from logger_local.MetaLogger import module_wrapper

from .Constants import (COMMUNICATION_TYPE, DIALOG_WORKFLOW_CODE_LOGGER_OBJECT,
                        CommunicationTypeEnum, WorkflowActionEnum, seperator)

logger = Logger.create_logger(object=DIALOG_WORKFLOW_CODE_LOGGER_OBJECT)

# from circles_local_aws_s3_storage_python.AWSStorage import AwsS3Storage

# TODO:Let's move to Object Oriented Programming
DEFAULT_STATE_ID = 1


def process_message(communication_type: CommunicationTypeEnum, action_type: WorkflowActionEnum,
                    message: str) -> str | dict:
    """Processes message according to which communication_type is used: console or websocket
        If console then we continue the code normally.
        If websocket then we create a json out of the given message and exit(0)"""

    if communication_type == CommunicationTypeEnum.CONSOLE:
        message = message.replace(seperator, '\n')
    elif communication_type == CommunicationTypeEnum.WEBSOCKET:
        message = update_json_message(action_type, message)

    return message


def update_json_message(action_type: WorkflowActionEnum, message: str) -> json:
    """Update message to json format"""

    dict_message = {"message": message}
    if action_type == WorkflowActionEnum.AGE_DETECTION:
        dict_message["type"] = "command"
    else:
        dict_message["type"] = "text"
    json_message = json.dumps(dict_message)

    return json_message


# TODO get_last_dialog_workflow_state_id() - This is the name in the database, let's be consistance
# TODO Shall we move this function as static method in DialogWorkflowLocal?
# TODO Change the order of the parameters (alphabet order): campaign, channel, message, profile_context
# TODO Change the algorithem
# 1st priority profile_id+ message_id
# 2nd priority profile_id+ channel_id
# 3rd priority profile_id+ campaign_id
def get_curr_state_id(profile_id: int, channel_id: int = None, campaign_id: int = None, message_id: int = None) -> int:
    """Returns profiles' curernt state number"""

    crud = GenericCRUD(
        default_schema_name='campaign_message_profile',
        default_table_name='campaign_message_profile_table',
        default_view_table_name='campaign_message_profile_general_view')

    select_clause_value = "last_dialog_workflow_state_id"
    where = "profile_id = %s"
    params = (profile_id,)
    if channel_id:
        where += " AND channel_id = %s"
        params += (channel_id,)
    if campaign_id:
        where += " AND campaign_id = %s"
        params += (campaign_id,)
    if message_id:
        where += " AND message_id = %s"
        params += (message_id,)
    # Note: there can be multiple matchs
    curr_state = crud.select_one_value_by_where(where=where, params=params, select_clause_value=select_clause_value,
                                                order_by="updated_timestamp DESC")
    if not curr_state:
        if campaign_id:
            logger.warning(f"No state found for the given profile_id, looking for state by {campaign_id=}",
                           object=locals())
            curr_state = get_state_id_by_campaign_id(campaign_id)
        if not curr_state:
            curr_state = DEFAULT_STATE_ID
            logger.warning("No state found for the given campaign_id, using default state " + str(DEFAULT_STATE_ID),
                           object=locals())
            crud.insert(data_dict={"profile_id": profile_id, "campaign_id": campaign_id,
                                   "message_id": message_id, "last_dialog_workflow_state_id": curr_state})

    logger.info(
        f"Current state: {profile_id=}, {curr_state=}", object=locals())
    return curr_state


def get_state_id_by_campaign_id(campaign_id: int) -> int:
    crud = GenericCRUD(
        default_schema_name='campaign',
        default_table_name='campaign_table',
        default_view_table_name='campaign_general_view')
    start_state_id = crud.select_one_value_by_column_and_value(
        select_clause_value="start_state_id", column_name="campaign_id", column_value=campaign_id)

    return start_state_id


def update_profile_curr_state_in_db(new_state: int, profile_id: int, channel_id: int = None,
                                    campaign_id: int = None, message_id: int = None) -> None:
    """This function updates the last_dialog_workflow_state_id in campaign_message_profile to the new state.
       Note that this function UPDATES the field and doesn't INSERT into the table. """

    crud = GenericCRUD(
        default_schema_name='campaign_message_profile',
        default_table_name='campaign_message_profile_table',
        default_view_table_name='campaign_message_profile_general_view')

    where = "profile_id = %s"
    params = (profile_id,)
    if channel_id:
        where += " AND channel_id = %s"
        params += (channel_id,)
    crud.update_by_where(where=where, params=params, data_dict={"last_dialog_workflow_state_id": new_state},
                         limit=1, order_by="updated_timestamp DESC")
    if message_id and campaign_id:
        crud.update_by_column_and_value(schema_name="message", table_name="message_table",
                                        column_name="message_id", column_value=message_id,
                                        data_dict={"campaign_id": campaign_id})


# TODO: Make sure we have good testing coverage to this function
def store_age_detection_picture(age_range: str, profile_id: int) -> None:
    """Stores the picture in Nir's storage schema, gets a storage_id and inserts into the computer_vision_storage_table"""
    # storage = AwsS3Storage(bucket_name="storage.us-east-1.dvlp1.bubblez.life", region="us-east-1")
    # storage_id = storage.upload_file("C:\\Users\\User\\OneDrive\\Circles\\age-detection-backend\\src\\alonPicture.png", "Alon's picture", "", 1)

    # age_range_split = age_range.split('-')
    # TODO Why this is commented?
    # TODO Why we commented this? Let's uncomment
    # min_age = int(age_range_split[0][:len(age_range_split[0])-1])
    # max_age = int((age_range_split[1])[1:])
    # cursor.execute("""USE computer_vision_storage""")
    # cursor.execute("""INSERT INTO computer_vision_storage_table
    #                 (storage_id, profile_id, min_age, max_age) VALUES (%s, %s, %s, %s)""",
    #                [storage_id, profile_id, min_age, max_age])
    # connection.commit()
    pass


def get_child_nodes_of_current_state(fields: list, table_name: str, values_from_where_to_select: tuple,
                                     variables_from_where_to_select: list) -> list[dict]:
    """Recieves all the relevant information and selects the child nodes of the current state from the given table, and returns them"""
    crud = GenericCRUD(default_schema_name='dialog_workflow',
                       default_table_name=table_name)
    select_clause_value = ", ".join(fields)
    where = " AND ".join(
        f"{variable} = %s" for variable in variables_from_where_to_select)
    child_nodes = crud.select_multi_dict_by_where(select_clause_value=select_clause_value,
                                                  where=where, params=values_from_where_to_select)
    # cursor.execute(sql_query, values_from_where_to_select)
    # child_nodes = cursor.fetchall()

    return child_nodes


class Group:
    def __init__(self, parameter1: int) -> None:
        self.parameter1 = parameter1

    # TODO Make sure we have tests for this and all other methods
    def get_group_childs_id_bellow_parent_id(self) -> list[int]:
        """returns all the childs ids below the given parent_id.
            This function gets all the id's of records that their parent_state_id is the given id, and continues to add id's  recursively
            until all the records that their parent_state_id matches an id in the table."""

        connection = Connector.connect("group")
        cursor = connection.cursor(dictionary=True, buffered=True)
        # TODO Fix this SQL  [why?]
        cursor.execute("""
        WITH RECURSIVE cte AS (
            SELECT group_view.group_id FROM group_view WHERE group_id = %s
            UNION ALL
            SELECT group_view.group_id FROM group_view
            JOIN cte ON group_view.parent_group_id = cte.group_id
        )
        SELECT cte.group_id FROM cte""", (self.parameter1,))
        group_id_dict = cursor.fetchall()
        group_childs_id = [group['group_id'] for group in group_id_dict]

        return group_childs_id

    def get_child_group_names(self) -> list:
        """Gets all the child title names from the ml table of the given parent_id."""

        group_ids = self.get_group_childs_id_bellow_parent_id()
        crud = GenericCRUD(default_schema_name='group',
                           default_view_table_name='group_ml_view')
        select_clause_value = "title"
        group_id_placeholders = ','.join(["%s"] * len(group_ids))
        params = tuple(group_ids)
        where = f"group_id IN ({group_id_placeholders})"
        child_group_names = crud.select_multi_value_by_where(select_clause_value=select_clause_value,
                                                             where=where, params=params)
        # child_group_names = [group['title'] for group in group_name_dict]

        return child_group_names

    # def get_child_group_id(self) -> list[int]:
    #     """Gets the id of all the records with the given group name"""
    #     cursor.execute("""USE `group`""")
    #     cursor.execute("""SELECT group_id from group_ml_en_view WHERE title = %s""", [self.parameter1])
    #     group_id_dict = cursor.fetchall()
    #     return [group['group_id'] for group in group_id_dict]


# TODO Shall we move this to a menu class?
def generic_menu(*, options: list, got_response: bool, chosen_numbers: str, choose_one_option: bool,
                 outgoing_message: str) -> list[int] | dict:
    """A generic function for displaying a menu for the user.
        Returns: If not got_response: the menu options as json to send to user.
                 Otherwise, returns the chosen numbers as list in int"""
    logger.info(object=locals())
    outgoing_message_json = None
    if not got_response:
        outgoing_message += f"Please choose EXACTLY ONE option between 1-{len(options)}:{seperator}" if choose_one_option else \
            f"Please select your desired choices, You may select any of the numbers between 1-{len(options)} with a comma seperator between each choice:{seperator}"  # noqa
        outgoing_message_json = None
        for i, option in enumerate(options):
            outgoing_message = outgoing_message + \
                f'{i + 1}) {option}{seperator}'
            outgoing_message_json = process_message(communication_type=COMMUNICATION_TYPE,
                                                    action_type=WorkflowActionEnum.TEXT_MESSAGE_ACTION,
                                                    message=outgoing_message)
        if COMMUNICATION_TYPE == CommunicationTypeEnum.WEBSOCKET:
            return outgoing_message_json

    if not chosen_numbers and COMMUNICATION_TYPE == CommunicationTypeEnum.CONSOLE:
        if outgoing_message_json:  # print to console
            print(outgoing_message_json.replace(seperator, "\n"))
        chosen_numbers = input(
            f"Please choose the options you want between 1-{len(options)}: ")
    chosen_numbers = chosen_numbers.split(',')
    generic_menu_result = [int(x) for x in chosen_numbers if x.isdigit()]
    if not generic_menu_result:
        logger.exception("No chosen numbers", object=locals())
    elif not all(x.isdigit() for x in chosen_numbers):
        logger.warning("Not all chosen numbers are digits", object=locals())
    return generic_menu_result


module_wrapper(logger)
