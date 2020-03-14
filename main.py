﻿from functions import *
from User import *
from Task import *
from os import getcwd, sep

'''
/*******************************************************************************
Autor: Carlos Henrique de Oliveira Valadão
Componente Curricular: Algoritmos I
Concluido em: 14/03/2020
Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
trecho de código de outro colega ou de outro autor, tais como provindos de livros e
apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.
******************************************************************************************/
'''


# Root path of script main obviously this can change with each script execution
SCRIPT_ROOT_PATH = getcwd()
# Name of file that store the users registered in the system
NAME_USERS_FILE = "users.txt"
# Name of directory that will storage the tasks of users
NAME_TASKS_DIR = "tasks"


selected_option = 0
while selected_option != 3:

    selected_option = main_menu()
    # Case the user wants register a new user in the system
    if selected_option == 1:
        while True:
            nick = input("\033[1mEntre com o seu nick: \033[m")
            # Validating the nickname typed
            if nick.strip().isidentifier():
                nick = nick.strip()
                # Verifying existence of file that storage users of system
                create_file(NAME_USERS_FILE, 0)
                # Verifying existence of typed nickname on system
                if login_exists(nick, NAME_USERS_FILE):
                    alert("O nick informado já está cadastrado no sistema")
                    alert("Por favor, tente outro nick")
                    freeze_screen()
                else:
                    password = input("\033[1mEntre com a sua senha: \033[m")
                    break
            # Case invalid nickname
            else:
                alert("Nick inválido")
                alert("O seu nick deve ser composto somente por caracteres alfanumericos e underline")
                freeze_screen()
        # User informations collected with successful
        alert("Cadastrando...")
        # Making an object User
        new_user = User(nick, password)
        # Registering the user on system
        register_user(new_user, NAME_USERS_FILE)
        alert("Usuario cadastrado com sucesso!")
        freeze_screen()

    # Case the user want log in the system
    elif selected_option == 2:
        while True:
            login = input("\033[1mDigite o seu login: \033[m")
            password = input("\033[1mDigite a sua senha: \033[m")
            alert("Logando no sistema...")
            # Verifying existence of file that storage users of system
            create_file(NAME_USERS_FILE, 0)
            # Authenticating the user in the system
            if autenticate_user(login, password, NAME_USERS_FILE):
                alert("Login realizado com sucesso!")
                freeze_screen()
                verify_files_post_login(NAME_TASKS_DIR, SCRIPT_ROOT_PATH, login)
                # User task file path
                USER_TASK_FILE_PATH = SCRIPT_ROOT_PATH + sep + NAME_TASKS_DIR + sep + login + sep + login + "_tasks.pbl"
                # User info file path
                USER_INFO_FILE_PATH = SCRIPT_ROOT_PATH + sep + NAME_TASKS_DIR + sep + login + sep + login + "_info.pbl"
                # Object of user logged in system, at some point he was dead in file users.txt
                resurrected_user = User(login, password)
                # Getting tasks from the logged user file
                user_task_list = read_b(USER_TASK_FILE_PATH)
                resurrected_user.set_tasks(user_task_list)
                sub_menu_option_selected = sub_menu()
                while 5 != sub_menu_option_selected:

                    # If the user wants create a new task
                    if sub_menu_option_selected == 1:
                        task_title = input("\033[1mTitulo da tarefa: \033[m")
                        task_description = input("\033[1mDescricao da tarefa: \033[m")
                        task_priority = menu_priority_task()
                        verify_files_post_login(NAME_TASKS_DIR, SCRIPT_ROOT_PATH, login)
                        # Getting the id of task
                        task_id = read_b(USER_INFO_FILE_PATH)
                        task_id += 1
                        # Making a Task object
                        new_task = Task(task_id, task_title, task_description, task_priority)
                        verify_files_post_login(NAME_TASKS_DIR, SCRIPT_ROOT_PATH, login)
                        resurrected_user.set_task(new_task)
                        write_b(resurrected_user.get_tasks(), USER_TASK_FILE_PATH)
                        write_b(task_id, USER_INFO_FILE_PATH)
                        alert("Criando tarefa...")
                        alert("Tarefa criada com sucesso!")
                        freeze_screen()

                    # If the user wants to show a task
                    elif sub_menu_option_selected == 2:
                        verify_files_post_login(NAME_TASKS_DIR, SCRIPT_ROOT_PATH, login)
                        user_task_list = read_b(USER_TASK_FILE_PATH)
                        cls()
                        if not show_tasks(user_task_list):
                            alert("Você ainda não cadastrou tarefas!")
                        print()
                        alert("\t\t </ENTER> TO CONTINUE")
                        input()

                    # If the user wants to edit a task
                    elif sub_menu_option_selected == 3:
                        verify_files_post_login(NAME_TASKS_DIR, SCRIPT_ROOT_PATH, login)
                        user_task_list = read_b(USER_TASK_FILE_PATH)
                        if show_tasks(user_task_list):
                            alert("Qual o ID da tarefa você deseja alterar?")
                            searched_task = read_int()
                            if find_task(user_task_list, searched_task) > -1:
                                task_index_searched = find_task(user_task_list, searched_task)
                                item = task_change_menu()
                                if item == 1:
                                    modify_item = input("> ")
                                    user_task_list[task_index_searched].set_title(modify_item)
                                elif item == 2:
                                    modify_item = input("> ")
                                    user_task_list[task_index_searched].set_description(modify_item)
                                elif item == 3:
                                    modify_item = task_change_menu()
                                    user_task_list[task_index_searched].set_priority(modify_item)
                                verify_files_post_login(NAME_TASKS_DIR, SCRIPT_ROOT_PATH, login)
                                # Updating the user task file of user
                                write_b(user_task_list, USER_TASK_FILE_PATH)
                                resurrected_user.set_tasks(user_task_list)
                                alert("Modificando a tarefa...")
                                alert("Tarefa modificada com sucesso!")
                                freeze_screen()
                            else:
                                alert("Não existe nenhuma tarefa com o ID informado")
                                alert("Por favor, tente novamente")
                                freeze_screen()
                        else:
                            alert("Você ainda não cadastrou tarefas!")
                            freeze_screen()

                    # If the user wants to remove a task
                    elif sub_menu_option_selected == 4:
                        verify_files_post_login(NAME_TASKS_DIR, SCRIPT_ROOT_PATH, login)
                        user_task_list = read_b(USER_TASK_FILE_PATH)
                        if show_tasks(user_task_list):
                            alert("Qual o ID da tarefa você deseja remover?")
                            remove_id = read_int()
                            if remove_task(user_task_list, remove_id):
                                verify_files_post_login(NAME_TASKS_DIR, SCRIPT_ROOT_PATH, login)
                                # Updating the user task file of user
                                write_b(user_task_list, USER_TASK_FILE_PATH)
                                resurrected_user.set_tasks(user_task_list)
                                alert("Removendo tarefa do sistema...")
                                alert("Tarefa removida com sucesso!")
                                freeze_screen()
                            else:
                                alert("Não existe nenhuma tarefa com esse id!")
                                freeze_screen()
                        else:
                            alert("Você ainda não cadastrou tarefas!")
                            freeze_screen()

                    cls()
                    sub_menu_option_selected = sub_menu()
                #  If the user logout of account
                alert("Deslogando da conta... \033[m")
                alert("Aguarde...")
                freeze_screen()
                break
            # Case login and/or password entered are incorrect
            else:
                alert("Login e/ou senha incorretos!")
                freeze_screen()
# Exiting of system
alert("Saindo do programa...")
alert("Aguarde...")
freeze_screen()