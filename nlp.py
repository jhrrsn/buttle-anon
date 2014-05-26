# -*- coding: utf-8 -*-
import sys, csv
from nltk.tag.stanford import NERTagger

# Take input file from command line.
input_file = sys.argv[1]

# Set up NER Tagger
st = NERTagger('./stanford-ner-2014-01-04/classifiers/english.all.3class.distsim.crf.ser.gz', './stanford-ner-2014-01-04/stanford-ner.jar')

# Reporting stats
total_count = 0
statement_count = 0

def anonymise(content):
  # Clean content
  exclude = set(['!', '#', '"', '%', '$', "'", '&', ')', '(', '+', '*', '-', ';', ':', '=', '<', '?', '>', '@', '[', ']', '\\', '_', '^', '`', '{', '}', '|', '~'])
  content = ''.join(ch for ch in content if ch not in exclude)
  content = content.replace('’', '')

  # Split statement into lines
  no_newline_content = content.replace('\n', '')
  lines = no_newline_content.split('.')

  people = []

  # Iterate through each sentence in the content, finding and replacing PERSONs, LOCATIONs & ORGANISATIONs with generic terms.
  for line in lines:
    if len(line) > 0:
      tokens = line.lstrip().split()
      tagged = st.tag(tokens)
      for i in range(len(tagged)):
        if tagged[i][1] != "O" and tagged[i][0] != 'UK':
            tokens[i] = '*****'
      print ' '.join(tokens) + '.'

# Open CSV file
lines = csv.reader(open(input_file, 'rU'))
headers = lines.next()
for line in lines:
  statement = line[52]
  total_count += 1
  if statement != '':
    statement_count += 1
    anonymise(statement)

print "%d of %d rows had a statement." % (statement_count, total_count)