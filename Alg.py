import numpy as np
import cv2


def is_blood_connected(img_sample, threshold=145, opening_kernel_size=(4, 4), min_connected_rows=5, min_connected_cols=50):
    # convert the image to gray
    gray = cv2.cvtColor(img_sample, cv2.COLOR_BGR2GRAY)
    # convert it to binary
    _, bin_img = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    # setup the kernel (SE) for opening process
    kernel = np.ones(opening_kernel_size, np.uint8)
    # start opening process to reduce the holes and to smooth the image
    img2 = cv2.morphologyEx(~bin_img, cv2.MORPH_OPEN, kernel)

    # initializing section (set a default values before entering the loop)
    previous_row_index = 0
    nof_equal_cols = 0
    previous_col = 0
    connected_rows = 0
    row_index = 0
    connected_shape_detected = False

    # loop over each row of the image
    for row in img2:
        # reset the number of connected columns for this row
        nof_equal_cols = 0
        # loop over each column in this row
        for col_val in row:
            # check if the current column value is equal 255
            if col_val == 255:
                # check if the prev column value is also 255
                if previous_col == 255:
                    # if true increase nof connected continuous columns by 1
                    nof_equal_cols += 1
                # set the previous column value to 255
                previous_col = 255
            else:
                # if the current column value is not 255, set the previous column value to 0
                previous_col = 0
                # if the number of connected columns for the current row is less than the minimum required,
                # reset the counter because the current column value is zero which breaks the continuity of
                # the connected columns
                if nof_equal_cols < min_connected_cols:
                    nof_equal_cols = 0
                # if the number of connected columns is greater than or equal to the minimum required,
                # break the loop because we have a connected row
                else:
                    break

        # check if the current row has connected columns
        if nof_equal_cols > 0:
            # if the current connected row index is just after the previous connected row index,
            # increase the number of connected rows
            if row_index - previous_row_index == 1:
                connected_rows += 1
            # set the current row index to be the previous row index for next time
            previous_row_index = row_index

        # check if the number of connected rows is greater than or equal to the minimum required,
        # set the connected_shape_detected flag and break the loop
        if connected_rows >= min_connected_rows:
            connected_shape_detected = True
            break

        # increment the row index
        row_index += 1

    return connected_shape_detected, ~bin_img