from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from rasa_core.agent import Agent
from rasa_core.policies import FallbackPolicy
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter
# from rasa_core.train import interactive
from rasa_core.training import interactive
from rasa_core.utils import EndpointConfig

logger = logging.getLogger(__name__)

fallback = FallbackPolicy(nlu_threshold=0.05 ,core_threshold= 0.05 , fallback_action_name='utter_unclear')


def run_weather_online(interpreter,
                       domain_file="domain.yml",
                       training_data_file='./data/dialogue/stories.md'):
    action_endpoint = EndpointConfig(url="http://localhost:5005/webhook")
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(max_history=3),fallback, KerasPolicy(max_history=3, epochs=300, batch_size=50)],
                  interpreter=interpreter,
                  action_endpoint=action_endpoint)

    data = agent.load_data(training_data_file)
    agent.train(data)
    interactive.run_interactive_learning(agent, training_data_file)
    return agent


if __name__ == '__main__':
    logging.basicConfig(level="INFO")
    nlu_interpreter = RasaNLUInterpreter('./models/dialogue/default/dialogue_model')
    run_weather_online(nlu_interpreter)
