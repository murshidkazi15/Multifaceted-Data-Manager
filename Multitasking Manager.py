import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import datetime
from tkcalendar import Calendar
import sqlite3
import tempfile
import os

class CompsciA:
    def __init__(self, root):
        self.root = root
        self.root.title("CompsciIA")

        # Set the color scheme
        self.root.configure(bg='#000000')  # Set the background color to black

        # Connect to the SQLite database
        self.conn = sqlite3.connect('multitask_manager.db')
        self.cursor = self.conn.cursor()

        # Create tables if they don't exist
        self.create_notes_table()
        self.create_todo_table()
        self.create_events_table()
        self.create_files_table()

        # Variables
        self.notes = []
        self.todo_list = []
        self.calendar_events = []

        # UI Components
        self.label_time = tk.Label(root, text="", font=('Helvetica', 12), bg='#000000', fg='#FFFFFF')  # Set text color to white

        # Header Frame
        self.header_frame = tk.Frame(root, bg='#000000')
        self.header_frame.grid(row=0, column=0, columnspan=4, pady=10)

        # Note Section Frame
        self.note_frame = tk.Frame(root, bg='#000000')
        self.note_frame.grid(row=1, column=0, padx=10, pady=10)

        # To-Do Section Frame
        self.todo_frame = tk.Frame(root, bg='#000000')
        self.todo_frame.grid(row=1, column=1, padx=10, pady=10)

        # Calendar Section Frame
        self.calendar_frame = tk.Frame(root, bg='#000000')
        self.calendar_frame.grid(row=1, column=2, padx=10, pady=10)

        # File Section Frame
        self.file_frame = tk.Frame(root, bg='#000000')
        self.file_frame.grid(row=1, column=3, padx=10, pady=10)

        # Call methods to set up each section
        self.setup_header()
        self.setup_notes_section()
        self.setup_todo_section()
        self.setup_calendar_section()
        self.setup_file_section()

        # Update time
        self.update_time()

        # Close database connection on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_notes_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                note TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def create_todo_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS todo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                todo TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                completed INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

    def create_events_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                event TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def create_files_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_content BLOB NOT NULL
            )
        ''')
        self.conn.commit()

    def setup_header(self):
        self.label_time.pack(in_=self.header_frame)

    def setup_notes_section(self):
        self.label_note = tk.Label(self.note_frame, text="Notes:", bg='#000000', fg='#FFFFFF')
        self.text_note = tk.Text(self.note_frame, height=5, width=40, bg='#000000', fg='#FFFFFF', insertbackground='#FFFFFF', selectbackground='#FFFFFF')
        self.button_add_note = tk.Button(self.note_frame, text="Add Note", command=self.add_note, bg='#FFFFFF', fg='#000000')
        self.button_edit_note = tk.Button(self.note_frame, text="Edit Note", command=self.edit_note, bg='#FFFFFF', fg='#000000')
        self.button_delete_note = tk.Button(self.note_frame, text="Delete Note", command=self.delete_note, bg='#FFFFFF', fg='#000000')
        self.listbox_notes = tk.Listbox(self.note_frame, height=5, width=40, bg='#000000', fg='#FFFFFF', selectbackground='#FFFFFF')
        self.listbox_notes.bind("<<ListboxSelect>>", self.populate_note_textbox)

        self.label_note.grid(row=0, column=0, pady=5, sticky='w')
        self.text_note.grid(row=1, column=0, pady=5)
        self.button_add_note.grid(row=2, column=0, pady=2)
        self.button_edit_note.grid(row=3, column=0, pady=2)
        self.button_delete_note.grid(row=4, column=0, pady=2)
        self.listbox_notes.grid(row=5, column=0, pady=5)

        # Update notes listbox
        self.update_notes_listbox()

    def setup_todo_section(self):
        self.label_todo = tk.Label(self.todo_frame, text="To-Do List:", bg='#000000', fg='#FFFFFF')
        self.listbox_todo = tk.Listbox(self.todo_frame, selectmode=tk.SINGLE, height=5, width=40, bg='#000000', fg='#FFFFFF', selectbackground='#FFFFFF')
        self.button_add_todo = tk.Button(self.todo_frame, text="Add To-Do", command=self.add_todo, bg='#FFFFFF', fg='#000000')
        self.button_check_todo = tk.Button(self.todo_frame, text="Check To-Do", command=self.check_todo, bg='#FFFFFF', fg='#000000')
        self.button_delete_todo = tk.Button(self.todo_frame, text="Delete To-Do", command=self.delete_todo, bg='#FFFFFF', fg='#000000')

        self.label_todo.grid(row=0, column=0, pady=5, sticky='w')
        self.listbox_todo.grid(row=1, column=0, pady=5)
        self.button_add_todo.grid(row=2, column=0, pady=2)
        self.button_check_todo.grid(row=3, column=0, pady=2)
        self.button_delete_todo.grid(row=4, column=0, pady=2)

        # Update todo listbox
        self.update_todo_listbox()

    def setup_calendar_section(self):
        self.label_calendar = tk.Label(self.calendar_frame, text="Calendar:", bg='#000000', fg='#FFFFFF')
        self.button_add_event = tk.Button(self.calendar_frame, text="Add Event", command=self.add_event, bg='#FFFFFF', fg='#000000')
        self.button_show_events = tk.Button(self.calendar_frame, text="Show Events", command=self.show_events, bg='#FFFFFF', fg='#000000')
        self.cal = Calendar(self.calendar_frame, selectmode="day", year=datetime.now().year, month=datetime.now().month, day=datetime.now().day, bg='#000000', fg='#FFFFFF', selectbackground='#FFFFFF')

        self.label_calendar.grid(row=0, column=0, pady=5, sticky='w')
        self.button_add_event.grid(row=1, column=0, pady=2)
        self.button_show_events.grid(row=2, column=0, pady=2)
        self.cal.grid(row=3, column=0, pady=5)

    def setup_file_section(self):
        self.button_upload_file = tk.Button(self.file_frame, text="Upload File", command=self.upload_file, bg='#FFFFFF', fg='#000000')
        self.button_view_files = tk.Button(self.file_frame, text="View Files", command=self.view_files, bg='#FFFFFF', fg='#000000')

        self.button_upload_file.grid(row=0, column=0, pady=2)
        self.button_view_files.grid(row=1, column=0, pady=2)

    def add_note(self):
        note = self.text_note.get(1.0, tk.END).strip()
        if note:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute('INSERT INTO notes (note, timestamp) VALUES (?, ?)', (note, timestamp))
            self.conn.commit()
            self.update_notes_listbox()  # Update the listbox after adding
            messagebox.showinfo("Success", "Note added successfully!")
            self.text_note.delete(1.0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a valid note.")

    def edit_note(self):
        selected_note_index = self.listbox_notes.curselection()
        if selected_note_index:
            new_note = self.text_note.get(1.0, tk.END).strip()
            if new_note:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                note_id = self.notes[selected_note_index[0]][1]
                self.cursor.execute('UPDATE notes SET note = ?, timestamp = ? WHERE id = ?', (new_note, timestamp, note_id))
                self.conn.commit()
                self.update_notes_listbox()  # Update the listbox after editing
                messagebox.showinfo("Success", "Note edited successfully!")
                self.text_note.delete(1.0, tk.END)
            else:
                messagebox.showwarning("Warning", "Please enter a valid note to edit.")
        else:
            messagebox.showwarning("Warning", "Please select a note to edit.")

    def delete_note(self):
        selected_note_index = self.listbox_notes.curselection()
        if selected_note_index:
            note_id = self.notes[selected_note_index[0]][1]
            self.cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
            self.conn.commit()
            self.update_notes_listbox()  # Update the listbox after deleting
            messagebox.showinfo("Success", "Note deleted successfully!")
        else:
            messagebox.showwarning("Warning", "Please select a note to delete.")

    def populate_note_textbox(self, event):
        selected_index = self.listbox_notes.curselection()
        if selected_index:
            selected_note = self.notes[selected_index[0]]
            self.text_note.delete(1.0, tk.END)
            self.text_note.insert(tk.END, selected_note[0])

    def update_notes_listbox(self):
        self.listbox_notes.delete(0, tk.END)
        self.notes = []  # Reset the notes list
        notes = self.cursor.execute('SELECT note, id FROM notes').fetchall()
        for note in notes:
            self.listbox_notes.insert(tk.END, note[0])
            self.notes.append((note[0], note[1]))

    def add_todo(self):
        todo = self.text_note.get(1.0, tk.END).strip()
        if todo:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute('INSERT INTO todo (todo, timestamp, completed) VALUES (?, ?, ?)', (todo, timestamp, 0))
            self.conn.commit()
            self.update_todo_listbox()  # Update the to-do listbox after adding
            messagebox.showinfo("Success", "To-Do added successfully!")
            self.text_note.delete(1.0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a valid to-do item.")

    def check_todo(self):
        selected_index = self.listbox_todo.curselection()
        if selected_index:
            todo_item = self.todo_list[selected_index[0]]
            updated_item = (todo_item[0], todo_item[1], not todo_item[2], todo_item[3])
            self.cursor.execute('UPDATE todo SET completed = ? WHERE id = ?', (1 if updated_item[2] else 0, updated_item[3]))
            self.conn.commit()
            self.update_todo_listbox()  # Update the to-do listbox after checking
        else:
            messagebox.showwarning("Warning", "Please select a to-do item to check.")

    def delete_todo(self):
        selected_index = self.listbox_todo.curselection()
        if selected_index:
            todo_id = self.todo_list[selected_index[0]][2]
            self.cursor.execute('DELETE FROM todo WHERE id = ?', (todo_id,))
            self.conn.commit()
            self.update_todo_listbox()  # Update the to-do listbox after deleting
            messagebox.showinfo("Success", "To-Do deleted successfully!")
        else:
            messagebox.showwarning("Warning", "Please select a to-do item to delete.")

    def update_todo_listbox(self):
        self.listbox_todo.delete(0, tk.END)
        self.todo_list = []  # Reset the todo_list
        todos = self.cursor.execute('SELECT todo, completed, id FROM todo').fetchall()
        for todo in todos:
            self.listbox_todo.insert(tk.END, f"{todo[0]} (Completed)" if todo[1] else todo[0])
            self.todo_list.append((todo[0], todo[1], todo[2]))

    def add_event(self):
        selected_date = self.cal.get_date()
        event = simpledialog.askstring("Input", "Enter event:")
        if event:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute('INSERT INTO events (date, event, timestamp) VALUES (?, ?, ?)', (selected_date, event, timestamp))
            self.conn.commit()
            messagebox.showinfo("Success", "Event added successfully!")

    def show_events(self):
        selected_date = self.cal.get_date()
        events = self.cursor.execute('SELECT event FROM events WHERE date = ?', (selected_date,)).fetchall()
        if events:
            event_text = "\n".join(event[0] for event in events)
            messagebox.showinfo("Events", f"Events for {selected_date}:\n\n{event_text}")
        else:
            messagebox.showinfo("Events", f"No events for {selected_date}.")

    def upload_file(self):
        file_path = filedialog.askopenfilename(title="Select a File")
        if file_path:
            with open(file_path, 'rb') as file:
                file_content = file.read()
                self.cursor.execute('INSERT INTO files (file_content) VALUES (?)', (file_content,))
                self.conn.commit()
                messagebox.showinfo("Success", "File uploaded successfully!")

    def view_files(self):
        files = self.cursor.execute('SELECT id FROM files').fetchall()
        if files:
            file_ids = [file[0] for file in files]
            selected_file_id = simpledialog.askinteger("Select File", "Enter File ID:", parent=self.root)
            if selected_file_id in file_ids:
                self.show_file_content(selected_file_id)
            else:
                messagebox.showwarning("Warning", "Invalid File ID. Please select a valid File ID.")
        else:
            messagebox.showinfo("Info", "No files available.")

    def show_file_content(self, file_id):
        file_content = self.cursor.execute('SELECT file_content FROM files WHERE id = ?', (file_id,)).fetchone()[0]
        # Create a new window to display file content
        file_window = tk.Toplevel(self.root)
        file_window.title("File Content")
        text_widget = tk.Text(file_window, wrap="none", width=80, height=24)
        text_widget.insert(tk.END, file_content.decode("utf-8"))
        text_widget.pack()

    def update_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.label_time.configure(text=current_time)
        self.root.after(1000, self.update_time)

    def on_close(self):
        self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CompsciA(root)
    root.mainloop()
