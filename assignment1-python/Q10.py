import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import os


DATA_FILE = "assignments.json"


class AssignmentTracker:

    def __init__(self, root):
        self.root = root

        self.root.title("Student Assignment Tracker")
        self.root.geometry("1000x650")

        # Store records in a list
        self.records = []

        # Load previously saved records
        self.load_data()

        self.create_widgets()

        self.refresh_table()

    # ------------------------------------------------
    # DATA HANDLING
    # ------------------------------------------------

    def load_data(self):

        if not os.path.exists(DATA_FILE):
            self.records = []
            return

        try:
            with open(
                DATA_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                self.records = json.load(file)

        except Exception:
            self.records = []

    def save_data(self):

        with open(
            DATA_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.records,
                file,
                indent=4
            )

    # ------------------------------------------------
    # GUI
    # ------------------------------------------------

    def create_widgets(self):

        title = ttk.Label(
            self.root,
            text="Student Assignment Tracker",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=10)

        # -------------------------
        # Input Frame
        # -------------------------

        input_frame = ttk.LabelFrame(
            self.root,
            text="Assignment Details"
        )

        input_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

        # Enrollment
        ttk.Label(
            input_frame,
            text="Enrollment:"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.enrollment_entry = ttk.Entry(
            input_frame,
            width=20
        )

        self.enrollment_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        # Name
        ttk.Label(
            input_frame,
            text="Name:"
        ).grid(row=0, column=2, padx=5)

        self.name_entry = ttk.Entry(
            input_frame,
            width=20
        )

        self.name_entry.grid(
            row=0,
            column=3,
            padx=5
        )

        # Assignment
        ttk.Label(
            input_frame,
            text="Assignment:"
        ).grid(row=1, column=0, padx=5, pady=5)

        self.assignment_entry = ttk.Entry(
            input_frame,
            width=20
        )

        self.assignment_entry.grid(
            row=1,
            column=1,
            padx=5
        )

        # Marks
        ttk.Label(
            input_frame,
            text="Marks:"
        ).grid(row=1, column=2, padx=5)

        self.marks_entry = ttk.Entry(
            input_frame,
            width=20
        )

        self.marks_entry.grid(
            row=1,
            column=3,
            padx=5
        )

        # Status
        ttk.Label(
            input_frame,
            text="Status:"
        ).grid(row=2, column=0, padx=5, pady=5)

        self.status = tk.StringVar(
            value="Pending"
        )

        ttk.Radiobutton(
            input_frame,
            text="Pending",
            variable=self.status,
            value="Pending"
        ).grid(row=2, column=1)

        ttk.Radiobutton(
            input_frame,
            text="Completed",
            variable=self.status,
            value="Completed"
        ).grid(row=2, column=2)

        # Remarks
        ttk.Label(
            input_frame,
            text="Remarks:"
        ).grid(row=3, column=0, padx=5)

        self.remarks_entry = ttk.Entry(
            input_frame,
            width=50
        )

        self.remarks_entry.grid(
            row=3,
            column=1,
            columnspan=3,
            padx=5,
            pady=5
        )

        # -------------------------
        # Buttons
        # -------------------------

        button_frame = ttk.Frame(
            self.root
        )

        button_frame.pack(
            pady=10
        )

        ttk.Button(
            button_frame,
            text="Add Record",
            command=self.add_record
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            button_frame,
            text="Update Marks",
            command=self.update_marks
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            button_frame,
            text="Delete",
            command=self.delete_record
        ).grid(row=0, column=2, padx=5)

        ttk.Button(
            button_frame,
            text="Export CSV",
            command=self.export_csv
        ).grid(row=0, column=3, padx=5)

        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_fields
        ).grid(row=0, column=4, padx=5)

        # -------------------------
        # Filter
        # -------------------------

        filter_frame = ttk.Frame(
            self.root
        )

        filter_frame.pack(
            fill="x",
            padx=10
        )

        ttk.Label(
            filter_frame,
            text="Filter:"
        ).pack(side="left")

        self.filter_value = tk.StringVar(
            value="All"
        )

        filter_box = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_value,
            values=[
                "All",
                "Pending",
                "Completed"
            ],
            state="readonly",
            width=15
        )

        filter_box.pack(
            side="left",
            padx=10
        )

        filter_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_table()
        )

        # -------------------------
        # Table
        # -------------------------

        table_frame = ttk.Frame(
            self.root
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        columns = (
            "enrollment",
            "name",
            "assignment",
            "status",
            "marks",
            "remarks"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "enrollment": "Enrollment",
            "name": "Name",
            "assignment": "Assignment",
            "status": "Status",
            "marks": "Marks",
            "remarks": "Remarks"
        }

        for column in columns:

            self.table.heading(
                column,
                text=headings[column]
            )

            self.table.column(
                column,
                width=130
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

    # ------------------------------------------------
    # VALIDATION
    # ------------------------------------------------

    def validate_input(self):

        enrollment = self.enrollment_entry.get().strip()
        name = self.name_entry.get().strip()
        assignment = self.assignment_entry.get().strip()
        marks_text = self.marks_entry.get().strip()

        if not enrollment:
            messagebox.showerror(
                "Error",
                "Enrollment is required."
            )
            return False

        if not name:
            messagebox.showerror(
                "Error",
                "Name is required."
            )
            return False

        if not assignment:
            messagebox.showerror(
                "Error",
                "Assignment is required."
            )
            return False

        try:
            marks = float(marks_text)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Marks must be numeric."
            )
            return False

        if marks < 0 or marks > 100:
            messagebox.showerror(
                "Error",
                "Marks must be between 0 and 100."
            )
            return False

        return True

    # ------------------------------------------------
    # ADD
    # ------------------------------------------------

    def add_record(self):

        if not self.validate_input():
            return

        record = {
            "enrollment":
                self.enrollment_entry.get().strip(),

            "name":
                self.name_entry.get().strip(),

            "assignment":
                self.assignment_entry.get().strip(),

            "status":
                self.status.get(),

            "marks":
                float(
                    self.marks_entry.get().strip()
                ),

            "remarks":
                self.remarks_entry.get().strip()
        }

        self.records.append(record)

        self.save_data()

        self.refresh_table()

        self.clear_fields()

        messagebox.showinfo(
            "Success",
            "Assignment record added."
        )

    # ------------------------------------------------
    # UPDATE MARKS
    # ------------------------------------------------

    def update_marks(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a record first."
            )
            return

        try:
            new_marks = float(
                self.marks_entry.get()
            )

        except ValueError:
            messagebox.showerror(
                "Error",
                "Enter valid marks."
            )
            return

        if not 0 <= new_marks <= 100:
            messagebox.showerror(
                "Error",
                "Marks must be between 0 and 100."
            )
            return

        item = self.table.item(
            selected[0]
        )

        values = item["values"]

        enrollment = values[0]
        assignment = values[2]

        for record in self.records:

            if (
                record["enrollment"] == enrollment
                and record["assignment"] == assignment
            ):

                record["marks"] = new_marks
                record["status"] = self.status.get()

                break

        self.save_data()

        self.refresh_table()

        messagebox.showinfo(
            "Success",
            "Record updated."
        )

    # ------------------------------------------------
    # DELETE
    # ------------------------------------------------

    def delete_record(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a record first."
            )
            return

        item = self.table.item(
            selected[0]
        )

        values = item["values"]

        enrollment = values[0]
        assignment = values[2]

        self.records = [
            record
            for record in self.records
            if not (
                record["enrollment"] == enrollment
                and record["assignment"] == assignment
            )
        ]

        self.save_data()

        self.refresh_table()

    # ------------------------------------------------
    # TABLE REFRESH
    # ------------------------------------------------

    def refresh_table(self):

        # Clear existing rows
        for item in self.table.get_children():
            self.table.delete(item)

        selected_filter = self.filter_value.get()

        for record in self.records:

            if (
                selected_filter != "All"
                and record["status"] != selected_filter
            ):
                continue

            self.table.insert(
                "",
                "end",
                values=(
                    record["enrollment"],
                    record["name"],
                    record["assignment"],
                    record["status"],
                    record["marks"],
                    record["remarks"]
                )
            )

    # ------------------------------------------------
    # EXPORT CSV
    # ------------------------------------------------

    def export_csv(self):

        if not self.records:
            messagebox.showwarning(
                "Warning",
                "No records available."
            )
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV Files", "*.csv")
            ]
        )

        if not filename:
            return

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Enrollment",
                "Name",
                "Assignment",
                "Status",
                "Marks",
                "Remarks"
            ])

            for record in self.records:

                writer.writerow([
                    record["enrollment"],
                    record["name"],
                    record["assignment"],
                    record["status"],
                    record["marks"],
                    record["remarks"]
                ])

        messagebox.showinfo(
            "Success",
            "CSV exported successfully."
        )

    # ------------------------------------------------
    # CLEAR
    # ------------------------------------------------

    def clear_fields(self):

        self.enrollment_entry.delete(
            0,
            tk.END
        )

        self.name_entry.delete(
            0,
            tk.END
        )

        self.assignment_entry.delete(
            0,
            tk.END
        )

        self.marks_entry.delete(
            0,
            tk.END
        )

        self.remarks_entry.delete(
            0,
            tk.END
        )

        self.status.set("Pending")


# ------------------------------------------------
# MAIN
# ------------------------------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = AssignmentTracker(root)

    root.mainloop()