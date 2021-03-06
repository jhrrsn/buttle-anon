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

##################
# Names Database #
##################

filename = "namesdb.dat"
names = []
first_names = []
ok_first = ['charity', 'paying', 'bank', 'morning', 'unborn', 'memory', 'trip', 'even', 'worn', 'fine', 'modest', 'les', 'more', 'mini', 'add', 'driver', 'fare', 'law', 'unknown', 'say', 'loan', 'rusty', 'said', 'harm', 'car', 'story', 'rural', 'down', 'foster', 'rehab', 'every', 'deal', 'shown', 'hope', 'camp', 'read', 'day', 'days', 'meet', 'me', 'you', 'able', 'or', 'argos', 'ever', 'friend', 'trust', 'hose', 'divan', 'low', 'cope', 'share', 'way', 'deep', 'nor', 'via', 'standard', 'general', 'special', 'wash', 'la', 'edas', 'iron', 'church', 'tag', 'park', 'nass', 'real', 'constant', 'mat', 'ward', 'wm', 'english', 'mr', 'ms', 'mrs', 'miss', 'master', 'like', 'case', 'soon', 'hoover', 'many', 'job', 'little', 'white', 'do', 'daily', 'free', 'boy', 'girl', 'male', 'female', 'cash', 'grant', 'the', 'no', 'in', 'access', 'will', 'bunk', 'council', 'be', 'an', 'any', 'future', 'other', 'wa', 'not', 'doe', 'thi', 'baby', 'ha', 'had', 'so', 'son', 'daughter', 'brother', 'sister', 'her', 'him', 'lot', 'than', 'life', 'she', 'he', 'travel', 'set', 'winter', 'summer', 'autumn', 'spring', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'young', 'younger', 'can', 'care', 'heart', 'given', 'west', 'east', 'north', 'south', 'northern', 'southern', 'eastern', 'western', 'born', 'my', 'money', 'per', 'watt', 'normal', 'gates', 'man', 'woman']

# Open names database and add possessive versions of each name
for line in open(filename, 'r'):
    item = line.rstrip() 
    name = item.split(',')[0]
    names.append(name.lower())
    names.append(name.lower() + 's')
    if item.split(',')[4] == '1' and name.lower() not in ok_first:
      first_names.append(name.lower())
      first_names.append(name.lower() + 's')

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
        if words[i].lower() in nes or words[i].lower() in names:
          words[i] = '____'

      processed.append(' '.join(words) + '.')

  return ' '.join(processed)


###############################################
# Define simple name strip anonymise function #
###############################################

def simple_anonymise(content):
  # Split content into lines, strip punctuation.
  content = regex.sub(' ', content)
  lines = content.split('.')

  # Init output list
  processed = []

  # Replace the names in each line with a blank line.
  for line in lines:
    if len(line) != 0:
      words = re.sub("[^\w]", " ",  line).split()
      for i in range(len(words)):
        if words[i].lower() in first_names:
          words[i] = '____'

      processed.append(' '.join(words) + '.')

  return ' '.join(processed)

################
# Process data #
################

# Prepare file for writing
outloc = open(sys.argv[2], 'w')
outwriter = csv.writer(outloc)
header = [['id', 'anon-request', 'anon-statement', 'anon-recommend']]
outwriter.writerows(header)

# Open souce data file
lines = csv.reader(open(input_file, 'rU'))
headers = lines.next()
email_header = '0---------- INCOMING EMAIL MESSAGE ----------0'

# Read through lines and anonymise
for line in lines:
  request = line[51]
  statement = line[52]
  recommend = line[53]
  _id = line[0]
  total_count += 1

  if statement != '':
    statement_count += 1

    if statement_count % 5 == 0:
      elapsed = (time.time() - start)
      print "%d statements processed in %d seconds." % (statement_count, elapsed)
    email_index = statement.find(email_header)
    if email_index >= 0:
      statement = statement[0:email_index]
    
    anonymised_request = simple_anonymise(request)
    anonymised_statement = anonymise(statement)
    anonymised_recommend = simple_anonymise(recommend)
    outwriter.writerows([[_id, anonymised_request, anonymised_statement, anonymised_recommend]])

# Calculate total runtime 
elapsed = (time.time() - start)

# Performance logging
print "%d of %d rows had a supporting statement to process." % (statement_count, total_count)
print "Processing took %d seconds to complete." % (elapsed)