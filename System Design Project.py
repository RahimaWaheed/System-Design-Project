import streamlit as st
from datetime import datetime

# Function to record time
def record_time():
    return datetime.now()

# Function to save data to a file
def save_data(start_time, finish_time, elapsed_time):
    with open("recorded_data.txt", "a") as file:
        file.write(f"Start Time: {start_time}, Finish Time: {finish_time}, Elapsed Time: {elapsed_time}\n")

# Function to retrieve data from the file
def retrieve_data():
    try:
        with open("recorded_data.txt", "r") as file:
            data = file.read()
            return data
    except FileNotFoundError:
        return "No recorded data available."

# Function to plot recorded data using Streamlit line chart
# Function to plot recorded data using Streamlit line chart
def plot_data():
    try:
        with open("recorded_data.txt", "r") as file:
            lines = file.readlines()
            start_times = []
            elapsed_times = []

            for line in lines:
                if "Start Time:" in line and "Elapsed Time:" in line:
                    start_time_str = line.split("Start Time:")[1].split(",")[0].strip()
                    elapsed_time_str = line.split("Elapsed Time:")[1].strip()
                    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S.%f")  # Updated format
                    elapsed_time = sum(map(int, elapsed_time_str.split(":"))) + start_time.microsecond / 1e6
                    start_times.append(start_time)
                    elapsed_times.append(elapsed_time)

            # Plotting the data using Streamlit line chart
            chart_data = {"Start Time": start_times, "Elapsed Time": elapsed_times}
            st.line_chart(chart_data)

    except FileNotFoundError:
        st.warning("No recorded data available.")

def main():
    st.title("Time Recorder App")

    # Initialize session state
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'finish_time' not in st.session_state:
        st.session_state.finish_time = None

    # Create three columns
    col1, col2, col3 = st.columns(3)

    # Add "Start" button to the first column
    if col1.button("Start", key="start_button"):
        st.session_state.start_time = record_time()
        st.success(f"Recording started at: {st.session_state.start_time}")

    # Add "Finish" button to the second column
    if col2.button("Finish", key="finish_button"):
        if st.session_state.start_time is None:
            st.warning("Please start recording first.")
        else:
            st.session_state.finish_time = record_time()
            st.success(f"Recording finished at: {st.session_state.finish_time}")

            # Calculate and display elapsed time
            elapsed_time = st.session_state.finish_time - st.session_state.start_time
            st.info(f"Elapsed time: {elapsed_time}")

            # Save data to a file
            save_data(st.session_state.start_time, st.session_state.finish_time, elapsed_time)

    # Display recorded times
    if st.session_state.start_time is not None:
        st.info(f"Start Time: {st.session_state.start_time}")
    if st.session_state.finish_time is not None:
        st.info(f"Finish Time: {st.session_state.finish_time}")

    # Add a button to retrieve data
    if col3.button("Retrieve Recorded Data"):
        recorded_data = retrieve_data()
        st.text_area("Recorded Data:", recorded_data)

    # Add a button to plot the data
    if col3.button("Plot Recorded Data"):
        plot_data()

if __name__ == "__main__":
    main()
