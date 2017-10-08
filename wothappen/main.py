from flask import Flask, request, abort
import json
import requests

import get
import csutils

import parse_command

'''
Read config.json for BOT data
'''
config = ""
with open('config.json') as config_file:    
  config = json.load(config_file)

BOT_ID = config["BOT_ID"]
BOT_ACCESS_TOKEN = config["BOT_ACCESS_TOKEN"]
PORT = int(config["PORT"])

PARAMS = {
  'Authorization': "Bearer " + BOT_ACCESS_TOKEN,
  'Content-Type': "application/json; charset=utf-8"
}

def getRequestData():
  return request.json['data']

def getConnMessageBody(id):
  url = "https://api.ciscospark.com/v1/messages/" + str(id)
  return json.loads(requests.get(url, headers=PARAMS).text)

def sendConnReply(roomId, output):
  payload = {
    "roomId": roomId,
    "text": output
  }
  posturl = 'https://api.ciscospark.com/v1/messages'  
  print(roomId)
  print(output)
  res = requests.post(posturl, json=payload, headers=PARAMS)

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handler:
  data = getRequestData() # dict

  message = getConnMessageBody(data['id']) # json

  reply = parse_command.parse(message['text'], data['roomId'])

  sendConnReply(data['roomId'], reply)

  return 'post firehose all', 200


if __name__ == "__main__":
  app.run(port=PORT, debug=True)