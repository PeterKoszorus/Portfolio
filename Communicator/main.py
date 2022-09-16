from Server import Server
from Client import Client


def main():
    while select_mode():
        pass


# Function for selecting Server/Client side runs python scripts
def select_mode():
    print("------------------------------------------------------------")
    print("SELECT THE MODE OF APPLICATION: 0 for SERVER, 1 for CLIENT, 4 for exiting the app")
    print("------------------------------------------------------------")
    mode = input("MOD:")

    if mode == "0":
        print("Hello this is Server")
        Server.server()
        return True
    elif mode == "1":
        print("Hello this is a Client")
        VELKOST_REZIE = Client.client()
        print(f"Velkost rezie celeho behu clienta bola: {VELKOST_REZIE * 8}B")
        return True
    elif mode == "4":
        print("Ending the application")
        return False
    else:
        print("You have entered a wrong mode!")
        return True


if __name__ == '__main__':
    main()
