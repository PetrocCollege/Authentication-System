import os

from time import sleep
from random import randint

from modules.database import Authentication

class Program:

    def __init__(self) -> None:
        self.user_id_attempts = 3
        self.pin_attempts = 1
        self.password_attempts = 3

        self.user_id_correct = False
        self.pin_correct = False 
        self.password_correct = False 

        self.user_id: str 
        self.pin: str
        self.password: str

        self.authentication_functions = {
            1: self.register,
            2: self.login
        }
    
    @staticmethod 
    def clear_console() -> None:
        os.system('cls' if os.name=='nt' else 'clear')

    def register(self) -> None:
        Program.clear_console()
        print("--------- Registration ---------\n")

        random_user_id = randint(1000000000, 9999999999)
        random_pin = randint(1000, 9999)
        password = input("[INPUT] Create password: ")
        sleep(0.4)

        print("\n--------- Account Creation Success ---------\n")
        print(f"User ID: {random_user_id}\nPin: {random_pin}\nPassword: {password}\n")

        credentials = (random_user_id, random_pin, password)
        Authentication.add_user(credentials)
        
        input("Press enter to go back to the menu: ")
        self.start_menu()
    
    def user_id_auth(self) -> bool:
        self.user_id_attempts = 3
        while self.user_id_attempts != 0 and self.user_id_correct == False:
            
            self.user_id_attempts = self.user_id_attempts - 1
            user_id = input("[INPUT] User ID: ")

            if Authentication.check_user_id(user_id):
                self.user_id_correct = True 
                self.user_id = user_id
                return True
            
            print(f"\n[RESPONSE] Incorrect User ID, you have {self.user_id_attempts} attempts left \n")
            sleep(0.7)

        return False
    
    def pin_auth(self) -> bool:
        self.pin_attempts = 1
        while self.pin_attempts != 0 and self.pin_correct == False:

            self.pin_attempts = self.pin_attempts - 1
            pin = input("[INPUT] Pin: ")
            
            if Authentication.check_pin(self.user_id, pin):
                self.pin_correct = True 
                self.pin = pin
                return True
            
            sleep(0.7)

        return False

    def password_auth(self) -> bool: 
        self.password_attempts = 3
        characters_correct = 0

        while self.password_attempts != 0 and self.password_correct == False:

            self.password_attempts = self.password_attempts - 1
            password = input("[INPUT] Password: ")
            saved_password = Authentication.fetch_password(self.user_id, self.pin)
            saved_password_char_list = [_ for _ in saved_password]

            for char in password:
                if char in saved_password_char_list:
                    characters_correct = characters_correct + 1
                    saved_password_char_list.remove(char)  

            if characters_correct >= 3:
                return True 

            else:
                print(f"\n[RESPONSE] Incorrect password, you have {self.password_attempts} attempts left \n")
                sleep(0.7)

        return False
            
    def login(self) -> None:
        Program.clear_console()
        print("--------- Login ---------\n")
        input("\nPress enter to start the login process: ")
        
        if not self.user_id_auth():
            print("[AUTHENTICATION FAILED] You failed to enter a valid ID")
            sleep(2)
            self.login()
        
        if not self.pin_auth():
            self.user_id_correct = False
            print("\n[AUTHENTICATION FAILED] Pin did not match with user ID")
            sleep(2)
            self.login()
        
        if not self.password_auth():
            self.user_id_correct = False 
            self.pin_correct = False
            print("\n[AUTHENTICATION FAILED] You didn't provide 3 correct characters in your password.")
            sleep(3)
            self.login()
        
        sleep(0.8)
        Program.clear_console()

        print("--------- Login Success ---------\n")
        print(f"Welcome, {self.user_id}")
        input()

    def start_menu(self) -> None:
        Program.clear_console()
        print("--------- Authentication System ---------")

        try:
            choice = int(input("\n[1] Register\n[2] Login\n\n[INPUT] Choice: "))
        
        except ValueError:
            print("[ERROR] Input must be a number.")
            sleep(1)
            Program.clear_console()
            Program.start_menu()
        
        try:
            self.authentication_functions[choice]()
        
        except KeyError:
            print("[ERROR] Not a valid option.")
        

if __name__ == "__main__":
    Authentication.initialise()

    program = Program()
    program.start_menu()