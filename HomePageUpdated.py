import streamlit as st
from datetime import datetime
import sqlite3


def get_db_connection():
    return sqlite3.connect('TimeLogAppInfor.db', check_same_thread=False)

if 'db_conn' not in st.session_state:
    st.session_state.db_conn = get_db_connection()

def create_table():
    conn = st.session_state.db_conn
    with conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS Activity_Infors (
                            Activity_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                            Activity_Name TEXT, 
                            Description TEXT,
                            Date DATE,
                            Start_time TIME,
                            End_time TIME)''')
        conn.commit()
        

def add_Activity(Activity_Name, Description):
    current_time = datetime.now()
    Start_time = current_time.strftime('%H:%M:%S')
    Datenow = datetime.now()
    Date =Datenow.date()
    
    conn = st.session_state.db_conn
    with conn:
        cur = conn.cursor()
        cur.execute ('INSERT INTO Activity_Infors ( Activity_Name, Description, Start_time, Date) VALUES (?, ?, ?, ?)', (Activity_Name, Description, Start_time, Date ))
        Activity_id = cur.lastrowid
        conn.commit()
    
    return Activity_id
   
    
# Function to retrieve Activitys from the database
def get_Activity():
    conn = st.session_state.db_conn
    with conn:
        cur = conn.cursor()
        cur.execute('SELECT Activity_id, Activity_Name, description, Start_time FROM Activity_Infors ')
        Activity = cur.fetchone()
    
    return Activity


def update_Endtime(Activity_id, End_time):
    
    conn = st.session_state.db_conn
    with conn:
        cur = conn.cursor()
        cur.execute('UPDATE Activity_Infors SET End_time=? WHERE Activity_ID=?', (End_time, Activity_id))
        Activity_id = cur.lastrowid
    conn.commit()
   

def delete_Activity(Activity_id):
    conn = st.session_state.db_conn
    with conn:
        cur = conn.cursor()
        cur.execute('DELETE FROM Activity_Infors WHERE Activity_ID=?', (Activity_id,))
    conn.commit()
    


# Main Streamlit app
def main():
     
    hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    st.title('Task TimeLog')

    create_table()

    # Initialize session state variables if they don't exist
    if 'Activity_Name' not in st.session_state:
        st.session_state.activity_name = ""
    if 'description' not in st.session_state:
        st.session_state.description = ""
    if 'Activity_id' not in st.session_state:
        st.session_state.Activity_id = None
   
    Activity_Name = st.text_input("Activity Name", value=st.session_state.activity_name, key="Activity_Name")
    Description = st.text_area("Description", value=st.session_state.description, key="Description")

    # Button to call the add_activity function with the inputs from text input and text area
    if st.button('Start'):
        Activity_id= add_Activity(Activity_Name, Description)
        st.session_state['Activity_id'] = Activity_id

        #show activity
        Activity = get_Activity()
        if Activity:
            Activity_id, Activity_Name, Description, Start_time = Activity
            col1, col2, col3, col4, col5 = st.columns([2, 2, 4, 2, 2])
            with col1:
                st.write(f'Activity ID: {Activity_id}')
            with col2:
                st.write(f'Activity: {Activity_Name}')
            with col3:
                st.write(f'Description: {Description}')
            with col4:
                st.write(f'Start Time: {Start_time}')
            with col5:
                if st.button("Delete"):
                    if 'Activity_id' in st.session_state and st.session_state['Activity_id']:
                         st.write(st.session_state['Activity_id'])
                         Activity_id = st.session_state['Activity_id']
                         delete_Activity(Activity_id)
                         st.write(st.session_state['Activity_id'])
                         
                         
                    else:
                        st.error("No activity selected for deletion.")

        else:
            st.error('Failed to add or retrieve Activity.')
            
            
    if st.button('End'):
        if 'Activity_id' in st.session_state and st.session_state['Activity_id'] is not None:
            # Get the current time as the end time
            end_time = datetime.now().strftime('%H:%M:%S')
            # Pass both Activity_id and the end time to the update_status function
            update_Endtime(st.session_state['Activity_id'], end_time)
            st.success("Activity ended successfully.")
            # Clear the activity from session state
            del st.session_state['Activity_id']
        else:
            st.error('No active Activity to end.')

    
        
if __name__ == '__main__':
    main()



