import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime

class Task:
    def __init__(self, name, priority, date):
        self.name = name
        self.priority = priority
        self.date = datetime.strptime(date, "%Y-%m-%d")  # Convert date to datetime object

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Taskify")

        self.tasks = []

        self.task_name_var = tk.StringVar()
        self.priority_var = tk.StringVar()
        self.date_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Task Name Label
        tk.Label(self.root, text="Task Name:").grid(row=0, column=0, sticky="w")
        task_name_entry = tk.Entry(self.root, textvariable=self.task_name_var, width=25)
        task_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Priority Dropdown
        tk.Label(self.root, text="Priority:").grid(row=1, column=0, sticky="w")
        priority_values = ["Low", "Medium", "High"]
        priority_dropdown = ttk.Combobox(self.root, textvariable=self.priority_var, values=priority_values, state="readonly", width=22)
        priority_dropdown.grid(row=1, column=1, padx=10, pady=5)

        # Date Picker
        tk.Label(self.root, text="Due Date:").grid(row=2, column=0, sticky="w")
        self.date_entry = DateEntry(self.root, textvariable=self.date_var, date_pattern='yyyy-MM-dd',width=22)
        self.date_entry.grid(row=2, column=1, padx=10, pady=5)

        # Add Task Button
        self.add_task_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_task_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Task List Treeview
        self.task_list_treeview = ttk.Treeview(self.root, columns=("Task Name", "Priority", "Due Date"), show="headings")
        self.task_list_treeview.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        self.task_list_treeview.heading("Task Name", text="Task Name")
        self.task_list_treeview.heading("Priority", text="Priority")
        self.task_list_treeview.heading("Due Date", text="Due Date")

        # Delete Task Button
        delete_task_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        delete_task_button.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        # Edit Task Button
        edit_task_button = tk.Button(self.root, text="Edit Task", command=self.edit_task)
        edit_task_button.grid(row=5, column=1, padx=10, pady=5, sticky="e")

    def add_task(self):
        name = self.task_name_var.get()
        priority = self.priority_var.get()
        date = self.date_entry.get_date().strftime("%Y-%m-%d")

        if name and priority and date:
            task = Task(name, priority, date)
            self.tasks.append(task)

            # Sort tasks before displaying
            self.sort_tasks()
            self.refresh_task_list()

            # Clear input fields
            self.task_name_var.set("")
            self.priority_var.set("")
            self.date_entry.set_date(datetime.today())
        else:
            messagebox.showerror("Error", "Please enter all the fields.")

    def delete_task(self):
        selected_item = self.task_list_treeview.selection()
        if selected_item:
            task_index = int(selected_item[0])  # Get index
            del self.tasks[task_index]  # Remove from task list
            self.refresh_task_list()  # Refresh display

    def edit_task(self):
        selected_item = self.task_list_treeview.selection()
        if selected_item:
            task_index = int(selected_item[0])  # Get selected index
            task = self.tasks[task_index]

            # Populate fields with existing values
            self.task_name_var.set(task.name)
            self.priority_var.set(task.priority)
            self.date_entry.set_date(task.date.strftime("%Y-%m-%d"))

            # Remove old task from list
            del self.tasks[task_index]
            self.refresh_task_list()

            # Override Add Task button to "Save Task"
            def save_edited_task():
                new_name = self.task_name_var.get()
                new_priority = self.priority_var.get()
                new_date = self.date_entry.get_date().strftime("%Y-%m-%d")

                if new_name and new_priority and new_date:
                    updated_task = Task(new_name, new_priority, new_date)
                    self.tasks.append(updated_task)

                    # Sort and refresh task list
                    self.sort_tasks()
                    self.refresh_task_list()

                    # Restore Add Task button function
                    self.task_name_var.set("")
                    self.priority_var.set("")
                    self.date_entry.set_date(datetime.today())
                    self.add_task_button.config(text="Add Task", command=self.add_task)
                else:
                    messagebox.showerror("Error", "Please enter all the fields.")

            # Change button to "Save Task"
            self.add_task_button.config(text="Save Task", command=save_edited_task)
        else:
            messagebox.showerror("Error", "Please select a task to edit.")

    def sort_tasks(self):
        """Sort tasks by priority (High → Medium → Low) and then by date (latest first)."""
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        
        # Sort tasks: first by priority, then by date (latest date first)
        self.tasks.sort(key=lambda task: (priority_order[task.priority], task.date))

    def refresh_task_list(self):
        """Refresh the displayed task list in the Treeview."""
        self.task_list_treeview.delete(*self.task_list_treeview.get_children())  # Clear Treeview
        for index, task in enumerate(self.tasks):
            self.task_list_treeview.insert("", index, values=(task.name, task.priority, task.date.strftime("%Y-%m-%d")), iid=index)

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()


