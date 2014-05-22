# -*- coding: utf-8 -*-

from nltk.tag.stanford import NERTagger

# Set up NER Tagger
st = NERTagger('/Users/jeharrison/Downloads/stanford-ner-2014-01-04/classifiers/english.all.3class.distsim.crf.ser.gz', '/Users/jeharrison/Downloads/stanford-ner-2014-01-04/stanford-ner.jar')

# Sample content
content = """Ali is a young unaccompanied minor who arrived in the UK from Afghanistan in February 2009. He had been travelling with his brother but they had become separated and Ali ended up travelling here on his own. The separation from his brother was very traumatic for Ali and this has affected his mental health. As Ali was only 15 years old when he arrived he was accommodated in a Children’s Unit until he moved to Branston Court on 05/02/10.

          Since he came to Branston Court he has received support and advice regarding managing his tenancy (housework, door control, grocery shopping, cooking, paying bills, adhering to occupancy agreement), finances, physical and emotional health, education and legal matters.
          Ali attends Anniesland College where his main subject of study is English; his language skills have improved vastly since he arrived in 2009 and he has integrated well into life in Scotland.

          Ali has not had any new clothing for approximately a year and is in need of a winter jacket, trousers, shoes, shirt, socks, pyjamas and underwear. He cannot afford to purchase these on his current income as he requires to pay £8 fuel, £20 plus on groceries, £5 and £15 on bus fares and £12 on lunches at college each week.
          Ali would greatly appreciate a grant to purchase new clothing as he is short of appropriate clothing for the inclement weather and he would no longer need to wear his clothes for the Mosque as pyjamas."""

exclude = set(['!', '#', '"', '%', '$', "'", '&', ')', '(', '+', '*', '-', ';', ':', '=', '<', '?', '>', '@', '[', ']', '\\', '_', '^', '`', '{', '}', '|', '~'])
content = ''.join(ch for ch in content if ch not in exclude)
content = content.replace('’', '')

# Split statement into lines
no_newline_content = content.replace('\n', '')
lines = no_newline_content.split('.')

people = []

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