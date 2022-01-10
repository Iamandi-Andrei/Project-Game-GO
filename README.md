# Project-Game-GO  ID:18

Se va crea o interfata grafica minimala ce va oferi utilizatorului posibilitatea sa joace o partida
de GO, atat cu calculatorul, cat si cu un alt oponent. Calculatorul va lua decizii aleatorii, insa
conform cu regulile jocului.  

INPUT: checkers.py tip_adversar  

OUTPUT: Interfata grafica cu tabla de go. Dupa terminarea jocului se va afisa un mesaj
corespunzator.


# Example photo
https://imgur.com/9vTeC8J  

# Simple Game Description 
You have to capture as many enemy pieces and board territories as possible.  
3 Simple placement rules:  
You can't put pieces over enemy pieces.  
You can't capture the piece placed by the enemy in the previous turn if that piece only captured one of your pieces. ( Simple 2 turn loop)  
You can't "suicide" your own piece ( placing it where it will be captured instantly ) unless by doing so you capture enemy pieces and free the "suicidal" piece.  

# Score calculation  
The final score is computed as the sum between the total number of enemy pieces captured and territories on the board that are in the player's control ( fully surrounded by the player's pieces) 

# Game end  
When both players skipped their turn or someone resigned.  
