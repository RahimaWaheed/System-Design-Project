import streamlit as st
from datetime import datetime
import sqlite3

#SQLite code: data mamangement

# Function to create a table if it doesn't exist
def create_table():
    conn = sqlite3.connect('timeLog.db')
    c = conn.cursor()
    c.execute(''' CREATE TABLE IF NOT EXISTS USER_INFO (TASK_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                                      name TEXT, email TEXT, task TEXT, description TEXT, start_time) ''')
    conn.commit()
    conn.close()

# Function to add user infor to the database
def add_infor(name,email,task, description):
    conn = sqlite3.connect('timeLog.db')
    start = datetime.now()
    c = conn.cursor()
    c.execute('INSERT INTO USER_INFO (name, email, task, description) VALUES (?, ?, ?, ?)', (name , email, task, description, start ))
    conn.commit()
    conn.close()


# Function to retrieve user infor from the database
def get_infor():
    conn = sqlite3.connect('timeLog.db')
    c = conn.cursor()
    c.execute(' select name, email, task, description from USER_INFOR')
    infor = c.fetchall()
    conn.close()
    return infor

# Function to delete user infor
def delete_infor(task_id):
    conn = sqlite3.connect('timelog.db')
    c = conn.cursor()
    c.execute('DELETE FROM TODO_INFO WHERE TASK_ID=?', (task_id,))
    conn.commit()
    conn.close()
    

# streamlit app code
def main():
    st.title("Time Log System")

    create_table()
    
    # add user and task infor

    name = st.text_input("Name")
    email = st.text_input("Email")
    task = st.text_input("Task")
    description = st.text_area("Description")

   
    Start = st.button("Start Time") 
    End = st.button("End Time")
    
    new_task =len(name, email, task, description)!=0
    
    
    if new_task:
        add_infor(new_task)
        st.success(f'Task "{new_task}" added successfully!')

    else :
          st.warning('Please enter a task.')
        

    # shows the list of tasks
        
      

    if Start:
        st.session_state.start_timestamp = datetime.now()
        formatestart_time = st.session_state.start_timestamp.strftime('%H:%M')
        st.sidebar.write("Start time:",formatestart_time)
       

    if End:
        if "start_timestamp" in st.session_state:
            end_timestamp = datetime.now()
            formateend_time = end_timestamp.strftime('%H:%M')
            st.sidebar.write("End time :",formateend_time)
            
            
        else:
            st.warning("Please set the start time first.")


if __name__ == "__main__":
    main()
