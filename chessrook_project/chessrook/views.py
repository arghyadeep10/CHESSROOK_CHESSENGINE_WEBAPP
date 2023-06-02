# Python imports
import pickle
import time

# Django imports
from django.shortcuts import render, redirect
from django import forms
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Django models imports
from chessrook.models import ChessGames
from django.contrib.auth.models import User

# Other imports
from . import gameplay

assets = {
    "~~": 'chessrook/chess_pieces/empty_square.png',

    "bR": 'chessrook/chess_pieces/black_rook.png',
    "bB": 'chessrook/chess_pieces/black_bishop.png',
    "bN": 'chessrook/chess_pieces/black_knight.png',
    "bQ": 'chessrook/chess_pieces/black_queen.png',
    "bK": 'chessrook/chess_pieces/black_king.png',
    "bP": 'chessrook/chess_pieces/black_pawn.png',

    "wR": 'chessrook/chess_pieces/white_rook.png',
    "wB": 'chessrook/chess_pieces/white_bishop.png',
    "wN": 'chessrook/chess_pieces/white_knight.png',
    "wQ": 'chessrook/chess_pieces/white_queen.png',
    "wK": 'chessrook/chess_pieces/white_king.png',
    "wP": 'chessrook/chess_pieces/white_pawn.png',
}

def convert_grid_to_dict(grid_board):
    dict_board = {}
    for row in range(0,8):
        for col in range(0,8):
            key = f"cell_{row}{col}"
            value = assets[grid_board[row][col]]
            dict_board[key] = value
    return dict_board    

class PlayerCommandForm(forms.Form):
    cmd = forms.CharField(label="cmd", widget=forms.TextInput(attrs={'id': 'cmd','type':'hidden'}))

class NewGameForm(forms.Form):
    game_name = forms.CharField(max_length=50, label="", widget=forms.TextInput(attrs={
        'id': 'game_name-id',
        'type':"text",
        'class':"form-control game-name",
        'placeholder':'Game Name (50 char or less)',
        'aria-describedby':'basic-addon2'
    }))

class GameEditForm(forms.Form):
    game_name_edit = forms.CharField(label="game_name_edit", widget=forms.TextInput(attrs={'id': 'game_name_edit-id','type':'hidden'}))
    game_notes_edit = forms.CharField(label="game_notes_edit", widget=forms.TextInput(attrs={'id': 'game_notes_edit-id','type':'hidden'}))

gameplay_monitor_instance_USER = -1
game_req_USER = -1
game_id_USER = -1
game_replay_snapshot_idx_USER = -1
game_replay_snapshot_len_USER = -1


class GameDisplay():
    def __init__(self, game_id, game_name, game_notes, game_time, status, status_detailed) -> None:
        self.id = game_id
        self.name = game_name
        self.notes = game_notes
        if len(self.notes) >= 184:
            self.mini_notes = game_notes[:184] # first 184 chracters of game notes
        else:
            self.mini_notes = game_notes
        self.time = game_time
        self.status = status
        self.status_detailed = status_detailed

# Create your views here.

def home_screen(request):
    if request.user.is_authenticated:
        return redirect('/home_page')
    else:
        return render(request, "chessrook/home_screen.html")


@login_required
def home_page(request):
    allGames = ChessGames.objects.filter(player=request.user)

    games = []
    for game_obj in allGames:
        gameplay_monitor_instance = pickle.loads(game_obj.game_play_monitor_instance)
        status_detailed = "NIL"
        print(gameplay_monitor_instance)
        if gameplay_monitor_instance.game_end == True:
            status = "Game Over"
            if gameplay_monitor_instance.white_won == True:
                status_detailed = "White Won"
            elif gameplay_monitor_instance.black_won == True:
                status_detailed = "Black Won"
            elif gameplay_monitor_instance.draw == True:
                status_detailed = "Draw"
        else:
            status = "Active"
        games.append(GameDisplay(game_obj.id, game_obj.game_name, game_obj.game_notes, game_obj.date_started, status, status_detailed))

    games.reverse()
    return render(request, "chessrook/home_page.html", {
        "form": NewGameForm(),
        "games": games
    })

@login_required
def serve_test_board(request, id):
    # convert this id str into int
    game_id_req = int(id)

    # obtain this game
    game_req_list = ChessGames.objects.filter(id=game_id_req)
    
    # check if such a valid game exists or not
    if len(game_req_list) == 0:
        # invalid game_id
        return render(request, "chessrook/invalid_game_id.html")
    else:
        # obtain game state
        game_req = game_req_list[0]
        
        # check if this game.player == request.user
        if game_req.player != request.user:
            return render(request, "chessrook/invalid_game_id.html")
        else:
            global game_req_USER
            global game_id_USER
            global gameplay_monitor_instance_USER
            
            game_req_USER = game_req
            game_id_USER = game_id_req
            gameplay_monitor_instance_USER = pickle.loads(game_req.game_play_monitor_instance)

            return HttpResponseRedirect(reverse("chessrook:test_board"))

@login_required
def serve_test_board_new_game(request):
    global game_req_USER
    global gameplay_monitor_instance_USER
        

    if request.method == "GET":
        current_timestamp = time.time()
        new_game_name = f"default_name_{current_timestamp}"
        new_gameplay_monitor_instance = gameplay.GamePlayMonitor()
        new_game_user = request.user
        new_game_req = ChessGames(game_name=new_game_name, game_play_monitor_instance=pickle.dumps(new_gameplay_monitor_instance),player=new_game_user)
        new_game_req.save()

        
        game_req_USER = new_game_req
        gameplay_monitor_instance_USER = new_gameplay_monitor_instance

        return HttpResponseRedirect(reverse("chessrook:test_board"))
    elif request.method == "POST":
        form = NewGameForm(request.POST)
        if form.is_valid():            
            new_game_name = form.cleaned_data["game_name"]
            new_gameplay_monitor_instance = gameplay.GamePlayMonitor()
            new_game_user = request.user
            new_game_req = ChessGames(game_name=new_game_name, game_play_monitor_instance=pickle.dumps(new_gameplay_monitor_instance),player=new_game_user)
            new_game_req.save()

            game_req_USER = new_game_req
            gameplay_monitor_instance_USER = new_gameplay_monitor_instance

            return HttpResponseRedirect(reverse("chessrook:test_board"))

@login_required
def test_board(request):
    global game_req_USER
    global game_id_USER
    global gameplay_monitor_instance_USER

    if game_req_USER == -1:
        return HttpResponseRedirect(reverse('chessrook:home_page'))
    
    game_id_USER = game_req_USER.id
    gameplay_monitor_instance_USER = pickle.loads(game_req_USER.game_play_monitor_instance)

    if gameplay_monitor_instance_USER.game_end == True:
        return redirect(f'/serve_replay_board/{game_id_USER}')
    
    status_detailed = "NIL"
    if gameplay_monitor_instance_USER.game_end == True:
        status = "Game Over"
        if gameplay_monitor_instance_USER.white_won == True:
            status_detailed = "White Won"
        elif gameplay_monitor_instance_USER.black_won == True:
            status_detailed = "Black Won"
        elif gameplay_monitor_instance_USER.draw == True:
            status_detailed = "Draw"
    else:
        status = "Active"
    
    game = GameDisplay(game_req_USER.id, game_req_USER.game_name, game_req_USER.game_notes, game_req_USER.date_started, status, status_detailed)

    master_dict = {}
    master_dict["game"] = game
    master_dict["form"] = PlayerCommandForm()
    master_dict["game_edit_form"] = GameEditForm()
    master_dict.update(convert_grid_to_dict(gameplay_monitor_instance_USER.gstate.board))
    
    bpc_raw = gameplay_monitor_instance_USER.gstate.black_pieces_captured
    bpc_processed = []
    for ele in bpc_raw:
        bpc_processed.append(assets[ele])

    wpc_raw = gameplay_monitor_instance_USER.gstate.white_pieces_captured
    wpc_processed = []
    for ele in wpc_raw:
        wpc_processed.append(assets[ele])

    game_snapshot_list = gameplay_monitor_instance_USER.game_snapshot_list
    white_moves_chess_notation_modified = []
    black_moves_chess_notation_modified = []
    for idx, game_snapshot in enumerate(game_snapshot_list):
        if idx == 0:
            continue
        
        if idx % 2 == 1:
            # white's move
            white_moves_chess_notation_modified.append(game_snapshot.chess_notation_modified)
        else:
            black_moves_chess_notation_modified.append(game_snapshot.chess_notation_modified)
    
    master_dict["white_moves"] = white_moves_chess_notation_modified
    master_dict["black_moves"] = black_moves_chess_notation_modified

    master_dict["bpc_1"] = bpc_processed[:len(bpc_processed)//2]
    master_dict["bpc_2"] = bpc_processed[len(bpc_processed)//2:]
    master_dict["wpc_1"] = wpc_processed[:len(wpc_processed)//2]
    master_dict["wpc_2"] = wpc_processed[len(wpc_processed)//2:]
    master_dict["value_black_captured"] = gameplay_monitor_instance_USER.gstate.value_black_captured
    master_dict["value_white_captured"] = gameplay_monitor_instance_USER.gstate.value_white_captured

    # this ensures that broswer reload is restricted to only two initiators:
    # 1. the initial loading done by serve_test_board/<str:id> route or serve_test_board_new_game
    # 2. the final auto reload at end of game done by Javascript
    game_req_USER = -1

    return render(request, "chessrook/test_board.html", master_dict)

@login_required
def update_game_details(request):
    if request.method == "POST":
        print("Received command via AJAX for edit of game details")
        game_name_edit = request.POST['game_name_edit']
        game_notes_edit = request.POST['game_notes_edit']
        gid = request.POST['gid']

        game_req_GAME = ChessGames.objects.filter(id=gid).first()

        game_req_GAME.game_name = game_name_edit
        game_req_GAME.game_notes = game_notes_edit
        game_req_GAME.save()

        return JsonResponse({
            'edit_status':'edited_successfully'
        })

@login_required
def exe_cmd(request):
    # this view will received AJAX data - cmd of user
    global game_req_USER
    if request.method == "POST":
        print("Received cmd via AJAX")
        form = PlayerCommandForm(request.POST)
        cmd = request.POST['command']
        gid = request.POST['gid']

        game_req_GAME = ChessGames.objects.filter(id=gid).first()
        gameplay_monitor_instance_GAMEID = pickle.loads(game_req_GAME.game_play_monitor_instance)

        if gameplay_monitor_instance_GAMEID.game_end == True:
            # invalid move
            return JsonResponse({
                'cmd_status':'cmd executed',
                'move_status':'invalid'
            })

        # self.game_end = False
        # self.white_won = False
        # self.black_won = False
        # self.draw = False
        # self.draw_due_to_stalemate = False

        if cmd == "WHITE_RESIGN":
            print("WHITE RESIGN")
            gameplay_monitor_instance_GAMEID.game_end = True
            gameplay_monitor_instance_GAMEID.black_won = True
            game_req_GAME.game_play_monitor_instance = pickle.dumps(gameplay_monitor_instance_GAMEID)
            game_req_GAME.save()

            # Javascript will now do a browser reload after getting this confirmation that game has ended
            # doing a reload will essentially call the test_board() function, which uses gameplay_monitor_instance_USER
            # so that needs to be setup as follows
            game_req_USER = game_req_GAME

            return JsonResponse({
                'cmd_status':'cmd executed',
            })

        if cmd == "BLACK_RESIGN":
            print("BLACK RESIGN")
            gameplay_monitor_instance_GAMEID.game_end = True
            gameplay_monitor_instance_GAMEID.white_won = True
            game_req_GAME.game_play_monitor_instance = pickle.dumps(gameplay_monitor_instance_GAMEID)
            game_req_GAME.save()

            # Javascript will now do a browser reload after getting this confirmation that game has ended
            # doing a reload will essentially call the test_board() function, which uses gameplay_monitor_instance_USER
            # so that needs to be setup as follows
            game_req_USER = game_req_GAME

            return JsonResponse({
                'cmd_status':'cmd executed',
            })

        move_type = gameplay_monitor_instance_GAMEID.run_cmd(cmd)
        print(f"black_pieces_captured : {gameplay_monitor_instance_GAMEID.gstate.black_pieces_captured}")
        print(f"value_black_captured = {gameplay_monitor_instance_GAMEID.gstate.value_black_captured}")
        print(f"white_pieces_captured : {gameplay_monitor_instance_GAMEID.gstate.white_pieces_captured}")
        print(f"value_white_captured = {gameplay_monitor_instance_GAMEID.gstate.value_white_captured}")
        print(move_type)
        if move_type == "Valid":
            dict_to_be_rendered_next = convert_grid_to_dict(gameplay_monitor_instance_GAMEID.gstate.board)

            list_black_pieces_captured = gameplay_monitor_instance_GAMEID.gstate.black_pieces_captured
            list_white_pieces_captured = gameplay_monitor_instance_GAMEID.gstate.white_pieces_captured
            value_black_captured = gameplay_monitor_instance_GAMEID.gstate.value_black_captured
            value_white_captured = gameplay_monitor_instance_GAMEID.gstate.value_white_captured
            
            dict_data_in_list_form = []
            for key in dict_to_be_rendered_next:
                dict_data_in_list_form.append(key)
                dict_data_in_list_form.append(f"static/{dict_to_be_rendered_next[key]}") # this is because when Django loads this static asset into the page we need the url excluding static/, but when JS wishes to do same it starts looking from source dir, and for any Django system source dir is always from static/ so this needs to be appended
            
            bpc_raw = gameplay_monitor_instance_GAMEID.gstate.black_pieces_captured
            bpc_processed = []
            for ele in bpc_raw:
                bpc_processed.append(assets[ele])

            wpc_raw = gameplay_monitor_instance_GAMEID.gstate.white_pieces_captured
            wpc_processed = []
            for ele in wpc_raw:
                wpc_processed.append(assets[ele])

            game_snapshot_list = gameplay_monitor_instance_GAMEID.game_snapshot_list
            white_moves_chess_notation_modified = []
            black_moves_chess_notation_modified = []
            for idx, game_snapshot in enumerate(game_snapshot_list):
                if idx == 0:
                    continue
                
                if idx % 2 == 1:
                    # white's move
                    white_moves_chess_notation_modified.append(game_snapshot.chess_notation_modified)
                else:
                    black_moves_chess_notation_modified.append(game_snapshot.chess_notation_modified)

            game_req_GAME.game_play_monitor_instance = pickle.dumps(gameplay_monitor_instance_GAMEID)
            game_req_GAME.save()

            if gameplay_monitor_instance_GAMEID.game_end == True:
                # Javascript will now do a browser reload after getting this confirmation that game has ended
                # doing a reload will essentially call the test_board() function, which uses gameplay_monitor_instance_USER
                # so that needs to be setup as follows
                game_req_USER = game_req_GAME

            return JsonResponse({
                'cmd_status':'cmd executed',
                'move_status':'valid',
                'dict_data_in_list_form':dict_data_in_list_form,
                'bpc_1':list(bpc_processed[:len(bpc_processed)//2]),
                'bpc_2':list(bpc_processed[len(bpc_processed)//2:]),
                'wpc_1':list(wpc_processed[:len(wpc_processed)//2]),
                'wpc_2':list(wpc_processed[len(wpc_processed)//2:]),
                'value_black_captured':value_black_captured,
                'value_white_captured':value_white_captured,
                'white_moves': white_moves_chess_notation_modified,
                'black_moves': black_moves_chess_notation_modified,
                'game_end': gameplay_monitor_instance_GAMEID.game_end
            })
        elif move_type == "QUIT_GAME":
            game_req_GAME.game_play_monitor_instance = pickle.dumps(gameplay_monitor_instance_GAMEID)
            game_req_GAME.save()
            return JsonResponse({
                'cmd_status':'cmd executed'
            })
        else:
            # invalid move
            return JsonResponse({
                'cmd_status':'cmd executed',
                'move_status':'invalid'
            })

@login_required
def serve_replay_board(request, id):
    # convert this id str into int
    game_id_req = int(id)

    # obtain this game
    game_req_list = ChessGames.objects.filter(id=game_id_req)
    
    # check if such a valid game exists or not
    if len(game_req_list) == 0:
        # invalid game_id
        return render(request, "chessrook/invalid_game_id.html")
    else:
        # obtain game state
        game_req = game_req_list[0]

        # check if this game.player == request.user
        if game_req.player != request.user:
            return render(request, "chessrook/invalid_game_id.html")
        else:        
            global game_req_USER
            global game_id_USER
            global gameplay_monitor_instance_USER
            global game_replay_snapshot_idx_USER
            global game_replay_snapshot_len_USER
            
            game_req_USER = game_req
            game_id_USER = game_id_req
            gameplay_monitor_instance_USER = pickle.loads(game_req.game_play_monitor_instance)

            game_replay_snapshot_idx_USER = 0
            game_replay_snapshot_len_USER = len(gameplay_monitor_instance_USER.game_snapshot_list)

            return HttpResponseRedirect(reverse("chessrook:replay_board"))

@login_required
def replay_board(request):
    global game_req_USER
    global game_replay_snapshot_idx_USER
    global game_replay_snapshot_len_USER

    if game_req_USER == -1:
        return HttpResponseRedirect(reverse('chessrook:home_page'))

    print(f"game_replay_snapshot_idx_USER = {game_replay_snapshot_idx_USER}")
    print(f"game_replay_snapshot_len_USER = {game_replay_snapshot_len_USER}")    

    print(gameplay_monitor_instance_USER.game_snapshot_list[game_replay_snapshot_idx_USER].snapshot_gstate_after_cmd.board)
    
    status_detailed = "NIL"
    if gameplay_monitor_instance_USER.game_end == True:
        status = "Game Over"
        if gameplay_monitor_instance_USER.white_won == True:
            status_detailed = "White Won"
        elif gameplay_monitor_instance_USER.black_won == True:
            status_detailed = "Black Won"
        elif gameplay_monitor_instance_USER.draw == True:
            status_detailed = "Draw"
    else:
        status = "Active"
    
    game = GameDisplay(game_req_USER.id, game_req_USER.game_name, game_req_USER.game_notes, game_req_USER.date_started, status, status_detailed)

    master_dict = {}
    master_dict["game"] = game
    master_dict["form"] = PlayerCommandForm()
    master_dict["game_edit_form"] = GameEditForm()
    master_dict["move_number"] = game_replay_snapshot_idx_USER
    master_dict.update(convert_grid_to_dict(gameplay_monitor_instance_USER.game_snapshot_list[game_replay_snapshot_idx_USER].snapshot_gstate_after_cmd.board))
    
    bpc_raw = gameplay_monitor_instance_USER.game_snapshot_list[game_replay_snapshot_idx_USER].snapshot_gstate_after_cmd.black_pieces_captured
    bpc_processed = []
    for ele in bpc_raw:
        bpc_processed.append(assets[ele])

    wpc_raw = gameplay_monitor_instance_USER.game_snapshot_list[game_replay_snapshot_idx_USER].snapshot_gstate_after_cmd.white_pieces_captured
    wpc_processed = []
    for ele in wpc_raw:
        wpc_processed.append(assets[ele])

    game_snapshot_list = gameplay_monitor_instance_USER.game_snapshot_list
    white_moves_chess_notation_modified = []
    black_moves_chess_notation_modified = []
    for idx, game_snapshot in enumerate(game_snapshot_list):
        if idx > game_replay_snapshot_idx_USER:
            break

        if idx == 0:
            continue
        
        if idx % 2 == 1:
            # white's move
            white_moves_chess_notation_modified.append(game_snapshot.chess_notation_modified)
        else:
            black_moves_chess_notation_modified.append(game_snapshot.chess_notation_modified)
    
    master_dict["white_moves"] = white_moves_chess_notation_modified
    master_dict["black_moves"] = black_moves_chess_notation_modified

    master_dict["bpc_1"] = bpc_processed[:len(bpc_processed)//2]
    master_dict["bpc_2"] = bpc_processed[len(bpc_processed)//2:]
    master_dict["wpc_1"] = wpc_processed[:len(wpc_processed)//2]
    master_dict["wpc_2"] = wpc_processed[len(wpc_processed)//2:]
    master_dict["value_black_captured"] = gameplay_monitor_instance_USER.game_snapshot_list[game_replay_snapshot_idx_USER].snapshot_gstate_after_cmd.value_black_captured
    master_dict["value_white_captured"] = gameplay_monitor_instance_USER.game_snapshot_list[game_replay_snapshot_idx_USER].snapshot_gstate_after_cmd.value_white_captured

    # this ensures that broswer reload is restricted to only two initiators:
    # 1. the initial loading done by serve_test_board/<str:id> route or serve_test_board_new_game
    # 2. the final auto reload at end of game done by Javascript
    game_req_USER = -1

    return render(request, "chessrook/replay_board.html", master_dict)

@login_required
def replay_exe_cmd(request):
    # this view will received AJAX data - cmd of user
    if request.method == "POST":
        print("Received cmd via AJAX")
        form = PlayerCommandForm(request.POST)
        cmd = request.POST['command']
        gid = request.POST['gid']
        move_no = int(request.POST['move_number'])

        game_req_GAME = ChessGames.objects.filter(id=gid).first()
        gameplay_monitor_instance_GAMEID = pickle.loads(game_req_GAME.game_play_monitor_instance)

        game_replay_snapshot_len_GAME = len(gameplay_monitor_instance_GAMEID.game_snapshot_list)
        game_replay_snapshot_idx_GAME = move_no

        if cmd == "FWD":
            if game_replay_snapshot_idx_GAME < game_replay_snapshot_len_GAME - 1:
                game_replay_snapshot_idx_GAME += 1

                next_gstate = gameplay_monitor_instance_GAMEID.game_snapshot_list[game_replay_snapshot_idx_GAME].snapshot_gstate_after_cmd
                print("next_gstate.board = ")
                print(next_gstate.board)

                dict_to_be_rendered_next = convert_grid_to_dict(next_gstate.board)

                list_black_pieces_captured = next_gstate.black_pieces_captured
                list_white_pieces_captured = next_gstate.white_pieces_captured
                value_black_captured = next_gstate.value_black_captured
                value_white_captured = next_gstate.value_white_captured
                
                dict_data_in_list_form = []
                for key in dict_to_be_rendered_next:
                    dict_data_in_list_form.append(key)
                    dict_data_in_list_form.append(f"static/{dict_to_be_rendered_next[key]}") # this is because when Django loads this static asset into the page we need the url excluding static/, but when JS wishes to do same it starts looking from source dir, and for any Django system source dir is always from static/ so this needs to be appended
                
                bpc_raw = next_gstate.black_pieces_captured
                bpc_processed = []
                for ele in bpc_raw:
                    bpc_processed.append(assets[ele])

                wpc_raw = next_gstate.white_pieces_captured
                wpc_processed = []
                for ele in wpc_raw:
                    wpc_processed.append(assets[ele])

                game_snapshot_list = gameplay_monitor_instance_GAMEID.game_snapshot_list
                white_moves_chess_notation_modified = []
                black_moves_chess_notation_modified = []
                for idx, game_snapshot in enumerate(game_snapshot_list):
                    if idx > game_replay_snapshot_idx_GAME:
                        break

                    if idx == 0:
                        continue
                    
                    if idx % 2 == 1:
                        # white's move
                        white_moves_chess_notation_modified.append(game_snapshot.chess_notation_modified)
                    else:
                        black_moves_chess_notation_modified.append(game_snapshot.chess_notation_modified)

                return JsonResponse({
                    'cmd_status':'cmd executed',
                    'replay_status':'valid',
                    'dict_data_in_list_form':dict_data_in_list_form,
                    'bpc_1':list(bpc_processed[:len(bpc_processed)//2]),
                    'bpc_2':list(bpc_processed[len(bpc_processed)//2:]),
                    'wpc_1':list(wpc_processed[:len(wpc_processed)//2]),
                    'wpc_2':list(wpc_processed[len(wpc_processed)//2:]),
                    'value_black_captured':value_black_captured,
                    'value_white_captured':value_white_captured,
                    'white_moves': white_moves_chess_notation_modified,
                    'black_moves': black_moves_chess_notation_modified,
                    'move_number': game_replay_snapshot_idx_GAME
                })

            else:
                return JsonResponse({
                    'cmd_status':'cmd executed',
                    'replay_status':'game_overflow'
                })
            
        elif cmd == "REV":
            if game_replay_snapshot_idx_GAME > 0:
                game_replay_snapshot_idx_GAME -= 1

                next_gstate = gameplay_monitor_instance_GAMEID.game_snapshot_list[game_replay_snapshot_idx_GAME].snapshot_gstate_after_cmd

                dict_to_be_rendered_next = convert_grid_to_dict(next_gstate.board)

                list_black_pieces_captured = next_gstate.black_pieces_captured
                list_white_pieces_captured = next_gstate.white_pieces_captured
                value_black_captured = next_gstate.value_black_captured
                value_white_captured = next_gstate.value_white_captured
                
                dict_data_in_list_form = []
                for key in dict_to_be_rendered_next:
                    dict_data_in_list_form.append(key)
                    dict_data_in_list_form.append(f"static/{dict_to_be_rendered_next[key]}") # this is because when Django loads this static asset into the page we need the url excluding static/, but when JS wishes to do same it starts looking from source dir, and for any Django system source dir is always from static/ so this needs to be appended
                
                bpc_raw = next_gstate.black_pieces_captured
                bpc_processed = []
                for ele in bpc_raw:
                    bpc_processed.append(assets[ele])

                wpc_raw = next_gstate.white_pieces_captured
                wpc_processed = []
                for ele in wpc_raw:
                    wpc_processed.append(assets[ele])

                game_snapshot_list = gameplay_monitor_instance_GAMEID.game_snapshot_list
                white_moves_chess_notation_modified = []
                black_moves_chess_notation_modified = []
                for idx, game_snapshot in enumerate(game_snapshot_list):
                    if idx > game_replay_snapshot_idx_GAME:
                        break

                    if idx == 0:
                        continue
                    
                    if idx % 2 == 1:
                        # white's move
                        white_moves_chess_notation_modified.append(game_snapshot.chess_notation_modified)
                    else:
                        black_moves_chess_notation_modified.append(game_snapshot.chess_notation_modified)

                return JsonResponse({
                    'cmd_status':'cmd executed',
                    'replay_status':'valid',
                    'dict_data_in_list_form':dict_data_in_list_form,
                    'bpc_1':list(bpc_processed[:len(bpc_processed)//2]),
                    'bpc_2':list(bpc_processed[len(bpc_processed)//2:]),
                    'wpc_1':list(wpc_processed[:len(wpc_processed)//2]),
                    'wpc_2':list(wpc_processed[len(wpc_processed)//2:]),
                    'value_black_captured':value_black_captured,
                    'value_white_captured':value_white_captured,
                    'white_moves': white_moves_chess_notation_modified,
                    'black_moves': black_moves_chess_notation_modified
                })
            else:
                return JsonResponse({
                    'cmd_status':'cmd executed',
                    'replay_status':'game_underflow'
                })

        else:
            return JsonResponse({
                'cmd_status':'cmd executed',
                'replay_status':'invalid'
            })