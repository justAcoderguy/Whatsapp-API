import os
import requests
import json

from dotenv import load_dotenv
load_dotenv()


class WhatsAppWrapper:

    API_URL = "https://graph.facebook.com/v13.0/"
    API_TOKEN = os.environ.get("WHATSAPP_API_TOKEN")
    NUMBER_ID = os.environ.get("WHATSAPP_NUMBER_ID")

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.API_TOKEN}",
            "Content-Type": "application/json",
        }
        self.API_URL = self.API_URL + self.NUMBER_ID

    def send_template_message(self, template_name, language_code, phone_number):

            payload = json.dumps({
                "messaging_product": "whatsapp",
                "to": phone_number,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {
                        "code": language_code
                    }
                }
            })

            response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)

            assert response.status_code == 200, "Error sending message"

            return response.status_code

    def process_webhook_notification(self, data):
        """Process webhook notification
        """

        response = []
        
        for entry in data["entry"]:
            for change in entry["changes"]:
                if "messages" in change["value"]:
                    for message in change["value"]["messages"]:
                        if message["type"] == "text":
                            response.append(
                                {
                                    "phone": message["from"],
                                    "timestamp": message["timestamp"],
                                    "message": message["text"]["body"]
                                }
                            )
        return response