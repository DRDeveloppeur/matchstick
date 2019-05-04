#! /usr/bin/env python3

import sys
import re

if len(sys.argv) == 3 and int(sys.argv[1]) < 100 and int(sys.argv[1]) > 1 and int(sys.argv[2]) > 0:
    nbr_col = int(sys.argv[1])
    max_rm = int(sys.argv[2])
    nbr_space = nbr_col
    nbr_rm = 0
    nbr_stick = 0
    player = 1
    win = 0
    lin = 0
    col = []
    n = 0
    
    # Create initial pyramide
    while nbr_space != 0:
        col = col + [list("*" + (" " * (nbr_space-1)) + ("|" * ((nbr_col+1) - (nbr_space)) ) + ("|" * (nbr_col - (nbr_space)) ) + (" " * (nbr_space-1)) + "*")]
        n = n+1
        nbr_space = nbr_space-1
    
    # Print pyramide
    def show_game():
        print("*" * ((nbr_col*2)+1))    
        for array in col:
            print(''.join(map(str, array)))
        print("*" * ((nbr_col*2)+1))
    
    # Remove sticks
    def remove_stick(lign, rm):
        lign = int(lign)
        rm = int(rm)
        lign = lign - 1
        last = -1
        while col[lign][last] != "|":
            last = last - 1
        while rm != 0:
            col[lign][last] = ' '
            rm = rm - 1
            last = last - 1

    def player_one():
        global nbr_rm
        global lin
        global win
        global player
        global max_rm
        global nbr_stick
        nbr_stick_lin = 0
        nbr_stick = 0
       
        print('Your turn:')
        lin = input('Line:')
        try:
            lin = int(lin)
        except:
            print('Error: invalid input (positive number expected)')
            player_one()
        if len(col) < lin or lin < 1:
            print('Error: this line is out of range')
            player_one()

        for array in col[lin-1]:
            if array == '|':
                nbr_stick_lin = nbr_stick_lin + 1
        
        nbr_rm = input('Matches:')
        try:
            nbr_rm = int(nbr_rm)
        except:
            print('Error: invalid input (positive number expected)')
            player_one()
        if nbr_rm < 1:
            print('Error: you have to remove at least one match')
            player_one()
        if nbr_rm > nbr_stick_lin:
            print('Error: not enough matches on this line')
            player_one()
        if nbr_rm > max_rm:
            print('Error: you cannot remove more than ' + str(max_rm) + ' matches per turn')
            player_one()

        print('Player removed ' + str(nbr_rm) + ' match(es) from line ' + str(lin))
        remove_stick(lin, nbr_rm)
        show_game()
        for array in col:
            if '|' in array:
                nbr_stick = nbr_stick + 1
        if nbr_stick > 0:
            player = 2
            Ai()
        else:
            print('AI\'s turn...')
            print('You lost, too bad...')
            sys.exit()

    def win_lose():
        global nbr_stick
        nbr_stick = 0
        
        for array in col:
            if '|' in array:
                nbr_stick = nbr_stick + 1
        if nbr_stick == 0:
            print('I lost... snif... but I\'ll get you next time!!')
            sys.exit()

    def action(idx, nbr_rm):
        remove_stick(idx+1, nbr_rm)
        player = 1
        print('AI removed ' + str(nbr_rm) + ' match(es) from line ' + str(idx+1))
        show_game()
        win_lose()
        player_one()


    def Ai():
        global player
        global nbr_rm
        nbr_stick_lin = 0
        nbr_stick = 0
        this_line = 0
        nbr_rm = 0

        print('AI\'s turn...')
        for array in col:
            for item in array:
                if '|' in item:
                    nbr_stick = nbr_stick + 1
        
        for idx, array in enumerate(col):
            nbr_stick_lin = 0
            for line in array:
                if line == '|':
                    nbr_stick_lin = nbr_stick_lin + 1
            if nbr_stick > nbr_stick_lin:
                if nbr_stick_lin == 1 and nbr_stick > (max_rm+2):
                    nbr_rm = 1
                    action(idx, nbr_rm)
                if nbr_stick_lin > 1:
                    if nbr_stick == (max_rm*2)+2 and (nbr_stick-1) != nbr_stick:
                        nbr_rm = max_rm
                        action(idx, nbr_rm)
                    if nbr_stick_lin <= (max_rm) and (nbr_stick_lin+1) == nbr_stick:
                        nbr_rm = max_rm
                        while (nbr_stick_lin-nbr_rm) != 0:
                            nbr_rm = nbr_rm - 1
                        if (nbr_stick_lin-nbr_rm) == 0 and nbr_rm > 0:
                            action(idx, nbr_rm)
                    if nbr_stick <= (max_rm*2)+1 and nbr_stick_lin > (max_rm+1) and (nbr_stick_lin+1) == nbr_stick:
                        nbr_rm = 1
                        action(idx, nbr_rm)
                    if nbr_stick <= (max_rm+2):
                        nbr_rm = nbr_stick_lin
                        action(idx, nbr_rm)
                                  
            if nbr_stick_lin > 0 and nbr_stick == nbr_stick_lin:
                if nbr_stick_lin <= (max_rm+1):
                    nbr_rm = max_rm
                    while (nbr_stick_lin-nbr_rm) != 1:
                        nbr_rm = nbr_rm - 1
                    if (nbr_stick_lin-nbr_rm) == 1 and nbr_rm > 0:
                        action(idx, nbr_rm)
                if nbr_stick_lin == 1:
                    nbr_rm = 1
                    action(idx, nbr_rm)
                if nbr_stick_lin > (max_rm+1) and (nbr_stick_lin-1) > (max_rm*2)+1:
                    nbr_rm = 1
                    action(idx, nbr_rm)
                else:
                    nbr_rm = max_rm
                    while (nbr_stick_lin-nbr_rm) != (max_rm+2):
                        nbr_rm = nbr_rm - 1
                    if nbr_rm > 0:
                        action(idx, nbr_rm)
            if nbr_stick_lin > 0:
                nbr_rm = 1
                action(idx, nbr_rm)
            nbr_stick_lin = 0
        for item in array:
            if '|' in item:
                nbr_stick_lin = nbr_stick_lin + 1
            if nbr_stick_lin > 0:
                nbr_rm = 1
                action(idx, nbr_rm)
        print('Je ne sais pas quoi faire !!!')
        sys.exit()
    show_game()
    
    if player == 1:
        player_one()
    else:
        Ai()


    
else:
    print('Argument manquant ou en trop !')
