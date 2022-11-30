'''import customtkinter, tkinter

app = customtkinter.CTk()
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

# create scrollable textbox
tk_textbox = tkinter.Text(app, highlightthickness=0)
tk_textbox.grid(row=0, column=0, sticky="nsew")

# create CTk scrollbar
ctk_textbox_scrollbar = customtkinter.CTkScrollbar(app, command=tk_textbox.yview)
ctk_textbox_scrollbar.grid(row=0, column=1, sticky="ns")

# connect textbox scroll event to CTk scrollbar
tk_textbox.configure(yscrollcommand=ctk_textbox_scrollbar.set)

app.mainloop()'''
import cv2

# read image
img = cv2.imread('image.jpg')

# show image
cv2.imshow('image', img)


# define the events for the
# mouse_click.
def mouse_click(event, x, y,
                flags, param):
    # to check if left mouse
    # button was clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        # font for left click event
        font = cv2.FONT_HERSHEY_TRIPLEX
        LB = 'Left Button'

        # display that left button
        # was clicked.
        cv2.putText(img, LB, (x, y),
                    font, 1,
                    (255, 255, 0),
                    2)
        cv2.imshow('image', img)

    # to check if right mouse
    # button was clicked
    if event == cv2.EVENT_RBUTTONDOWN:
        # font for right click event
        font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
        RB = 'Right Button'

        # display that right button
        # was clicked.
        cv2.putText(img, RB, (x, y),
                    font, 1,
                    (0, 255, 255),
                    2)
        cv2.imshow('image', img)


cv2.setMouseCallback('image', mouse_click)

cv2.waitKey(0)

# close all the opened windows.
cv2.destroyAllWindows()
