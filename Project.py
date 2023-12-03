import tkinter as tk
from tkinter import messagebox
import sqlite3  # For regular expression validation
import re
import csv
conn = sqlite3.connect("Users1.db")

class golf_cart:

   def _init_(self,root):
        self.root = root
        self.root.title("Sign Up")
        #self.root.configure(bg="#543454")
        self.root.iconbitmap("C:\\Users\\User\\Downloads\\golf_cart_icon_138526.ico")

        # Initialize variables to store user input
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.user_class_var = tk.StringVar()
        self.student_id_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()

        # Create labels and entry widgets
        tk.Label(root, text="First Name:").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=self.first_name_var,width=25).grid(row=0, column=1, padx=15, pady=5)

        tk.Label(root, text="Last Name:").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=self.last_name_var,width=25).grid(row=1, column=1, padx=15, pady=5)

        tk.Label(root, text="User Class:").grid(row=2, column=0, padx=10, pady=5)
        user_classes = ['Student', 'Faculty', 'Employee']
        tk.OptionMenu(root, self.user_class_var, *user_classes).grid(row=2, column=1, padx=10, pady=10)

        tk.Label(root, text="ID Number:").grid(row=3, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=self.student_id_var,width=25).grid(row=3, column=1, padx=15, pady=5)

        tk.Label(root, text="Password:").grid(row=4, column=0, padx=10, pady=5)
        tk.Entry(root, show="*", textvariable=self.password_var,width=25).grid(row=4, column=1, padx=15, pady=5)

        tk.Label(root, text="Email:").grid(row=5, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=self.email_var,width=25).grid(row=5, column=1, padx=15, pady=5)

        tk.Label(root, text="Phone:").grid(row=6, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=self.phone_var,width=25).grid(row=6, column=1, padx=15, pady=5)

        # Create the Submit button
        tk.Button(root, text="Submit", command=self.submit).grid(row=7, column=0, columnspan=2, pady=10)

        # Create the Login button
        tk.Button(root, text="Login", command= self.open_login_window).grid(row=8, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Exit", command=self.root.destroy).grid(row=8, column=1, columnspan=2, pady=20)


   def submit(self):

       # Validate input
       if not self.validate_input():
          return

       id_length = len(self.student_id_var.get())
       if id_length != 10 and id_length !=6 :
          messagebox.showerror("Error", "the Student ID must be 10 digits for Student or 6 ")
          return
        # Hash the password (In a real-world scenario, you would use a stronger hash function)

       hashed_password = hash(self.password_var.get())

        # Check if the user is already registered (you would replace this with a database check)
       if self.is_user_registered():
            messagebox.showerror("Error", "User already registered")
            return False
       else:
            self.save_to_database(hashed_password)
            messagebox.showinfo("Success", "User registered successfully")
        # Display a success message
       #messagebox.showinfo("Success", "User registered successfully")
       self.open_login_window()

   def validate_input(self):
        # Perform input validation
       if not self.first_name_var.get() or not self.last_name_var.get() or not self.user_class_var.get() \
             or not self.student_id_var.get() or not self.password_var.get() or not self.email_var.get() \
             or not self.phone_var.get():
            messagebox.showerror("Error", "All fields must be filled")
            return False

        # Validate email format using a regular expression
       email_pattern = re.compile(r'^[a-zA-Z0-9]+@ksu\.edu\.sa$')
       if not email_pattern.match(self.email_var.get()):
            messagebox.showerror("Error", "Invalid email format")
            return False

        # Validate phone number format using a regular expression
       phone_pattern = re.compile(r'^05[0-9]{8}$')
       if not phone_pattern.match(self.phone_var.get()):
           messagebox.showerror("Error", "Invalid phone number format")
           return False

       return True

   def is_user_registered(self):

       conn = sqlite3.connect("Users1.db")
       cursor = conn.cursor()
       try:
          cursor.execute("SELECT ID FROM COMPANY WHERE user_class=?",(self.user_class_var.get(),))
          user_data =cursor.fetchone()
          print(user_data)
          if user_data and self.student_id_var.get() == user_data[0]:
             return True
          else:
             return False
       except sqlite3.Error as e:
           messagebox.showerror("Database Error","ERROR1")


   def save_to_database(self,hashed_password):
       conn = sqlite3.connect("Users1.db")
       try:
         query = "INSERT INTO COMPANY(ID, first_name, last_name, user_class, email, phone, password) VALUES(?,?,?,?,?,?,?)"
         data = (
           self.student_id_var.get(), self.first_name_var.get(), self.last_name_var.get(),
           self.user_class_var.get(), self.email_var.get(), self.phone_var.get(), hashed_password
         )
         conn.execute(query, data)
         conn.commit()

         print("Saving to database:")
         print("First Name:", self.first_name_var.get())
         print("Last Name:", self.last_name_var.get())
         print("User Class:", self.user_class_var.get())
         print("Student ID:", self.student_id_var.get())
         print("Email:", self.email_var.get())
         print("Phone:", self.phone_var.get())


       except sqlite3.Error as e:
           messagebox.showerror("Database Error","THE User ID is already registered")

       self.first_name_var.set("")
       self.last_name_var.set("")
       self.user_class_var.set("")
       self.student_id_var.set("")
       self.password_var.set("")
       self.email_var.set("")
       self.phone_var.set("")

   def open_login_window(self):
        # Destroy the current Sign-Up window and open the Login window
       self.root.destroy()
       self.root1 = tk.Tk()
       self.root1.title("Login")
       self.root1.iconbitmap("C:\\Users\\User\\Downloads\\golf_cart_icon_138526.ico")
       ## self.database = database

        # Initialize variables to store user input
       self.user_id_var = tk.StringVar()
       self.password_var = tk.StringVar()

        # Create labels and entry widgets for user ID and password
       tk.Label(self.root1, text="User ID:").grid(row=0, column=0, padx=10, pady=5)
       tk.Entry(self.root1, textvariable=self.user_id_var).grid(row=0, column=1, padx=10, pady=5)

       tk.Label(self.root1, text="Password:").grid(row=1, column=0, padx=10, pady=5)
       tk.Entry(self.root1, show="*", textvariable=self.password_var).grid(row=1, column=1, padx=10, pady=5)

       tk.Button(self.root1, text="Submit", command=self.submit1).grid(row=3, column=0, columnspan=2, pady=10)



   def submit1(self):
       #self.Admin_window()
       hashh = hash(self.password_var.get())
       conn = sqlite3.connect("Users1.db")
       if not self.user_id_var.get() or not self.password_var.get():
           messagebox.showerror("Error", "All fields must be filled")
       else:
           print(hashh)
           cursor = conn.cursor()
           try:
              cursor.execute("SELECT password,user_class FROM COMPANY where ID=?", (self.user_id_var.get(),))
              user_data = cursor.fetchone()
              print(user_data)
              if user_data and str(hashh) == user_data[0]:
                  messagebox.showinfo("Login Success", "Successfully logging in")
                  if user_data[1] == "Student" and len(self.student_id_var.get())==10:
                      self.root1.destroy()
                      self.User_window()
                  else:
                      self.root1.destroy()
                      self.Admin_window()


              else:
                messagebox.showerror("Error", "The User not found")

           except sqlite3.Error as e:
                messagebox.showerror("Database Error", "ERROR3")




   def User_window(self):


       print("your in User window")


   def Admin_window(self):

       print("your in Admin window")
       conn1 = sqlite3.connect('golf_cart_database.db')

       self.root2 = tk.Tk()
       self.root2.iconbitmap("C:\\Users\\User\\Downloads\\golf_cart_icon_138526.ico")
       self.root2.title('Golf Cart Management System')

       self.plate_number = tk.StringVar()
       self.college = tk.StringVar()

       tk.Label(self.root2, text='Plate Number:').grid(row=0, column=0, padx=10, pady=10)
       tk.Entry(self.root2,textvariable=self.plate_number).grid(row=0, column=1, padx=10, pady=10)

       tk.Label(self.root2, text='College:').grid(row=1, column=0, padx=10, pady=10)
       tk.Entry(self.root2,textvariable= self.college).grid(row=1, column=1, padx=10, pady=10)

       create_button = tk.Button(self.root2, text='Create', command=self.add_golf_cart)
       create_button.grid(row=2, column=0, columnspan=2, pady=10)

       logout_button = tk.Button(self.root2, text='Logout', command=self.logout)
       logout_button.grid(row=3, column=0, columnspan=2, pady=10)

       backup_button = tk.Button(self.root2, text='Backup', command=self.backup_database)
       backup_button.grid(row=4, column=0, columnspan=2, pady=10)

   def add_golf_cart(self):
       conn1= sqlite3.connect("golf_cart1.db")
       cursor = conn1.cursor()


       if not self.plate_number or not self.college:
           messagebox.showwarning('Warning', 'Please enter both plate number and college.')
           return

        # Insert the data into the database
       insert ='INSERT INTO golf_carts1 (plate_number, college , ID) VALUES (?, ?, ?)'
       value = (self.plate_number.get(),self.college.get(),self.user_id_var.get())
       cursor.execute(insert,value)
       conn1.commit()
       self.user_id_var.set("")
       self.college.set("")
       self.plate_number.set("")

       messagebox.showinfo('Success', 'Golf cart information added successfully.')

   def backup_database(self):
       conn1 = sqlite3.connect('golf_cart_database.db')
       cursor = conn1.cursor()
       cursor.execute('SELECT * FROM golf_carts')
       data = cursor.fetchall()

       with open('backup.csv', 'w', newline='') as csvfile:

           csv_writer = csv.writer(csvfile)
           csv_writer.writerow(['ID', 'Plate Number', 'College'])
           csv_writer.writerows(data)

       messagebox.showinfo('Backup', 'Database backed up successfully.')

   def logout(self):
       self.root2.destroy()
        ##self._init_(self)

root = tk.Tk()


# Create and run the SignUpWindow

golf_cart1 = golf_cart(root)
# Run the Tkinter event loop
root.mainloop()