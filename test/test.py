from tabulate import tabulate

movies = []
movie = []

attributes_wanted = ['title', 'year', 'url', 'plot', 'onlineRating']
lines = ['Gone Girl', '2014', "With his wife's disappearance having become the focus of an intense media circus, a man sees the spotlight turned on him when it's suspected that he may not be innocent.", '8.1', 'https://www.imdb.com/title/tt2267998']

for line in lines:

    if len(line) > 50:
        index = 0
        
        while len(line) > index:

            line = line[:index] + '\n' + line[index:]

            index+=50


    movie.append(line)
movies.append(movie)

print(tabulate(movies, headers=attributes_wanted))