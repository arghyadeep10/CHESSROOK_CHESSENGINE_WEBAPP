from . import chess_engine
import copy

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

class GameSnapshot():
    def __init__(self, initGSTATE, pieceMoved, cmd, gstate):
        if initGSTATE:
            self.cmd = "NO_COMMAND"
            self.snapshot_gstate_after_cmd = gstate
            self.piece_moved = "NO_PIECEMOVED"
            self.chess_notation_modified = "NO_CHESSNOTATION"
        else:
            self.cmd = cmd
            self.snapshot_gstate_after_cmd = gstate
            self.piece_moved = pieceMoved

            a = int(cmd[0])
            b = int(cmd[1])

            c = int(cmd[3])
            d = int(cmd[4])
            
            self.chess_notation_modified = f"{pieceMoved} | {convert_matrix_columns_to_files[b]}{convert_matrix_rows_to_ranks[a]} > {convert_matrix_columns_to_files[d]}{convert_matrix_rows_to_ranks[c]}"
    
    def print_game_snapshot(self):
        print("Game Snapshot")
        print(f"cmd = {self.cmd}")
        print(f"piece_moved: {self.piece_moved}")
        print(f"chess notation modified: {self.chess_notation_modified}")
        print(f"Game state info")
        print(self.snapshot_gstate_after_cmd.board)


class GamePlayMonitor():
    def __init__(self):
        self.counter1 = 0
        self.counter2 = 0

        self.gstate = chess_engine.Game_state()
        self.valid_moves = self.gstate.obtain_valid_moves()

        self.counter1 += 1

        self.game_active = True

        self.square_selected = () 
        #this a tuple that stores the x and y coordinate of a square
        
        self.squares_clicked_by_player = [] 
        #an array of tuples that stores the coordinates of the squares selected by player i.e start square and end square

        self.game_snapshot_list = []
        game_snapshot = GameSnapshot(True, "NO_PIECEMOVED", "NO_COMMAND", copy.deepcopy(self.gstate)) # initGSTATE = True as this is init gstate
        game_snapshot.print_game_snapshot()
        self.game_snapshot_list.append(game_snapshot)

        self.game_end = False
        self.white_won = False
        self.black_won = False
        self.draw = False
        self.draw_due_to_stalemate = False

    def run_cmd(self, cmd):
        if cmd == "QUIT":
            print(f"Counter1 = {self.counter1}")
            print(f"Counter2 = {self.counter2}")
            self.game_active = False
            return "QUIT_GAME" # since this is a valid move type

        elif cmd == "UNDO":
            if len(self.game_snapshot_list) == 1:
                # this is the init game state - undo is not possible
                return "Invalid"

            self.gstate.undo_takeback_move()
            #time_to_generate_valid_moves = True
            self.valid_moves = self.gstate.obtain_valid_moves()
            self.counter1 += 1
            self.game_snapshot_list.pop() # when a move is undone, the last game snapshot is popped
            last_snapshot = self.game_snapshot_list[-1]
            last_gstate = last_snapshot.snapshot_gstate_after_cmd
            self.gstate.black_pieces_captured = copy.deepcopy(last_gstate.black_pieces_captured)
            self.gstate.white_pieces_captured = copy.deepcopy(last_gstate.white_pieces_captured)
            self.gstate.value_black_captured = copy.deepcopy(last_gstate.value_black_captured)
            self.gstate.value_white_captured = copy.deepcopy(last_gstate.value_white_captured)
            return "Valid" # since this is a valid move type

        else:
            # it is a chess move

            # cmd will be of following ab_cd
            # where ab is (a,b) - coordinate of init position
            # cd is (c,d) - coordinate of final position

            a = int(cmd[0])
            b = int(cmd[1])

            c = int(cmd[3])
            d = int(cmd[4])

            self.squares_clicked_by_player = [(a,b), (c,d)]

            pieceMoved = self.gstate.board[a][b]

            #create an object of Class Move. This object is named as move_object
            #Now when we instantiate this object, it calls its constructor which is the makemove function
            move_object = chess_engine.Move(self.squares_clicked_by_player[0], self.squares_clicked_by_player[1], self.gstate.board)

            #at this point the user has made the move, now we check if this move is in our list of valid_moves[]
            #if it is then we will call the make_chess_move() with this move_object
            isValidMove = False
            for valid_move in self.valid_moves:
                if move_object.id == valid_move.id:
                    isValidMove = True
                    #time_to_generate_valid_moves = True
                    break
                #else:
                    #time_to_generate_valid_moves = False

            if isValidMove == True:
                if valid_move.pawnPromotion == True:
                    # cmd = ab_cd_[promotion_piece]
                    selected_piece_for_promotion = cmd[6:]
                    selected_piece_for_promotion = selected_piece_for_promotion.lower()
                    if selected_piece_for_promotion == "q":
                        valid_move.pawnPromotionPiece = "Q"
                    elif selected_piece_for_promotion == "r":
                        valid_move.pawnPromotionPiece = "R"
                    elif selected_piece_for_promotion == "b":
                        valid_move.pawnPromotionPiece = "B"
                    elif selected_piece_for_promotion == "n":
                        valid_move.pawnPromotionPiece = "N"                
                
                move_type = "Valid"

                # piece capture logic
                # it is a valid move as valid move check is done before - piece capture possible in normal move and en passant only
                # print(f"startRow = {valid_move.startRow}")
                # print(f"startColumn = {valid_move.startColumn}")
                # print(f"self.board[move.startRow][move.startColumn] = {self.board[valid_move.startRow][valid_move.startColumn]}")
                # print(f"endRow = {valid_move.endRow}")
                # print(f"endColumn = {valid_move.endColumn}")
                # print(f"self.board[move.endRow][move.endColumn] = {self.board[valid_move.endRow][valid_move.endColumn]}")

                if self.gstate.board[valid_move.endRow][valid_move.endColumn] != "~~":
                    # its a piece capture
                    # find piece color
                    pieceCaptured = self.gstate.board[valid_move.endRow][valid_move.endColumn]
                    pieceCapturedColor = pieceCaptured[0]
                    pieceCapturedType = pieceCaptured[1]

                    if pieceCapturedColor == "w":
                        self.gstate.white_pieces_captured.append(pieceCaptured)
                        self.gstate.value_white_captured += self.gstate.pieceValue[pieceCapturedType]
                    else:
                        self.gstate.black_pieces_captured.append(pieceCaptured)
                        self.gstate.value_black_captured += self.gstate.pieceValue[pieceCapturedType]
                # piece capture logic ends

                self.gstate.make_chess_move(valid_move)
                #here we are passing valid_move as the parameter and not move_object, because we want to pass the move created by engine that matches our move. This is because, castling, en passant and pawn promotion are special kinds of move that will require engine generated move.
                
                self.square_selected = ()
                self.squares_clicked_by_player = []

                self.valid_moves = self.gstate.obtain_valid_moves()
                self.counter1 += 1
            else:
                move_type = "Invalid"

        self.counter2 += 1	
        # render the new board
        
        if move_type == "Valid":
            # a valid move has been made so game state changed and hence a snapshot is generated and added to our list
            game_snapshot = GameSnapshot(False, pieceMoved, cmd, copy.deepcopy(self.gstate)) # initGSTATE = FALSE as this is not initial game state a move has been made
            game_snapshot.print_game_snapshot()
            self.game_snapshot_list.append(game_snapshot)

        # logic for detecting game end or not
        # self.game_end = False
        # self.white_won = False
        # self.black_won = False
        # self.draw = False
        # self.draw_due_to_stalemate = False

        if self.gstate.currently_Checkmate == True:
            self.game_end = True
            if self.gstate.white_to_move == True:
                # white has lost
                self.white_won = False
                self.black_won = True
            else:
                # black has lost
                self.black_won = False
                self.white_won = True
        elif self.gstate.currently_Stalemate == True:
            self.game_end = True
            self.draw = True
            self.draw_due_to_stalemate = True

        return move_type
