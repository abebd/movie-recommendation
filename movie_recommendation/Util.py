import os

from datetime import datetime
import sys

def get_secret(file_name="api.key"):
    # Used to read an api

    with open(f'etc/secrets/{file_name}', 'r') as file: # TODO replace with value from .properties
    
        return file.readline()
    
def get_current_timestamp():
    now = datetime.now()
    date = now.strftime("%y-%m-%d")
    time = now.strftime('%H:%M:%S')

    return f'{date} {time}'    

def remove_files_in_folder(folder_path):

    if not os.path.exists(folder_path):
        
        print(f'could not find folder {folder_path}')
        return

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:

            if os.path.isfile(file_path) or os.path.islink(file_path):
                
                os.unlink(file_path)
        except Exception as e:

            print('issue {e}')
            
            
def log(log_path, message):

    if not os.path.exists(log_path):
        err = f'unable to find path {log_path}'
        raise(err)

    index = _get_last_line_index(log_path) + 1

    today = get_current_timestamp()
    date, time = today.split(' ')
    line = f'{str(index)}, {date}, {time}, {message}'

    with open(log_path, 'a') as file:
        file.write(f'{line}\n')


def _get_last_line_index(file_path):
    
    with open(file_path, 'rb') as f:
        
        try:  # catch OSError in case of a one line file 
            f.seek(-2, os.SEEK_END)
            
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
        
        except OSError:
            f.seek(0)

        last_line = f.readline().decode()
        #print(last_line)

        if last_line != '':
            last_line = last_line.split(', ')
            #print(last_line)
            return int(last_line[0])
        
        return 0
    


def get_time_delta(timestamp):
    d1 = datetime.strptime(get_current_timestamp(), "%y-%m-%d %H:%M:%S")
    d2 = datetime.strptime(timestamp, "%y-%m-%d %H:%M:%S")

    delta = d1 - d2
    
    if delta.days != 0:
        return f'about {delta.days} day(s)'

    hours = 0
    seconds = delta.seconds
    while seconds > 3600:
        hours += 1
        seconds -= 3600

    if delta.seconds > 3600:
        return f'about {hours} hour(s)'

    return 'few minutes'

def create_hyperlink(label, url):

    parameters = ''

    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'
    return escape_mask.format(parameters, url, label)


def shorten_string(string, max_width=39):

    if len(string) > max_width:
        index = 0
        
        while len(string) > index:
            
            string = string[:index] + '\n' + string[index:]

            index+=max_width


    return string


def validate_path(path):

    if not os.path.exists(path):
        
        print(f'<<< could not find folder {path}, quitting >>>')
        exit()

    return path


    