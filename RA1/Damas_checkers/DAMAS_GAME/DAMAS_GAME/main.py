from juego import Juego 

def principal():
    print("¡Bienvenido a Damas!")
    print("Selecciona el modo de juego:")
    print("1. Humano vs Bot")
    print("2. Humano vs Humano")
    print("3. Bot vs Bot")
    eleccion_modo = input("Elige (1 o 2 o 3): ")

    if eleccion_modo == "1":
        juego = Juego(modo="HvB")
    elif eleccion_modo == "2":
        juego = Juego(modo="HvH")
    elif eleccion_modo == "3":
        juego = Juego(modo="BvB") 
    else:
        print("Opcion no valida. Se iniciara en modo Humano vs Bot por defecto.")
        juego = Juego(modo="HvB")

    juego.jugar_partida()

if __name__ == "__main__":
    principal()
