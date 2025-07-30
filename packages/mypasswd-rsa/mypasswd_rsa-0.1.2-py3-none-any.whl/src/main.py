import os
from src.helper.rsa_crypt import setup_new_keys
from src.helper.add_passwd_db import new_site
from rich import print
from src.helper.mypasswd_helper import (
    testing, 
    get_file_path, 
    print_passwd_db, 
    get_db_path_and_file,
    file_exist,
    )


# Globals
file_path = get_file_path()
db_file = get_db_path_and_file()


def welcome():
    print(r"""
 __  __                                       _ 
|  \/  |_   _ _ __   __ _ ___ _____      ____| |
| |\/| | | | | '_ \ / _` / __/ __\ \ /\ / / _` |
| |  | | |_| | |_) | (_| \__ \__ \\ V  V / (_| |
|_|  |_|\__, | .__/ \__,_|___/___/ \_/\_/ \__,_|
        |___/|_|                                
""")


def check_pem() -> bool:
    '''  check if private.pem exist  '''
    print('[magenta]********************************')
    menu()
    # check if private.pem exist
    if not file_exist(file_path + 'private.pem'):
        print(file_path + "private.pem")
        print('"private.pem" do not exist! Do you wont to set up new public and private.pem?')
        answer = input("(Y/n): ")
        if answer == "y" or answer == "Y" or  answer == "":
            os.mkdir(file_path, mode=0o770, dir_fd=None)
            setup_new_keys(file_path)
            print("new keys in: ", file_path)
            return True
        else:
            return False
    return True


def menu():
    print("[green]*[/green] [yellow]'q'[/yellow] [green]-[/green] [yellow]quit [/yellow]")
    print("[green]*[/green] [yellow]'m'[/yellow] [green]-[/green] [yellow]menu [/yellow]")
    print("[green]*[/green] [yellow]'l'[/yellow] [green]-[/green] [yellow]list passwd db [/yellow]")
    print("[green]*[/green] [yellow]'a'[/yellow] [green]-[/green] [yellow]add new site [/yellow]")
    print('[magenta]********************************')


def main():
    welcome()
    run = True
    if not check_pem():
        run = False
        print('Somthing went wrong! Could not create: ', db_file)

    while run:
        answer = input("mypasswd ('q' - quit or 'm' - menue): ")
        if answer == 'q':
            run = False
        elif answer == 'm':
            menu()
        elif answer == 'l':
            print_passwd_db(db_file)
        elif answer == 'a':
            new_site()
        elif answer == 't':
            testing()


if __name__ == "__main__":
    main()