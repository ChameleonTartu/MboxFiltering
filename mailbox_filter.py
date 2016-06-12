#!/usr/bin/python
# -*- coding: utf-8 -*-

# Arguments:
# <sample_mbox.csv> <filter_out.csv> <phrases.csv> <file_to_write_occurances_of_phrases.csv>(by default "phrase_occurances.csv")


import pandas as pd
import sys
import re
from collections import defaultdict
import csv
from os import stat, path
import io

def search_for_phrases_in(questions, phrases):
	phrases_count = defaultdict(lambda: 0)
	for client_email, client_questions in questions.iteritems():
		for question, amount in client_questions.items():
			for phrase in phrases:
				for m in re.finditer(phrase, question):
					phrases_count[phrase] += amount
	return phrases_count 

def write_questions_to(questions, filename = "Question.csv"):
	with io.open(filename, "w", encoding="utf-8") as question_out:
		for key, value in questions.iteritems():
			question_out.write(key + u"\r\n")
			for k in value.keys():
				question_out.write(k + u"\r\n")
	return None	


def search_for_questions(data, filter_out_emails, start_questions = [u"How", u"Why", u"What", u"Where", u"Is", u"Are", u"Do", u"Does", u"When", u"Did", u"Have", u"Will", u"Had", u"Was", u"Where", u"Shall", u"Would", u"Should", u"Could", u"Who", u"Which", u"Didn't", u"Haven't", u"Hadn't", u"Wouldn't", u"Shouldn't", u"Couldn't", u"Can", u"May", u"Aren't", u"Isn't", u"Weren't", u"Wasn't", u"Cannot", u"Can't", u"Что"]):
	questions = defaultdict(lambda: dict())
	for index in range(data.shape[0]):
		body = str(data.iloc[index].values[-1])
		body = unicode(body, "utf-8")
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
		for m in re.finditer("<\S+@\S+>", message_from):
			message_sender = message_from[m.start() + 1: m.end() - 1]
			break

		for start_question in start_questions:
			for m in re.finditer(start_question +  u"\s.+?\?", body):
				questions[message_sender][body[m.start():m.end()]] = 1
		
		write_questions_to(questions)	
	return questions

def write_questions(questions):
	with io.open("FAQ.csv", "w", encoding="utf-8") as write_questions:
		for client_mail, client_questions in questions.iteritems():
			[write_questions.write(question + u"\r\n") for question in client_questions.keys()]
	return None

def filter_data_by(filter_out_emails, data):
	for email in filter_out_emails:
		if email[0:2] == "*@":
			email = email[1:]
		data = data[~data["from"].str.contains(email)]
	return data

def throw_exception(message):
	print message
	sys.exit()

def retrieve_data_from(filename):
	if not path.isfile(filename):
		throw_exception("Mailbox csv file does not exist!")
	if stat(filename).st_size == 0:
		throw_exception("Mailbox csv file is empty!")
	data = pd.read_csv(filename, sep = ",", header = None)
	if data.shape[1] != 4:
		throw_exception("Mailbox csv file is inccorrect!")
	data.columns = ["subject", "from", "date", "body"]
	return data	
	
def retrieve_filter_out_emails_from(filename):
	if not path.isfile(filename):
		throw_exception("Filter out csv file does not exist!")

	with io.open(filename, "r", encoding="utf-8") as filter_file:
		reader = csv.reader(filter_file, delimiter = ',')
		filter_out_emails = ["".join([word.strip() for word in line]) for line in reader]
	
	return filter_out_emails		

def retrieve_phrases_from(filename):
	phrases = defaultdict(lambda: 0)
					
	if not path.isfile(filename):
		throw_exception("File with predefined phrases does not exist!")

	with io.open(filename, "r", encoding= "utf-8") as phrases_file:
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
