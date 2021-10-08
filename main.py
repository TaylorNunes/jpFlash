from bs4 import BeautifulSoup
import requests 
import urllib.request
import json

main_url = 'https://jlptsensei.com/jlpt-n3-grammar-list/page/5/'
main_response = requests.get(main_url)
main_soup = BeautifulSoup(main_response.text, 'html.parser')

deck_name = 'Japanese Grammar'
note_type = 'Japanese Grammar'

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

# Connecting to AnkiConnect 
def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        print(response['error'])
    return response['result']

# Gets the html for the list of grammar points 
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

    print(jap_sentence)

    note_id = invoke('findNotes',**{'query':jap_sentence})

    if len(note_id) > 1:
        print("Error: There is more than one note with with this sentence. Skipping")
        continue
    
    note = {'note':{'fields':{'Expression':jap_sentence,'Meaning':eng_sentence,'Target':grammar_point}}}

    if len(note_id)==0:     
        note['note']['deckName'] = deck_name
        note['note']['modelName'] = note_type
        invoke("addNote", **note)   
    else:
        note['note']['id'] = note_id[0]
        invoke("updateNoteFields", **note) 


