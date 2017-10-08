from flask import Flask, request, abort
import json
import requests

import get
import csutils

BOT_ID = "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNDc5NTE1MS0yODg5LTQ1NzUtOGNhZC0zYjZiOWUzOTNmMWQ"
BOT_ACCESS_TOKEN = "OThiZGYxOTEtZTE0Zi00ZTMzLTljMDktOWMyYjIxYzAyZjBkZmI2YTZjNmItZjg0"

app = Flask(__name__)

@app.route('/', methods=['POST'])
def test():
  json_file =request.json
  data = json_file['data']

  url = "https://api.ciscospark.com/v1/messages/" + data['id']
  getParams = {
    'Authorization': "Bearer NmZlNGIzNjktMTc3YS00MDM1LTk0NDAtNzQ0MzFkZWJmNzk0Zjc2M2E1YTItOWU1",
    'Content-Type': "application/json; charset=utf-8"
  }
  # the message that prompts the bot to react
  message = json.loads(requests.get(url, headers=getParams).text)

  # if 'show me the insights' in message.text and BOT_ID in message.mentionedPeople:
  output = str(get.output(data['roomId']))
  payload = {
    "roomId": data['roomId'],
    "text": output
  }
  posturl = 'https://api.ciscospark.com/v1/messages'  

  print(data['roomId'])
  print(output)
  botParams = {
    'Authorization': "Bearer " + BOT_ACCESS_TOKEN,
    'Content-Type': "application/json; charset=utf-8"
  }
  res = requests.post(posturl, json=payload, headers=botParams)
  return 'post firehose all', 200

if __name__ == "__main__":
  app.run(port=4041, debug=True)