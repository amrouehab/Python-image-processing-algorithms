import cv2
import numpy as np

def is_blood_connected(img_sample, threshold=145, min_connected_rows=4, min_connected_cols=50):
    """
    Determine if a blood sample is connected based on image analysis.

    Args:
    img_sample: np.array
        An image of the blood sample.
    threshold: int, optional
        The threshold value for converting the image to binary. Defaults to 145.
    min_connected_rows: int, optional
        The minimum number of connected rows required to consider the blood sample as connected. Defaults to 4.
    min_connected_cols: int, optional
        The minimum number of connected columns in a row required to consider the row as part of a connected blood sample. Defaults to 50.

    Returns:
    connected: bool
        Whether the blood sample is connected or not.
    bin_img: np.array
        The binary image used for analysis.
    """
    # convert the image to grayscale
    gray = cv2.cvtColor(img_sample, cv2.COLOR_BGR2GRAY)
    
    # convert to binary using a threshold
    ret, bin_img = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    
    # apply morphological opening to reduce holes and smooth the image
    kernel = np.ones((4, 4), np.uint8)
    img2 = cv2.morphologyEx(~bin_img, cv2.MORPH_OPEN, kernel)

    # initialize variables for loop
    prev_col_val = 0
    prev_row_index = 0
    nof_connected_cols = 0
    nof_connected_rows = 0
    connected_shape_detected = False
    
    # loop through each row in the image
    for i, row in enumerate(img2):
        # reset connected column count for this row
        nof_connected_cols = 0
        
        # loop through each column in the row
        for j, col_val in enumerate(row):
            if col_val == 255: # if the pixel is connected
                nof_connected_cols += 1 # increment the connected column count
                prev_col_val = 255 # update previous column value to 255
            else: # if the pixel is not connected
                prev_col_val = 0 # update previous column value to 0
                # check if the number of connected columns in this row is sufficient
                if nof_connected_cols < min_connected_cols:
                    nof_connected_cols = 0 # reset count if not sufficient
                else: # if the number of connected columns is sufficient, break out of column loop
                    break
        
        # check if this row has any connected columns
        if nof_connected_cols > 0:
            # check if this row is directly below the previous connected row
            if i - prev_row_index == 1:
                nof_connected_rows += 1 # increment connected row count
            prev_row_index = i # update previous row index to current row
        
        # check if enough connected rows have been found
        if nof_connected_rows >= min_connected_rows:
            connected_shape_detected = True
            break
    
    # return whether a connected shape was detected and the binary image used for analysis
    return connected_shape_detected, ~bin_img

# example usage
filename = 'b+antib.png'
img_sample = cv2.imread(filename)

# set optional parameters
threshold = 127
min_connected_rows = 5
min_connected_cols = 25

# determine if sample is connected
connected, img2 = is_blood_connected(img_sample, threshold, min_connected_rows, min_connected_cols)

if connected:
  print("The blood is connected.")
else:
    print("The blood is not connected.")