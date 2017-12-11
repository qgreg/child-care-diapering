# coding=utf-8

# child care diapering
# By Greg Quinlan <greg@gregquinlan.work>
#
# An Alexa Skill to step through Diaper Changing Steps for a Child Care Setting 

import logging
from datetime import datetime
from flask import Flask, json, render_template
from flask_ask import Ask, request, session, question, statement

__author__ = 'Greg Quinlan'
__email__ = 'greg@gregquinlan.work'


app = Flask(__name__)
ask = Ask(app, '/')
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# Session starter
#
# This intent is fired automatically at the point of launch (= when the session starts).
# Use it to register a state machine for things you want to keep track of, such as what the last intent was, so as to be
# able to give contextual help.

@ask.on_session_started
def start_session():
    """
    Fired at the start of the session, this is a great place to initialise state variables and the like.
    """
    session.attributes['msgs_txt'] = [
        'prepare_text',
        'clean_text',
        'remove_text',
        'replace_text',
        'wash_child_text',
        'clean_up_text',
        'wash_your_text']
    session.attributes['msgs_detail'] = [
        'prepare_detail',
        'clean_detail',
        'remove_detail',
        'replace_detail',
        'wash_child_detail',
        'clean_up_detail',
        'wash_your_detail']
    session.attributes['msg_index'] = 0
    session.attributes['detail'] = True
    logging.debug("Session started at {}".format(datetime.now().isoformat()))

# Launch intent
#
# This intent is fired automatically at the point of launch.
# Use it as a way to introduce your Skill and say hello to the user. If you envisage your Skill to work using the
# one-shot paradigm (i.e. the invocation statement contains all the parameters that are required for returning the
# result

@ask.launch
def handle_launch():
    """
    (QUESTION) Responds to the launch of the Skill with a welcome statement and a card.

    Templates:
    * Initial statement: 'welcome'
    * Reprompt statement: 'welcome_re'
    * Card title: 'child care diapering
    * Card body: 'welcome_card'
    """

    welcome_text = render_template('welcome')
    welcome_re_text = render_template('welcome_re')
    welcome_card_text = render_template('welcome_card')

    return question(welcome_text).reprompt(welcome_re_text).standard_card(title="Child Care Diapering", text=welcome_card_text)


# Built-in intents
#
# These intents are built-in intents. Conveniently, built-in intents do not need you to define utterances, so you can
# use them straight out of the box. Depending on whether you wish to implement these in your application, you may keep
# or delete them/comment them out.
#
# More about built-in intents: http://d.pr/KKyx

@ask.intent('NextStepIntent')
def handle_next():
    """
    (STATEMENT) Handles the 'next' built-in intention.
    """
    this_index = session.attributes['msg_index']
    if session.attributes['msg_index'] <= (len(
            session.attributes['msgs_txt']) - 2):
        next_tagline = render_template('next_tagline')
        next_reprompt = render_template('reg_reprompt')
        session.attributes['msg_index'] += 1
    else:
        next_tagline = render_template('last_tagline')
        next_reprompt = render_template('last_reprompt')
    next_text = render_template(session.attributes['msgs_txt'][this_index])
    if session.attributes['detail']:
        next_detail = render_template(
            session.attributes['msgs_detail'][this_index])
        next_message = next_text + next_detail + next_tagline
    else:
        next_message = next_text + next_tagline
    logging.debug('Question item {}'.format(
        this_index))
    return question(next_message).reprompt(next_reprompt)


@ask.intent('AMAZON.StopIntent')
def handle_stop():
    """
    (STATEMENT) Handles the 'stop' built-in intention.
    """
    farewell_text = render_template('stop_bye')
    return statement(farewell_text)


@ask.intent('AMAZON.CancelIntent')
def handle_cancel():
    """
    (STATEMENT) Handles the 'cancel' built-in intention.
    """
    farewell_text = render_template('cancel_bye')
    return statement(farewell_text)


@ask.intent('AMAZON.HelpIntent')
def handle_help():
    """
    (QUESTION) Handles the 'help' built-in intention.

    You can provide context-specific help here by rendering templates conditional on the help referrer.
    """

    help_text = render_template('help_text')
    return question(help_text)


@ask.intent('DetailIntent')
def handle_detail():
    """
    (?) Handles the 'detail' intention.
    """
    session.attributes['detail'] = True

    return handle_next()


@ask.intent('SummaryIntent')
def handle_detail():
    """
    (?) Handles the 'detail' intention.
    """
    session.attributes['detail'] = False

    return handle_next()


@ask.intent('AMAZON.NoIntent')
def handle_no():
    """
    (?) Handles the 'no' built-in intention.
    """
    session.attributes['detail'] = False

    return handle_next()

@ask.intent('AMAZON.YesIntent')
def handle_yes():
    """
    (?) Handles the 'yes'  built-in intention.
    """
    session.attributes['detail'] = True

    return handle_next()


@ask.intent('AMAZON.PreviousIntent')
def handle_back():
    """
    (?) Handles the 'go back!'  built-in intention.
    """
    if session.attributes['msg_index'] >= 2:
        session.attributes['msg_index'] += -2
        return handle_next()
    else:
        no_back_text = render_template('no_back')
        next_reprompt = render_template('reg_reprompt')
        return question(no_back_text).reprompt(next_reprompt)



@ask.intent('AMAZON.StartOverIntent')
def start_over():
    """
    (QUESTION) Handles the 'start over!'  built-in intention.
    """
    session.attributes['msg_index'] = 0
    return handle_next()


# Ending session
#
# This intention ends the session.

@ask.session_ended
def session_ended():
    """
    Returns an empty for `session_ended`.

    .. warning::

    The status of this is somewhat controversial. The `official documentation`_ states that you cannot return a response
    to ``SessionEndedRequest``. However, if it only returns a ``200/OK``, the quit utterance (which is a default test
    utterance!) will return an error and the skill will not validate.

    """
    return statement("")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
