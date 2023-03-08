import sqlite3
import pandas as pd
import pyttsx3
import sys

from src.prediction import predict
from src.exception import equip9_Exception


class QueryGenerator:
    def __init__(self, text, not_req, req, eqp, loc, Qty):
        self.text = text
        self.not_req = not_req
        self.req = req
        self.eqp = eqp
        self.loc = loc
        self.Qty = Qty
        self.spoken_words = text.split()


    def generate_query(self):

        '''It will be used to generate query using words spoken by user'''

        try:
            # take only required words from spoken words
            req_words = [word for word in self.spoken_words if word not in self.not_req]

            # take only words which are required for query generator
            final_words = [word for word in req_words if word in self.req]

            # replace words with words which are available in database
            final_words = [word.replace('cranes', 'crane').replace('crains', 'crane').replace("trains","crane").replace("jcb's", "jcb").
                                replace('jcbs','jcb').replace('rollers','roller').replace('bulldozers','bulldozer').
                                replace('excavators','excavator') for word in final_words]

            # select all equipments name
            lst = []
            for i in final_words:
                if i in self.eqp:
                    lst.append(i)
            
            # if equipment name is not present in above list then, it will use predict function to 
            # predict equipment name from spoken words and append it into final words list.
            if len(lst) == 0:
                not_spoken_well = []
                for i in req_words:
                    if i not in self.eqp and i not in self.req:
                        not_spoken_well.append(i)
                final_words = predict(final_words, not_spoken_well)

            # replace prdicted equipment names with names present in our database    
            final_words = [word.replace('cranes', 'crane').replace('crains', 'crane').replace("trains","crane").replace("jcb's", "jcb").
                                replace('jcbs','jcb').replace('rollers','roller').replace('bulldozers','bulldozer').
                                replace('excavators','excavator') for word in final_words]
            
            # replace string quantity with integer
            mapping = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7,
                        'eight': 8, 'nine': 9, 'ten': 10, '1' : 1, '2' : 2,'3' : 3, '4' : 4, '5' : 5,
                        '6' : 6, '7' : 7, '8' : 8, '9' : 9, '10' : 10}
            
            # replace string quantity with integer and append into query words  
            query_words = []
            for x in final_words:
                try:
                    query_words.append(mapping[x])
                except:
                    query_words.append(x)

            # basic query
            query = 'SELECT * FROM my_table WHERE equipment_name ='

            # if equipment name is present in query words then add it into query
            for i in query_words:
                if i in self.eqp:
                    lst.append(i)
                    query = query + ' ' +f'"{i}"'
                    break
            
            # if location is present in query words then add it into query
            for i in query_words:
                if i in self.loc:
                    query = query + ' ' + 'AND location =' + ' ' + f'"{i}"'
                    break
                else:
                    query = query
            
            # if quantity is present in query words then add it into query
            for i in query_words:
                if i in self.Qty:
                    query = query + ' ' + 'ORDER BY equipment_id LIMIT'+' '+f'{i+1}'
                else:
                    query = query
                    break
            
            else:
                pass

            print(query)
            
            # connect to database
            conn = sqlite3.connect('my_database.db')
            cursor = conn.cursor()

            # execute query
            rows = cursor.execute(query)

            # if query is not executed then mode will say below sentence
            if rows.fetchone() is None:
                # Initialize the engine
                engine = pyttsx3.init()

                # Convert text to speech
                text = "Sorry, please say again."
                engine.say(text)

                # Speak the text
                engine.runAndWait()

            # print all rows which are fetched by query
            for row in rows:
                print(row)

            conn.close()

        except  Exception as e:
                raise  equip9_Exception(e,sys)