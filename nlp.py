# -*- coding: utf-8 -*-

from nltk.tag.stanford import NERTagger

# Set up NER Tagger
st = NERTagger('./stanford-ner-2014-01-04/classifiers/english.all.3class.distsim.crf.ser.gz', './stanford-ner-2014-01-04/stanford-ner.jar')

# Sample content
content = ""

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
        if tagged[i][1] == 'PERSON':
          if tagged[i][0][0:3] not in people:
            people.append(tagged[i][0][0:3])
          tokens[i] = 'PERSON_' + str(people.index(tagged[i][0][0:3]))
        else:    
          tokens[i] = tagged[i][1]
    print ' '.join(tokens) + '.'