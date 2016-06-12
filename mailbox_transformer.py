#!/usr/bin.python
# -*- coding: utf-8 -*- 

# Assumes your file is called mbox (which it is if you export from Mac Mail)
# writes to a file called mbox.csv

import mailbox
import csv
import sys


from mailbox_filter import throw_exception
# motherfucking recursion, because email is damn weird.
# each payload can contain many other payloads, which can contain many *other* payloads
# this only exports the text/plain payload, the thing you read
def more_payloads(message):
	body = ""
	if message.is_multipart():
		for payload in message.get_payload():
			body += more_payloads(payload)
	else:
		if message.get_content_type() == 'text/plain':
			body = message.get_payload(decode=True)
	return body

def main():
	# sys.argv[1] = "mbox.csv"
	# sys.argv[2] = "sample.mbox"
	if len(sys.argv) >= 3:
		with open(sys.argv[2], "wb") as outfile:
			writer = csv.writer(outfile)
			for message in mailbox.mbox(sys.argv[1]):
				body = more_payloads(message)
				writer.writerow([message['subject'], message['from'], message['date'], body])
	else:
		throw_exception("Not enough input parameters! Proper call should look:  python mailbox_transformer.py <file>.mbox <file>.csv")
	return None

if __name__ == "__main__":
	main()
