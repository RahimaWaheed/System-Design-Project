import streamlit as st
from datetime import datetime
import pandas as pd
import sqlite3

#SQLite code: data mamangement

def create_table():
    conn = sqlite3.connect('TimeLogAppInfor.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Activity_Infors (
                    Activity_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                    Activity_Name TEXT, 
                    Description TEXT,
                    Date DATE,
                    Start_time TIME,
                    End_time TIME)''')
    conn.commit()
    conn.close()

def add_Activity(Activity_Name, Description):
    current_time = datetime.now()
    Start_time = current_time.strftime('%H:%M:%S')
    Datenow = datetime.now()
    Date =Datenow.date()
    conn = sqlite3.connect('TimeLogAppInfor.db')
    c = conn.cursor()
    c.execute ('INSERT INTO Activity_Infors ( Activity_Name, Description, Start_time, Date) VALUES (?, ?, ?, ?)', (Activity_Name, Description, Start_time, Date ))
    Activity_id = c.lastrowid
    conn.commit()
    conn.close()
    return Activity_id
   
    
# Function to retrieve Activitys from the database
def get_Activity():
    conn = sqlite3.connect('TimeLogAppInfor.db')
    c = conn.cursor()
    c.execute('SELECT Activity_id, Activity_Name, description, Start_time FROM Activity_Infors ')
    Activity = c.fetchone()
    conn.close()
    return Activity


def update_Endtime(Activity_id, End_time):
    
    conn = sqlite3.connect('TimeLogAppInfor.db')
    c = conn.cursor()
    c.execute('UPDATE Activity_Infor SET End_time=? WHERE Activity_ID=?', (End_time, Activity_id))
    Activity_id = c.lastrowid
    conn.commit()
    conn.close()

def delete_Activity(Activity_id):
    conn = sqlite3.connect('TimeLogAppInfor.db')
    c = conn.cursor()
    c.execute('DELETE FROM Activity_Infor WHERE Activity_ID=?', (Activity_id,))
    conn.commit()
    conn.close()


# Main Streamlit app
def main():
    st.title('Activity TimeLog')

    create_table()

    # Initialize session state variables if they don't exist
    if 'Activity_Name' not in st.session_state:
        st.session_state.activity_name = ""
    if 'description' not in st.session_state:
        st.session_state.description = ""
    if 'Activity_id' not in st.session_state:
        st.session_state.Activity_id = None
        st.write(st.session_state['Activity_id'])
    # Create text input for the activity name
    Activity_Name = st.text_input("Activity Name", value=st.session_state.activity_name, key="Activity_Name")

    # Create text area for the activity description
    Description = st.text_area("Description", value=st.session_state.description, key="Description")

    # Button to call the add_activity function with the inputs from text input and text area
    if st.button('Start'):
        Activity_id=add_Activity(Activity_Name, Description)
        st.session_state['Activity_id'] = Activity_id

        #show activity
        Activity = get_Activity()
        if Activity:
            Activity_id, Activity_Name, Description, Start_time = Activity
            col1, col2, col3, col4, col5 = st.columns([2, 2, 4, 2, 2])
            with col1:
                st.write(f'Activity ID: {Activity_id}')
                st.write(st.session_state['Activity_id'])
            with col2:
                st.write(f'Activity: {Activity_Name}')
            with col3:
                st.write(f'Description: {Description}')
            with col4:
                st.write(f'Start Time: {Start_time}')
            with col5:
                delete_button = st.button("❌", key=f"delete_{Activity_id}")
                if delete_button:
                    delete_Activity(Activity_id)
                    st.experimental_rerun()  
            st.write(st.session_state['Activity_id'])
        else:
            st.error('Failed to add or retrieve Activity.')
            
        st.write(st.session_state['Activity_id'])
            
    if st.button('End'):
        if 'Activity_id' in st.session_state and st.session_state['Activity_id'] is not None:
            # Get the current time as the end time
            end_time = datetime.now().strftime('%H:%M:%S')
            # Pass both Activity_id and the end time to the update_status function
            update_Endtime(st.session_state['Activity_id'], end_time)
            st.success("Activity ended successfully.")
            # Clear the activity from session state
            print("Updating End time for Activity ID:", st.session_state['Activity_id'])

            del st.session_state['Activity_id']
        else:
            st.error('No active Activity to end.')

    
        
if __name__ == '__main__':
    main()



