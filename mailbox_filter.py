#!/usr/bin/python

# Arguments:
# <sample_mbox.csv> <filter_out.csv> <phrases.csv> <file_to_write_occurances_of_phrases.csv>(by default "phrase_occurances.csv")


import pandas as pd
import sys
import re
from collections import defaultdict

def search_for_phrases_in(questions, phrases):
	phrases_count = defaultdict(lambda: 0)
	for client_email, client_questions in questions.iteritems():
		for question, amount in client_questions.items():
			for phrase in phrases:
				for m in re.finditer(phrase, question):
					phrases_count[phrase] += amount
	return phrases_count 

def search_for_questions(data, filter_out_emails, start_questions = ["How ", "Why ", "What ", "Where "]):
	questions = defaultdict(lambda: dict())
	for index in range(data.shape[0]):
		body = str(data.iloc[index].values[-1])
		for email in filter_out_emails:
			email = str(email).strip()
			if email[0:2] == "*@":
				email = email[1:]
			if len(email) > len(body):
				break
			for m in re.finditer(email, body):
				body = body[:m.start()]
				break
		message_from = data.iloc[index].values[1]
		for m in re.finditer("<.+@.+>", message_from):
			message_sender = message_from[m.start() + 1: m.end() - 1]
			break

		for start_question in start_questions:
			for m in re.finditer(start_question + ".+\?", str(body)):
				questions[message_sender][body[m.start():m.end()]] = 1
		
	with open("Question.csv", "wb") as question_out:
		for key, value in questions.iteritems():
			question_out.write(key + "\r\n")
			for k in value.keys():
				question_out.write(k + "\r\n")
		
	return questions

def write_questions(questions):
	with open("FAQ.csv", "wb") as write_questions:
		for client_mail, client_questions in questions.iteritems():
			[write_questions.write(question + "\r\n") for question in client_questions.keys()]
	return None

def filter_data_by(filter_out_emails, data):
	for email in filter_out_emails:
		if email[0:2] == "*@":
			email = str(email[1:]).strip()
		data = data[~data["from"].str.contains(email)]
	return data


def main():
	if len(sys.argv) > 2:
		data = pd.read_csv(sys.argv[1], sep = ",", header = None)
		data.columns = ["subject", "from", "date", "body"]

		with open(sys.argv[2], "r") as filter_file:
			filter_out_emails = [line.strip() for line in filter_file]
		
		data = filter_data_by(filter_out_emails, data)
		questions = search_for_questions(data, filter_out_emails)
		write_questions(questions)

		if len(sys.argv) > 3:
			phrases = defaultdict(lambda: 0)
			with open(sys.argv[3], "r") as phrases_file:
				phrases = [line.strip() for line in phrases_file]
			phrases = search_for_phrases_in(questions, phrases)	
			phrases_frame = pd.DataFrame(dict(phrases).items(), columns = ["phrase", "occurance"])
			file_name = "phrase_occurances.csv"
			if len(sys.argv) > 4:
				file_name = sys.argv[4]
			phrases_frame.sort(["phrase", "occurance"], ascending = [1, 1], inplace = True)
			phrases_frame.to_csv(file_name, sep=",", index = False, header = True)

if __name__ == "__main__":
	main()
