# -*- coding: utf-8 -*-
import re, string, sys, time, csv
from nltk.tag.stanford import NERTagger

# Record start time.
start = time.time()

# Take input file from command line.
input_file = sys.argv[1]

# Set up NER Tagger
st = NERTagger('./stanford-ner-2014-01-04/classifiers/english.all.3class.distsim.crf.ser.gz', './stanford-ner-2014-01-04/stanford-ner.jar')

# Reporting stats
total_count = 0
statement_count = 0

# Setup regex
regex = re.compile('[^\w\s\.]')


def anonymise(content):
  # Clean content
  content = regex.sub(' ', content)

  # Split statement into lines
  no_newline_content = content.replace('\n', '')
  lines = no_newline_content.split('.')

  output = []

  # Iterate through each sentence in the content, finding and replacing PERSONs, LOCATIONs & ORGANISATIONs with generic terms.
  for line in lines:
    if len(line) > 0:
      tokens = line.lstrip().split()
      tagged = st.tag(tokens)
      for i in range(len(tagged)):
        if tagged[i][1] != "O" and tagged[i][0] != 'UK':
            tokens[i] = '*****'
      output.append(' '.join(tokens) + '.')

  return ' '.join(output)


######################
######################

# Prepare file for writing
outloc = open(sys.argv[2], 'w')
outwriter = csv.writer(outloc)
header = [['id', 'anon-statement']]
outwriter.writerows(header)

# Open souce data file
lines = csv.reader(open(input_file, 'rU'))
headers = lines.next()
for line in lines:
  statement = line[52]
  _id = line[0]
  total_count += 1
  if statement != '':
    statement_count += 1
    anonymised_statement = anonymise(statement)
    outwriter.writerows([[_id, anonymised_statement]])
    break

elapsed = (time.time() - start)

print "%d of %d rows had a supporting statement to process." % (statement_count, total_count)
print "Processing took %d seconds to complete." % (elapsed)