import streamlit as st
import pandas as pd


def getAll_Activity(start_date, end_date):
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    conn = st.session_state.db_conn
    with conn:
        cur = conn.cursor()
        cur.execute('SELECT Activity_Name, description, Date, Start_time, End_time FROM Activity_Infors WHERE Date >= ? AND Date<= ? ', (start_date, end_date))
        data = cur.fetchall()
    return data

def main():

     # Initialize or update session states for Start_time and End_time
    if 'Start_time' not in st.session_state:
        st.session_state.Start_time = pd.to_datetime("today").date()  # Default to today
    if 'End_time' not in st.session_state:
        st.session_state.End_time = pd.to_datetime("today").date()  # Default to today

    Start_date = st.date_input("Start Date", value=st.session_state.Start_time)
    End_date = st.date_input("End Date", value=st.session_state.End_time)

    if Start_date > End_date:
        st.error('Error: End date must fall after start date.')

    if 'db_conn' in st.session_state:
        data = getAll_Activity(Start_date, End_date)
        if data:
            # Convert data into a DataFrame for display
            df = pd.DataFrame(data, columns=['Activity_Name', 'Description', 'Date', 'Start_time', 'End_time'])
            st.write(f"Displaying activities from {Start_date} to {End_date}:")
            st.dataframe(df)  # Using st.dataframe for better formatting and interaction
        else:
            st.write("No activities found within the selected date range.")
    

if __name__ == '__main__':
    main()




