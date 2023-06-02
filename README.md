# Project Overview
Chessrook is a fully functional web application built using Python Django Framework in the back-end with the front-end consisting of HTML, CSS and Javascript with additional frontend frameworks like JQuery and Bootstrap that allows users to play entire chess games following valid and legal chess gameplay facilitated using Chessrook's built-in robust Chess Engine.

I personally love to play Chess and always wanted to improve my game. According to experts in the field of Chess, two things are required in order to achieve Chess mastery. One of them is playing chess games with yourself. This enhances your thinking power, and the second is to analyze past games. 

Although there are multipe websites out there that allow to play chess games, I could never really find the correct analysis tools like game notes, archiving past chess games, etc. features that Chessrook offers. This was the main motivation behind building Chessrook.

# How to run the application
## Step 1:

Clone this repo from Github

### Directory Structure
- CHESSROOK_CHESSENGINE_WEBAPP [dir] (repo name)
    - chessrook_project [dir]
        - chessrook_project [dir]
        - chessrook [dir]
        - users [dir]
        - manage.py
    - README.md
    - requirements.txt

## Step 2:

#### **For Windows**
Create a virtual environment as follows:

In the dir `CHESSROOK_CHESSENGINE_WEBAPP` open cmd and execute:

```shell
python -m venv chessrook_env
```

Activate the venv as follows: 

In that same directory open terminal and execute:
```shell
chessrook_env\Scripts\activate
```

#### **For Linux**
Create a virtual environment as follows:

If this is your first time creating a virtual environment in your Linux machine, then run the following command:

```shell
sudo apt install -y python3-venv
```

In the dir `CHESSROOK_CHESSENGINE_WEBAPP` open terminal and execute:

```shell
python -m venv chessrook_env
```

Activate the venv as follows:

In that same directory open terminal and execute:
```shell
source chessrook_env/bin/activate
```

## Step 3:

Install the necessary dependencies using pip and the `requirements.txt` file
```shell
pip install -r requirements.txt
```

## Step 4:

Create a `.env` file to store your `SECRET_KEY` and `DEBUG` status

Create a new file name `.env` inside your `CHESSROOK_CHESSENGINE_WEBAPP/chessrook_project` dir (Thus .env file will be alongside the manage.py file)

Inside the file write:
```txt
SECRET_KEY=<any_alphanumeric_combination>
DEBUG=1 [for DEBUG properties to be on]
DEBUG=0 [for DEBUG properties to be off]
```

Example:
```txt
SECRET_KEY=kpsopwjkb3ki720801nk1bkh2972j
DEBUG=1
```

## Step 5:

Apply all the migrations

Open cmd or terminal in the `CHESSROOK_CHESSENGINE_WEBAPP/chessrook_project` dir which contains the `manage.py` file and execute the command as follows:

```shell
python manage.py migrate 
```


## Step 6:

Start the server

Open cmd or terminal in the `CHESSROOK_CHESSENGINE_WEBAPP/chessrook_project` dir which contains the `manage.py` file and execute the command as follows:

```
python manage.py runserver
```

#### Optional Task:
To visualize the backend and database you may create a superuser as follows:

Open cmd or terminal in the `CHESSROOK_CHESSENGINE_WEBAPP/chessrook_project` dir which contains the `manage.py` file and execute the command as follows:

```shell
python manage.py createsuperuser
```

Follow the prompts
Then you can visit the `/admin` route and enter super user credentials and view the admin page.

## Step 7:

- Open http://127.0.0.1:8000/ in browser, and you will be welcome with the Chessrook Home Screen.
- You can now click Register and create an account, after which you can login to chessrook
- After logging in for first time, you won't have any games showing up in your home page. Go ahead and start a new game, by typing a name for your game and clicking the new game button


# Distinctiveness and Complexity

1. Chessrook has an aesthetically pleasing **Home Screen** (not signed in view) that welcomes users to Chessrook encouraging to Create an Account or Sign In, built using Bootstrap Cover.

2. Chessrook has a **Register** page that asks user to enter details for registering in Chessrook system. A modern account creation form designed using Bootstrap and the Django User Creation form in backend. It also has a redirection prompt and link to to Sign In page.

3. Chessrook has a **Login** page that asks users to enter username and password and post verification either grants or denies entry into Chessrook system. A modern login page form designed using Bootstrap and the Django User Login form in backend. It also has a redirection prompt and link to to Sign Up page.

4. Chessrook features a **Nav Bar** that changes its contents based on whether user is logged in or not. It has the following buttons (when user is logged in):
    - **Logout**
    - **Profile**
    - **Chessrook Name** which always redirects to **User Home Page**

    And has the following buttons (when user is not logged in):
    - **Login**
    - **Register**
    - **Chessrook Name** which always redirects to **Home Screen**

<br>

5. Chessrook has a **User Home Page** that consists of multiple sub features:
    - **Create New Game System** : It has a input area where user enters name of game *(It has checks to accept only game names that are 50 character or less)* and New Game Button, which when pressed redirects to a page displaying a brand new chess game for the user. The new game is created under the account of that user (who is logged in)
    
    - **All Games Section**: An aesthetic, structured grid and card system (using Bootstrap) that displays all games created by the user (both Active Games and games that are Over). If there are no games, then Bootstrap Alert is displayed stating it. Games created by current logged in user are only shown here.

    - **Structure of a card for a game**:             
        - **Name of game**
        - **Id of game** in a red badge
        - **Status of Game** *(Active or Game Over)* in a yellow badge
        - **Date of game creation**
        - **Games Notes**: The Game Notes is written by user to describe the game, make notes of important sections of game, why certain moves were made, and so on. This field has a max limit of 5000 characters, but only the first 184 characters are displayed here in the view.
        - **Resume** button (green colored) which when pressed takes user to game exactly where he/she last left of. It redirects user to the /test_board route with game data preloaded, for currently active games.
        - **Analyze** button (blue colored) which when pressed takes user to the /replay_board route with game data preloaded, for games that are over.

<br>

6. Chessrook has an **Active Gameplay System**. Pressing the **New Game** or **Resume** button in the card views of games in home page, opens up the gameplay system with that particular game loaded. The Active Gameplay System is at the heart of Chessrook web app.

    - **ChessBoard Master Layout**: The left hand side of the page consists of the master layout of the chess board, which consists of the subsections:
        - **Chess Board**: a 8*8 chess board following all the traditional requirements of a chess board.
        - **Captured Pieces**: Above and below the board there is a light green rectangular section that shows all the pieces captured by both sides as the game progresses.
        - **Value of Pieces Captured**: In Chess every piece has a value associated with it. Queen: 9, Rook: 5, Bishop: 3, Knight: 3, Pawn: 1. Above and below the board there is a dark green rectangular section that shows value of all the pieces captured by both sides as the game progresses.
    - **Giving Moves**: Firstly Chessrook allows users to give chess moves by just clicking the piece they wish to move, and then click on where to move that piece. The square where the piece is present originally gets colored green, while the destination square gets colored blue. All this is facilitated using Javascript. The Javascript engine understands what is the intended move of the user and sends that info to backend, where the intended move is verified, if its a valid move, a green signal is given to Javascript and it makes the move, otherwise if the intended move is invalid, no action is taken. If a user selects a square by mistake, then he/she can deselect that square easily by clicking on that square again.
    - **Result of Giving a valid Move**: Chessrook is highly dynamic, as soon as valid move is given, changes are made to both the backend (done by Python-Django) as well asynchronously made to the frontend using Javascript AJAX (discussed later in depth) as follows:
            1. The origin piece is moved to its destination position from its original position
            2. The captured piece if any is removed and put in the captured pieces section
            4. The value of the captured pieces is adjusted.
            5. The move made gets displayed in the move table.
            6. If the move made results in a end game scenario, i.e Checkmate or a  Stalemate, then Chessrook treats it as a special case, and this is the only time when Javascript performs an auto reload alongside its AJAX call. Then badges are added beside the game name on the right indicating game status as Game Over and Results of the game

    - **Instrumentation Cluster**: The entire right hand side of the page constitutes the instrumentation cluster that provides valueable information related to the game as follows:
        - **Game Details** section on the top: 
            - **Name of game**. It also has a Edit button, which when clicked opens a Javascript Prompt containing the current game name. The user can then change accordingly and press OK, following which a check of <= 50 character will be made post which it will be reflected in real time and also sent to Django in backend.
            - **Id of game** in a red badge
            - **Status of Game** *(Active or Game Over)* in a yellow badge, as well as details about who won (White or Black), in case the game was not a draw.
            - **Date of game creation**
        - **Button Cluster**:
            - **QUIT** button which when pressed redirects to the home page
            - **UNDO** button which when pressed undoes the last move made in the game.
            - **White Resign** button which White should press when he/she decides to Resign from the game, the game then ends and Black Wins
            - **Black Resign** button which Black should press when he/she decides to Resign from the game, the game then ends and White Wins
        - **Move Table**: All the move made during the game gets displayed in the move table in a simplified chess notation devised by me, which is more beginner friendly, and offers greater clarity
        - **Game Notes**: The game notes section features an area where the game notes is displayed. It also has a Edit button, which when clicked opens a Javascript Prompt containing the current game notes. The user can then change accordingly and press OK, following which a check of <= 5000 character will be made post which it will be reflected in real time and also sent to Django in backend.

<br>

7. Chessrook has a **Game Replay System**. Pressing the **Analyze** button in the card views of games in home page, opens game replay system with that particular game loaded.

    - **ChessBoard Master Layout**: The left hand side of the page consists of the master layout of the chess board, which consists of the subsections:
        - **Chess Board**: a 8*8 chess board following all the traditional requirements of a chess board like the pieces, alternating colored (dark and light) squares and file and rank notation on the edges of the board
        - **Captured Pieces**: Above and below the board there is a light green rectangular section that shows all the pieces captured by both sides as the game progresses or goes backwards when user clicks FWD or REV buttons respectively. The box above the black pieces showes all the white pieces that black captured and the box below the white pieces shows all the black pieces that white captured
        - **Value of Pieces Captured**: In Chess every piece has a value associated with it. Queen: 9, Rook: 5, Bishop: 3, Knight: 3, Pawn: 1. Above and below the board there is a dark green rectangular section that shows value of all the pieces captured by both sides as the game progresses or goes backwards when user clicks FWD or REV buttons respectively. The box above the black pieces showes value of all the white pieces that black captured and the box below the white pieces shows value of all the black pieces that white captured

    - **Replaying the game**: The game can be replayed using **FWD** and **REV** buttons. In the backend, Chessrook keeps extensive snapshots of each state of the game and all its details. This allows user to seamlessly replay through the game similar to way one replays a video. We can unfold the next move played by clicking the **FWD** button and go back a move by clicking the **REV** button. If the board is at start state **REV** will not work, and if the game is at end state **FWD** will not work.
    - **Result of replaying the game**: Chessrook is highly dynamic, as soon as **FWD** or **REV** buttons are pressed, changes are made to both the backend (done by Python-Django) as well asynchronously made to the frontend using Javascript AJAX (discussed later in depth) as follows:
            1. The origin piece is moved to its destination position from its original position
            2. If there is an enemy piece (other than King) in destination square then it is removed from the board. This piece is called a captured piece
            3. The captured piece (if any) is moved to its appropriate position in captured pieces section
            4. The value of the captured pieces (if any) is added to total value of captured pieces and displayed accordingly.
            5. The move made gets displayed in the move table on the right in a simplified chess notation devised by me, which is more beginner friendly, and offers greater clarity. That is even in replay, the moves made appear just as in they were made in the actual game, its a dynamic setup.
    - **Instrumentation Cluster**: The entire right hand side of the page constitutes the instrumentation cluster that provides valueable information related to the game as follows:
        - **Game Details** section on the top: 
            - **Name of game**. It also has a Edit button, which when clicked opens a Javascript Prompt containing the current game name. The user can then change accordingly and press OK, following which a check of <= 50 character will be made post which it will be reflected in real time and also sent to Django in backend.
            - **Id of game** in a red badge
            - **Status of Game** *(Active or Game Over)* in a yellow badge, as well as details about who won (White or Black), in case the game was not a draw.
            - **Date of game creation**
        - **Button Cluster**:
            - **QUIT** button which when pressed redirects to the home page
            - **REV** go back a move
            - **FWD** unfold the next move played.
            - there is also a small badge (aqua blue colored) that shows the **Move Number** (0 - indexed).
        - **Move Table**: All the move made during the game gets displayed in the move table in a simplified chess notation devised by me, which is more beginner friendly, and offers greater clarity
        - **Game Notes**: The game notes section features an area where the game notes is displayed. It also has a Edit button, which when clicked opens a Javascript Prompt containing the current game notes. The user can then change accordingly and press OK, following which a check of <= 5000 character will be made post which it will be reflected in real time and also sent to Django in backend.

<br>

8. The **Core Chess Engine** is what drives the entire Chessrook web app and makes it functional. The entire blueprint of a valid chess game is embedded inside it. It is manifested as the chess_engine.py file. Chess as a game has quite the complexity and exceptions which are all handled by the core chess engine as follows:
    - The game has multiple types of piece each having different values and abilities
    - Different pieces follow differt rules wrt movement in the board:
        - Pawn move straight but only in steps of 1
        - Bishop moves diagonally
        - Knight moves in a 2-units horizontal and 1-unit vertical or 1-unit horizontal and 2-units vertical method
        - Rook moves vertically as well as horizontally
        - Queen can move diagonally as well as vertically and horizontally
        - King can move 1 unit in all directions
    - Logic of piece capture varies depending on the piece being captured, for e.g.:
        - the King cannot be captured
        - white cannot capture white pieces
        - black cannot capture black pieces
    - While normal pieces get captured, the King undergoes what is called a Check. When the King is under Check, the player must first attempt to put his/her King out of Check. We need to write logic to detect when the King is under Check and when its Safe
    - The possible valid/legal moves in game of Chess depends heavily on the game state.
        - Firstly the move itself has to satisfy all the criteria relating to movement of piece and capture of piece as discussed above
        - Secondly the move must ensure that after the move is made, it doesn't automatically put the King in a check. This conception leads to number of Chess intricacies like Forks, Pins e.t.c.
    - At each and every state of the game we need to monitor whether it has reached an end game scenario:
        - Checkmate: a special scenario in the game where the player has no valid move to make and the King is under check (basically cannot put King in a safe state and currently King is under attack)
        - Stalemate: a special scenario in the game where the player has no valid move to make and the King is not under check
    - Apart from this there are some special nuances of the game of Chess as follows:
        - Pawn Promotion: When a pawn is moved to it's last rank, it has to be replaced with any a Bishop, Knight, Rook or Queen.
        - En Passant: it is a special case of pawn movement where a pawn captures a horizontally adjacent enemy pawn that has just made an initial two-square advance. En Passant is especially tricky as it has state or temporal sensitivity. That is the diagonal capture or the horizontal pawn needs to happen just after the two-square advance. If some intermediate move is made, right to perform En Passant expires.
        - Castling: it is a special Rook and King simultaneous movement used to put the King in a safe spot in the board. Casting is extremely tricky as it has both spatial and temporal sensitivity as follows:
            - The king and rook need to be in their initial position
            - The king and rook shouldn't have been moved throughout the games
            - There shouldn't be any piece (irrespective of black or white) between the King and Rook
            - The king shouldn't be under Check
            - Any intermediate square between King and Rook should also not be under attack. As if the King should not experience a pseudo Check as it traverses the intermediate squares
            - The final position of the King after Castling shouldn't be under Check
        Adding further to complexity, castling can be of two types Long Castling and Short Castling

<br>

9. The **Core Chess Engine** that we discussed above contains all the methods that are required to facilitate valid chess gameplay. However these methods and utilities are not available to end user satisfying Abstraction and Encapsulation Principles of Object Oriented Programming. This led to the birth of the **Intermediate Gameplay System**. It manifests as **`gameplay.py`** as well as in some methods of **`views.py`** and heavily in **`ajax.html`**, **`replay_ajax.html`**. 

    Thus commands from the user which are obtain in form of clicks are processed using the **Intermediate Gameplay System**. Here basically we process and figure out the intended move of the user. This intended move is then executed with the help of API of the **Core Chess Engine**

<br>

- Chessrook utilizes two Django models in backend:
    - Users (which stores all user data for the web app)
    - ChessGames (which stores all the games every played in the web app)

- Chessrook uses Javascript (as well as JQuery) in the front-end which facilitates its AJAX calls and asynchronous updates to the site as the game is going on without any browser refresh or reload. The entire Javascript code for Chessrook can be found in the following two files:
    - /chessrook/templates/chessrook/**`ajax.html`**
    - /chessrook/templates/chessrook/**`replay_ajax.html`**

    The AJAX Integration of Chessrook is [discussed in details below](#robust-and-extensive-ajax-integration).

<br>

- Chessrook is completely mobile responsive. 
- Multiple elements of components of front-end of chessrook have CSS Styling that changes based on screen properties like width and height. 
- This allows user to always have the best possible layout of Chessrook irrespective of whether he/she is viewing the app in Laptop, Tablet or Smartphone.
- The screen dimension dependent CSS Code is present in both the /chessrook/static/chessrook/**`styles.css`** file as well as in select html files inside script tags.

<br>

# Documentation of the Project

## Models
1. ### Users
    Built-in model of Django\
    **Fields:**
    - **`username`** (type - CharField) [*To store the username of the user*]
    - **`first_name`** (type - CharField) [*To store the first name of the user*]
    - **`last_name`** (type - CharField) [*To store the last name of the user*]
    - **`email`** (type - CharField) [*To store the email of the user*]
    - **`password`** (type - CharField) [*To store the password of the user*]
    
    <br>

    **Requirement and Use Case:**
    - Everytime a new user registers, the user data is stored in the database under this model
    - Everytime a user logs into the system, the username and password are verified against this model
    - When a user wishes to view his/her profile details, the data is fetched from this model
    - When a user wishes to edit his/her profile details, the CRUD operations are performed against this model

2. ### ChessGames
    Model created for Chessrook to store every game played in the system\
    **Fields:**
    - **`game_name`** (type - CharField) (max_length = 50) [*To store the name of the game*]
    - **`game_play_monitor_instance`** (type - BinaryField) [*Internally the chess game and all its assets is processed as a Python object of the class **GamePlayMonitor**. When we wish to store this data in database, it is converted to Binary Byte Stream using the **pickle** module of Python*]
    - **`date_started`** (type - DateTimeField) [*To store the date and time when the game was created*]
    - **`player`** (type - ForeignKey w.r.t the **User** Model) [*To store the player who is owner/player of this game. When displaying or accessing games, a user is able to view, play, and replay games that have been created by him/her, i.e they are the owner/player of that game*]
    - **`game_notes`** (type - CharField) (max_length = 5000) [*To store notes for a game, that a player can refer to later while revising the game. One of the most important aspects of Game Analysis which I longed for dearly but wasn't available in most platforms in the Internet*]

    <br>

    **Requirement and Use Case:**
    - Everytime a new game is created, an entry corresponding to that game is made in the database against this model
    - When a user requests to open a game either for playing or replay analysis, the game is fetched from this model
    - As a player is playing the game, and moves are being made, pieces are being captured, the state of game changes with every move. These changes are processed and get reflected in the **GamePlayMonitor** object. This object is then pickled and stored in the database against that game in real time. This means if user suddenly closes the game, all changes are automatically saved.
    - Changes to game name, game notes also get updated in this model

## URL Routing
### URL Routing of the project
1. **Admin** - **`/admin`**

    The Admin site which super users and site administrators can use to make changes to the web app's models

2. **Register** - **`/register`**

    User can register into chessrook by filling up the registration form. GET request to this route calls the **`register`** view in /users/**`views.py`**

3. **Login** - **`/login`**

    User can login into chessrook by providing username and password. GET request to this route calls the **`auth_views.LoginView.as_view`** view, which is Django's built in User Login View imported from **`django.contrib.auth`**

4. **Logout** - **`/logout`**

    Logs user out of the web app. GET request to this route calls the **`auth_views.LogoutView.as_view`** view, which is Django's built in User Logout View imported from **`django.contrib.auth`**

5. **Profile** - **`/profile`**

    User can view their profile by visiting this route. GET request to this route calls the **`profile`** view in /users/**`views.py`**

6. **Update Profile** - **`/profile_update`**

    User can update their profile by visiting this route. GET request to this route calls the **`profile_update`** view in /users/**`views.py`**

7. **Routing to chessrook app** - **`/`**

    Redirects all URL Routing to /chessrook/**`urls.py`**

### URL Routing of the chessrook app
1. **Home Screen** - **`/`**
    The home screen of chessrook that is presented to a user who is not logged into the system. GET request to this route calls the **home_screen** view of /chessrook/**`views.py`**


2. **Home Page** - **`/home_page`**
    The home page of chessrook that displays all games played by user who is logged into the system. GET request to this route calls the **home_page** view of /chessrook/**`views.py`**

3. **Serve Test Board** - **`/serve_test_board/<str:id>`**
    Parameterized URL route. GET request to this route calls the **serve_test_board** view of /chessrook/**`views.py`**. The id of the game is passed on

4. **Serve Test Board New Game** - **`/serve_test_board_new_game`**
    GET request to this route calls the **serve_test_board_new_game** view of /chessrook/**`views.py`**

5. **Test Board** - **`/test_board`**
    GET request to this route calls the **test_board** view of /chessrook/**`views.py`**. However by design user should never have to request this route. User indirectly using the **Serve Test Board** and **Serve Test Board New Game** makes request for active game to resume or to play a new game. Internally a call to this route is made, and all assets for that game are loaded

6. **Execute Command** - **`/exe_cmd`**
    POST request to this route is made by AJAX Javascript code in the front-end which calls the **exe_cmd** view of /chessrook/**`views.py`**

7. **Serve Replay Board** - **`/serve_replay_board/<str:id>`**
    Parameterized URL route. GET request to this route calls the **serve_replay_board** view of /chessrook/**`views.py`**. The id of the game is passed on

8. **Replay Board** - **`/replay_board`**
    GET request to this route calls the **replay_board** view of /chessrook/**`views.py`**. However by design user should never have to request this route. User indirectly using the **Serve Replay Board** makes request for replaying a game. Internally a call to this route is made, and all assets for that game are loaded

9. **Replay Execute Command** - **`/replay_exe_cmd`**
    POST request to this route is made by AJAX Javascript code in the front-end which calls the **replay_exe_cmd** view of /chessrook/**`views.py`**

10. **Update Game Details** - **`/update_game_details`**
    POST request to this route is made by AJAX Javascript code in the front-end which calls the **update_game_details** view of /chessrook/**`views.py`**

## Views
### Views, Functions, and Classes of the chessrook app
1. ```python 
    def convert_grid_to_dict(grid_board) 
    ```
    Internally the methods of chess_engine.py and gameplay.py work with a 2D grid to represent the chess board. However while rendering the board in html, we need to pass the information of the board in form of a dict. This is facilitated by this function

2. ```python 
    class PlayerCommandForm(forms.Form)
    ```
    The command of the user given using mouse and button clicks be it a **move of a piece** or pressing any of buttons like **UNDO**, **REV**, **FWD** is extracted by Javascript, and converted into a text based command, populates it inside the PlayerCommandForm and then sent to the **`views.py`** using a AJAX call via POST request

3. ```python 
    class NewGameForm(forms.Form)
    ```
    This form is used for obtaining the name of the game while creating a new game. User fills this details in the front-end and presses new game button, the data is then sent by a POST request

4. ```python 
    class GameEditForm(forms.Form)
    ```
    When the user wishes to edit the name of game or game notes, and presses the corresponding Edit buttons, Javascript presents an prompt, and extracts the data filled in it by user and then populates it inside the GameEditForm and then sent to the **`views.py`** using a AJAX call via POST request 

5. ```python
    class GameDisplay()
    ```
    This class is used to maintain all the data about a game that is displayed in the home page

6. ```python
    def home_screen(request)
    ```
    This is a view that is called when the **`/`** route is requested via a GET request. It renders the **`home_screen.html`** template

7. ```python
    @login_required
    def home_page(request)
    ```
    This is view that displays the home page when the **`/home_page`** route is requested via GET
    
    *This view is available only for logged in users*

8. ```python
    @login_required
    def serve_test_board(request, id)
    ```
    This is view that gets called when the **`/serve_test_board/<str:id>`** route is requested via GET
    It first fetches the game with this parameter id, if not found renders the **`invalid_game_id.html`** template. 
    If found then it loads the assets of this game from the database and then stores it in memory and makes GET request to the **`/test_board`** route
    
    *This view is for active gameplay.*\
    *This view is available only for logged in users*

9. ```python
    @login_required
    def serve_test_board_new_game(request)
    ```
    This view can be accessed by two ways:
    - Generally users should fill in game name and press the new game button in home page, a POST request is then sent to this view, and a new game with this game name and current date and time is created and stored in database.
    It then loads this game and all its assets into memory and makes GET request to the **`/test_board`** route
    - A GET request can also be made, in that case a default name as follows: **`f"default_name_{current_timestamp}"`** is assigned and a new game with this game name and current date and time is created and stored in database.
    It then loads this game and all its assets into memory and makes GET request to the **`/test_board`** route
    
    *This view is for active gameplay.*\
    *This view is available only for logged in users*

10. ```python
    @login_required
    def test_board(request)
    ```
    As discussed above the **`serve_test_board_new_game`** and **`serve_test_board`** load assets of the game into global memory variables. These variables are:

    ```python
    global game_req_USER
    global game_id_USER
    global gameplay_monitor_instance_USER
    ```

    The **`test_board`** view first checks whether the GET request made to it is valid (i.e system generated via the **`serve_test_board_new_game`** and **`serve_test_board`** views). This validity check can be done based on the value of the above global variables. If it is -1, its an invalid request, and redirection to **`home_page`** is performed. But if thats not the case then the value presiding is the one loaded by **`serve_test_board_new_game`** and **`serve_test_board`**, and **`test_board`** accordingly renders it via the **`test_board.html`** template. Once this is done, this view doesn't handle the active gameplay. That is handled by **`exe_cmd`** view.

    *This view is for active gameplay.*\
    *This view is available only for logged in users*

11. ```python
    @login_required
    def update_game_details(request)
    ```
    When the user wishes to edit the name of game or game notes, and presses the corresponding Edit buttons, Javascript presents an prompt, and extracts the data filled in it by user and then populates it inside the GameEditForm and then sent to this view using a AJAX call via POST request.

    The view then saves this updated details in the database, returns a JsonResponse.

    *This view is for both active gameplay and game replay.*\
    *This view is available only for logged in users*

12. ```python
    @login_required
    def exe_cmd(request)
    ```
    The command of the user given using mouse and button clicks be it a **move of a piece** or pressing buttons like **UNDO**, is extracted by Javascript, and converted into a text based command, populates it inside the PlayerCommandForm and then sent to this view using a AJAX call via POST request.

    The view then using the API from **`gameplay.py`** and **`chess_engine.py`** executes this move (after performing validation checks of its own).

    After the move or command is executed firstly necessary changes are made to the database entry for this game. Then the modified assets of the game are sent to Javascript in the front-end, which asynchronously makes changes to web page without the need of any browser reloads.

    *This view is for active gameplay.*\
    *This view is available only for logged in users*

13. ```python
    @login_required
    def serve_replay_board(request, id)
    ```
    This is view that gets called when the **`/serve_replay_board/<str:id>`** route is requested via GET
    It first fetches the game with this parameter id, if not found renders the **`invalid_game_id.html`** template. 
    If found then it loads the assets of this game from the database and then stores it in memory and makes GET request to the **`/test_board`** route
    
    *This view is for game replay.*\
    *This view is available only for logged in users*

14. ```python
    @login_required
    def replay_board(request)
    ```
    As discussed above the **`serve_replay_board`** loads assets of the game into global memory variables. These variables are:

    ```python
    global game_req_USER
    global game_replay_snapshot_idx_USER
    global game_replay_snapshot_len_USER
    ```

    The **`replay_board`** view first checks whether the GET request made to it is valid (i.e system generated via the **`serve_replay_board`** view). This validity check can be done based on the value of the above global variables. If it is -1, its an invalid request, and redirection to **`home_page`** is performed. But if thats not the case then the value presiding is the one loaded by **`serve_replay_board`**, and **`replay_board`** accordingly renders it via the **`replay_board.html`** template. Once this is done, this view doesn't handle the game replay. That is handled by **`replay_exe_cmd`** view.

    *This view is for game replay.*\
    *This view is available only for logged in users*

15. ```python
    @login_required
    def replay_exe_cmd(request)
    ```
    The command of the user given by pressing any of buttons like **REV**, **FWD** is extracted by Javascript, and converted into a text based command, populates it inside the PlayerCommandForm and then sent to this view using a AJAX call via POST request.

    The view then using the API from **`gameplay.py`** and **`chess_engine.py`** executes this move (after performing validation checks of its own).

    After the move or command is executed then the modified assets of the game are sent to Javascript in the front-end, which asynchronously makes changes to web page without the need of any browser reloads.

    *This view is for game replay.*\
    *This view is available only for logged in users*

### Views and forms of the users app
1. ```python
    def register(request)
    ```
    This view handles user registration. It can be called via both a GET request and a POST request to the **`/register`** route.

    If requested via GET, then an empty **`UserRegistrationForm`** form is rendered.

    If the user fills up the form and sends request via POST method, then first validation checks are performed on the form data. If form data is not valid, the Registration form filled by user is rendered again with appropriate error messages. Otherwise if the form data is valid, then we simply save the form. This form is already linked to the model **`User`**. Thus saving the form, saves that entry in the database against the **`User`** model.

2. ```python
    @login_required
    def profile(request)
    ```
    GET request to this view renders the profile details of current logged in user.

    *This view is available only for logged in users*

3. ```python
    @login_required
    def profile_update(request):
    ```
    This view handles user profile details updation. It can be called via both a GET request and a POST request to the **`/profile_update`** route.

    If requested via GET, then an empty **`UserUpdateForm`** form is rendered.

    If the user fills up the form and sends request via POST method, then first validation checks are performed on the form data. If form data is not valid, the Registration form filled by user is rendered again with appropriate error messages. Otherwise if the form data is valid, then we simply save the form. This form is already linked to the model **`User`**. Thus saving the form, saves that entry in the database against the **`User`** model.

4. ```python
    class UserRegistrationForm(UserCreationForm)
    ```
    This is the User Registration Form that is used to obtain user details from the front-end during user registration. The form is linked to model **`User`**.

5. ```python
    class UserUpdateForm(UserChangeForm)
    ```
    This is the User Updation Form that is used to obtain updated user details from the front-end during user's profile details updation. The form is linked to model **`User`**.


## Robust and Extensive AJAX Integration
One of aspects of Chessrook that adds to its complexity is its extensive AJAX intergation using Javascript and JQuery. 

A chess gameplay system has lots of moving parts and is very dynamic system. For example, when you move a piece, I have mentioned earlier how the state of the game changes, the entire 8*8 board, the captured piece sections, the value of captured pieces sections, the move table, and even addition of Game Over / Win or Draw status badges.

When a player is playing a game of chess it is very frustrating if the browser needs to reload with every move given, or UNDO press. This is because browser reload is a time consuming activity and often distracts the player. To address this challenge I have heavily implemented AJAX which has significantly added to the complexity of the project. 

You will find two files:
1. /chessrook/templates/chessrook/**`ajax.html`**
2. /chessrook/templates/chessrook/**`replay_ajax.html`**

which handle all the Javascript logic used in Chessrook and also the AJAX component. 

The reason for the added complexity is that CRUD operations now need to happen in two places Django Backend and also the Javascript front-end.

Areas where AJAX CRUD manipulation is needed are:
- Making a Move
- Pressing UNDO button
- Editing Game Name
- Editing Game Notes
- Pressing FWD button
- Pressing REV button

Separate methods have been implemented in /chessrook/**`views.py`** to handle AJAX calls from the Javascript side:
- `replay_exe_cmd(request)`
- `exe_cmd(request)`
- `update_game_details(request)`

These functions are responsible for the following broad activities:
- receiving AJAX calls made from client side by Javascript
- performing internal computations with the help of logic from gameplay.py and chess_engine.py and other internal structures
- updating the corresponding model with the CRUD operation
- sending a JsonResponse to the client side Javascript as a response to the AJAX call made by it. The Javascript code then makes changes to the page based on this response.

A user can have multiple "active" games running, alongside analyzing multiple "game-over" games all together, and the Chessrook Django Server can handle it - to facilitate this AJAX code has been used alongside the def exe_cmd() and def replay_exe_cmd() in views.py file. This allows each game be it active gameplay or game replay to run independently, and have no conflict with each other.

However to safeguard application integrity random user reloads must be prevented. Chessrook is designed in such a fashion, that user never needs to touch the url bar or ever reload the browser. This is done to provide a holistic user experience.

So we ensure all user initiated reloads in test_board and replay_board redirect to home_page by adding logic in the test_board() and replay_board() methods in views.py. This is because user is not supposed to press reload while in test_board or replay_board. Since AJAX support is there each and every functionality of the test_board and replay_board are available without the need of any browser reloads. Hence a user initiated browser reload is invalid, and hence redirects to home page.

However Chessrook saves any minor change made to its state and keeps record of it. So even if by mistake user presses the browser reload button, and gets redirected to home page, he/she can then again open that game easily and find all progress saved, as if he/she never left the game.

# Contents of each file created in the project

1. /chessrook/static/chessrook/**`styles.css`** -
    - **Number of Lines:** 472
    - **Contents:** CSS Styling for all the html pages used in the Chessrook Web App.
2. /chessrook/static/chessrook/**`cover.css`** -
    - **Contents:** CSS Styling for the cover page used in home screen - obtained from Bootstrap
3. /chessrook/static/chessrook/**`chess_pieces`** - 
    - **Number of files inside this directoty:** 13
    - **Contents:** a directory consisting of all images of chess pieces
4. /chessrook/static/chessrook/js/**`jquery.js`** - 
    - **Contents:** JQuery Code downloaded from official JQuery website
5. /chessrook/templates/chessrook/**`ajax.html`** - 
    - **Number of lines:** 491
    - **Number of functions:** 12
    - **Contents:** Javascript and AJAX code for handling functionality of test_board.html which is the main page displayed when a user is playing an active game with all assets for that game loaded. The code in ajax.html dynamically alters the assets of this page and sends AJAX calls to the backend to execute CRUD operations on the system and database
6. /chessrook/templates/chessrook/**`base.html`** - 
    - **Number of lines:** 119
    - **Contents:** Base HTML Template which other html pages inherit
7. /chessrook/templates/chessrook/**`home_page.html`** - 
    - **Number of lines:** 103
    - **Contents:** HTML of Home Page
8. /chessrook/templates/chessrook/**`invalid_game_id.html`** - 
    - **Number of lines:** 14
    - **Contents:** HTML of Invalid Game ID Page
9. /chessrook/templates/chessrook/**`replay_ajax.html`** - 
    - **Number of lines:** 321
    - **Number of functions:** 8
    - **Contents:** Javascript and AJAX code for handling functionality of replay_board.html which is the main page displayed when a user is replaying a past game that is over, with all assets for that game loaded. The code in replay_ajax.html dynamically alters the assets of this page and sends AJAX calls to the backend to execute CRUD operations on the system and database
10. /chessrook/templates/chessrook/**`replay_board.html`** - 
    - **Number of lines:** 360
    - **Contents:** HTML code for replay_board page
11. /chessrook/templates/chessrook/**`test_board.html`** - 
    - **Number of lines:** 362
    - **Contents:** HTML code for test_board page
12. /chessrook/templates/chessrook/**`home_screen.html`** - 
    - **Number of lines:** 106
    - **Contents:** HTML of Home Screen - based on Bootstrap Cover
13. /chessrook/**`chess_engine.py`** - 
    - **Number of lines:** 1155
    - **Number of functions:** 29
    - **Number of classes:** 3
    - **Contents:** The Core Chess Engine logic.
14. /chessrook/**`gameplay.py`** - 
    - **Number of lines:** 217
    - **Number of functions:** 4
    - **Number of classes:** 2
    - **Contents:** The Intermediate Gameplay System connecting **`views.py`** with chess_engine.py
15. /chessrook/**`models.py`** - 
    - **Number of lines:** 18
    - **Number of functions:** 1
    - **Number of class:** 1
    - **Contents:** Classes for the models used. [Refer to the section on Models](#models)
16. /chessrook/**`urls.py`** - 
    - **Number of lines:** 17
    - **Contents:** url routing information for the chessrook app of the project. [Refer to the section on URL Routing of the chessrook app](#url-routing-of-the-chessrook-app)
17. /chessrook/**`views.py`** - 
    - **Number of lines:** 674
    - **Number of functions:** 12
    - **Number of class:** 4
    - **Contents:** Classes and methods for different views used in chessrook app. [Refer to the section on Views of the chessrook app](#views-functions-and-classes-of-the-chessrook-app)
18. /users/templates/users/**`login.html`** - 
    - **Number of lines:** 85
    - **Contents:** HTML for the login page
19. /users/templates/users/**`register.html`** - 
    - **Number of lines:** 110
    - **Contents:** HTML for the register page
20. /users/templates/users/**`logout.html`** - 
    - **Number of lines:** 13
    - **Contents:** HTML for the logout page
21. /users/templates/users/**`profile_update.html`** - 
    - **Number of lines:** 73
    - **Contents:** HTML for the profile update page.
22. /users/templates/users/**`profile.html`** - 
    - **Number of lines:** 91
    - **Contents:** HTML for the profile page.
23. /users/**`forms.py`** - 
    - **Number of lines:** 87
    - **Number of functions:** 2
    - **Number of class:** 4
    - **Contents:** Classes for forms used in users app. [Refer to the section on Views and forms of the users app](#views-and-forms-of-the-users-app)
24. /users/**`views.py`** - 
    - **Number of lines:** 51
    - **Number of functions:** 3
    - **Contents:** Classes and methods for different views used in users app. [Refer to the section on Views and forms of the users app](#views-and-forms-of-the-users-app)
25. /chessrook_project/**`urls.py`** - 
    - **Number of lines:** 31
    - **Contents:** url routing for the entire project as well as for the users app. [Refer to the URL Routing of the project](#url-routing-of-the-project)
26. /**`README.md`** - 
    - **Contents:** README file for the project