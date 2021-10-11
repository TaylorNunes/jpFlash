from bs4 import BeautifulSoup
import requests 
import urllib.request
import json
from ac_functions import invoke, request
from db_functions import make_db, check_table, make_table, insert_row, get_values

main_url = 'https://jlptsensei.com/jlpt-n3-grammar-list/page/5/'
main_response = requests.get(main_url)
main_soup = BeautifulSoup(main_response.text, 'html.parser')

deck_name = 'Japanese Grammar'
note_type = 'Japanese Grammar'
table_name = "vocab"

# Makes the db
conn = make_db()
curr = conn.cursor()

if check_table(curr, table_name):
  print("Using table {0}".format(table_name))
  curr.execute("DROP TABLE {0}".format(table_name))
  make_table(curr, table_name)
else:
  print("Making table {0}".format(table_name))
  make_table(curr, table_name)

# Gets the html for the list of grammar points and saves to db
grammar_row = main_soup.find_all('tr','jl-row')
print(len(grammar_row))
for irow in range(len(grammar_row)):
    ex_num = 1
    link = grammar_row[irow].find_all('a','jl-link')
    sub_url = link[0]['href']
    sub_response = requests.get(sub_url)
    sub_soup = BeautifulSoup(sub_response.text, 'html.parser') 

    grammar_point = sub_soup.find_all('span','d-block p-3 text-centeret-gram')[0].find_all('span')[0].get_text()
    jap_sentence = sub_soup.find_all('p','m-0 jp')[ex_num].get_text()
    eng_sentence = sub_soup.find_all('div','alert alert-primary')[ex_num].get_text()

    insert_row(curr, table_name, ("jlptsensei_g3",jap_sentence,eng_sentence,grammar_point))

# Gets cards from db and puts them into anki via anki connect
card_list = get_values(curr, table_name, "jlptsensei_g3")
for card in card_list:
    
    jap_sentence_c = card[2]
    eng_sentence_c = card[4]
    grammar_point_c = card[5]
    
    note_id = invoke('findNotes',**{'query':jap_sentence_c})

    if len(note_id) > 1:
        print("Error: There is more than one note with with this sentence. Skipping")
        continue
    
    note = {'note':{'fields':{'Expression':jap_sentence_c,'Meaning':eng_sentence_c,'Target':grammar_point_c}}}

    if len(note_id)==0:     
        note['note']['deckName'] = deck_name
        note['note']['modelName'] = note_type
        invoke("addNote", **note)   
    else:
        note['note']['id'] = note_id[0]
        invoke("updateNoteFields", **note) 








