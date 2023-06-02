class Game_state():
    def __init__(self):
        self.board = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],                
        ["~~", "~~", "~~", "~~", "~~", "~~", "~~", "~~"],
        ["~~", "~~", "~~", "~~", "~~", "~~", "~~", "~~"],
        ["~~", "~~", "~~", "~~", "~~", "~~", "~~", "~~"],
        ["~~", "~~", "~~", "~~", "~~", "~~", "~~", "~~"],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]        
        ]
        self.white_to_move = True
        self.moves_log = []

        self.pieceValue = {
            'R': 5,
            'N': 3,
            'B': 3,
            'Q': 9,
            'P': 1
        }

        self.white_pieces_captured = []
        self.value_white_captured = 0
        self.black_pieces_captured = []
        self.value_black_captured = 0

        self.enPassantPossibility = () 
        #This is the coordinate of the square where enpassant is possible

        self.currently_Checkmate = False
        self.currently_Stalemate = False

        self.position_of_white_king = (7,4) #a tuple (row, column)
        self.position_of_black_king = (0,4) #a tuple (row, column)

        self.current_castling_possibility = Castling_Possibility(True, True, True, True)

        self.castling_possibilitiy_log = [Castling_Possibility(self.current_castling_possibility.wks, self.current_castling_possibility.bks, self.current_castling_possibility.wqs, self.current_castling_possibility.bqs)]
        """
        This castling_possibility_log[] array maintains the castling possibilitiy states wrt piece movement at each and every stage of the game. This is required when we undo a move, because undo of a move can change castle rights. We then need to revert the current_castling_possibility to the previous state of castling possibility which will be obtained from this array
        """


    """This function simply takes a move and executes it. """
    def make_chess_move(self, move):
        self.board[move.startRow][move.startColumn] = "~~"
        self.board[move.endRow][move.endColumn] = move.pieceMoved
        self.moves_log.append(move)
        
        self.white_to_move = not self.white_to_move

        if move.pieceMoved == "wK":
            #update position_of_white_king
            self.position_of_white_king = (move.endRow, move.endColumn)
        elif move.pieceMoved == "bK":
            self.position_of_black_king = (move.endRow, move.endColumn)

        #Pawn Promotion
        if move.pawnPromotion == True:            
            self.board[move.endRow][move.endColumn] = f"{move.pieceMoved[0]}{move.pawnPromotionPiece}"

        #en Passant Move
        if move.isEnpassantMove == True:
            self.board[move.startRow][move.endColumn] = "~~" #Capturing the pawn on (startRow, endCol)

        #update isEnpassantMove variable with every two times adavnce of a pawn
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2 :
            self.enPassantPossibility = ((move.startRow + move.endRow)/2, move.startColumn)
        else:
            self.enPassantPossibility = ()

        #Castling Possibility Update
        self.updateCastlingPossibility(move)
        #after updating, you need to append this new Castling state into the castle possibility log
        self.castling_possibilitiy_log.append(Castling_Possibility(self.current_castling_possibility.wks, self.current_castling_possibility.bks, self.current_castling_possibility.wqs, self.current_castling_possibility.bqs))

        #Castling Move
        #Note the movement of the king (i.e pieceMoved) has already been taken care by the normal part of the make_chess_move(), here we are moving the rooks
        if move.isCastleMove == True:
            
            if move.endColumn - move.startColumn == 2: #this means it is ks castle
                self.board[move.endRow][move.endColumn-1] = self.board[move.endRow][move.endColumn + 1] #This moves the king side rook to the left of the new position of the king
                
                self.board[move.endRow][move.endColumn + 1] = "~~"
                #erase the old king side rook
                

            else: #this means it is a qs castle
                self.board[move.endRow][move.endColumn+1] = self.board[move.endRow][move.endColumn -2] #This moves the queen side rook to the right of the new position of the king
                self.board[move.endRow][move.endColumn -2] = "~~"
                #erase the old queen side rook
            

    """Undo or Takeback function"""
    def undo_takeback_move(self):
        if len(self.moves_log) != 0 :
            previous_move = self.moves_log.pop() #as we pop this move data from the move log, we also obtain it and store it in the variable previous_move
            self.board[previous_move.startRow][previous_move.startColumn] = previous_move.pieceMoved
            self.board[previous_move.endRow][previous_move.endColumn] = previous_move.pieceCaptured
            
            self.white_to_move = not self.white_to_move

            if previous_move.pieceMoved == "wK":
                #update position_of_white_king
                self.position_of_white_king = (previous_move.startRow, previous_move.startColumn)
            elif previous_move.pieceMoved == "bK":
                self.position_of_black_king = (previous_move.startRow, previous_move.startColumn)

            #undo the enPassant Move
            if previous_move.isEnpassantMove == True:
                self.board[previous_move.endRow][previous_move.endColumn] = "~~"
                self.board[previous_move.startRow][previous_move.endColumn] = previous_move.pieceCaptured
                self.enPassantPossibility = (previous_move.endRow, previous_move.endColumn)

            #undo the change of enPassantPossibility variable when undoing a two square pawn advance
            if previous_move.pieceMoved[1] == "P" and abs(previous_move.startRow - previous_move.endRow) == 2:
                self.enPassantPossibility = ()

            #undo Castling Possibility
            #with every undo move, we pop the last item from the castling_possibilitiy_log
            #Then we set current_castling_possibility to the new last item or actually the earlier second last item from the castling_possibilitiy_log
            self.castling_possibilitiy_log.pop()
            new_castling_possibility = self.castling_possibilitiy_log[-1]
            self.current_castling_possibility = Castling_Possibility(new_castling_possibility.wks, new_castling_possibility.bks, new_castling_possibility.wqs, new_castling_possibility.bqs)

            #undo castling move
            #Note the movement of the king (i.e pieceMoved) has already been taken care by the normal part of the undo_takeback_move(), here we are moving the rooks
            if previous_move.isCastleMove == True:
                if previous_move.endColumn - previous_move.startColumn == 2: #it was a ks castle
                    self.board[previous_move.endRow][previous_move.endColumn + 1] = self.board[previous_move.endRow][previous_move.endColumn-1] #moving the ks rook back to its place
                    self.board[previous_move.endRow][previous_move.endColumn-1] = "~~"
                    #removing the ks rook from its castling position
                else: #it was a qs castle
                    self.board[previous_move.endRow][previous_move.endColumn - 2] = self.board[previous_move.endRow][previous_move.endColumn+1] #moving the qs rook back to its place
                    self.board[previous_move.endRow][previous_move.endColumn+1] = "~~"
                    #removing the qs rook from its castling position


    def updateCastlingPossibility(self, move):
        if move.pieceMoved == "wK":
            self.current_castling_possibility.wks = False
            self.current_castling_possibility.wqs = False
        elif move.pieceMoved == "bK":
            self.current_castling_possibility.bks = False
            self.current_castling_possibility.bqs = False
        elif move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startColumn == 0: #wqs
                    self.current_castling_possibility.wqs = False
                elif move.startColumn == 7: #wks
                    self.current_castling_possibility.wks = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startColumn == 0: #bqs
                    self.current_castling_possibility.bqs = False
                elif move.startColumn == 7: #bks
                    self.current_castling_possibility.bks = False

        #now we handle the cases when the rooks are captured, because then also castling isn't allowed
        if move.pieceCaptured == "wR":
            if move.endRow == 7 and move.endColumn == 0: #This is the wqs rook
                self.current_castling_possibility.wqs = False
            elif move.endRow == 7 and move.endColumn == 7: #This is the wks rook
                self.current_castling_possibility.wks = False
        if move.pieceCaptured == "bR":
            if move.endRow == 0 and move.endColumn == 0: #This is the bqs rook
                self.current_castling_possibility.bqs = False
            elif move.endRow == 0 and move.endColumn == 7: #This is the bks rook
                self.current_castling_possibility.bks = False
    
    def obtain_valid_moves(self):
        print("Printing current_castling_possibility:")
        print(f"wks:{self.current_castling_possibility.wks} bks:{self.current_castling_possibility.bks} wqs:{self.current_castling_possibility.wqs} bqs{self.current_castling_possibility.bqs}")

        print("Printing the castling Logs:")
        for i in self.castling_possibilitiy_log:
            print(f"wks:{i.wks} bks:{i.bks} wqs:{i.wqs} bqs{i.bqs}")
        """
        A better algorithm to check for valid moves is as follows:
        1. For every move in current_possible_moves, first make the move
        2. Then call the function efficient_is_under_check()
        3. If that move is invalid remove it from current_possible_moves
        4. undo the move
        5. Here you don't have to do any manual change of white_to_move flag
        """
        #we don't want to disturb the current isEnPassantMove variable when we call the move and undo function so many times to generate the moves
        tempEnPassantPossibility = self.enPassantPossibility

        temp_castling_possibility = Castling_Possibility(self.current_castling_possibility.wks, self.current_castling_possibility.bks, self.current_castling_possibility.wqs, self.current_castling_possibility.bqs)

        current_possible_moves = self.obtain_all_possible_moves()
        if self.white_to_move:
            self.obtainCastleMoves(self.position_of_white_king[0], self.position_of_white_king[1], current_possible_moves, "w")
        else:
            self.obtainCastleMoves(self.position_of_black_king[0], self.position_of_black_king[1], current_possible_moves, "b")

        i = len(current_possible_moves) - 1
        while i>=0:
            #currently player is set to 1 aka player = 1
            self.make_chess_move(current_possible_moves[i])
            #player = 2
            
            #change to player 1
            self.white_to_move = not self.white_to_move
            #player = 1
            if self.efficient_is_under_check(): #so when we call this function we have player = 1
                current_possible_moves.remove(current_possible_moves[i])

            #change to player 2
            self.white_to_move = not self.white_to_move
            #player = 2

            self.undo_takeback_move()
            #player = 1
            
            i -= 1
        
        if len(current_possible_moves) == 0: #this means it can either be a checkmate or a stalemate
            if self.white_to_move == True:
                loser = "White" #because white is to move and it cannot move
                winner = "Black"
            else:
                loser = "Black" #because black is to move and it cannot move
                winner = "White"            

            if self.efficient_is_under_check():
                self.currently_Checkmate = True
                print(f"Checkmate : {winner} wins and {loser} loses")
            else:
                self.currently_Stalemate = True
                print(f"Stalemate: Draw")

        else:
            self.currently_Stalemate = False
            self.currently_Checkmate = False
            #we had to this explicitly again, because say one move resulted in a checkmate or stalemate, but then the player undo the move, then one of these flags would still be set to True. So this was necessary

        self.enPassantPossibility = tempEnPassantPossibility
        self.current_castling_possibility = temp_castling_possibility
        return current_possible_moves

    def efficient_is_under_check(self):
        #c will the color marker for the piece. This variable will be used in Python f strings below
        #obtain row and column of the king
        if self.white_to_move == True:
            c = "w"
            king_row = self.position_of_white_king[0]
            king_column = self.position_of_white_king[1]
        else:
            c = "b"
            king_row = self.position_of_black_king[0]
            king_column = self.position_of_black_king[1]

        
        if self.rook_and_queen_check(c, king_row, king_column) :
            return True
        if self.bishop_and_queen_check(c, king_row, king_column):
            return True
        if self.knight_check(c, king_row, king_column):
            return True
        if self.pawn_check(c, king_row, king_column):
            return True
        if self.king_check(c, king_row, king_column):
            return True
        

        return False

    
    def generic_efficient_is_under_check(self, king_row, king_column, piece_color):

        c = piece_color
        
        if self.rook_and_queen_check(c, king_row, king_column) :
            return True
        if self.bishop_and_queen_check(c, king_row, king_column):
            return True
        if self.knight_check(c, king_row, king_column):
            return True
        if self.pawn_check(c, king_row, king_column):
            return True
        if self.king_check(c, king_row, king_column):
            return True
        

        return False


    def rook_and_queen_check(self, c, row, column):
        #our king is in (row, column) and its color is c
        #c is the color of our King
        #o is the color of the opposite side whose pieces can check us

        if c == "w":
            o = "b"
        else:
            o = "w"


        #to generate all moves along the given column
        #first cover upper part of column
        row_generator = row - 1
        while row_generator >= 0:  
            if self.board[row_generator][column][0] == f"{c}": #we have our own pice protecting
                break  
            if self.board[row_generator][column][0] == f"{o}" and (self.board[row_generator][column] != f"{o}R" and self.board[row_generator][column] != f"{o}Q"): #it is a opponent piece but not rook or queen, so no check  
                break     
            if self.board[row_generator][column] == f"{o}R" or self.board[row_generator][column] == f"{o}Q": #it is a opposite color rook or queen so its is check
                return True

            row_generator -= 1

        #now cover lower part of column
        row_generator = row + 1
        while row_generator <= 7:
            if self.board[row_generator][column][0] == f"{c}": #we have our own piece protecting
                break
            if self.board[row_generator][column][0] == f"{o}" and (self.board[row_generator][column] != f"{o}R" and self.board[row_generator][column] != f"{o}Q"): #it is a opponent piece but not rook or queen, so no check  
                break
            if self.board[row_generator][column] == f"{o}R" or self.board[row_generator][column] == f"{o}Q": #it is a opposite color rook or queen so its is check
                return True

            row_generator += 1

        #to generate all moves along the given row
        #first cover left part of row
        column_generator = column - 1
        while column_generator >= 0:                 
            if self.board[row][column_generator][0] == f"{c}": #we have our own piece protecting
                break
            if self.board[row][column_generator][0] == f"{o}" and (self.board[row][column_generator] != f"{o}R" and self.board[row][column_generator] != f"{o}Q"): #it is a opponent piece but not rook or queen, so no check  
                break
            if self.board[row][column_generator] == f"{o}R" or self.board[row][column_generator] == f"{o}Q": #it is a opposite color rook or queen so its is check
                return True

            column_generator -= 1

        #now cover right part of row
        column_generator = column + 1
        while column_generator <= 7:
            if self.board[row][column_generator][0] == f"{c}": #we have our own piece protecting
                break
            if self.board[row][column_generator][0] == f"{o}" and (self.board[row][column_generator] != f"{o}R" and self.board[row][column_generator] != f"{o}Q"): #it is a opponent piece but not rook or queen, so no check  
                break
            if self.board[row][column_generator] == f"{o}R" or self.board[row][column_generator] == f"{o}Q": #it is a opposite color rook or queen so its is check
                return True            

            column_generator += 1

        return False

    def bishop_and_queen_check(self, c, row, column):
        #our king is in (row, column) and its color is c
        #c is the color of our King
        #o is the color of the opposite side whose pieces can check us

        if c == "w":
            o = "b"
        else:
            o = "w"

        #to cover the upper right diagonal
        row_generator = row-1
        column_generator = column+1
        while row_generator >= 0 and column_generator <= 7: #which ever reaches first
            if self.board[row_generator][column_generator][0] == f"{c}": #we have our own pice protecting
                break
            if self.board[row_generator][column_generator][0] == f"{o}" and (self.board[row_generator][column_generator] != f"{o}B" and self.board[row_generator][column_generator] != f"{o}Q"):#it is a opponent piece but not bishop or queen, so no check
                break 
            if self.board[row_generator][column_generator] == f"{o}B" or self.board[row_generator][column_generator] == f"{o}Q": #it is a opposite color bishop or queen, so it is a check
                return True
            
            row_generator -= 1
            column_generator += 1

        #to cover the upper left diagonal
        row_generator = row-1
        column_generator = column-1
        while row_generator >= 0 and column_generator >= 0: #which ever reaches first
            if self.board[row_generator][column_generator][0] == f"{c}": #we have our own pice protecting
                break
            if self.board[row_generator][column_generator][0] == f"{o}" and (self.board[row_generator][column_generator] != f"{o}B" and self.board[row_generator][column_generator] != f"{o}Q"):#it is a opponent piece but not bishop or queen, so no check
                break
            if self.board[row_generator][column_generator] == f"{o}B" or self.board[row_generator][column_generator] == f"{o}Q": #it is a opposite color bishop or queen, so it is a check
                return True
            
            row_generator -= 1
            column_generator -= 1

        #to cover the lower right diagonal
        row_generator = row+1
        column_generator = column+1
        while row_generator <= 7 and column_generator <= 7: #which ever reaches first
            if self.board[row_generator][column_generator][0] == f"{c}": #we have our own pice protecting
                break
            if self.board[row_generator][column_generator][0] == f"{o}" and (self.board[row_generator][column_generator] != f"{o}B" and self.board[row_generator][column_generator] != f"{o}Q"):#it is a opponent piece but not bishop or queen, so no check
                break
            if self.board[row_generator][column_generator] == f"{o}B" or self.board[row_generator][column_generator] == f"{o}Q": #it is a opposite color bishop or queen, so it is a check
                return True
            
            row_generator += 1
            column_generator += 1

        #to cover the lower left diagonal
        row_generator = row+1
        column_generator = column-1
        while row_generator <= 7 and column_generator >=0: #which ever reaches first
            if self.board[row_generator][column_generator][0] == f"{c}": #we have our own pice protecting
                break
            if self.board[row_generator][column_generator][0] == f"{o}" and (self.board[row_generator][column_generator] != f"{o}B" and self.board[row_generator][column_generator] != f"{o}Q"):#it is a opponent piece but not bishop or queen, so no check
                break
            if self.board[row_generator][column_generator] == f"{o}B" or self.board[row_generator][column_generator] == f"{o}Q": #it is a opposite color bishop or queen, so it is a check
                return True
            
            row_generator += 1
            column_generator -= 1

        return False



    def knight_check(self, c, row, column):
        #our king is in (row, column) and its color is c
        #c is the color of our King
        #o is the color of the opposite side whose pieces can check us

        if c == "w":
            o = "b"
        else:
            o = "w"

        #there can be 8 cases of a knight check
        #case 1:
        row_generator = row - 2
        column_generator = column + 1
        if row_generator >= 0 and row_generator <=7 and column_generator >= 0 and column_generator <=7 and self.board[row_generator][column_generator] == f"{o}N": #it is a opposite color knight, so it is a check
                return True
    

        #case 2:
        row_generator = row - 1
        column_generator = column + 2
        if row_generator >= 0 and row_generator <=7 and column_generator >= 0 and column_generator <=7 and self.board[row_generator][column_generator] == f"{o}N": #it is a opposite color knight, so it is a check
                return True

        #case 3:
        row_generator = row + 1
        column_generator = column + 2
        if row_generator >= 0 and row_generator <=7 and column_generator >= 0 and column_generator <=7 and self.board[row_generator][column_generator] == f"{o}N": #it is a opposite color knight, so it is a check
                return True

        #case 4:
        row_generator = row + 2
        column_generator = column + 1
        if row_generator >= 0 and row_generator <=7 and column_generator >= 0 and column_generator <=7 and self.board[row_generator][column_generator] == f"{o}N": #it is a opposite color knight, so it is a check
                return True

        #case 5:
        row_generator = row - 2
        column_generator = column - 1
        if row_generator >= 0 and row_generator <=7 and column_generator >= 0 and column_generator <=7 and self.board[row_generator][column_generator] == f"{o}N": #it is a opposite color knight, so it is a check
                return True

        #case 6:
        row_generator = row - 1
        column_generator = column - 2
        if row_generator >= 0 and row_generator <=7 and column_generator >= 0 and column_generator <=7 and self.board[row_generator][column_generator] == f"{o}N": #it is a opposite color knight, so it is a check
                return True

        #case 7:
        row_generator = row + 1
        column_generator = column - 2
        if row_generator >= 0 and row_generator <=7 and column_generator >= 0 and column_generator <=7 and self.board[row_generator][column_generator] == f"{o}N": #it is a opposite color knight, so it is a check
                return True

        #case 8:
        row_generator = row + 2
        column_generator = column - 1
        if row_generator >= 0 and row_generator <=7 and column_generator >= 0 and column_generator <=7 and self.board[row_generator][column_generator] == f"{o}N": #it is a opposite color knight, so it is a check
                return True

        return False

    def pawn_check(self, c, row, column):
        #our king is in (row, column) and its color is c
        #c is the color of our King
        #o is the color of the opposite side whose pieces can check us

        if c == "w":
            o = "b"
        else:
            o = "w"

        if c == "w": #it is the white king, so black pawns can give it a check. 
            #Case 1: When black pawn is in (row - 1, column - 1)
            row_generator = row - 1
            column_generator = column - 1
            if row_generator >= 0 and row_generator <=7 and column_generator >= 0 and column_generator <=7 and self.board[row_generator][column_generator] == f"{o}P": #it is a opposite color pawn, so it is a check
                return True
            
            #Case 2: When black pawn is in (row - 1, column + 1)
            row_generator = row - 1
            column_generator = column + 1
            if row_generator >= 0 and row_generator <=7 and column_generator >= 0 and column_generator <=7 and self.board[row_generator][column_generator] == f"{o}P": #it is a opposite color pawn, so it is a check
                return True
        else: #it is the black king, so white pawns can give it a check.
            #Case 1: When white pawn is in (row - 1, column - 1)
            row_generator = row + 1
            column_generator = column - 1
            if row_generator >= 0 and row_generator <=7 and column_generator >= 0 and column_generator <=7 and self.board[row_generator][column_generator] == f"{o}P": #it is a opposite color pawn, so it is a check
                return True
            
            #Case 2: When white pawn is in (row - 1, column + 1)
            row_generator = row + 1
            column_generator = column + 1
            if row_generator >= 0 and row_generator <=7 and column_generator >= 0 and column_generator <=7 and self.board[row_generator][column_generator] == f"{o}P": #it is a opposite color pawn, so it is a check
                return True

        return False

    def king_check(self, c, row, column):
        #our king is in (row, column) and its color is c
        #c is the color of our King
        #o is the color of the opposite side whose pieces can check us

        if c == "w":
            o = "b"
        else:
            o = "w"

        #There are 8 squares surrounding a king. An enemy queen in any of those squares is a check
        #Case 1:
        row_generator = row - 1
        column_generator = column - 1
        if row_generator >= 0 and row_generator <=7 and column_generator >= 0 and column_generator <=7 and self.board[row_generator][column_generator] == f"{o}K": #it is a opposite color King, so it is a check
                return True

        #Case 2:
        row_generator = row - 1
        column_generator = column
        if row_generator >= 0 and row_generator <=7 and column_generator >= 0 and column_generator <=7 and self.board[row_generator][column_generator] == f"{o}K": #it is a opposite color King, so it is a check
                return True

        #Case 3:
        row_generator = row - 1
        column_generator = column + 1
        if row_generator >= 0 and row_generator <=7 and column_generator >= 0 and column_generator <=7 and self.board[row_generator][column_generator] == f"{o}K": #it is a opposite color King, so it is a check
                return True

        #Case 4:
        row_generator = row
        column_generator = column - 1
        if row_generator >= 0 and row_generator <=7 and column_generator >= 0 and column_generator <=7 and self.board[row_generator][column_generator] == f"{o}K": #it is a opposite color King, so it is a check
                return True

        #Case 5:
        row_generator = row
        column_generator = column + 1
        if row_generator >= 0 and row_generator <=7 and column_generator >= 0 and column_generator <=7 and self.board[row_generator][column_generator] == f"{o}K": #it is a opposite color King, so it is a check
                return True

        #Case 6:
        row_generator = row + 1
        column_generator = column - 1
        if row_generator >= 0 and row_generator <=7 and column_generator >= 0 and column_generator <=7 and self.board[row_generator][column_generator] == f"{o}K": #it is a opposite color King, so it is a check
                return True

        #Case 7:
        row_generator = row + 1
        column_generator = column
        if row_generator >= 0 and row_generator <=7 and column_generator >= 0 and column_generator <=7 and self.board[row_generator][column_generator] == f"{o}K": #it is a opposite color King, so it is a check
                return True

        #Case 8
        row_generator = row + 1
        column_generator = column + 1
        if row_generator >= 0 and row_generator <=7 and column_generator >= 0 and column_generator <=7 and self.board[row_generator][column_generator] == f"{o}K": #it is a opposite color King, so it is a check
                return True

        
        return False

    
    def obtain_all_possible_moves(self):
        possible_moves = []
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                piece = self.board[row][column]
                color_of_piece = piece[0]
                type_of_piece = piece[1]

                if (color_of_piece == 'w' and self.white_to_move == True) or (color_of_piece == 'b' and self.white_to_move == False):
                    if type_of_piece == 'P': #Pawn
                        self.obtain_pawn_moves(row, column, possible_moves)
                    if type_of_piece == 'R': #Rook
                        self.obtain_rook_moves(row, column, possible_moves)
                    if type_of_piece == 'B': #Bishop
                        self.obtain_bishop_moves(row, column, possible_moves)
                    if type_of_piece == 'Q': #Queen
                        self.obtain_queen_moves(row, column, possible_moves)
                    if type_of_piece == 'N': #Knight
                        self.obtain_knight_moves(row, column, possible_moves)
                    if type_of_piece == 'K': #King
                        self.obtain_king_moves(row, column, possible_moves)

        return possible_moves
                    

    def obtain_pawn_moves(self, row, column, possible_moves):
        """
        Moving pawns is lightly tricky, because :
        1. A pawn can move twice in its first movement, but after the first move a pawn can move only once
                - This issue can be solved by checking if the row is 6 for white pawn and row is 1 for black pawn
                cause if that is the case, then that means the pawn has not moved yet, so it can go once or twice

        2. The white pawn moves from Row 6 towards Row 0, while 
           the black pawn moves from Row 1 towards Row 1
                - This can be solved by the color of pawn

        3. A pawn moves diagonally when it captures a piece
                - This can be solved if we check if there is any pice in the forward diagonals of the pawn

        """

        

        if self.white_to_move == True: #This means white pawn moves
            
            #our white pawn is in (row, column)

            #pawn moves up
            if row - 1 >= 0 and self.board[row-1][column] == "~~":
                possible_moves.append(Move((row, column),(row-1, column), self.board))

                #now check whether the pawn is in Row 6 - This means it can move twice
                if row == 6 and self.board[row-2][column] == "~~":
                    possible_moves.append(Move((row, column),(row-2, column), self.board))
            
            #pawn does diagonal right capture
            if row - 1 >= 0 and column + 1 <= 7 and self.board[row-1][column+1][0] == "b":
                possible_moves.append(Move((row, column),(row-1, column+1), self.board))

            #enPassant Capture to Right
            if row - 1 >= 0 and column + 1 <= 7 and (row - 1, column + 1) == self.enPassantPossibility:
                possible_moves.append(Move((row, column), (row -1, column + 1), self.board, isEnpassantMove = True))

            #pawn does diagonal left capture
            if row - 1 >= 0 and column - 1 >= 0 and self.board[row-1][column-1][0] == "b":
                possible_moves.append(Move((row, column),(row-1, column-1), self.board))

            #enPassant Capture to Left
            if row - 1 >= 0 and column - 1 >= 0 and (row - 1, column - 1) == self.enPassantPossibility:
                possible_moves.append(Move((row, column), (row -1, column - 1), self.board, isEnpassantMove = True))
            

            
        else: #This means black pawn moves
            #our black pawn is in (row, column)

            #pawn moves down
            if row + 1 <= 7 and self.board[row+1][column] == "~~":
                possible_moves.append(Move((row, column),(row+1, column), self.board))

                #now check whether the pawn is in Row 6 - This means it can move twice
                if row == 1 and self.board[row+2][column] == "~~":
                    possible_moves.append(Move((row, column),(row+2, column), self.board))
            
            #pawn does diagonal right capture
            if row + 1 <= 7 and column + 1 <= 7 and self.board[row+1][column+1][0] == "w":
                possible_moves.append(Move((row, column),(row+1, column+1), self.board))

            #enPassant Capture to Right
            if row + 1 <= 7 and column + 1 <= 7 and (row + 1, column + 1) == self.enPassantPossibility:
                possible_moves.append(Move((row, column), (row +1, column + 1), self.board, isEnpassantMove = True))

            #pawn does diagonal left capture
            if row + 1 <= 7 and column - 1 >= 0 and self.board[row+1][column-1][0] == "w":
                possible_moves.append(Move((row, column),(row+1, column-1), self.board))

            #enPassant Capture to Left
            if row + 1 <= 7 and column - 1 >= 0 and (row + 1, column - 1) == self.enPassantPossibility:
                possible_moves.append(Move((row, column), (row +1, column - 1), self.board, isEnpassantMove = True))

            
            

#possible_moves.append(Move((row, column),(), self.board))

    def obtain_rook_moves(self, row, column, possible_moves):
        #so our rook is in (row, column)

        if self.white_to_move == True:
            #to generate all moves along the given column
            #first cover upper part of column
            row_generator = row - 1
            while row_generator >= 0:                 
                if self.board[row_generator][column] == "~~": #empty square so you can move
                    possible_moves.append(Move((row, column),(row_generator, column), self.board))
                if self.board[row_generator][column][0] == "b": #it is a black piece so capture and then break
                    possible_moves.append(Move((row, column),(row_generator, column), self.board))
                    break
                if self.board[row_generator][column][0] == "w": #it is a white piece, so simply break
                    break

                row_generator -= 1

            #now cover lower part of column
            row_generator = row + 1
            while row_generator <= 7:
                if self.board[row_generator][column] == "~~": #empty square so you can move
                    possible_moves.append(Move((row, column),(row_generator, column), self.board))
                if self.board[row_generator][column][0] == "b": #it is a black piece so capture and then break
                    possible_moves.append(Move((row, column),(row_generator, column), self.board))
                    break
                if self.board[row_generator][column][0] == "w": #it is a white piece, so simply break
                    break

                row_generator += 1

            #to generate all moves along the given row
            #first cover left part of row
            column_generator = column - 1
            while column_generator >= 0:                 
                if self.board[row][column_generator] == "~~": #empty square so you can move
                    possible_moves.append(Move((row, column),(row, column_generator), self.board))
                if self.board[row][column_generator][0] == "b": #it is a black piece so capture and then break
                    possible_moves.append(Move((row, column),(row, column_generator), self.board))
                    break
                if self.board[row][column_generator][0] == "w": #it is a white piece, so simply break
                    break

                column_generator -= 1

            #now cover right part of row
            column_generator = column + 1
            while column_generator <= 7:
                if self.board[row][column_generator] == "~~": #empty square so you can move
                    possible_moves.append(Move((row, column),(row, column_generator), self.board))
                if self.board[row][column_generator][0] == "b": #it is a black piece so capture and then break
                    possible_moves.append(Move((row, column),(row, column_generator), self.board))
                    break
                if self.board[row][column_generator][0] == "w": #it is a white piece, so simply break
                    break

                column_generator += 1

        else:
            #to generate all moves along the given column
            #first cover upper part of column
            row_generator = row - 1
            while row_generator >= 0:                 
                if self.board[row_generator][column] == "~~": #empty square so you can move
                    possible_moves.append(Move((row, column),(row_generator, column), self.board))
                if self.board[row_generator][column][0] == "w": #it is a white piece so capture and then break
                    possible_moves.append(Move((row, column),(row_generator, column), self.board))
                    break
                if self.board[row_generator][column][0] == "b": #it is a black piece, so simply break
                    break

                row_generator -= 1

            #now cover lower part of column
            row_generator = row + 1
            while row_generator <= 7:
                if self.board[row_generator][column] == "~~": #empty square so you can move
                    possible_moves.append(Move((row, column),(row_generator, column), self.board))
                if self.board[row_generator][column][0] == "w": #it is a white piece so capture and then break
                    possible_moves.append(Move((row, column),(row_generator, column), self.board))
                    break
                if self.board[row_generator][column][0] == "b": #it is a black piece, so simply break
                    break

                row_generator += 1

            #to generate all moves along the given row
            #first cover left part of row
            column_generator = column - 1
            while column_generator >= 0:                 
                if self.board[row][column_generator] == "~~": #empty square so you can move
                    possible_moves.append(Move((row, column),(row, column_generator), self.board))
                if self.board[row][column_generator][0] == "w": #it is a white piece so capture and then break
                    possible_moves.append(Move((row, column),(row, column_generator), self.board))
                    break
                if self.board[row][column_generator][0] == "b": #it is a black piece, so simply break
                    break

                column_generator -= 1

            #now cover right part of row
            column_generator = column + 1
            while column_generator <= 7:
                if self.board[row][column_generator] == "~~": #empty square so you can move
                    possible_moves.append(Move((row, column),(row, column_generator), self.board))
                if self.board[row][column_generator][0] == "w": #it is a white piece so capture and then break
                    possible_moves.append(Move((row, column),(row, column_generator), self.board))
                    break
                if self.board[row][column_generator][0] == "b": #it is a black piece, so simply break
                    break

                column_generator += 1

    def obtain_bishop_moves(self, row, column, possible_moves):
        if self.white_to_move == True:
            #to cover the upper right diagonal
            row_generator = row-1
            column_generator = column+1
            while row_generator >= 0 and column_generator <= 7: #which ever reaches first
                if self.board[row_generator][column_generator] == "~~": #empty square so you can move
                    possible_moves.append(Move((row, column),(row_generator, column_generator), self.board))
                if self.board[row_generator][column_generator][0] == "b": #it is a black piece so capture and then break
                    possible_moves.append(Move((row, column),(row_generator, column_generator), self.board))
                    break
                if self.board[row_generator][column_generator][0] == "w": #it is a white piece, so simply break
                    break
                row_generator -= 1
                column_generator += 1

            #to cover the upper left diagonal
            row_generator = row-1
            column_generator = column-1
            while row_generator >= 0 and column_generator >= 0: #which ever reaches first
                if self.board[row_generator][column_generator] == "~~": #empty square so you can move
                    possible_moves.append(Move((row, column),(row_generator, column_generator), self.board))
                if self.board[row_generator][column_generator][0] == "b": #it is a black piece so capture and then break
                    possible_moves.append(Move((row, column),(row_generator, column_generator), self.board))
                    break
                if self.board[row_generator][column_generator][0] == "w": #it is a white piece, so simply break
                    break
                row_generator -= 1
                column_generator -= 1

            #to cover the lower right diagonal
            row_generator = row+1
            column_generator = column+1
            while row_generator <= 7 and column_generator <= 7: #which ever reaches first
                if self.board[row_generator][column_generator] == "~~": #empty square so you can move
                    possible_moves.append(Move((row, column),(row_generator, column_generator), self.board))
                if self.board[row_generator][column_generator][0] == "b": #it is a black piece so capture and then break
                    possible_moves.append(Move((row, column),(row_generator, column_generator), self.board))
                    break
                if self.board[row_generator][column_generator][0] == "w": #it is a white piece, so simply break
                    break
                row_generator += 1
                column_generator += 1

            #to cover the lower left diagonal
            row_generator = row+1
            column_generator = column-1
            while row_generator <= 7 and column_generator >=0: #which ever reaches first
                if self.board[row_generator][column_generator] == "~~": #empty square so you can move
                    possible_moves.append(Move((row, column),(row_generator, column_generator), self.board))
                if self.board[row_generator][column_generator][0] == "b": #it is a black piece so capture and then break
                    possible_moves.append(Move((row, column),(row_generator, column_generator), self.board))
                    break
                if self.board[row_generator][column_generator][0] == "w": #it is a white piece, so simply break
                    break
                row_generator += 1
                column_generator -= 1

        else:
            #to cover the upper right diagonal
            row_generator = row-1
            column_generator = column+1
            while row_generator >= 0 and column_generator <= 7: #which ever reaches first
                if self.board[row_generator][column_generator] == "~~": #empty square so you can move
                    possible_moves.append(Move((row, column),(row_generator, column_generator), self.board))
                if self.board[row_generator][column_generator][0] == "w": #it is a white piece so capture and then break
                    possible_moves.append(Move((row, column),(row_generator, column_generator), self.board))
                    break
                if self.board[row_generator][column_generator][0] == "b": #it is a black piece, so simply break
                    break
                row_generator -= 1
                column_generator += 1

            #to cover the upper left diagonal
            row_generator = row-1
            column_generator = column-1
            while row_generator >= 0 and column_generator >= 0: #which ever reaches first
                if self.board[row_generator][column_generator] == "~~": #empty square so you can move
                    possible_moves.append(Move((row, column),(row_generator, column_generator), self.board))
                if self.board[row_generator][column_generator][0] == "w": #it is a white piece so capture and then break
                    possible_moves.append(Move((row, column),(row_generator, column_generator), self.board))
                    break
                if self.board[row_generator][column_generator][0] == "b": #it is a black piece, so simply break
                    break
                row_generator -= 1
                column_generator -= 1

            #to cover the lower right diagonal
            row_generator = row+1
            column_generator = column+1
            while row_generator <= 7 and column_generator <= 7: #which ever reaches first
                if self.board[row_generator][column_generator] == "~~": #empty square so you can move
                    possible_moves.append(Move((row, column),(row_generator, column_generator), self.board))
                if self.board[row_generator][column_generator][0] == "w": #it is a white piece so capture and then break
                    possible_moves.append(Move((row, column),(row_generator, column_generator), self.board))
                    break
                if self.board[row_generator][column_generator][0] == "b": #it is a black piece, so simply break
                    break
                row_generator += 1
                column_generator += 1

            #to cover the lower left diagonal
            row_generator = row+1
            column_generator = column-1
            while row_generator <= 7 and column_generator >=0: #which ever reaches first
                if self.board[row_generator][column_generator] == "~~": #empty square so you can move
                    possible_moves.append(Move((row, column),(row_generator, column_generator), self.board))
                if self.board[row_generator][column_generator][0] == "w": #it is a white piece so capture and then break
                    possible_moves.append(Move((row, column),(row_generator, column_generator), self.board))
                    break
                if self.board[row_generator][column_generator][0] == "b": #it is a black piece, so simply break
                    break
                row_generator += 1
                column_generator -= 1

    def obtain_queen_moves(self, row, column, possible_moves):
        #a Queen can do all the moves that a Bishop and a Rook can do
        self.obtain_rook_moves(row, column, possible_moves)
        self.obtain_bishop_moves(row, column, possible_moves)

    def obtain_knight_moves(self, row, column, possible_moves):        
        piece_color = self.board[row][column][0]

        #our Knight is in  (row, column)
        #it can only go to 8 possible squares, we handle these cases separately as follows

        #case 1:
        row_generator = row - 2
        column_generator = column + 1
        self.knight_valid_check(row, column, row_generator, column_generator, piece_color, possible_moves)
    

        #case 2:
        row_generator = row - 1
        column_generator = column + 2
        self.knight_valid_check(row, column, row_generator, column_generator, piece_color, possible_moves)

        #case 3:
        row_generator = row + 1
        column_generator = column + 2
        self.knight_valid_check(row, column, row_generator, column_generator, piece_color, possible_moves)

        #case 4:
        row_generator = row + 2
        column_generator = column + 1
        self.knight_valid_check(row, column, row_generator, column_generator, piece_color, possible_moves)

        #case 5:
        row_generator = row - 2
        column_generator = column - 1
        self.knight_valid_check(row, column, row_generator, column_generator, piece_color, possible_moves)

        #case 6:
        row_generator = row - 1
        column_generator = column - 2
        self.knight_valid_check(row, column, row_generator, column_generator, piece_color, possible_moves)

        #case 7:
        row_generator = row + 1
        column_generator = column - 2
        self.knight_valid_check(row, column, row_generator, column_generator, piece_color, possible_moves)

        #case 8:
        row_generator = row + 2
        column_generator = column - 1
        self.knight_valid_check(row, column, row_generator, column_generator, piece_color, possible_moves)

    
    def knight_valid_check(self, row, column, row_generator, column_generator, piece_color, possible_moves):
        if row_generator >= 0 and row_generator <= 7 and column_generator >= 0 and column_generator <=7:
            if self.board[row_generator][column_generator] == "~~":
                possible_moves.append(Move((row, column), (row_generator, column_generator), self.board))
            
            if self.board[row_generator][column_generator][0] == "b" and piece_color == "w": #capture is possible
                possible_moves.append(Move((row, column), (row_generator, column_generator), self.board))

            if self.board[row_generator][column_generator][0] == "w" and piece_color == "b": #capture is possible
                possible_moves.append(Move((row, column), (row_generator, column_generator), self.board))
            


    def obtain_king_moves(self, row, column, possible_moves):
        piece_color = self.board[row][column][0]
        #a king can move one step in all directions and there are 8 directions
        #it is very similar to a knight

        #case 1:
        row_generator = row - 1
        column_generator = column - 1
        self.king_valid_check(row, column, row_generator, column_generator, piece_color, possible_moves)
    

        #case 2:
        row_generator = row - 1
        column_generator = column
        self.king_valid_check(row, column, row_generator, column_generator, piece_color, possible_moves)

        #case 3:
        row_generator = row - 1
        column_generator = column + 1
        self.king_valid_check(row, column, row_generator, column_generator, piece_color, possible_moves)

        #case 4:
        row_generator = row
        column_generator = column - 1
        self.king_valid_check(row, column, row_generator, column_generator, piece_color, possible_moves)

        #case 5:
        row_generator = row + 1
        column_generator = column - 1
        self.king_valid_check(row, column, row_generator, column_generator, piece_color, possible_moves)

        #case 6:
        row_generator = row + 1
        column_generator = column
        self.king_valid_check(row, column, row_generator, column_generator, piece_color, possible_moves)

        #case 7:
        row_generator = row + 1
        column_generator = column + 1
        self.king_valid_check(row, column, row_generator, column_generator, piece_color, possible_moves)

        #case 8:
        row_generator = row
        column_generator = column + 1
        self.king_valid_check(row, column, row_generator, column_generator, piece_color, possible_moves)

        


    #this is similar to knight_valid_check() function
    def king_valid_check(self, row, column, row_generator, column_generator, piece_color, possible_moves):
        if row_generator >= 0 and row_generator <= 7 and column_generator >= 0 and column_generator <=7:
            if self.board[row_generator][column_generator] == "~~":
                possible_moves.append(Move((row, column), (row_generator, column_generator), self.board))
            
            if self.board[row_generator][column_generator][0] == "b" and piece_color == "w": #capture is possible
                possible_moves.append(Move((row, column), (row_generator, column_generator), self.board))

            if self.board[row_generator][column_generator][0] == "w" and piece_color == "b": #capture is possible
                possible_moves.append(Move((row, column), (row_generator, column_generator), self.board))


    def obtainCastleMoves(self, row, column, possible_moves, piece_color):        
        
        #first we have to check if the king in (row, column) is currently under check. If the king is under check, then we cannot do anything
        if self.efficient_is_under_check():
            return

        #now to check whether ks castling is possible either for white or for black
        if (self.white_to_move and self.current_castling_possibility.wks) or (not self.white_to_move and self.current_castling_possibility.bks):
            self.obtain_ks_castle_moves(row, column, possible_moves, piece_color)
            

        #now to check whether qs castling is possible either for white or for black
        if (self.white_to_move and self.current_castling_possibility.wqs) or (not self.white_to_move and self.current_castling_possibility.bqs):
            self.obtain_qs_castle_moves(row, column, possible_moves, piece_color)
            


    def obtain_ks_castle_moves(self, row, column, possible_moves, piece_color):
        #first check if the two squares to the right of the king are empty
        if self.board[row][column+1] == "~~" and self.board[row][column+2] == "~~":
            
            #now check if these squares are under check. For this we will use the generic_efficient_is_under_check() function
            if not self.generic_efficient_is_under_check(row, column+1, piece_color) and not self.generic_efficient_is_under_check(row, column+2, piece_color):
                possible_moves.append(Move((row, column), (row, column+2), self.board, isCastleMove = True))
                print("ks castle okay")

    def obtain_qs_castle_moves(self, row, column, possible_moves, piece_color):
        #first check if the three squares to the left of the king are empty
        if self.board[row][column-1] == "~~" and self.board[row][column-2] == "~~" and self.board[row][column-3] == "~~":
            
            #now check if these squares are under check. For this we will use the generic_efficient_is_under_check() function
            if not self.generic_efficient_is_under_check(row, column-1, piece_color) and not self.generic_efficient_is_under_check(row, column-2, piece_color) and not self.generic_efficient_is_under_check(row, column-3, piece_color):
                possible_moves.append(Move((row, column), (row, column-2), self.board, isCastleMove = True))
                print("qs castle okay")

class Castling_Possibility():
    #this function takes care of whether the castling is possible wrt the fact that there has been no previous move of the king or the rook whose side castling is to be done

    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
        #wks -> white king side castling
        #bks -> black king side castling
        #wqs -> white queen side castling
        #bqs -> black queen side castling

class Move():
    #now in the chessboard the ranks are from 8 (in top) to 1 (in bottom)
    #and there are columns called files from a (in the left) to h (in the right)
    #now in our 2D matrix board, the top row is 0 and bottom row is 7
    #and the leftmost column is 0 and rightmost column is 7
    convert_ranks_to_matrix_rows = {
        "1" : 7, "2" : 6, "3" : 5, "4" : 4, "5" : 3, "6" : 2, "7" : 1, "8" : 0
    }

    convert_files_to_matrix_columns = {
        "a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" : 7
    }

    convert_matrix_rows_to_ranks = {
        x : y for y, x in convert_ranks_to_matrix_rows.items()
    }

    convert_matrix_columns_to_files = {
        x : y for y, x in convert_files_to_matrix_columns.items()
    }

    def __init__(self, start_square, end_square, board, isEnpassantMove = False, isCastleMove = False):
        self.startRow = start_square[0]
        self.startColumn = start_square[1]

        self.endRow = end_square[0]
        self.endColumn = end_square[1]

        self.pieceMoved = board[self.startRow][self.startColumn]
        self.pieceCaptured = board[self.endRow][self.endColumn]

        #Stuff related to Pawn Promotion
        self.pawnPromotion = False
        self.pawnPromotionPiece = 'Q' #set to Queen by default

        if (self.pieceMoved == "wP" and self.endRow == 0) or (self.pieceMoved == "bP" and self.endRow == 7):
            self.pawnPromotion = True
            print("Hello")
            print(f"{self.pawnPromotion}")
            print(f"{self.pawnPromotionPiece}")

        #stuff related to enPassant        
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove == True:
            if self.pieceMoved == "wP":
                self.pieceCaptured = "bP"
            else:
                self.pieceCaptured = "wP"

        
        #stuff related to castling
        self.isCastleMove = isCastleMove
        
        self.id = 1000*self.startRow + 100*self.startColumn + 10*self.endRow + self.endColumn
        
    def obtain_Move_data(self):
        return self.obtain_rank_and_file(self.startRow, self.startColumn) + self.obtain_rank_and_file(self.endRow, self.endColumn)


    def obtain_rank_and_file(self, row, column):
        return self.convert_matrix_columns_to_files[column] + self.convert_matrix_rows_to_ranks[row]