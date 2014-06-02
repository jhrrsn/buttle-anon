# -*- coding: utf-8 -*-
import sys, time, re, csv, nltk


#########
# Setup #
#########

# Record start time.
start = time.time()

# Take input file from command line.
input_file = sys.argv[1]

# Reporting stats
total_count = 0
statement_count = 0

# Setup regex
regex = re.compile('[^\w\s\.]')


#############################
# Define anonymise function #
#############################

def anonymise(content):
  # Split content into lines, strip punctuation.
  content = regex.sub(' ', content)
  lines = content.split('.')
  
  # List of named entities in string.
  nes = []

  # Init output list
  processed = []

  # Search through the lines for NEs
  for line in lines:
    tokens = nltk.word_tokenize(line)
    pos_tags = nltk.pos_tag(tokens)
    sentences = nltk.ne_chunk(pos_tags)

    output = []

    for i in range(len(sentences)):
      if type(sentences[i]) == nltk.tree.Tree:
        if type(sentences[i][0][0]) == str and sentences[i][0][0].lower() not in nes:
          nes.append(sentences[i][0][0].lower())
      elif sentences[i][0].lower() in ['mr', 'mrs', 'ms', 'miss', 'master']:
        if i+1 < len(sentences):
          if type(sentences[i+1][0]) == str and sentences[i+1][0].lower() not in nes:
            nes.append(sentences[i+1][0].lower())

  # Replace the NEs in each line with a blank line.
  for line in lines:
    if len(line) != 0:
      words = re.sub("[^\w]", " ",  line).split()
      for i in range(len(words)):
        if words[i].lower() in nes:
          words[i] = '____'

      processed.append(' '.join(words) + '.')

  return ' '.join(processed)


################
# Process data #
################

# Prepare file for writing
outloc = open(sys.argv[2], 'w')
outwriter = csv.writer(outloc)
header = [['id', 'anon-statement']]
outwriter.writerows(header)

# Open souce data file
lines = csv.reader(open(input_file, 'rU'))
headers = lines.next()
email_header = '0---------- INCOMING EMAIL MESSAGE ----------0'
for line in lines:
  statement = line[52]
  _id = line[0]
  total_count += 1
  if statement != '':
    statement_count += 1
    email_index = statement.find(email_header)
    if email_index >= 0:
      statement = statement[0:email_index]
    anonymised_statement = anonymise(statement)
    outwriter.writerows([[_id, anonymised_statement]])

elapsed = (time.time() - start)

print "%d of %d rows had a supporting statement to process." % (statement_count, total_count)
print "Processing took %d seconds to complete." % (elapsed)