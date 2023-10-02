import pandas as pd
import re

# Define a regular expression pattern to match date-time lines and messages.
#date_time_pattern = r'\[(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}:\d{2})\] ~\s([\w\s]+):'
#message_pattern = r'(\d+\.\s[\w\s+]+\S*)\s✅?'


date_time_pattern = r'\[(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}:\d{2})\](?: ~\s)?([\w\s]+):'
message_pattern = r'(\d+\.\s[\w\s+]+\S*)\s✅?'


# Initialize variables to store date-time, sender, and messages.
current_date_time = None
current_sender = None
messages = []

# Open the WhatsApp chat file.
with open('rapta.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # Check if the line matches the date-time pattern.
        date_time_match = re.match(date_time_pattern, line)
        if date_time_match:
            # Extract the date-time and sender information.
            current_date_time = date_time_match.group(1)
            current_sender = date_time_match.group(2)
        else:
            # Check if the line contains a message.
            message_match = re.search(message_pattern, line)
            if message_match:
                # Extract and append the message to the messages list.
                messages.append([current_date_time, current_sender, message_match.group(1)])

# Create a Pandas DataFrame with three columns.
df = pd.DataFrame(messages, columns=['Timestamp', 'Sender', 'Message'])


# Remove leading spaces from the entire column
df['Sender'] = df['Sender'].str.strip()


# Print the DataFrame
# print(df)
# print(df.head(15))

df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d/%m/%Y, %H:%M:%S')

# Filter rows where the sender is "Hez Holland" and the message contains "Hez"
# filtered_df = df[(df['Sender'] == 'Hez Holland') & df['Message'].str.contains('Hez')]

# Extract the day of the week and add it to a new column
df['day_sent'] = df['Timestamp'].dt.strftime('%A')

pd.set_option('display.max_rows', None)

newdf = df[df["day_sent"] == 'Sunday'].copy()


# Initialize a variable to keep track of the last sender name
last_sender = None

# Create an empty list to store the indices of rows to be removed
rows_to_remove = []

# Iterate through the DataFrame
for index, row in newdf.iterrows():
    sender_name = row['Sender']
    
    # Check if the sender name is the same as the last one
    if sender_name == last_sender:
        rows_to_remove.append(index)
    else:
        last_sender = sender_name

# Drop the rows to be removed
newdf.drop(rows_to_remove, inplace=True)

# Reset the index if needed
newdf.reset_index(drop=True, inplace=True)

# Display the modified DataFrame
print(newdf)

