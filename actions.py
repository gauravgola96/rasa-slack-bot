from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals


from rasa_core_sdk import Action
from rasa_core_sdk.forms import FormAction
from rasa_core_sdk.events import FollowupAction, Restarted ,UserUttered
from config import mlsql_api
import re
import requests


from rasa_core.processor import ACTION_LISTEN_NAME

from rasa_core_sdk.events import ConversationPaused ,ConversationResumed
from rasa_core.channels.slack import SlackBot





class ActionRestarted(Action):
    def name(self):
        return 'action_restart'
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template('utter_greetings.bye',tracker=tracker)
        return[Restarted()]


class ActionListen(Action):
    """The first action in any turn - bot waits for a user message.

    The bot should stop taking further actions and wait for the user to say
    something."""

    def name(self):
        return 'action_listen'

    def run(self, dispatcher, tracker, domain):
        return []


class utter_message_:
    def __init__(self):
        return

    def utter_message(self, message, dispatcher):
        dispatcher.utter_message(message)
        return []


class ActionSql(Action):

    def name(self):
        return 'action_sql'

    def run(self,dispatcher, tracker, domain):

        if tracker.latest_message['text'] == 'Default csv':
            dispatcher.utter_message('Using default csv with link : https://drive.google.com/file/d/1pSi0n_SE0lJzvd58hlFuK2KDpb8eK-cK/view?usp=sharing')
            dispatcher.utter_template('utter_csv_question', tracker)

        if tracker.latest_message['text'] == 'User value':
            dispatcher.utter_message('This feature is work in progress')
            dispatcher.utter_template('action_restart',tracker=tracker)

        return []





class Actionsqlapi(Action):

    def name(self):
        return 'action_sql_api'

    def run(self, dispatcher, tracker, domain):
        '''
        This is for hitting mlsql api
        '''
        message = tracker.latest_message['text']
        if message == 'User value':
            dispatcher.utter_message('This feature is not in working phase. Please contact my developer')
            dispatcher.utter_template('action_restart', tracker=tracker)

        elif re.search(pattern='question',string=message) :

            path = 'bag_mlsql.csv'

            csv = {'csv': open(path, 'rb').read()}

            url = mlsql_api

            user_input = tracker.latest_message['text']
            question = user_input.split(":")[1]

            payload = {'q' : question}
            response = requests.post(url=url,files=csv,data=payload,verify= True)

            if response.status_code != 200:
                dispatcher.utter_message('No response from sql api \n Status code : {}'.format(response.status_code))

            answer = response.json()['answer'][0]
            parameter = response.json()['params']
            sql = response.json()['sql']


            dispatcher.utter_message('Answer : {}'.format(answer))
            dispatcher.utter_message('Generated query : {}'.format(sql))
            dispatcher.utter_message('Paramter : {}'.format(parameter))
        else:
            dispatcher.utter_message('Something happened on which I am not trained. Report the flow to my developer.')
            dispatcher.utter_template('restart_action',tracker=tracker)

        return[]





class questionform(FormAction):

    def name(self):

        return "question_form"

    @staticmethod
    def required_slots(tracker):
        """A list of required slots that the form has to fill"""

        return ["question"]

