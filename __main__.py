import argparse

from movie_recommendation.main import Main

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='movie_recommendation',
        description='',
        epilog='yo'
    )

    parser.add_argument('--fetch', action='store_true')
    parser.add_argument('--list_new', action='store_true')
    parser.add_argument('--list_alt', action='store_true')
    parser.add_argument('--recommend', action='store_true')
    parser.add_argument('--excel', action='store_true')

    args = parser.parse_args()

    main = Main()

    if args.fetch == True:
        main.run_fetch()
        exit()

    if args.list_new == True:
        main.run_list_new()
        exit()
    
    if args.list_alt == True:
        main.run_list_alt()
        exit()

    if args.recommend == True:
        main.run_recommend()

    if args.excel == True:
        main.run_sheets()
        exit()
    
    main.run()

