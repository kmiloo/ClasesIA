from game import Game

def main():
    print("Bienvenido a Damas!")
    print("Selecciona el modo de juego:")
    print("1. Humano vs Bot")
    print("2. Humano vs Humano")
    print("3. Bot vs Bot")
    mode_choice = input("Elige (1 o 2 o 3): ")

    if mode_choice == "1":
        game = Game(mode="HvB")
    elif mode_choice == "2":
        game = Game(mode="HvH")
    elif mode_choice == "3":
        game = Game(mode="BvB") 
    else:
        print("Opción no válida. Se iniciará en modo Humano vs Bot por defecto.")
        game = Game(mode="HvB")

    game.play_game()

if __name__ == "__main__":
    main()
