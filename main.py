from code import QueensSolver, QueensGUI, LinkedInScrapper
from dotenv import load_dotenv
import os


if __name__ == '__main__':
    '''
    load data from txt file 
    '''
    path_to_level = 'data/93.txt'

    with open(path_to_level, 'r') as lvl_file:
        level_grid = [line.strip().split() for line in lvl_file.readlines()]


    '''
    scrape data from linkedin
    '''
    # load env variables
    # load_dotenv()
    # email = os.getenv('EMAIL')
    # password = os.getenv('PASSWORD')

    # colors = ['v','g','r','o','b','p','y', 't']

    # scrape data from linkedin 
    # scr = LinkedInScrapper()
    # gameboard_colors_in_sequence = scr.scrape(
    #     url='https://www.linkedin.com/games/queens/', 
    #     username=email, password=password, 
    #     class_name='scaffold-layout__main'
    # )

    # transforms data to NxN color grid
    # gameboard_colors_in_sequence = [colors[num] for num in gameboard_colors_in_sequence]
    # n = int(len(gameboard_colors_in_sequence) ** (1/2))
    # level_grid = [gameboard_colors_in_sequence[i * n:(i + 1) * n] for i in range(n)]
   
    
    '''
    solve gameboard and visualize gameboard
    '''
    solver = QueensSolver()
    queens_position = solver.solve(level_grid)

    q = QueensGUI(level_grid, queens_position)
    q.main()

     