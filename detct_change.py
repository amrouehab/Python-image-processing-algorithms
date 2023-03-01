import cv2
import numpy as np


# this function takes the sample image and return a bool which indicate whether the blood sample is connected or not
def is_blood_connected(img_sample):
    # convert the image to gray
    gray = cv2.cvtColor(img_sample, cv2.COLOR_BGR2GRAY)
    # convert it to binary
    ret, bin_img = cv2.threshold(gray, 145, 255, cv2.THRESH_BINARY)
    # setup the kernel (SE) for opening process
    kernel = np.ones((4, 4), np.uint8)
    # start opening process to reduce the holes and to smooth the image
    img2 = cv2.morphologyEx(~bin_img, cv2.MORPH_OPEN, kernel)
    # initializing section (set a default values before entering the loop)
    previous_row_index = 0
    nof_equal_colms = 0
    previous_colm = 0
    connected_rows = 0
    row_index = 0
    connected_shape_detected = False
    # ############ start the loop (which loop around the image point by point to indicate any connected rows ) and
    # the main idea is by detecting for every row any connected pixels in a single row if there are more than 50
    # continuous points which have a value of 255 this means that this row has high probability to be part of a
    # connected blood so after that increase the connected rows by 1 then do this for all rows until the nof
    # connected rows be >4 then now we have more than 4 continuous rows which have more than 50 continuous connected
    # pixels then break the loop and return a bool which indicate that the blood is connected

    for row in img2:  # get the current row from the outer loop
        for col_val in row:  # loop around this row
            if col_val == 255:  # check if the current col_value is equal 255
                if previous_colm == 255:  # check also if the prev colum value is 255
                    nof_equal_colms = nof_equal_colms + 1  # if true increase nof connected continuous columns by 1
                previous_colm = 255  # set the previous column value to be 255 cuz the current column is 255 and will be a previous one
            else:  # if the currnet column value not 255 then set the prev_colum value to be 0
                previous_colm = 0
                if nof_equal_colms < 50:  # check if the nof connected columns for the current row is more than 50
                    # if so reset the counter because the current column value is zero which breaks the continuity of
                    #  the connected columns
                    nof_equal_colms = 0
                else:  # if nof connected columns >255 break the loop because we have got a connected row
                    break

        if nof_equal_colms > 0:  # check if the current row is have  connected columns
            if row_index - previous_row_index == 1:  # if the current connected row index is just after the prev connected row
                connected_rows = connected_rows + 1  # increase connected rows by 1

            previous_row_index = row_index  # set the current row index to be a previous row for next time
        if connected_rows > 4:  # check if the detected connected rows is more than 4 to break the loop
            connected_shape_detected = True
            break
        row_index = row_index + 1  # increment the row index

    return connected_shape_detected, ~bin_img


filename = 'b+antib.png'
img_sample = cv2.imread(filename)
connected, img2 = is_blood_connected(img_sample)

if connected:
    print("the blood is connected")
else:
    print("the blood isn't connected")
# cv2.imshow("image",img2)
cv2.imshow("image3", img2)
filename = 'b+antib.png'
img = cv2.imread(filename)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret2, bin_img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
kernel = np.ones((5, 5), np.uint8)
opening = cv2.morphologyEx(~bin_img, cv2.MORPH_OPEN, kernel)
cv2.imshow("image2", opening)
cv2.waitKey(0)
cv2.destroyAllWindows()
