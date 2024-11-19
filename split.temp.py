import os
import json

# Define the directory path
output_dir = "output"

# Prepare a list to hold the parsed data
scores = []

# Traverse through all the files in the directory
for file_name in os.listdir(output_dir):
    if "_" in file_name:  # Ensure the file name has the expected format
        try:
            # Split the file name into attempt and score
            attempt, score_with_ext = file_name.split("_")
            score = os.path.splitext(score_with_ext)[0]  # Remove the file extension
            
            # Convert the attempt and score to integers
            attempt = int(attempt)
            score = int(score)
            
            # Append the data as a tuple
            scores.append({"attempt": attempt, "score": score})
        except ValueError:
            print(f"Skipping file {file_name} due to unexpected format.")

# Sort the scores in descending order based on the 'score' key
scores.sort(key=lambda x: x["score"], reverse=True)

# Output JSON file path
output_json_path = "sorted_scores.json"

# Save the sorted data into a JSON file
with open(output_json_path, "w") as json_file:
    json.dump(scores, json_file, indent=4)

print(f"Scores successfully saved to {output_json_path}")
