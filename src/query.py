import sqlite3
import pandas as pd

from src.prediction import predict


class QueryGenerator:
    def __init__(self, text, not_req, req, eqp, loc):
        self.text = text
        self.not_req = not_req
        self.req = req
        self.eqp = eqp
        self.loc = loc
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
            

        query = 'SELECT * FROM my_table WHERE equipment_name ='
        for i in final_words:
            if i in self.eqp:
                lst.append(i)
                query = query + ' ' +f'"{i}"'
        print(query)

        for i in final_words:
            if i in self.loc:
                query = query + ' ' + 'AND location =' + ' ' + f'"{i}"'

        print(query)
        conn = sqlite3.connect('my_database.db')
        df = pd.read_sql_query(query, conn)
        print(df.head(10))
        conn.close()
