import http.client
import json


def send_bulk_sms(messageText, mobiles:list, sendDateTime=None):
    conn = http.client.HTTPSConnection("api.sms.ir")
    payload = json.dumps({
    "lineNumber": '30002108013697',
    "messageText": messageText,
    "mobiles": mobiles,
    "sendDateTime": sendDateTime
        })
    headers = {
    'X-API-KEY': 'HXaFsl9RSg1aaMozoaf7a26BZ3IYF8PCD2TuDaOEdEVltHk9',
    'Content-Type': 'application/json'
        }
    conn.request("POST", "/v1/send/bulk", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


def verifiction(mobile, code):
    conn = http.client.HTTPSConnection("api.sms.ir")
    # payload = "{\n  \"mobile\": \"09195121341",\n  \"templateId\": YourTemplateID,\n
    # \"parameters\": [\n    {\n      \"name\": \"PARAMETER1\",\n      \"value\": \"000000\"\n    },
    # \n    {\n        \"name\":\"PARAMETER2\",\n        \"value\":\"000000\"\n    }\n  ]\n}"
    payload = json.dumps({
        'mobile': mobile, 'templateId': 718828,
        'parameters': [{'name': 'CODE', 'value': code}]
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'text/plain',
      'x-api-key': 'HXaFsl9RSg1aaMozoaf7a26BZ3IYF8PCD2TuDaOEdEVltHk9'
    }
    conn.request("POST", "/v1/send/verify", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    
    
print('😊')