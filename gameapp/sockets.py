
from gameapp import socketio
from flask_socketio import join_room, leave_room, send, emit, disconnect
from flask import session, request

# Lista global de jugadores conectados en la sala principal
connected_players = {}

# Palabras asignadas (demo)
player_words = {}
game_started = False
impostor_sid = None


@socketio.on("connect")
def handle_connect():
    print("🔌 Un jugador se conectó")


@socketio.on("disconnect")
def handle_disconnect():
    # Eliminar jugador por sid
    if request.sid in connected_players:
        del connected_players[request.sid]
    # Emitir lista actualizada
    emit("update_players", list(connected_players.values()), room="principal")
    print("❌ Un jugador se desconectó")


@socketio.on("join_room")
def handle_join(data):
    room = data.get("room")
    nickname = data.get("nickname", "Desconocido")
    join_room(room)
    connected_players[request.sid] = nickname
    # Emitir lista actualizada a todos
    emit("update_players", list(connected_players.values()), room=room)

    # Si el juego ya empezó, asignar palabra al que entra tarde (no recomendado, pero por robustez)
    # No asignar palabra hasta que el juego comience
    if room and hasattr(room, 'get') and room.get('game_started'):
        if request.sid == impostor_sid:
            word = "windows"
        else:
            word = "linux"
        player_words[nickname] = word
        emit("assign_word", {"nickname": nickname, "word": word}, room=request.sid)
@socketio.on("start_game")
def handle_start_game():
    global game_started, impostor_sid, player_words
    if not connected_players or game_started:
        return
    # Permitir que solo el usuario 'LUCAS' pueda iniciar el juego
    lucas_sid = None
    for sid, nickname in connected_players.items():
        if nickname == 'LUCAS':
            lucas_sid = sid
            break
    if lucas_sid is None or request.sid != lucas_sid:
        return
    # Elegir impostor aleatorio
    import random
    sids = list(connected_players.keys())
    impostor_sid = random.choice(sids)
    game_started = True
    # Asignar palabras
    player_words = {}
    # Asignar palabras e impostor solo al comenzar
    for sid, nickname in connected_players.items():
        if sid == impostor_sid:
            word = "windows"
        else:
            word = "linux"
        player_words[nickname] = word
        emit("assign_word", {"nickname": nickname, "word": word}, room=sid)
    emit("game_started", {}, room="principal")
@socketio.on("chat_message")
def handle_chat_message(data):
    if not game_started:
        return
    nickname = data.get("nickname", "")
    message = data.get("message", "")
    emit("chat_message", {"nickname": nickname, "message": message}, room="principal")

@socketio.on("leave_room")
def handle_leave(data):
    room = data.get("room")
    leave_room(room)
    emit("player_left", {"msg": f"Un jugador salió de la sala {room}"}, room=room)
