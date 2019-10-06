from rasa_core.channels.slack import SlackInput
# from rasa_core.channels.slack import SlackBot
from rasa_core.agent import Agent
from rasa_core.interpreter import RegexInterpreter
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.utils import EndpointConfig



def run():
    nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/nlu_model')
    action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
    agent = Agent.load('./models/dialogue/default/dialogue_model', interpreter=nlu_interpreter,action_endpoint=action_endpoint)
    input_channel = SlackInput(
        slack_token="xoxb-673242585665-673266261441-Z26pD2yaxVv0KmHnohoQizdk"
        # this is the `bot_user_o_auth_access_token`
        # slack_channel="YOUR_SLACK_CHANNEL"
        # the name of your channel to which the bot posts (optional)
    )
    # set serve_forever=True if you want to keep the server running
    agent.handle_channels([input_channel], 5004, serve_forever=True)
    return agent

if __name__=='__main__':
    run()


