# an imitation of hitbox.io.
my biggest project. combining all my knowledge of python together: flask, websocket, classes, exceptions, interfaces, ...

## accounts :
### database :
    your account is saved in a database. 
    (currently not a hshed password.)
### friends :
    you can add accounts to be your friends.
    friends also being saved in a database.

## game :
### messages :
    you can send messages during games but they are not saved in a database.
### movement :
    you can move with the arrows during games.
    just the server is moving the players, not the front-end.
### eating :
    if you stand on someone's avatar and press space you "eat" the player and his avatar returns to position 0, 0.
### xp :
    every time you "eat" someone you get 10 xp (experience points).
    the xp is saved in a database.

## database :
### users :
    id int (pk, ai) | username varchar(255) | pass varchar(255) | xp int

### friends :
    friend int (fk: users(id)) | f_of int (fk: users(id))

# installation :
## requirements :
- mysql workbench database
(add the tables detailed above)

### if you have mysql workbench :
open terminal and run :<br>
`>>>pip install flask bcrypt PyMySQL dbutils cryptography https://erri4.github.io/package/filesforpip/WebsocketServer-0.1.4-py3-none-any.whl`<br>
`>>>git clone https://github.com/erri4/websocket.git`<br>
`>>>cd websocket`


# running :
    >>>flask run

the server is now running on your local net at your ip address.