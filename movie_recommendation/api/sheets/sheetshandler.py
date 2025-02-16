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
        
    def parse_file_with_movies(self):

        list = ["500 Days of Summer", "8 Mile", "All the Bright Places", "Arrival", "Asteroid City", "Batman Begins", "Blade Runner", "Blade Runner 2049", "Bridge to Terabithia", "Civil War", "Cruella", "Cruella 2", "Deadpool", "Deadpool 2", "Dear Kelly", "Detachment", "District 9", "Downton Abbey 3", "Dream Scenario", "Dune", "Dune - Part Two", "Edge of Tomorrow", "Empire of the Sun", "End of Watch", "Eternal Sunshine of the Spotless Mind", "Everything Everywhere All at Once", "Ex Machina", "Fantastic Mr Fox", "Fight Club", "Finch", "Forgetting Sarah Marshall", "Full Metal Jacket", "Get Smart", "Gone Girl", "Goodfellas", "Groundhog Day", "Guardians of the Galaxy", "Her", "Idiocracy", "Inception", "Interstella 5555 - The 5tory of the 5ecret 5tar 5ystem", "Juno", "Kingdom of Heaven", "Kiss Kiss Bang Bang", "La La Land", "Lars and the Real Girl", "Leatherheads", "Limitless", "Little Miss Sunshine", "Lost in Translation", "Manchester by the Sea", "Me and Earl and the Dying Girl", "Mean Girls", "Mean Girls 2", "Meet Joe Black", "Midnight in Paris", "Moon", "Moonlight", "Moonrise Kingdom", "No Hard Feelings", "Ocean's Eleven", "Office Space", "On the Beach", "On the Beach", "Poor Things", "Predestination", "Ricky Stanicky", "Scott Pilgrim vs the World", "Shaun of the Dead", "Sicario", "Sicario - Day of the Soldado", "Silver Linings Playbook", "Snatch.md", "Southpaw", "Split", "Stuck in Love", "The Accountant", "The Adjustment Bureau", "The Artist", "The Batman", "The Big Sick", "The Darjeeling Limited", "The Dark Knight", "The Dark Knight Rises", "The Fall Guy", "The Fault in Our Stars", "The Fundamentals of Caring", "The Garden of Words", "The Grand Budapest Hotel", "The Hitchhiker's Guide to the Galaxy", "The Imitation Game", "The Intouchables", "The Last King of Scotland", "The Man from UNCLE", "The Mask", "The Matrix", "The Ministry of Ungentlemanly Warfare", "The Naked Gun - From the Files of Police Squad!", "The Peanut Butter Falcon", "The Perks of Being a Wallflower", "The Prestige", "The Revenant", "The Secret Life of Walter Mitty", "The Shape of Water", "The Theory of Everything", "The Truman Show", "Warm Bodies", "Wedding Daze", "Whiplash", "Wildflower", "Your Name", "Zombieland", "Zombieland - Double Tap", "1883", "1923", "2 Broke Girls", "24", "Agents of SHIELD", "Arcane", "Attack on Titan", "Banshee", "Barry", "Big Little Lies", "Black Lagoon", "Boiling Point", "Boston Legal", "Chainsaw Man", "Chimp Empire", "Cyberpunk - Edgerunners", "Death Note", "Designated Survivor", "Detroiters", "Dexter", "Domestic Girlfriend", "Downton Abbey", "Fallout", "Fargo", "Fullmetal Alchemist", "Fullmetal Alchemist - Brotherhood", "Ghost Whisperer", "Hannibal", "Hell's Paradise - Jigokuraku", "Initial D - First Stage", "Invincible", "Jujutsu Kaisen", "K-On!", "Kidou Senshi Gundam - Tekketsu no Orphans - Urdr Hunt", "Kimetsu no Yaiba", "Legion", "Letterkenny", "Loudermilk", "Lucifer", "Masters of the Air", "Misfits", "Normal People", "Only Murders in the Building", "Preacher", "Sex Education", "Shogun", "Shrinking", "Smiling Friends", "Summer Time Rendering", "Sweetpea", "The Americans", "The Bear", "The Big Lez Show", "The Boondocks", "The Great", "The Midnight Gospel", "The Rookie", "Tokyo Vice", "Twilight of the Gods", "Veronica Mars", "Victoria", "Wayne", "We Own This City", "Yellowjackets", "Yellowstone"]

        for i in list:
            self.push_data(i)


    def push_data(self, movie_name):
        now = datetime.now()
        today = now.strftime("%y-%m-%d %H:%M:%S")

        json_obj = self.omdbh.get_movie_json(movie_name.strip())
        
        if json_obj == None:
            return
        
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









