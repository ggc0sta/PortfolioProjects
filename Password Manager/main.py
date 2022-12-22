# Canvas documentation: https://tkdocs.com/tutorial/canvas.html
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    # [new_item for item in list]
    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(symbols) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)
    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    # retrieve data from 3 text fields
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please complete all fields prior to saving")
    else:
        try:
            with open("passwords.json", mode="r") as data_file:
                # Reading old data
                data = json.load(data_file)

        except FileNotFoundError:
            with open("passwords.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)
            with open("passwords.json", mode="w") as data_file:
                # save data to a file
                json.dump(data, data_file, indent=4)  # number of spaces to indent
        finally:
            # clear data entries
            website_entry.delete(0, "end")
            password_entry.delete(0, "end")


# -------------------------- SEARCH PASSWORD ---------------------------#

def search_password():
    try:
        with open("passwords.json", mode="r") as data_file:
            data = json.load(data_file)
            credentials = data[website_entry.get()]
            email = credentials["email"]
            pw = credentials["password"]
            messagebox.showinfo(title=f"{website_entry.get()}", message=f"Email: {email} \n Password: {pw}")
            # print(f"site: {website_entry.get()}\nEmail: {email}\nPassword: {pw}")
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="You don't have any passwords saved.")
    except KeyError:
        # If there is no data for the given website
        messagebox.showinfo(title="Oops",
                            message=f"I didn't find credentials for {website_entry.get()} in the database.")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.config(padx=50, pady=50)
window.title("Password Manager")
logo = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=21)
website_entry.grid(column=1, row=1, columnspan=1)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "gabriel@gmail.com")
password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

# Buttons
search_button = Button(text="Search", width=10, command=search_password)
search_button.grid(column=2, row=1)
generate_button = Button(text="Gen Password", width=10, command=generate_password)
generate_button.grid(column=2, row=3)
add_button = Button(width=33, text="Add", command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
