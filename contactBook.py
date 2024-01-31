import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")

        self.setup_gui()
        self.configure_layout()

        self.contacts = []

    def setup_gui(self):
        self.load_background_image()
        self.create_style()

        self.create_contact_entry_widgets()
        self.create_buttons()

        self.create_search_widgets()

    def configure_layout(self):
        for i in range(10):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

    def load_background_image(self):
        self.image = Image.open('contact.gif')
        self.img_copy = self.image.copy()
        self.photo_image = ImageTk.PhotoImage(self.image, master=self.root)

        self.background_label = tk.Label(self.root, image=self.photo_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label.bind('<Configure>', self._resize_image)

    def create_style(self):
        style = ttk.Style()

        style.configure('TLabel', font=('Arial', 12))
        style.configure('TButton', font=('Arial', 12), padding=(5, 5, 5, 5))
        style.configure('TEntry', font=('Arial', 12), padding=(5, 5, 5, 5))

    def create_contact_entry_widgets(self):
        self.name_label = ttk.Label(self.root, text="Name:")
        self.name_label.grid(row=4, column=5, padx=5, pady=5, sticky="e")
        self.name_entry = ttk.Entry(self.root)
        self.name_entry.grid(row=4, column=6, padx=5, pady=5, sticky="w")

        self.phone_label = ttk.Label(self.root, text="Phone Number:")
        self.phone_label.grid(row=4, column=7, padx=5, pady=5, sticky="e")
        self.phone_entry = ttk.Entry(self.root)
        self.phone_entry.grid(row=4, column=8, padx=5, pady=5, sticky="w")

        self.email_label = ttk.Label(self.root, text="Email:")
        self.email_label.grid(row=5, column=5, padx=5, pady=5, sticky="e")
        self.email_entry = ttk.Entry(self.root)
        self.email_entry.grid(row=5, column=6, padx=5, pady=5, sticky="w")

        self.address_label = ttk.Label(self.root, text="Address:")
        self.address_label.grid(row=5, column=7, padx=5, pady=5, sticky="e")
        self.address_entry = ttk.Entry(self.root)
        self.address_entry.grid(row=5, column=8, padx=5, pady=5, sticky="w")

    def create_buttons(self):
        self.add_button = ttk.Button(self.root, text="Add Contact", command=self.add_contact)
        self.add_button.grid(row=6, column=5, columnspan=2, pady=5)

        self.view_button = ttk.Button(self.root, text="View Contacts", command=self.view_contacts)
        self.view_button.grid(row=6, column=7, columnspan=2, pady=5)

    def create_search_widgets(self):
        self.search_entry = ttk.Entry(self.root)
        self.search_entry.grid(row=0, column=10, padx=5, pady=5, sticky="w")

        self.search_button = ttk.Button(self.root, text="Search", command=self.search_contact)
        self.search_button.grid(row=0, column=9, padx=5, pady=5)

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if name and phone:
            contact = {"Name": name, "Phone": phone, "Email": email, "Address": address}
            self.contacts.append(contact)
            messagebox.showinfo("Success", "Contact added successfully!")
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Name and Phone Number are required fields.")

    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.photo_image = ImageTk.PhotoImage(self.image)
        self.background_label.configure(image=self.photo_image)

    def view_contacts(self):
        if not self.contacts:
            messagebox.showinfo("Info", "No contacts found.")
        else:
            view_window = tk.Toplevel(self.root)
            view_window.title("View Contacts")
            self.center_window(view_window)

            for i, contact in enumerate(self.contacts):
                contact_info = f"{contact['Name']}, {contact['Phone']}, {contact['Email']}, {contact['Address']}"
                contact_label = ttk.Label(view_window, text=contact_info)
                contact_label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

                update_button = ttk.Button(view_window, text="Update", command=lambda c=contact: self.update_selected_contact(c))
                update_button.grid(row=i, column=1, padx=5, pady=5)

                delete_button = ttk.Button(view_window, text="Delete", command=lambda c=contact: self.delete_selected_contact(c))
                delete_button.grid(row=i, column=2, padx=5, pady=5)

                save_button = ttk.Button(view_window, text="Save", command=lambda c=contact: self.save_updated_contact(c))
                save_button.grid(row=i, column=3, padx=5, pady=5)

    def center_window(self, window):
        window_width = window.winfo_reqwidth()
        window_height = window.winfo_reqheight()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_position = (screen_width - window_width) // 3
        y_position = (screen_height - window_height) // 2
        window.geometry(f"+{x_position}+{y_position}")

    def update_selected_contact(self, selected_contact):
        self.clear_entries()
        self.name_entry.insert(0, selected_contact.get("Name", ""))
        self.phone_entry.insert(0, selected_contact.get("Phone", ""))
        self.email_entry.insert(0, selected_contact.get("Email", ""))
        self.address_entry.insert(0, selected_contact.get("Address", ""))

    def save_updated_contact(self, selected_contact):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        selected_contact["Name"] = name
        selected_contact["Phone"] = phone
        selected_contact["Email"] = email
        selected_contact["Address"] = address

        messagebox.showinfo("Success", "Contact updated and saved successfully!")
        self.clear_entries()

    def search_contact(self):
        search_term = self.search_entry.get().lower()
        search_result = [contact for contact in self.contacts
                         if (search_term in contact["Name"].lower()) or
                         (search_term in contact["Phone"]) or
                         (search_term in contact.get("Address", "").lower()) or
                         (search_term in contact.get("Email", "").lower())]

        if search_result:
            search_list = "\n".join([f"Name: {contact.get('Name', '')}, Phone: {contact.get('Phone', '')}, Address: {contact.get('Address', '')}, Email: {contact.get('Email', '')}" for contact in search_result])
            messagebox.showinfo("Search Result", search_list)
        else:
            messagebox.showinfo("Search Result", "No matching contacts found.")

    def delete_selected_contact(self, selected_contact):
        self.contacts.remove(selected_contact)
        messagebox.showinfo("Success", "Contact deleted successfully!")
        self.clear_entries()

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    contact_book = ContactBook(root)
    root.mainloop()
