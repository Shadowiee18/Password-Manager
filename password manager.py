import os.path
from tkinter import ttk
from cryptography.fernet import Fernet
from tkinter import *
from tkinter import messagebox
import bcrypt


def create_key():  # Access key for passwords
    if os.path.exists('mykey.key'):
        with open('mykey.key', 'rb') as mykey:
            key = mykey.read()
            f = Fernet(key)

    elif not os.path.exists('mykey.key'):
        key = Fernet.generate_key()
        with open('mykey.key', 'wb') as mykey:
            mykey.write(key)
            f = Fernet(key)
    return f


def main_window():
    def save_password():
        f = create_key()
        path = 'password.txt'
        if os.path.exists(path):
            with open(path, 'ab') as file:
                file.writelines([
                    ('\n' + 'source ' + source_entry.get().lower() + '\n').encode(),
                    (username_entry.get() + '\n').encode(),
                    f.encrypt(password_entry.get().encode())
                ]
                )
        else:
            with open(path, 'wb') as file:
                file.writelines([
                    ('source ' + source_entry.get().lower() + '\n').encode(),
                    (username_entry.get() + '\n').encode(),
                    f.encrypt(password_entry.get().encode())
                ]
                )

    def view_password():
        def get_login_data():  # Get saved passwords from file
            login_data = {}
            try:
                with open("password.txt", 'rb') as file:
                    lines = file.readlines()
                    for index, line in enumerate(lines):
                        if line.split()[0].decode() == 'source':
                            source = ''.join(line.decode().split()[1:])
                            username = lines[index + 1].decode()
                            password = f.decrypt(lines[index + 2]).decode()
                            if source.capitalize() not in login_data:
                                login_data[source.capitalize()] = [username.strip(), password]
                            else:
                                login_data[source.capitalize()].extend([username.strip(), password])
            except FileNotFoundError:
                messagebox.showerror(message='No passwords found!')
            return login_data

        def get_values(event):
            selected = event.widget.get()
            username_data['text'] = '\n'.join([login_data[selected][i] for i in range(0, len(login_data[selected]), 2)])
            password_data['text'] = '\n'.join([login_data[selected][i] for i in range(1, len(login_data[selected]), 2)])

        f = create_key()
        view_passwords_window = Toplevel(app)

        login_data = get_login_data()
        # Place widgets
        Source = Label(view_passwords_window,
                       text='Source:',
                       font=('Arial', 25, 'bold')
                       )
        Username = Label(view_passwords_window,
                         text='Username:',
                         font=('Arial', 25, 'bold')

                         )
        Password = Label(view_passwords_window,
                         text='Password:',
                         font=('Arial', 25, 'bold')
                         )
        source_data = ttk.Combobox(view_passwords_window,
                                   values=[key for key in login_data.keys()]
                                   )
        source_data.bind('<<ComboboxSelected>>', get_values)
        username_data = Label(view_passwords_window,
                              text='',
                              font=('Arial', 25, 'bold')

                              )
        password_data = Label(view_passwords_window,
                              text='',
                              font=('Arial', 25, 'bold')
                              )
        Source.grid(row=0, column=0)
        source_data.grid(row=1, column=0)
        Username.grid(row=2, column=0)
        username_data.grid(row=3, column=0)
        Password.grid(row=4, column=0)
        password_data.grid(row=5, column=0)
        get_login_data()

    app = Tk()
    app.geometry('400x400')

    source = Label(app,
                   text='Source',
                   font=('Arial', 25, 'bold')
                   )
    source_entry = Entry(app,
                         font=('Arial', 15, 'bold')
                         )
    username = Label(app,
                     text='Username:',
                     font=('Arial', 25, 'bold')
                     )
    username_entry = Entry(app,
                           font=('Arial', 15, 'bold')
                           )
    password_entry = Entry(app,
                           font=('Arial', 15, 'bold'),
                           show='*'
                           )
    password = Label(app,
                     text='Password:',
                     font=('Arial', 25, 'bold')
                     )
    source.grid(column=0, row=0, sticky='w')
    source_entry.grid(column=0, row=1)
    username.grid(column=0, row=2, sticky='w', ipady=10)
    username_entry.grid(column=0, row=3, columnspan=1)
    password.grid(column=0, row=4, sticky='w', ipady=10)
    password_entry.grid(column=0, row=5)
    save = Button(app,
                  text='Save',
                  font=('Arial', 20, 'bold'),
                  command=save_password
                  )
    view = Button(app,
                  text='View',
                  font=('Arial', 20, 'bold'),
                  command=view_password
                  )
    save.grid(row=6, column=0, columnspan=1, pady=30)
    view.grid(row=6, column=1)


def login():
    user_username = admin_username.get().encode()
    user_password = admin_password.get().encode()
    with open('admin.txt', 'rb') as file:
        lines = file.readlines()
        if lines[0].strip() == user_username and bcrypt.checkpw(user_password, lines[1]):
            window.destroy()
            main_window()
        else:
            messagebox.showerror(title="Error", message="Invalid login.")


if __name__ == '__main__':
    window = Tk()
    window.title("Login form")
    window.geometry('500x500')
    window.configure(bg='#333333')

    frame = Frame(bg='#333333')

    # Creating widgets
    login_label = Label(
        frame, text="Login", bg='#333333', fg="#FF3399", font=("Arial", 30))
    username_label = Label(
        frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    admin_username = Entry(frame, font=("Arial", 16))
    admin_password = Entry(frame, show="*", font=("Arial", 16))
    password_label = Label(
        frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    login_button = Button(
        frame, text="Login", activebackground="#FF3399", activeforeground="#FFFFFF", bg="#FF3399", font=("Arial", 16),
        command=login)

    # Placing widgets on the screen
    login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
    username_label.grid(row=1, column=0)
    admin_username.grid(row=1, column=1, pady=20)
    password_label.grid(row=2, column=0)
    admin_password.grid(row=2, column=1, pady=20)
    login_button.grid(row=3, column=0, columnspan=2, pady=30)

    frame.pack()

    window.mainloop()
