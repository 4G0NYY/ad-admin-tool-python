import tkinter as tk
import pyad.adquery
import pyad.aduser

def connect_to_active_directory():
    domain = domain_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    try:
        # Connect to Active Directory server
        pyad.set_defaults(ldap_server=domain)
        pyad.aduser.ADUser(username=username, password=password)
        result_label.config(text="Connected successfully!")
    except pyad.pyadexceptions.AuthenticationError:
        result_label.config(text="Authentication failed!")
    except pyad.pyadexceptions.ADException as e:
        result_label.config(text=str(e))

def create_user():
    username = username_entry.get()
    password = password_entry.get()

    # Connect to Active Directory server
    connect_to_active_directory()

    # Create a new user
    new_user = pyad.aduser.ADUser.create(username)
    new_user.set_password(password)
    new_user.update()

    # Display a success message
    result_label.config(text="User created successfully!")

def delete_user():
    username = username_entry.get()

    # Connect to Active Directory server
    connect_to_active_directory()

    # Find the user to delete
    user = pyad.aduser.ADUser.from_cn(username)

    if user:
        # Delete the user
        user.delete()
        result_label.config(text="User deleted successfully!")
    else:
        result_label.config(text="User not found!")

# Create the main window
window = tk.Tk()
window.title("Active Directory Tool")

# Create labels and entry fields
domain_label = tk.Label(window, text="Domain:")
domain_label.pack()
domain_entry = tk.Entry(window)
domain_entry.pack()

username_label = tk.Label(window, text="Username:")
username_label.pack()
username_entry = tk.Entry(window)
username_entry.pack()

password_label = tk.Label(window, text="Password:")
password_label.pack()
password_entry = tk.Entry(window, show="*")
password_entry.pack()

result_label = tk.Label(window, text="")
result_label.pack()

# Create buttons
connect_button = tk.Button(window, text="Connect", command=connect_to_active_directory)
create_user_button = tk.Button(window, text="Create User", command=create_user)
delete_user_button = tk.Button(window, text="Delete User", command=delete_user)

# Position the buttons in the window
connect_button.pack()
create_user_button.pack()
delete_user_button.pack()

# Start the main event loop
window.mainloop()