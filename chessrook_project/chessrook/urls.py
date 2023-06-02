from django.urls import path
from . import views

app_name = 'chessrook'

urlpatterns = [
	path("", views.home_screen, name="home_screen"),
	path("home_page", views.home_page, name="home_page"),
	path("serve_test_board/<str:id>", views.serve_test_board, name="serve_test_board"),
	path("serve_test_board_new_game", views.serve_test_board_new_game, name="serve_test_board_new_game"),
	path("test_board", views.test_board, name="test_board"), 
	path("exe_cmd", views.exe_cmd, name="exe_cmd"),
	path("serve_replay_board/<str:id>", views.serve_replay_board, name="serve_replay_board"),
	path("replay_board", views.replay_board, name="replay_board"),
	path("replay_exe_cmd", views.replay_exe_cmd, name="replay_exe_cmd"),
	path("update_game_details", views.update_game_details, name="update_game_details")
]