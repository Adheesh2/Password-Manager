from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password = []

    [password.append(random.choice(letters)) for _ in range(nr_letters)]

    [password.append(random.choice(symbols)) for _ in range(nr_symbols)]

    [password.append(random.choice(numbers)) for _ in range(nr_numbers)]

    random.shuffle(password)
    password_string = "".join(password)
    password_entry.delete(0, END)
    password_entry.insert(0, password_string)
    pyperclip.copy(password_string)
    # print(f"Your Password is :{password_string}")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website_name = website_entry.get().title()
    user_name = user_name_entry.get()
    password = password_entry.get()

    if len(user_name) == 0 or len(website_name) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!!")
    else:
        is_ok = messagebox.askokcancel(title=website_name,
                                       message=f"These are the details Entered :\nEmail:{user_name}"
                                               f"\nPassword:{password}"
                                               f"\nIs it Ok to Save?")
        new_data = {
            website_name: {
                "email": user_name,
                "password": password
            }
        }
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    # Reading Old Data
                    data = json.load(data_file)
                    # Updating Old Data
                    data.update(new_data)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                if website_name in data:
                    is_ok = messagebox.askokcancel(title=website_name,
                                                   message=f"Password for {website_name} already Saved\n"
                                                           f"Would you Like to Update it?")
                    if is_ok:
                        data[website_name]["email"] = user_name
                        data[website_name]["password"] = password
                        with open("data.json", "w") as data_file:
                            json.dump(data, data_file, indent=4)
                else:
                    with open("data.json", "w") as data_file:
                        json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- SEARCH WEBSITE ------------------------------- #

def search_website():
    website_name = website_entry.get().title()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        messagebox.showerror(title="ERROR", message="No Entries Done")
    else:
        if website_name in data:
            messagebox.showinfo(title=website_name, message=f"Email:{data[website_name]['email']}"
                                                            f"\nPassword:{data[website_name]['password']}")
            pyperclip.copy(data[website_name]['password'])
        else:
            messagebox.showerror(title="ERROR", message=f"No details of {website_name} Found")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

logo = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

website_entry = Entry(width=21)
website_entry.grid(row=1, column=1, sticky="EW")
website_entry.focus()

search_button = Button(text="Search", command=search_website)
search_button.grid(row=1, column=2, sticky="EW")

user_label = Label(text="Email/Username:")
user_label.grid(row=2, column=0)

user_name_entry = Entry(width=35)
user_name_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
user_name_entry.insert(0, "user@email.com")

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky="EW")

password_button = Button(text="Generate Password", command=password_generator)
password_button.grid(row=3, column=2, sticky="EW")

add_button = Button(text="Add", width=36, command=save_password)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

window.mainloop()
