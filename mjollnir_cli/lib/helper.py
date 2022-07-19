#!/usr/bin/python3

"""
.. moduleauthor:: shellchocolat <shellchocolat@no-mail.com>
"""

class Helper(object):
    """This class is used to display a custom help during the use of the tool.
    """
    def __init__(self):
        self.ok = 'ok'

    def help_main_menu(self):
        print("""
==========
= BASICS =
==========
++ login -------------- Allows to login to the mjollnir-api
                          ex: login thor
++ logout ------------- Allows to logout
++ first_user --------- Command to use only once in order to create the first user
                          ex: first_user <user_name> --> create the user <user_name>
++ help --------------- Displays this help
++ exit --------------- Exit the mjollnir_cli

==========
= COMMON =
==========
+ mission ------------- Create/Edit/Delete/Select a mission and List all missions (-c, -e, -d, -s, -l)
                          ex: mission -c <mission_name>
                          ex: mission -e <mission_name>
+ listener ------------ Allow to access the listener menu, but also to list the active listener
                          ex: listener    --> access the listener menu
                          ex: listener -l --> list all active listeners
+ agent --------------- Allows to access the agent menu, but also to interact with an agent and to delete one and list all agents
                          ex: agent                --> access the agent menu
                          ex: agent -l             --> list all active agents
                          ex: agent -i <agent_uid> --> interaction with the <agent_uid>
                          ex: agent -d <agent_uid> --> delete the <agent_uid> from the database and all the associated task
+ download ------------ Downloads a freshly created agent
                          ex: download http://.../public/<agent_name> /tmp/<agent_name> --> download the <agent_name>
+ task ---------------- Read the result for a specific task
                          ex: task -r <task_uid> --> get the result for the <task_uid>
+ r-task -------------- Create a on-registering-task, that will execute as soon as a new agent activate based on its <agent_name>
                          ex: r-task win_x64_http --> create a task for all the win_x64_http agents as soon as they registered
+ g-task -------------- Create a task for all agents inside the <group_name>
                          ex: g-task <group_name> --> create a task for all agents inside the <group_name>
+ launcher ------------ 
+ shellcode -----------
""")

        return True
    
    def	help_agent_menu(self):
        self.help_main_menu()
        return True

    def help_registering_task_menu(self):
        self.help_main_menu()
        return True

    def help_agent_interaction_menu(self):
        self.help_main_menu()
        return True

    def help_listener_menu(self):
        self.help_main_menu()
        return True
    
    def help_shellcode_menu(self):
        self.help_main_menu()
        return True

    def help_launcher_menu(self):
        self.help_main_menu()
        return True

    def help_payload_menu(self):
        self.help_main_menu()
        return True

    def help_group_task_menu(self):
        self.help_main_menu()
        return True


