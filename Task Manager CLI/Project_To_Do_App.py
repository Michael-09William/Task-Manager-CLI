#import sqlite
import sqlite3
import random

#create database and connect it
db=sqlite3.connect('Job.db')

#setting up the cursor
cr=db.cursor()

#creating tasks table
cr.execute("create table if not exists tasks ( user_id integer , name text , deadline integer )")
cr.execute("create table if not exists completed_tasks ( user_id integer , name text )")


#Chossing Option
message="""Do You Want To
's' Show Your Tasks
'a' Add Task 
'u' Update Task
'd' Delete Task
'c' Mark As Completed Task
'x' Show Completed Task
'q' Quit 
"""



#List Of Option
options_list=['s','a','u','d','q','c','x']

#Validation On ID
def get_valid_user_id():
    userID = input("Write Your ID :")
    if not userID.isdigit():
        print("InValid Input In ID Please Try Again")
        return None
    return int(userID)

#Show All Tasks Function
def show_tasks():
    userID=get_valid_user_id()
    try: 
        cr.execute(f"select * from tasks where user_id = ? ",(userID,))
        result=cr.fetchall()
        if len(result)>0:
            print(f'You Have {len(result)} Tasks')
            for task in result:
                print(f'Task Name : \'{task[0]}\'',end=' ')
                print(f', Deadline : {task[1]} Days')
        else:
            print('There Is No Tasks Assign To You ')
    except sqlite3.Error as e:
        print(f"Database Error:{e} ")
     


#Add Funcion
def add_task():
    userID=get_valid_user_id()
    try: 
        name=input('Task Name :').strip().lower()
        if not name:
            print("Task name can't be empty.")
            return
        deadline=random.randrange(1,7)
        cr.execute("select * from tasks where user_id = ? and name =?",(userID,name))
        result=cr.fetchone()
        if result ==None:
        
            cr.execute("insert into tasks (name,deadline,user_id) values(?,?,?) ",(name,deadline,userID))

            print('Task Is Added')
        else:
            print(f"The task '{name}' already exists for user ID {userID}.")
    except sqlite3.Error as e:
        print(f"Database Error:{e} ")

    

#Update Function
def update_task():
    userID=get_valid_user_id()
    try: 
        name=input('Task Name :').strip().lower()
        if not name:
            print("Task name can't be empty.")
            return     
        cr.execute("select * from tasks where user_id =? and name =?",(userID,name))
        result=cr.fetchone()
        if result==None:
            print(f"Task Name \'{name}\' Not Found For User ID {userID}")
        else:
            new_deadline=input('Enter The Updated Deadline : ')
            if not new_deadline.isdigit():
                print("Invalid deadline , Must be a number ")
                return
            cr.execute("update tasks set deadline =? where name =? and user_id =?",(new_deadline,name,userID))
            print('Deadline Updated.')
    except sqlite3.Error as e:
        print(f"Database Error:{e} ")

#Delete Function 
def delete_task():
    userID=get_valid_user_id()
    try: 
        name=input('Task Name What You Want To Delete It : ').strip().lower()
        if not name:
            print("Task name can't be empty.")
            return
        cr.execute("select * from tasks where user_id = ? and name = ?",(userID,name))
        result=cr.fetchone()
        if result == None:
            print('Task Not Found To Delete It.')
        else:
            cr.execute("delete from tasks where user_id = ? and name = ?",(userID,name))
            print(f'Task {name} Deleted.')
    except sqlite3.Error as e:
        print(f"Database Error:{e} ")
     

#Completed Task Function
def completed_tasks():
    userID=get_valid_user_id()
    try: 
        name=input('Write Name Of Completed Task : ').strip().lower()
        if not name:
            print("Task name can't be empty.")
            return
        cr.execute("select * from tasks where user_id = ? and name = ? ",(userID,name))
        result=cr.fetchone()
        if result == None:
            print("Task Not Found In Your Tasks.")
        else:
            cr.execute('insert into completed_tasks (user_id,name) values (?,?)',(userID,name))
            cr.execute("delete from tasks where user_id = ? and name = ?", (userID, name)) 
            print('Great Work! Task moved to completed.')
    except sqlite3.Error as e:
        print(f"Database Error:{e} ")

#Show Completed Task
def show_completed_task():
    userID=get_valid_user_id()
    try:
        cr.execute("select * from completed_tasks where user_id = ?",(userID,))
        result=cr.fetchall()
        if result == None :
            print("There Is No Completed Task")
        else:
            for tasks in result:
                print(f'Task Name : {tasks[1]}')
    except sqlite3.Error as e:
        print(f"Database Error :{e}")


#Main Function
def main():
#Verifying The input
    while True:
        #user Input
        user_input=input(message).strip().lower()

        if user_input in options_list:
            if user_input == 's':
                show_tasks()
            
            elif user_input == 'a':
                add_task()

            elif user_input == 'u':
                update_task()

            elif user_input == 'd':
                delete_task()
            
            elif user_input == 'c':
                completed_tasks()

            elif user_input == 'x':
                show_completed_task()

            else:
                print('Quiting From The App..')
                break
        else:
            print('Input Not Found.')
            
        

    db.commit()
    db.close()
if __name__ == "__main__":
    main()