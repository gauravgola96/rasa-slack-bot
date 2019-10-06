from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

import rasa_core
from rasa_core.run import serve_application
from rasa_core.agent import Agent
# from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.utils import EndpointConfig

logger = logging.getLogger(__name__)


# def run_bot(serve_forever=True):
#     agent = Agent.load('./models/dialogue/default/dialogue_model', RasaNLUInterpreter('./models/nlu/default/nlu_model'))
#
#     if serve_forever:
#         agent.handle_channel(ConsoleInputChannel())
#
#     return agent

def run_bot(serve_forever=True):
    interpreter = RasaNLUInterpreter('./models/nlu/default/nlu_model')
    action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
    agent = Agent.load('./models/dialogue/default/dialogue_model/', interpreter=interpreter, action_endpoint=action_endpoint)
    rasa_core.run.serve_application(agent, channel='cmdline')

    return agent


if __name__ == '__main__':
    run_bot()