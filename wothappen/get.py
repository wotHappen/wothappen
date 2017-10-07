import requests
import json
import http, urllib

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

ACCESS_KEY = "e58438c7303146b79f63134b261d5b29"

class ChatText:
	def __init__(self, roomId):
		self.roomId = roomId
		self.all = []
		self.texts = []
		self.times = []

		url = "https://api.ciscospark.com/v1/messages?roomId=" + self.roomId
		params = {
			'Authorization': "Bearer ODYyNzQ3ZGYtMTM3Zi00ZmE5LTk3MTctM2U5YjViYTQ4MjFhYzkxZmIzNzUtZGI2",
			'Content-Type': "application/json; charset=utf-8"
		}

		num_iterations = 0
		while True:
			num_iterations += 1
			if num_iterations > 10 or not url:
				break
			print(url)
			r = requests.get(url, headers=params)
			self.json = json.loads(r.text)
			url = r.headers.get('Link', None)
			if url:
				url = url[1:url.find(';')-1]
			for item in self.json["items"]:
				self.all.append(item)
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

def createTextStream(chatText):
	textstream = ''
	for text in chatText:
		if type(text) is str:
			textstream += text + ". "
		else:
			textstream += text.decode('utf-8') + ". "
	return textstream

def createTextStreamMicrosoft(chatText):
	doc = {'documents': [
		{
			'id': '1',
			'language': 'en',
			'text': '',
		}
	]}
	for text in chatText:
		if type(text) is str:
			doc['documents'][0]['text'] += text + ". "
		else:
			doc['documents'][0]['text'] += text.decode('utf-8') + ". "

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

def getKeyPhrases(chatText, accessKey):
	uri = 'westus.api.cognitive.microsoft.com'
	path = '/text/analytics/v2.0/keyPhrases'

	headers = {'Ocp-Apim-Subscription-Key': accessKey}
	conn = http.client.HTTPSConnection(uri)
	# body = json.dumps(getLanguage(chatText, accessKey))
	body = str(createTextStream(chatText))

	conn.request("POST", path, body, headers)
	response = conn.getresponse()
	returnedJson = json.loads(response.read().decode('utf-8'))

	return returnedJson['documents'][0]['keyPhrases']

def getSummary(chatText):
	body = str(createTextStream(chatText))
	parser = PlaintextParser.from_string(body, Tokenizer("english"))
	stemmer = Stemmer("english")

	summarizer = Summarizer(stemmer)
	summarizer.stop_words = get_stop_words("english")

	return summarizer(parser.document, 5)

messages = ChatText("df53038c-1940-355e-aa24-e4bc8d67b64a")
sentiments = getSentiment(messages, ACCESS_KEY)
print(getOverallSentiment(sentiments))

messagesByDate = {}
for message in messages.all:
	key = message["created"][:10]
	value = message["text"]
	if key not in messagesByDate:
		messagesByDate[key] = []
	messagesByDate[key].append(value)

for k,v in messagesByDate.items():
	print("Summary of the conversation on " + k + ":")
	summaries = getSummary(v)
	for sentence in summaries[4:]:
		print(sentence)
	# keyPhrases = getKeyPhrases(v, ACCESS_KEY)
	# for phrase in keyPhrases:
	# 	print(phrase + ", ", end="")
