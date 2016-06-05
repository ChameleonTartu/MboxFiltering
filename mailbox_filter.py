#!/usr/bin/python

# Arguments:
# <sample_mbox.csv> <filter_out.csv> <phrases.csv> <file_to_write_occurances_of_phrases.csv>(by default "phrase_occurances.csv")


import pandas as pd
import sys
import re
from collections import defaultdict
import csv
import os

def search_for_phrases_in(questions, phrases):
	phrases_count = defaultdict(lambda: 0)
	for client_email, client_questions in questions.iteritems():
		for question, amount in client_questions.items():
			for phrase in phrases:
				for m in re.finditer(phrase, question):
					phrases_count[phrase] += amount
	return phrases_count 

def write_questions_to(questions, filename = "Question.csv"):
	with open(filename, "wb") as question_out:
		for key, value in questions.iteritems():
			question_out.write(key + "\r\n")
			for k in value.keys():
				question_out.write(k + "\r\n")
	return None	


def search_for_questions(data, filter_out_emails, start_questions = ["How ", "Why ", "What ", "Where ", "Is ", "Are ", "Do ", "Does ", "When ", "Did ", "Have ", "Will ", "Had ", "Was ", "Where ", "Shall ", "Would ", "Should ", "Could ", "Who ", "Which ", "Didn't ", "Haven't ", "Hadn't ", "Wouldn't ", "Shouldn't ", "Couldn't ", "Can ", "May ", "Aren't ", "Isn't ", "Weren't ", "Wasn't ", "Cannot ", "Can't "]):
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
		
		write_questions_to(questions)	
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

def throw_exception(message):
	print message
	sys.exit()

def retrieve_data_from(filename):
	if os.stat(filename).st_size == 0:
		throw_exception("Mailbox csv file is empty!")
	data = pd.read_csv(filename, sep = ",", header = None)
	if data.shape[1] != 4:
		throw_exception("Mailbox csv file is inccorrect!")
	data.columns = ["subject", "from", "date", "body"]
	return data	
	
def retrieve_filter_out_emails_from(filename):
	if not os.path.isfile(filename):
		throw_exception("Filter out csv file does not exist!")

	with open(filename, "rb") as filter_file:
		reader = csv.reader(filter_file, delimiter = ',')
		filter_out_emails = ["".join([word.strip() for word in line]) for line in reader]
	
	return filter_out_emails		

def retrieve_phrases_from(filename):
	phrases = defaultdict(lambda: 0)
					
	if not os.path.isfile(filename):
		throw_exception("File with predefined phrases does not exist!")

	with open(filename, "rb") as phrases_file:
		reader = csv.reader(phrases_file, delimiter = '|')
		phrases = ["".join([word.strip() for word in line]) for line in reader]
	if len(phrases) == 0:
		throw_exception("File with phrases is empty")	
	return phrases

def write_phrases_to(phrases_frame, filename = "phrase_occurances.csv"):
	file_name = filename
	if len(sys.argv) > 4:
		file_name = sys.argv[4]
		phrases_frame.sort(["phrase", "occurance"], ascending = [1, 1], inplace = True)
	phrases_frame.to_csv(file_name, sep=",", index = False, header = True)

def main():
	if len(sys.argv) > 2:
		data = retrieve_data_from(sys.argv[1])	
		filter_out_emails = retrieve_filter_out_emails_from(sys.argv[2])
		data = filter_data_by(filter_out_emails, data)
		questions = search_for_questions(data, filter_out_emails)
		write_questions(questions)

		if len(sys.argv) > 3:
			phrases = retrieve_phrases_from(sys.argv[3])
			phrases = search_for_phrases_in(questions, phrases)
			exit()	
			phrases_frame = pd.DataFrame(dict(phrases).items(), columns = ["phrase", "occurance"])
			
			write_phrases_to(phrases_frame)
			

if __name__ == "__main__":
	main()
