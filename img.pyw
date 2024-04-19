import sys
import os.path
from PIL import ImageGrab

# Define the directory path where you want to save the screenshots
directory = "C:/Users/Yu Ling/Documents/Python Scripts/projects/AI/screenshots/"
'''
nested_list_str = sys.argv[1]


# Convert the string representation back to a nested list
nested_list = eval(nested_list_str)
'''

# Define the base filename for the screenshot
filename = "0.png"

top = 90   # Top coordinate
for row in range(3):
    left = 660  # Left coordinate
    top = 240 + 200 * row
    for col in range(3):
        left = 660 + 200 * col
        width = 200  # Width of the region
        height = 200  # Height of the region

        # Calculate the right and bottom coordinates based on the width and height
        right = left + width
        bottom = top + height
        '''
        if nested_list[row][col] == "":
            directory = "C:/Users/Yu Ling/Documents/Python Scripts/projects/AI/training/blank/"
        elif nested_list[row][col] == "O":
            directory = "C:/Users/Yu Ling/Documents/Python Scripts/projects/AI/training/circle/"
        else:
            directory = "C:/Users/Yu Ling/Documents/Python Scripts/projects/AI/training/cross/"
        '''
        # Construct the full path to the filename
        full_path = os.path.join(directory, filename)

        # Check if the file already exists
        counter = 1
        while os.path.exists(full_path):
            # If the file already exists, append a counter to the filename
            full_path = os.path.join(directory, "{}.png".format(counter))
            counter += 1

        # Capture the screenshot
        screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

        # Save the screenshot to the file
        screenshot.save(full_path)
