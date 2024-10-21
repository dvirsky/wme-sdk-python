import pandas as pd
import matplotlib.pyplot as plt
import ast

# File path to the CSV
csv_file_path = './data/output.csv'

# Read the CSV file
df = pd.read_csv(csv_file_path)

# Convert the 'Electoral Vote' from string representation of list to actual list using `ast.literal_eval`
df['Electoral Vote'] = df['Electoral Vote'].apply(ast.literal_eval)

# Sort the DataFrame by 'Year'
df = df.sort_values(by='Year')

# Extract the votes for the winner, second, and third candidates
df['Winner'] = df['Electoral Vote'].apply(lambda x: x[0])
df['Second'] = df['Electoral Vote'].apply(lambda x: x[1])
df['Third'] = df['Electoral Vote'].apply(lambda x: x[2] if len(x) > 2 else None)


# Function to insert line breaks after every second word, except two-letter words
def format_nominee_text(nominee):
    words = nominee.split()
    formatted = []
    word_count = 0
    for word in words:
        if len(word) > 2:  # Only count words with more than two letters
            word_count += 1
        formatted.append(word)
        if word_count == 2:  # After every second long word, insert a line break
            formatted.append("\n")
            word_count = 0
    return " ".join(formatted).replace(" \n", "\n").replace("\n ", "\n")  # Clean up spaces around \n

# Create a formatted nominee column
df['Formatted_Nominee'] = df['Nominee'].apply(format_nominee_text)

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(df['Year'], df['Winner'], marker='o', label='Winner')
plt.plot(df['Year'], df['Second'], marker='o', label='Second')
plt.plot(df['Year'], df['Third'], marker='o', label='Third', linestyle='--')

# Set the main X-axis labels (Years) without rotation
plt.xticks(df['Year'], labels=df['Year'], fontsize=10)

# Labels and title
# plt.xlabel('Year')
plt.ylabel('Electoral Votes')
plt.title('Electoral Votes Over Time')
plt.legend()

# Adjust the bottom limit of the Y-axis to create space for the nominee labels
#plt.ylim(bottom=min(df['Winner']))  # Adjust bottom limit of Y-axis

# Place nominee labels below the X-axis at a 60-degree angle
for i, nominee in enumerate(df['Formatted_Nominee']):
    plt.text(df['Year'].iloc[i], min(df['Winner']) - 475, nominee, fontsize=8, ha='center', rotation=45)

# Show plot
plt.grid(True)
plt.tight_layout()
plt.show()
