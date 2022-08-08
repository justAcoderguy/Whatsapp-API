from cmath import log
import os

from flask import Flask, jsonify, request
from sqlalchemy import and_
from app.whatsapp_client import WhatsAppWrapper
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.helper import stringToTimestamp, timestampToString

import logging
logging.basicConfig(level='DEBUG')

app = Flask(__name__)
app.config.from_pyfile("config.py")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')

from app.models import Message

########### SENDING TEMPLATE MESSAGE ##################

@app.route("/send_template_message/", methods=["POST"])
def send_template_message():
    """Send message using a template to a phone number"""

    # Validation 
    if "language_code" not in request.json:
        return jsonify({"error": "Missing language_code"}), 400

    if "phone_number" not in request.json:
        return jsonify({"error": "Missing phone_number"}), 400

    if "template_name" not in request.json:
        return jsonify({"error": "Missing template_name"}), 400

    client = WhatsAppWrapper()

    response = client.send_template_message(
        template_name=request.json["template_name"],
        language_code=request.json["language_code"],
        phone_number=request.json["phone_number"],
    )

    return jsonify(
        {
            "data": response,
            "status": "success",
        },
    ), 200

######### WEBHOOK FUNCTIONS ########################

@app.route("/webhook", methods=["POST"])
def webhook_whatsapp():
    """
        Endpoint to store data provided by Meta.
        ie. Get message from Webhook.
    """
    client = WhatsAppWrapper()

    response = client.process_webhook_notification(request.get_json())


    for res in response:
        try:
            message = Message(
                phone = res["phone"],
                message = res["message"],
                timestamp = res["timestamp"]
            )
            db.session.add(message)
            db.session.commit()
            return jsonify({"status": "success - db updated"}, 200)

        except Exception as e:
            return(jsonify({"status": "failed db addition", "error": str(e)}, 400))
    return jsonify({"status": "success - db not updated"}, 200)


@app.route("/webhook/", methods=["GET"])
def webhook_verify():
    """Webhook verification challenge"""
    if request.method == "GET":
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return "Authentication failed. Invalid Token."


############## RETRIEVAL OF MESSAGES ###############################

@app.route("/messages/", methods=["POST", "GET"])
def messages():
    """
        Endpoint to retrieve ALL messages - GET request
        Endpoint to retrieve messages according to timestamp and phone number 
        - POST Request
    """
    if request.method == "GET":
        try:
            messages=Message.query.all()
            return  jsonify([message.serialize() for message in messages])
        except Exception as e:
            return(jsonify({"status": "failed message retrieval", "error": str(e)}, 400))

    phone = request.json.get("phone")
    start_time = request.json.get("start")
    end_time = request.json.get("end")
    if not phone:
        return(jsonify(
            {
                "status": "Fail",
                "message": "Details Required - Phone number",
            }
        ),400)
    if not start_time:
        return(jsonify(
            {
                "status": "Fail",
                "message": "Details Required - Start Time",
            }
        ),400)
    if not end_time:
        return(jsonify(
            {
                "status": "Fail",
                "message": "Details Required - End Time",
            }
        ),400)

    start = stringToTimestamp(start_time)
    end = stringToTimestamp(end_time)

    try:
        messages=Message.query.filter(Message.phone == phone).filter(Message.timestamp.between(
            start, end
        ))
        result = []
        for message in messages:
            result.append(
                {
                    "phone": message.phone,
                    "message": message.message,
                    "timestamp": timestampToString(message.timestamp)
                }
            )
            

        return (
            {
                    "status": "Success",
                    "message": "Success",
                    "data": result
            },
            200
        )
    except Exception as e:
        return(jsonify(
            {
                "status": "Fail",
                "message": str(e),
            }
        ),500)

