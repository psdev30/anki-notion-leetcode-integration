import os
import sys
from dotenv import load_dotenv
from functions import *
import requests

load_dotenv()
 

print(f"Command-line arguments: {sys.argv}")
if len(sys.argv) != 2:
    print("Usage: python script.py <Leetcode Question Name>")
    print(sys.argv)
    sys.exit(1)


problem_title = sys.argv[1]
print(f"Argument 1: {problem_title}")
deck_name = "Leetcode"
anki_card_id = find_card(deck_name=deck_name, problem_title=problem_title)["result"][0]
find_next_review_date(anki_card_id=anki_card_id)
# problem_id = find_notion_problem_id(problem_title=problem_title)
# update_notion_problem_entry(problem_id=problem_id, anki_card_id=anki_card_id, next_review_date="2024-03-04")
