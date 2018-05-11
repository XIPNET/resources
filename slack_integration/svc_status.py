import requests
import json

class ServiceStatus(object):
    """
    Just some quick prototyping for sending service status to slack channel

    The idea is that this will run as a cron job maybe or based on a trigger
    from splunk or some other app maybe to send the status of an internal service
    to slack...

    This will eventually get converted to an internal rocketChat instance we
    will prolly want to run just to keep it all internal

    """
    def __init__(self, service_owner):
        with open('api.json', 'r') as f:
            self.slack_url = json.load(f)['slack_webhook']
        self.service_owner = service_owner

    def post_message(self, message):
        headers = {"Content-type": "application/json"}
        message_text = self.service_owner + " Service: " + message
        pre_post_message = {"text": message_text}
        req = requests.post(self.slack_url, headers=headers, data=json.dumps(pre_post_message))
        return req


test = ServiceStatus("TonyPNode")

print(test.post_message("[insert service name]:[insert status here]"))


