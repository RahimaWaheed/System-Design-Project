import streamlit as st
from datetime import datetime
import pandas as pd
import sqlite3
import asyncio
import time

# SQLite code: data management
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
    Date = Datenow.date()
    conn = sqlite3.connect('TimeLogAppInfor.db')
    c = conn.cursor()
    c.execute ('INSERT INTO Activity_Infors (Activity_Name, Description, Start_time, Date) VALUES (?, ?, ?, ?)', (Activity_Name, Description, Start_time, Date))
    Activity_id = c.lastrowid
    conn.commit()
    conn.close()
    return Activity_id

def get_Activity(Activity_ID):
    conn = sqlite3.connect('TimeLogAppInfor.db')
    c = conn.cursor()
    c.execute('SELECT Activity_ID, Activity_Name, Description, Start_time FROM Activity_Infors WHERE Activity_ID=?', (Activity_ID,))
    Activity = c.fetchone()
    conn.close()
    return Activity

def update_Endtime(Activity_id, End_time):
    conn = sqlite3.connect('TimeLogAppInfor.db')
    c = conn.cursor()
    c.execute('UPDATE Activity_Infors SET End_time=? WHERE Activity_ID=?', (End_time, Activity_id))
    Activity_id = c.lastrowid
    conn.commit()
    conn.close()

def delete_Activity(Activity_id):
    try:
        conn = sqlite3.connect('TimeLogAppInfor.db')
        c = conn.cursor()
        c.execute('DELETE FROM Activity_Infors WHERE Activity_ID=?', (Activity_id,))
        conn.commit()
        conn.close()
        return "Success"
    except Exception as e:
        return f"Error: {e}"

def main():
    hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    st.title('Activity TimeLog')

    create_table()

    # Initialize session state variables if they don't exist
    if 'Activity_id' not in st.session_state:
        st.session_state.Activity_id = None

    # Create text input for the activity name
    Activity_Name = st.text_input("Activity Name")

    # Create text area for the activity description
    Description = st.text_area("Description")

    # Button to call the add_activity function with the inputs from text input and text area
    if st.button('Start'):
        Activity_id = add_Activity(Activity_Name, Description)
        st.session_state.Activity_id = Activity_id

    # Show activity if it exists
    if st.session_state.Activity_id is not None:
        Activity = get_Activity(st.session_state.Activity_id)
        if Activity:
            Activity_id, Activity_Name, Description, Start_time = Activity
            st.write(f'Activity ID: {Activity_id}')
            st.write(f'Activity: {Activity_Name}')
            st.write(f'Description: {Description}')
            st.write(f'Start Time: {Start_time}')
            delete_button = st.button("❌ Delete")
            if delete_button:
                print("Deleting Activity:", Activity_id)  # Debugging print statement
                delete_result = delete_Activity(Activity_id)
                print("Delete Result:", delete_result)  # Debugging print statement
                if delete_result == "Success":
                    st.success("Activity deleted successfully.")
                    time.sleep(1)  # Pause for 2 seconds
                    st.experimental_rerun()  # Refresh the page

    # Button to end activity
    if st.button('End'):
        if st.session_state.Activity_id is not None:
            end_time = datetime.now().strftime('%H:%M:%S')
            update_Endtime(st.session_state.Activity_id, end_time)
            st.success("Activity ended successfully.")
            time.sleep(1)
            st.experimental_rerun()



if __name__ == '__main__':
    main()
