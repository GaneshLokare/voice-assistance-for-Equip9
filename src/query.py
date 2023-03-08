import sqlite3
import pandas as pd
import pyttsx3

from src.prediction import predict


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

        req_words = [word for word in self.spoken_words if word not in self.not_req]
        final_words = [word for word in req_words if word in self.req]

        final_words = [word.replace('cranes', 'crane').replace('crains', 'crane').replace("trains","crane").replace("jcb's", "jcb").
                            replace('jcbs','jcb').replace('rollers','roller').replace('bulldozers','bulldozer').
                            replace('excavators','excavator') for word in final_words]

        lst = []
        for i in final_words:
            if i in self.eqp:
                lst.append(i)
        
        if len(lst) == 0:
            not_spoken_well = []
            for i in req_words:
                if i not in self.eqp and i not in self.req:
                    not_spoken_well.append(i)
            final_words = predict(final_words, not_spoken_well)
            
        final_words = [word.replace('cranes', 'crane').replace('crains', 'crane').replace("trains","crane").replace("jcb's", "jcb").
                            replace('jcbs','jcb').replace('rollers','roller').replace('bulldozers','bulldozer').
                            replace('excavators','excavator') for word in final_words]


        query = 'SELECT * FROM my_table WHERE equipment_name ='
        for i in final_words:
            if i in self.eqp:
                lst.append(i)
                query = query + ' ' +f'"{i}"'
        

        for i in final_words:
            if i in self.loc:
                query = query + ' ' + 'AND location =' + ' ' + f'"{i}"'

        for i in final_words:
            if i in self.Qty:
                query = query + ' ' + 'ORDER BY equipment_id LIMIT'+' '+f'{i}'
            else:
                query = query
        
        else:
            pass
        print(query)
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()

    
        rows = cursor.execute(query)

        if rows.fetchone() is None:
            # Initialize the engine
            engine = pyttsx3.init()

            # Convert text to speech
            text = "Sorry, please say again."
            engine.say(text)

            # Speak the text
            engine.runAndWait()

        for row in rows:
            print(row)

        conn.close()

       