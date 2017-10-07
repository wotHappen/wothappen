import requests
import json
import http, urllib

class ChatText:
	def __init__(self, roomId):
		self.roomId = roomId
		self.texts = []
		self.times = []
		params = {
			'Authorization': "Bearer ODYyNzQ3ZGYtMTM3Zi00ZmE5LTk3MTctM2U5YjViYTQ4MjFhYzkxZmIzNzUtZGI2",
			'Content-Type': "application/json; charset=utf-8"
		}
		r = requests.get("https://api.ciscospark.com/v1/messages?roomId=" + self.roomId, headers=params)
		self.json = json.loads(r.text)
		for item in self.json["items"]:
			self.texts.append(item["text"])
			self.times.append(item["created"])
		self.texts.reverse()


def createDocument(chatText):
	doc = {'documents': []}
	counter = 1
	for text in chatText.texts:
		doc['documents'].append({'id': str(counter), 'language': 'en', 'text': text})
		counter += 1
	return doc

# def getLanguage(chatText, accessKey):
# 	doc = createDocument(chatText)

# 	uri = 'westus.api.cognitive.microsoft.com'
# 	path = '/text/analytics/v2.0/languages'

# 	print("Hello")

# 	headers = {'Ocp-Apim-Subscription-Key': accessKey}
# 	conn = http.client.HTTPSConnection(uri)
# 	body = json.dumps (doc)
# 	conn.request ("POST", path, body, headers)
# 	response = conn.getresponse ()
# 	result = json.loads(json.dumps(response.read ()))

# 	for index, item in result["documents"]:
# 		doc["documents"][index]["language"] = ["detectedLanguages"]["iso6391Name"]

# 	print(doc)
# 	return doc

def getSentiment(chatText, accessKey):
	uri = 'westus.api.cognitive.microsoft.com'
	path = '/text/analytics/v2.0/sentiment'

	headers = {'Ocp-Apim-Subscription-Key': accessKey}
	conn = http.client.HTTPSConnection(uri)
	# body = json.dumps(getLanguage(chatText, accessKey))
	doc = createDocument(chatText)
	body = json.dumps(doc)

	conn.request("POST", path, body, headers)
	response = conn.getresponse()
	returnedJson = json.loads(response.read().decode('utf-8'))

	index = 0
	for item in returnedJson['documents']:
		doc['documents'][index]['score'] = item['score']
		index += 1

	return doc['documents']

def getOverallSentiment(messages):
	overall = 0
	size = 0
	for message in messages:
		size += 1
		overall += message['score']
	return overall / size

messages = getSentiment(ChatText("df53038c-1940-355e-aa24-e4bc8d67b64a"), "e58438c7303146b79f63134b261d5b29")
print(getOverallSentiment(messages))
