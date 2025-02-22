class InputHandler():

    def __init__(self, main):
        self.last_user_input = ''
        self.valid_commands = {
            'help': '',
            'h': '',
            'get new': 'Fetches more recommended movies',
            'list new': '',
            'list old': '',
            'list random': '',
            'exit': '',
            'quit': '',
        }

        self.main = main


    def get_input(self, prompt='$ '):

        self.last_user_input = input(prompt)
        
        return self.last_user_input
    

    def handle_input(self):

        if self.last_user_input not in self.valid_commands.keys():
            print(f"'{self.last_user_input}' is not a valid command, please use 'h' or 'help'")
            return

        if 'help' == self.last_user_input \
        or 'h' == self.last_user_input:
            self.print_help()
            return
        
        if 'get new' == self.last_user_input:
            self.main.get_movie_recomentations()
            return

        if 'list new' == self.last_user_input:
            self.main.list_movies(type='new')

        if 'list old' == self.last_user_input:
            self.main.list_movies(type='old')

        if 'list random' == self.last_user_input:
            self.main.list_movies(type='five random')

        if 'exit' == self.last_user_input \
        or 'quit' == self.last_user_input:
            exit()
            

    def print_help(self):

        print('Listing availible commands...')

        for val in self.valid_commands:
            print("  > " + val)

