from flask import Flask, request, abort
import json
import requests
import get

BOT_ID = "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNDc5NTE1MS0yODg5LTQ1NzUtOGNhZC0zYjZiOWUzOTNmMWQ"

app = Flask(__name__)

@app.route('/', methods=['POST'])
def test():
  json_file =request.json
  data = json_file['data']

  url = "https://api.ciscospark.com/v1/messages?messageId=" + data['id']
  params = {
    'Authorization': "Bearer ODYyNzQ3ZGYtMTM3Zi00ZmE5LTk3MTctM2U5YjViYTQ4MjFhYzkxZmIzNzUtZGI2",
    'Content-Type': "application/json; charset=utf-8"
  }
  message = requests.get(url, headers=params)
  
  if 'show me the insights' in message.text and BOT_ID in message.mentionedPeople:
    output = get.output()
    url = "https://api.ciscospark.com/v1/"

  


  print('data posted from firehose: ', data)
  return 'post firehose all', 200

if __name__ == "__main__":
  app.run(port=4041, debug=True)