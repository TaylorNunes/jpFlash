from bs4 import BeautifulSoup
import requests 
import urllib.request
import json
from ac_functions import invoke, request
from db_functions import make_db, check_table, make_table, insert_row, get_values


conn = make_db()
cur = conn.cursor()
table_name = "vocab"
source_urls = {
  "n1":"https://jlptsensei.com/jlpt-n1-grammar-list/",
  "n2":"https://jlptsensei.com/jlpt-n2-grammar-list/",
  "n3":"https://jlptsensei.com/jlpt-n3-grammar-list/",
  "n4":"https://jlptsensei.com/jlpt-n4-grammar-list/",
  "n5":"https://jlptsensei.com/jlpt-n5-grammar-list/"
}


while True:
  command = input("\nEnter a command ('h' for options): ")

  if command == "h":
    print("h - print the list of command")
    print("q - quit the program")
    print("d - make the vocab table")
    print("s - scrape the data from jlpt sensei")
    print("c - make cards from the database")
  
  elif command == "q":
    break
  
  elif command == "d":
    # Makes the db
    if check_table(cur, table_name):
      print("Table exists. Using table {0}".format(table_name))
    else:
      print("Making table {0}".format(table_name))
      make_table(cur, table_name)

  # Gets the html for the list of grammar points and saves to db
  elif command == "s":
    user_level = input("Enter a level (n1-n5):")
    first_url = source_urls[user_level]
    
    # Get all additional pages 
    fu_response = requests.get(first_url)
    fu_soup = BeautifulSoup(fu_response.text, 'html.parser')
    soup_url_list_both = fu_soup.find_all("a", class_=lambda x: x == "page-numbers")
    soup_url_list = []
    for tag in soup_url_list_both:
      if 'next' not in tag.attrs['class']:
         soup_url_list.append(tag)
    
    url_list = []
    url_list.append(first_url)
    for iurl in range(len(soup_url_list)):
      url_list.append(soup_url_list[iurl]['href'])
    
    page_num = 0
    for main_url in url_list:
      page_num += 1 
      main_response = requests.get(main_url)
      main_soup = BeautifulSoup(main_response.text, 'html.parser')
      grammar_row = main_soup.find_all('tr','jl-row')
      print("There are {0} grammar points on page {1}".format(len(grammar_row),page_num) )
      for irow in range(len(grammar_row)):
          ex_num = 1
          link = grammar_row[irow].find_all('a','jl-link')
          sub_url = link[0]['href']
          sub_response = requests.get(sub_url)
          sub_soup = BeautifulSoup(sub_response.text, 'html.parser') 

          grammar_point = sub_soup.find_all('span','d-block p-3 text-centeret-gram')[0].find_all('span')[0].get_text()
          jap_sentence = sub_soup.find_all('p','m-0 jp')[ex_num].get_text()
          eng_sentence = sub_soup.find_all('div','alert alert-primary')[ex_num].get_text()

          insert_row(cur, table_name, ("jlptsensei_g{0}".format(user_level),jap_sentence,eng_sentence,grammar_point,sub_url))
    conn.commit()

  # Gets cards from db and puts them into anki via anki connect
  elif command == "c":
    user_level = input("Enter a level (n1-n5):")
    note_type = 'Japanese Grammar'
    deck_name = 'Japanese Grammar::{0}'.format(user_level)
    card_list = get_values(cur, table_name, "jlptsensei_g{0}".format(user_level))
    for card in card_list:
        
        jap_sentence_c = card[2]
        eng_sentence_c = card[4]
        grammar_point_c = card[5]
        link = card[8]
        
        note_id = invoke('findNotes',**{'query':jap_sentence_c})

        if len(note_id) > 1:
            print("Error: There is more than one note with with this sentence. Skipping")
            continue
        
        note = {'note':{'fields':{'Expression':jap_sentence_c,'Meaning':eng_sentence_c,'Target':grammar_point_c,'URL':link}}}

        if len(note_id)==0:     
            note['note']['deckName'] = deck_name
            note['note']['modelName'] = note_type
            invoke("addNote", **note)   
        else:
            note['note']['id'] = note_id[0]
            invoke("updateNoteFields", **note) 








