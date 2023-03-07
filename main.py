from src.speech_to_text import SpeechRecognition
from src.query import QueryGenerator
from src.constants import not_req, req, eqp, loc, Qty
import os


# call the recognize_speech method on the instance
text = SpeechRecognition().recognize_speech()

query_gen = QueryGenerator(text, not_req, req, eqp, loc)
result = query_gen.generate_query()


folder_path = "pred"

# Get list of all files in the folder
files = os.listdir(folder_path)

# Iterate over each file and delete it
for file in files:
    file_path = os.path.join(folder_path, file)
    os.remove(file_path)
    
        