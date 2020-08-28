from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os
from dataclasses import dataclass
from database import look_up_patient_from_number
from wit import Wit
import random

app = Flask(__name__)

TWILIO_SID = os.environ.get('SID')
TWILIO_TOKEN = os.environ.get('TOKEN')
WIT_TOKEN = os.environ.get('WIT_TOKEN')

twilio_client = Client(TWILIO_SID, TWILIO_TOKEN)
wit_client = Wit(WIT_TOKEN)


@dataclass
class InboundMessage:
    from_number: str
    to_number: str
    body: str


@app.route('/', methods=['GET', 'POST'])
def request_handler():
    inbound_message = _parse_twilio_request(request)
    # response_message = part_1_response(inbound_message)
    # response_message = part_2_response(inbound_message)
    # response_message = part_3_response(inbound_message)
    # response_message = part_4_response(inbound_message)
    response_message = part_5_response(inbound_message)

    response = MessagingResponse()
    response.message(response_message)
    return str(response)


def part_1_response(inbound_message: InboundMessage) -> str:
    return 'Thanks you all'


def part_2_response(inbound_message: InboundMessage) -> str:
    patient = look_up_patient_from_number(inbound_message.from_number)

    return f'Hello {patient.name}. Looks like you are taking {patient.drug_name}.'


def part_3_response(inbound_message: InboundMessage) -> str:
    patient = look_up_patient_from_number(inbound_message.from_number)

    response = None
    body = inbound_message.body
    if body == 'Thanks':
        thanks_responses = ["You're welcome", "You got it", "Of course!"]
        # response = f"You're welcome {patient.name}"
        response = random.choice(thanks_responses)
    elif body == 'Ok':
        response = f"Cool {patient.name}"
    else:
        response = f"Sorry {patient.name} I didn't get that, someone will be with you shortly"

    return response


def part_4_response(inbound_message: InboundMessage) -> str:
    patient = look_up_patient_from_number(inbound_message.from_number)

    response = None
    body = inbound_message.body
    if body in {'Thanks', 'thanks', 'thx'}:
        # thanks_responses = ["You're welcome", "You got it", "Of course!"]
        response = f"You're welcome {patient.name}"
    # elif body == 'Ok':
    elif 'ok' in body or 'okay' in body:
        response = f"Cool {patient.name}"
    else:
        response = f"Sorry {patient.name} I didn't get that, someone will be with you shortly"

    return response


def part_5_response(inbound_message: InboundMessage) -> str:
    patient = look_up_patient_from_number(inbound_message.from_number)
    wit_response = wit_client.message(inbound_message.body)
    intents = wit_response['intents']
    response = 'No intent detected'
    if len(intents) > 0:
        intent = intents[0]['name']

        if intent == 'Thanks':
            response = 'You are welcome'
        elif intent == 'Acknowledge':
            response = 'Cool'
        elif intent == 'Refill':
            response = f'{patient.name}, we will submit a refill for your {patient.drug_name} right away!'

    return response


def _parse_twilio_request(req) -> InboundMessage:
    return InboundMessage(
        from_number=req.form['From'],
        to_number=req.form['To'],
        body=req.form['Body']
    )
