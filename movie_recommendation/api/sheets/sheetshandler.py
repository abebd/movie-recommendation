import gspread
from datetime import datetime
from movie_recommendation.util import get_secret, remove_files_in_folder, log
from movie_recommendation.media.moviehandler import MovieHandler
from movie_recommendation.api.chatbot.chatbothandler import ChatBotHandler
from movie_recommendation.api.omdb.omdbhandler import OmdbHandler
from omdbapi.movie_search import GetMovie # type: ignore

"""
svc_key_path = '../../../etc/secrets/valiant-circuit-446922-c0-143cdfb24d99.json'

gc = gspread.service_account(svc_key_path)

wb_id = '1VlTR1VYOZvllgOa6i5XakkG9RtzG1JzfTRt3iTSIAXg'
ws_name = "import"

wb = gc.open_by_key(wb_id)
ws = wb.worksheet(ws_name)
"""
class SheetsHandler():

    def __init__(self):
        self.omdbh = OmdbHandler()

        self.wb_id = '1VlTR1VYOZvllgOa6i5XakkG9RtzG1JzfTRt3iTSIAXg'
        self.ws_name = 'import'
        
        self.gc = gspread.service_account('etc/secrets/svc-acc01.key')
        self.wb = self.gc.open_by_key(self.wb_id)
        self.ws = self.wb.worksheet(self.ws_name)


    def get_max_id(self):

        # max id will always be in row 2 col 1
        return int(self.ws.cell(2,1).value)
        


    def push_data(self):
        now = datetime.now()
        today = now.strftime("%y-%m-%d %H:%M:%S")

        user_input = input("Movie id?")
        json_obj = self.omdbh.get_movie_json(user_input)
        keys = list(json_obj.keys())
        values = list(json_obj.values())

        # append extra columns
        curr_max_id = self.get_max_id()
        keys = ["d_id", "d_timestamp"] + keys
        values = [curr_max_id + 1, today] + values

        # cleanup
        i = 0
        while i < len(keys):
            if keys[i] == 'ratings':
                values[i] = '' # make it empty for now
            
            i += 1


        self.ws.insert_row(values, index=2)  # Inserts the values at the top (row 1)
        #self.ws.insert_row(keys, index=1)  # Inserts the values at the top (row 1)
        print(f'inserted {values}')









