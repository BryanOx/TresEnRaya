class Jugador():
    def __init__(self,nombre):
        self.nombre = nombre
        self.Victorias = 0
        self.Derrotas = 0
        self.Empates = 0

class Jugador1(Jugador):
    def __init__(self,nombre):
        super().__init__(nombre)
        self.letra = "X"
        self.num = 1

class Jugador2(Jugador):
    def __init__(self,nombre):
        super().__init__(nombre)
        self.letra = "O"
        self.num = 2