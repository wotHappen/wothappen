from string import Template
import random

import get

def selectRandomFrom(lst):
	return random.choice(lst)

EmptyResponseStrings = [
	'Here I am!',
	'Hello',
	'(Ooops, you found me)'
]
EmptyCommandStrings = [
	'\'?\' alone is an interesting mark, right?',
	'Now what?'
	'So?'
]
UnknownCommandStrings = [
	'What does THAT mean?',
	'Curious, but just cannot understand what you said...',
	'SyntaxError: Traceback... YourBrain'
]

def selectRandomTemplateFrom(lst, emoji):
	return random.choice(lst).substitute(emoji=emoji)

RandomTemplateStrings_0 = [
	Template("Oh NO! $emoji"),
	Template("$emoji What happened?!")
]
RandomTemplateStrings_1 = [
	Template("Pat pat we all have unhappy times $emoji"),
	Template("$emoji ...")
]
RandomTemplateStrings_2 = [
	Template("Peace of heart $emoji"),
	Template("$emoji (nothing special to say)")
]
RandomTemplateStrings_4 = [
	Template("Have a nice day! $emoji"),
	Template("$emoji You all look great today")
]
RandomTemplateStrings_5 = [
	Template("WOW!!! $emoji"),
	Template("$emoji Someone must have won a jackpot!")
]


def parse(s, roomId):
	cmd = str(s).strip().split()

	if len(cmd) <= 1:
		return processEmptyQuery()
	elif cmd[1][0] == '?':
		return processStrictCommand(" ".join(cmd[1:])[1:], roomId)
	else:
		return processSpeculation(" ".join(cmd[1:]), roomId)


def processEmptyQuery():
	return selectRandomFrom(EmptyResponseStrings)

def processStrictCommand(cmd, roomId):
	cmd_lst = cmd.split()
	if len(cmd_lst) <= 0:
		return selectRandomFrom(EmptyCommandStrings)
	else:
		if cmd_lst[0] == 'mood' or cmd_lst[0] == 'feel' or cmd_lst[0] == 'feeling' or cmd_lst[0] == 'sentiment':
			return caseSentiment(roomId)
		elif cmd_lst[0] == 'sum' or cmd_lst[0] == 'summary':
			return caseSummary(roomId)
		elif cmd_lst[0] == 'keyword':
			return caseKeyword(roomId)
		elif cmd_lst[0] == 'easteregg':
			return r"""
			  ___
			 /   \
			|     |
			|     |
 			 \___/
			     _____            _
                | ____|__ _  __ _| |
                |  _| / _` |/ _` | |
                | |__| (_| | (_| |_|
                |_____\__, |\__, (_)
                      |___/ |___/
			"""
		else:
			return selectRandomFrom(UnknownCommandStrings)

def processSpeculation(cmd, roomId):
	"""
	Speculation just implemented a very simple keyword-mapping approach
	"""
	word_lst = cmd.split()

	sentiment_count = 0
	summary_count = 0
	keyword_count = 0

	sentiment_lst = ["mood", "moods", "feel", "felt", "feels", "feeling", "feelings", "sentiment", "sentiments"]
	summary_lst = ["summary", "summaries", "general", "sum", "overall", "most"]
	keyword_lst = ["keyword", "keywords", "phrase", "phrases"]

	for word in word_lst:
		if word in keyword_lst:
			keyword_count += 1
		elif word in sentiment_lst:
			sentiment_count += 1
		elif word in summary_lst:
			summary_count += 1

	if keyword_count > 0 and keyword_count >= summary_count and keyword_count >= sentiment_count:
		return "You may want to know about keywords:\n" + caseKeyword(roomId)
	elif sentiment_count > 0 and sentiment_count >= summary_count:
		return "You may want to know about moods:\n" + caseSentiment(roomId)
	elif summary_count > 0:
		return "You may want to know about group summary:\n" + caseSummary(roomId)
	else:
		return "Sorry, but I am too dumb to guess what you want..."


def caseSentiment(roomId):
	sentiment = float(get.outputSentiment(roomId))
	pair = []
	if sentiment < 0.4:
		pair = ['\U0001F631', 0]
	elif sentiment < 0.47:
		pair = ['\U0001F630', 1]
	elif sentiment < 0.53:
		pair = ['\U0001F633', 2]
	elif sentiment < 0.8:
		pair = ['\U0001F60A', 3]
	else:
		pair = ['\U0001F604', 4]

	ret = ""
	ret += "Overall sentiment of the Group: " + str(sentiment) + "\n"
	if pair[1] == 0:
		ret += selectRandomTemplateFrom(RandomTemplateStrings_0, pair[0])
	elif pair[1] == 1:
		ret += selectRandomTemplateFrom(RandomTemplateStrings_1, pair[0])
	elif pair[1] == 2:
		ret += selectRandomTemplateFrom(RandomTemplateStrings_2, pair[0])
	elif pair[1] == 3:
		ret += selectRandomTemplateFrom(RandomTemplateStrings_3, pair[0])
	elif pair[1] == 4:
		ret += selectRandomTemplateFrom(RandomTemplateStrings_4, pair[0])

	return ret

def caseSummary(roomId):
	ret1 = "Here is the chat summary: \n"
	ret1 = get.outputSummaries(roomId)
	return ret1

def caseKeyword(roomId):
	# ret = "Here is the chat keywords: \n"
	ret = get.outputKeyPhrases(roomId)
	return ret