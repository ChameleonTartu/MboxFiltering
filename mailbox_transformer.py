# Assumes your file is called mbox (which it is if you export from Mac Mail)
# writes to a file called mbox.csv

import mailbox
import csv

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

with open("mbox.csv", "w") as outfile:
	writer = csv.writer(outfile)
	for message in mailbox.mbox('sample.mbox'):
		body = more_payloads(message)
		writer.writerow([message['subject'], message['from'], message['date'], body])
