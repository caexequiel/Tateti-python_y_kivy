import random
import math
import os

 
import kivy
kivy.require('2.1.0')
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label




Window.fullscreen = 0
tablero = ["-","-","-","-","-","-","-","-","-"]
#X is max = 1
#O in min = -1

class TicTacToe(App):
    wid_alfa = ObjectProperty(None)
    def __init__(self):
        super().__init__()

        self.humanPLayer = 'X'
        self.botPlayer = "O"
        self.board = tablero


    #Recordar: tablero es state y contine los valores de cada celda
    #Para ver si el tablero está lleno
    def is_board_filled(self,state):
        return not "-" in state

    #Para ver si alguien ganó
    def is_player_win(self,state,player):
        if state[0]==state[1]==state[2] == player: return True
        if state[3]==state[4]==state[5] == player: return True
        if state[6]==state[7]==state[8] == player: return True
        if state[0]==state[3]==state[6] == player: return True
        if state[1]==state[4]==state[7] == player: return True
        if state[2]==state[5]==state[8] == player: return True
        if state[0]==state[4]==state[8] == player: return True
        if state[2]==state[4]==state[6] == player: return True

        return False

    def checkWinner(self):
        if self.is_player_win(self.board,self.humanPLayer):
            print(self.board)
            print(f"   Player {self.humanPLayer} wins the game!")
            return True
            
        if self.is_player_win(self.board,self.botPlayer):
            print(self.board)
            print(f"   Player {self.botPlayer} wins the game!")
            return True

        # checking whether the game is draw or not
        if self.is_board_filled(self.board):
            print("   Match Draw!")
            return True
        return False

    
class ComputerPlayer(TicTacToe):
    def __init__(self,letter):
        self.botPlayer = "O"
        self.humanPlayer = "X" 
        self.state = tablero

    #Nos dice a quien le toca jugar
    def players(self, state):
        n = len(state)
        x = 0
        o = 0
        for i in range(9):
            if(state[i] == "X"):
                x = x+1
            if(state[i] == "O"):
                o = o+1
        
        if(self.humanPlayer == "X"):
            return "X" if x==o else "O"
        if(self.humanPlayer == "O"):
            return "O" if x==o else "X"
    
    #Nos muestre las opciones de movimiento
    def actions(self, state):
        return [i for i, x in enumerate(state) if x == "-"]
    
    #Le pasamos un tablero y un movimiento y devuelve un tablero nuevo con el movimiento
    def result(self, state, action):
        newState = state.copy()
        player = self.players(state)

        #Programar el movimiento de la IA
        newState[action] = player
        return newState
    
    #Comprueba quien ganó
    def terminal(self, state):
        if(self.is_player_win(state,"X")):
            return True
        if(self.is_player_win(state,"O")):
            return True
        return False

    def minimax(self, state, player):
        max_player = self.humanPlayer  # yourself
        other_player = 'O' if player == 'X' else 'X'

        # Comprueba si hay un ganador
        #Si la partida terminó
        if self.terminal(state):
            return {'position': None, 'score': 1 * (len(self.actions(state)) + 1) if other_player == max_player else -1 * (
                        len(self.actions(state)) + 1)}
        #Si hay un empate
        elif self.is_board_filled(state):
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # each score should maximize
        else:
            best = {'position': None, 'score': math.inf}  # each score should minimize
        #Por cadad movimiento posible
        for possible_move in self.actions(state):
            newState = self.result(state,possible_move)
            sim_score = self.minimax(newState, other_player)  # simulate a game after making that move

            sim_score['position'] = possible_move  # Representa al mejor próximo movimiento

            if player == max_player:  # X is max player
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best

    def machine_move(self, state):
        square = self.minimax(state,self.botPlayer)['position']
        return square

class Wid_Alfa(GridLayout):
    def __init__(self, **kwargs):
        super(Wid_Alfa, self).__init__(**kwargs)
        self.tateti = TicTacToe()
        self.botPlayer = "O"
        self.jugador = "X"
        self.board = tablero
        self.texto = self.ids.label 

    def button_pressed(self, numero_boton,player):
        #almacenamos el valor del botón presionado en el array
        self.board[numero_boton-1] = player
        #Mandamos a bloquear el botón
        self.bloquear_boton(numero_boton, player)
        #Player puede ser X (jugador) o O (bot)

    def bloquear_boton(self, numero_boton, player):
        #El botón
        boton = self.ids.grid_botones.ids[str(numero_boton)]
        # Bloquea el botón
        boton.disabled = True
        #Cambiamos el color del botón
        boton.disabled_color = "#ffffff"
        boton.disabled_opacity: 0
        # Establece el color de fondo del botón deshabilitado
        if player == "X":
            boton.background_color = (1, 0, 1, 1)   
        else:
            boton.background_color = (0, 1, 0, 1)   
        #Cambiamos el texto del botón
        self.update_label_text(boton, player)

    def update_label_text(self, boton,player):        
        #Cambiamos el texto de los botones
        boton.text = player
        #Cambiamos el texto del mensaje
        texto = self.texto
        texto.text = str(self.board)
        if self.tateti.checkWinner():
            texto.text = f"Partida finalizada!"
        if self.tateti.checkWinner() == False and player == "X":
            self.start_bot(texto, "la inteligencia")

    def start_bot(self, texto, juega):
        bot = ComputerPlayer(self.botPlayer)
        #Bot
        square = bot.machine_move(self.board)
        self.board[square] = self.botPlayer
        self.bloquear_boton(square+1, self.botPlayer)
    def reiniciar(self):
        self.board = tablero = ["-","-","-","-","-","-","-","-","-"]
        self.tateti.board = self.board
        self.texto.text = str(self.board)
        #Habilitamos los botones
        self.enable_all_buttons()

    def enable_all_buttons(self):
        for widget in self.walk():
            if isinstance(widget, Button):
                widget.disabled = False
                widget.background_color = (1,1,1)
                
            

class GridBack(GridLayout):
    None

class MainApp(App):
    def build(self):
        wid_alfa = Wid_Alfa()
        #tictactoe = TicTacToe(wid_alfa)
        return wid_alfa

if __name__ == '__main__':
	MainApp().run()