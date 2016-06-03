# MboxFiltering
File for mbox filtering

For converting mbox to csv(mailbox\_transformer.py) mainly is used script: https://gist.github.com/brianboyer/c9d412a26cb57b5ebbc7

- To start it you need <mailbox>.mbox

Arguments:

python mailbox\_transformer.py <input>.mbox <result>.csv

For filtering (mailbox\_filtering.csv).

- To use this scripts you need to have already created <result>.csv

Arguments:

python mailbox\_filtering.py <result>.csv <filter_out_emails>.csv <phrases_in_questions>.csv <phrases_and_occurances>.csv

