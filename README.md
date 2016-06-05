# MboxFiltering
File for mbox filtering

For converting mbox to csv(mailbox\_transformer.py) mainly is used script: https://gist.github.com/brianboyer/c9d412a26cb57b5ebbc7

- To start it you need <mailbox>.mbox

Arguments:

```python
python mailbox_transformer.py <input_content>.mbox <result>.csv
```

For filtering (mailbox\_filte.py).

- To use this scripts you need to have already created 
 
```python
<result>.csv
```

Arguments:

```python
python mailbox_filter.py <result>.csv <filter_out_emails>.csv <phrases_in_questions>.csv <phrases_and_occurances>.csv
```

The minimum required arguments:

```python
python mailbox_filter.py <result>.csv <filter_out_emails>.csv
```

Has side-effect automatically will produce FAQ.csv with list of questions now default words are How, Why, What, Where, When and etc.

Can be called with minimum 3 arguments:

```python
python mailbox_filter.py <result>.csv <filter_out_emails>.csv
```

Would extract all questions and produce FAQ.csv file.
