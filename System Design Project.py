import streamlit as st
from datetime import datetime
import sqlite3

#SQLite code: data mamangement

def create_table():
    conn = sqlite3.connect('TimeLogAppInfor.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Task_Infor (
                    TASK_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                    Task_Status TEXT,
                    Task_Name TEXT, 
                    Description TEXT, 
                    Start_time DATETIME,
                    End_time DATETIME)''')
    conn.commit()
    conn.close()

def add_task(Task_Name, Description):
    current_time = datetime.now()

    # Convert datetime object to string in ISO 8601 format

    Start_time = current_time.isoformat(sep=' ', timespec='seconds')
    conn = sqlite3.connect('TimeLogAppInfor.db')
    c = conn.cursor()
    c.execute('INSERT INTO Task_Infor ( Task_Name, Description, Start_time) VALUES (?, ?, ?)', (Task_Name, Description, Start_time))
    conn.commit()
    conn.close()
    
# Function to retrieve tasks from the database
def get_tasks():
    conn = sqlite3.connect('TimeLogAppInfor.db')
    c = conn.cursor()
    c.execute('SELECT MAX(Task_id), Task_Name, description, Start_time FROM Task_Infor ')
    tasks = c.fetchone()
    conn.close()
    return tasks

def update_status(task_id):
    currentend_time = datetime.now()
    End_time = currentend_time.isoformat(sep=' ', timespec='seconds')
    conn = sqlite3.connect('TimeLogAppInfor.db')
    c = conn.cursor()
    c.execute('UPDATE Task_Infor SET End_time=? WHERE TASK_ID=?', ( End_time, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect('TimeLogAppInfor.db')
    c = conn.cursor()
    c.execute('DELETE FROM Task_Infor WHERE TASK_ID=?', (task_id,))
    conn.commit()
    conn.close()


# Main Streamlit app
def main():
    st.title('Activity TimeLog')

    # Create the table if it doesn't exist
    create_table()

    # Store in a single variable as a dictionary
    
    Task_Name = st.text_input("Task Name", key="task_name")
    Description = st.text_area("Description", key="desc")

    if st.button('Start'):
        task_id = add_task(Task_Name, Description)  # Add task and retrieve its ID
        st.session_state.task_id = task_id
        task = get_tasks()  # Retrieve the most recent task to display
        
        if task:
            task_id, Task_Name, Description, Start_time = task
            col1, col2, col3, col4, col5 = st.columns([2, 2, 4, 2, 2])
            with col1:
                st.write(f'Task ID: {task_id}')
            with col2:
                st.write(f'Task: {Task_Name}')
            with col3:
                st.write(f'Description: {Description}')
            with col4:
                st.write(f'Start Time: {Start_time}')
            with col5:
                delete_button = st.button("❌", key=f"delete_{task_id}")
                if delete_button:
                    delete_task(task_id)
                    st.experimental_rerun()  
        else:
            st.error('Failed to add or retrieve task.')
   
    if st.button('End'):
        if 'task_id' in st.session_state:
            update_status(st.session_state.task_id)  # Update the task status using the stored task_id
            st.success('Task ended successfully.')
            del st.session_state.task_id  # Optionally, clear the task_id from session state
        else:
            st.error('No active task to end.')

        
if __name__ == '__main__':
    main()



