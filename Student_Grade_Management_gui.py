import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

SUBJECTS = ["Math", "Physics", "English", "Computer", "Urdu"]
PASSING_AVERAGE = 50

students = []

# =========================
# Utility & Data Functions
# =========================
def calculate_average(grades):
    return round(sum(grades.values()) / len(grades), 2)


def get_status(avg):
    return "✅ PASS" if avg >= PASSING_AVERAGE else "❌ FAIL"


def generate_id():
    if not students:
        return 1
    return max(student["id"] for student in students) + 1


def save_data():
    with open("students.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name"] + SUBJECTS)
        for student in students:
            row = [student["id"], student["name"]]
            for subject in SUBJECTS:
                row.append(student["grades"][subject])
            writer.writerow(row)


def load_data():
    global students
    students = []
    if not os.path.exists("students.csv"):
        return

    with open("students.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            grades = {}
            for subject in SUBJECTS:
                grades[subject] = float(row[subject])

            students.append({
                "id": int(row["ID"]),
                "name": row["Name"],
                "grades": grades
            })


# =========================
# Window 1: Add Student Window 📝
# =========================
def open_add_student_window():
    add_win = tk.Tk()
    add_win.title("📝 Add New Student")
    add_win.geometry("420x500")
    add_win.configure(bg="#F4F6F9")
    add_win.resizable(False, False)

    title_label = tk.Label(
        add_win, 
        text="🎓 STUDENT REGISTRATION 🎓", 
        font=("Helvetica", 13, "bold"), 
        bg="#2A3E5C", 
        fg="white", 
        pady=15
    )
    title_label.pack(fill=tk.X)

    form_frame = tk.Frame(add_win, bg="#F4F6F9", padx=20, pady=15)
    form_frame.pack(fill=tk.BOTH, expand=True)

    lbl_style = {"bg": "#F4F6F9", "fg": "#2A3E5C", "font": ("Helvetica", 10, "bold")}
    entry_style = {"font": ("Helvetica", 10), "bd": 1, "relief": "solid"}

    form_frame.columnconfigure(1, weight=1)

    tk.Label(form_frame, text="👤 Student Name:", **lbl_style).grid(row=0, column=0, sticky="w", pady=8)
    name_entry = tk.Entry(form_frame, **entry_style)
    name_entry.grid(row=0, column=1, sticky="ew", pady=8, ipady=3)

    subject_emojis = {
        "Math": "📐 Math:",
        "Physics": "⚛️ Physics:",
        "English": "📖 English:",
        "Computer": "💻 Computer:",
        "Urdu": "✍️ Urdu:"
    }

    entries = {}
    for idx, subject in enumerate(SUBJECTS, start=1):
        display_text = subject_emojis.get(subject, f"📚 {subject}:")
        tk.Label(form_frame, text=display_text, **lbl_style).grid(row=idx, column=0, sticky="w", pady=8)
        ent = tk.Entry(form_frame, **entry_style)
        ent.grid(row=idx, column=1, sticky="ew", pady=8, ipady=3)
        entries[subject] = ent

    def submit_student():
        name = name_entry.get().strip()
        if not name:
            messagebox.showerror("⚠️ Error", "Please enter the student name.", parent=add_win)
            return

        try:
            grades = {}
            for subj in SUBJECTS:
                val = float(entries[subj].get().strip())
                if val < 0 or val > 100:
                    raise ValueError
                grades[subj] = val
        except ValueError:
            messagebox.showerror("⚠️ Error", "Please enter valid marks between 0 and 100.", parent=add_win)
            return

        load_data()
        students.append({
            "id": generate_id(),
            "name": name,
            "grades": grades
        })
        save_data()

        messagebox.showinfo("🎉 Success", f"✨ {name} successfully added!", parent=add_win)
        add_win.destroy()
        open_dashboard()

    submit_btn = tk.Button(
        form_frame, 
        text="💾 Save & Open Dashboard 🚀", 
        command=submit_student, 
        bg="#2ECC71", 
        fg="white", 
        font=("Helvetica", 11, "bold"), 
        bd=0, 
        cursor="hand2", 
        pady=8
    )
    submit_btn.grid(row=7, column=0, columnspan=2, sticky="ew", pady=15)

    add_win.mainloop()


# =========================
# Window 2: Dashboard Window 📊
# =========================
def open_dashboard():
    dash = tk.Tk()
    dash.title("📊 Student Records Dashboard")
    dash.geometry("1020x580")
    dash.configure(bg="#F4F6F9")

    header = tk.Frame(dash, bg="#2A3E5C", height=70)
    header.pack(fill=tk.X)
    header.pack_propagate(False)

    header_title = tk.Label(
        header, 
        text="⚡ STUDENT GRADE DASHBOARD ⚡", 
        font=("Helvetica", 15, "bold"), 
        fg="white", 
        bg="#2A3E5C"
    )
    header_title.pack(side=tk.LEFT, padx=20, pady=15)

    control_frame = tk.Frame(dash, bg="#F4F6F9", pady=15, padx=20)
    control_frame.pack(fill=tk.X)

    tk.Label(control_frame, text="🔍 Search Student:", font=("Helvetica", 10, "bold"), bg="#F4F6F9", fg="#2A3E5C").pack(side=tk.LEFT, padx=5)
    search_entry = tk.Entry(control_frame, font=("Helvetica", 10), bd=1, relief="solid", width=25)
    search_entry.pack(side=tk.LEFT, padx=5, ipady=3)

    btn_config = {"font": ("Helvetica", 9, "bold"), "bd": 0, "fg": "white", "cursor": "hand2", "padx": 10}

    def populate_table(data_list):
        for row in tree.get_children():
            tree.delete(row)

        for student in data_list:
            avg = calculate_average(student["grades"])
            status = get_status(avg)
            name_emoji = "🧑‍🎓"
            
            item_id = tree.insert("", "end", values=(
                f"🆔 {student['id']}",
                f"{name_emoji} {student['name']}",
                student["grades"]["Math"],
                student["grades"]["Physics"],
                student["grades"]["English"],
                student["grades"]["Computer"],
                student["grades"]["Urdu"],
                f"📊 {avg}",
                status
            ))
            
            if "PASS" in status:
                tree.item(item_id, tags=("pass_row",))
            else:
                tree.item(item_id, tags=("fail_row",))

    def search():
        keyword = search_entry.get().strip().lower()
        filtered = [s for s in students if keyword in s["name"].lower()]
        populate_table(filtered)

    def reset():
        search_entry.delete(0, tk.END)
        load_data()
        populate_table(students)

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("⚠️ Warning", "Please select a student row to delete.", parent=dash)
            return

        confirm = messagebox.askyesno("🗑️ Confirm", "Are you sure you want to delete this record?", parent=dash)
        if not confirm:
            return

        values = tree.item(selected[0])["values"]
        student_id = int(values[0].replace("🆔", "").strip())

        global students
        students = [s for s in students if s["id"] != student_id]
        save_data()
        reset()

    def go_to_add_new():
        dash.destroy()
        open_add_student_window()

    # Naya Designed Form Class Report ke liye 🎨
    def show_class_report():
        if not students:
            messagebox.showwarning("⚠️ No Data", "No students available to generate a report!", parent=dash)
            return

        ranked_list = []
        all_averages = []
        for s in students:
            avg = calculate_average(s["grades"])
            ranked_list.append((s["name"], avg))
            all_averages.append(avg)

        ranked_list.sort(key=lambda x: x[1], reverse=True)

        total_students = len(students)
        class_avg = round(sum(all_averages) / total_students, 2)
        highest_avg = max(all_averages)
        lowest_avg = min(all_averages)
        passed = sum(1 for avg in all_averages if avg >= PASSING_AVERAGE)
        failed = total_students - passed

        # Designing Window Creation
        report_win = tk.Toplevel(dash)
        report_win.title("📊 Class Performance Report")
        report_win.geometry("520x600")
        report_win.configure(bg="#F4F6F9")
        report_win.resizable(False, False)
        report_win.transient(dash)
        report_win.grab_set()

        # Banner
        tk.Label(
            report_win, 
            text="📊 CLASS PERFORMANCE REPORT", 
            font=("Helvetica", 14, "bold"), 
            bg="#2A3E5C", 
            fg="white", 
            pady=12
        ).pack(fill=tk.X)

        # Stats Main Container
        stats_container = tk.Frame(report_win, bg="#F4F6F9", pady=15, padx=20)
        stats_container.pack(fill=tk.X)

        # Helper function grid cards banane ke liye
        def create_stat_card(parent, row, col, title, value, color):
            card = tk.Frame(parent, bg="white", bd=1, relief="solid", padx=10, pady=8)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            tk.Label(card, text=title, font=("Helvetica", 9, "bold"), bg="white", fg="#7F8C8D").pack(anchor="w")
            tk.Label(card, text=value, font=("Helvetica", 13, "bold"), bg="white", fg=color).pack(anchor="w", pady=(2,0))

        stats_container.columnconfigure((0, 1), weight=1)

        create_stat_card(stats_container, 0, 0, "👥 Total Students", str(total_students), "#2A3E5C")
        create_stat_card(stats_container, 0, 1, "📈 Class Average", f"{class_avg}%", "#3498DB")
        create_stat_card(stats_container, 1, 0, "⭐ Highest Average", f"{highest_avg}%", "#2ECC71")
        create_stat_card(stats_container, 1, 1, "📉 Lowest Average", f"{lowest_avg}%", "#E74C3C")
        create_stat_card(stats_container, 2, 0, "✅ Passed Students", str(passed), "#27AE60")
        create_stat_card(stats_container, 2, 1, "❌ Failed Students", str(failed), "#C0392B")

        # Rankings Section Section Header
        tk.Label(
            report_win, 
            text="🏆 STUDENT RANKINGS", 
            font=("Helvetica", 11, "bold"), 
            bg="#E2E7ED", 
            fg="#2A3E5C", 
            pady=6
        ).pack(fill=tk.X, marginTop=10)

        # Rankings Listbox / Treeview Frame
        rank_frame = tk.Frame(report_win, bg="#F4F6F9", padx=20, pady=10)
        rank_frame.pack(fill=tk.BOTH, expand=True)

        rank_tree = ttk.Treeview(rank_frame, columns=("Rank", "Name", "Average"), show="headings", height=8)
        rank_tree.heading("Rank", text="Rank")
        rank_tree.heading("Name", text="Student Name")
        rank_tree.heading("Average", text="Average Grade")

        rank_tree.column("Rank", width=70, anchor="center")
        rank_tree.column("Name", width=250, anchor="w")
        rank_tree.column("Average", width=120, anchor="center")

        scrollbar_r = ttk.Scrollbar(rank_frame, orient=tk.VERTICAL, command=rank_tree.yview)
        rank_tree.configure(yscroll=scrollbar_r.set)

        rank_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_r.pack(side=tk.RIGHT, fill=tk.Y)

        # Data Populate in Rankings Tree
        for rank, (name, avg) in enumerate(ranked_list, start=1):
            medal = "🥇 Topper" if rank == 1 else "🥈 2nd" if rank == 2 else "🥉 3rd" if rank == 3 else f"#{rank}"
            rank_tree.insert("", "end", values=(medal, f"🧑‍🎓 {name}", f"{avg}%"))

        # Close button
        tk.Button(
            report_win, 
            text="❌ Close Report", 
            command=report_win.destroy, 
            bg="#7F8C8D", 
            fg="white", 
            font=("Helvetica", 10, "bold"), 
            bd=0, 
            cursor="hand2", 
            pady=8
        ).pack(fill=tk.X, side=tk.BOTTOM)

    # Buttons Setup
    search_btn = tk.Button(control_frame, text="🔍 Search", command=search, bg="#3498DB", **btn_config)
    search_btn.pack(side=tk.LEFT, padx=5, ipady=3)

    reset_btn = tk.Button(control_frame, text="🔄 Show All", command=reset, bg="#95A5A6", **btn_config)
    reset_btn.pack(side=tk.LEFT, padx=5, ipady=3)

    add_new_btn = tk.Button(control_frame, text="➕ Add New Student", command=go_to_add_new, bg="#2ECC71", **btn_config)
    add_new_btn.pack(side=tk.RIGHT, padx=5, ipady=3)

    grid_frame = tk.Frame(dash, bg="#F4F6F9", padx=20)
    grid_frame.pack(fill=tk.BOTH, expand=True)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background="#2A3E5C", foreground="white")
    style.configure("Treeview", rowheight=30, font=("Helvetica", 9))
    style.map("Treeview", background=[("selected", "#34495E")], foreground=[("selected", "white")])

    columns = ("ID", "Name", "Math", "Physics", "English", "Computer", "Urdu", "Average", "Status")
    tree = ttk.Treeview(grid_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        if col in ["ID", "Average", "Status"]:
            tree.column(col, width=90, anchor="center")
        elif col == "Name":
            tree.column(col, width=170, anchor="w")
        else:
            tree.column(col, width=75, anchor="center")

    tree.tag_configure("pass_row", background="#E8F8F5", foreground="#117A65")
    tree.tag_configure("fail_row", background="#FDEDEC", foreground="#C0392B")

    scrollbar = ttk.Scrollbar(grid_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    bottom_frame = tk.Frame(dash, bg="#F4F6F9", pady=15, padx=20)
    bottom_frame.pack(fill=tk.X)

    report_btn = tk.Button(
        bottom_frame, 
        text="📊 Generate Class Report & Rankings", 
        command=show_class_report, 
        bg="#34495E", 
        **btn_config
    )
    report_btn.pack(fill=tk.X, ipady=5, pady=(0, 5))

    delete_btn = tk.Button(
        bottom_frame, 
        text="🗑️ Delete Selected Record", 
        command=delete_selected, 
        bg="#E74C3C", 
        **btn_config
    )
    delete_btn.pack(fill=tk.X, ipady=5)

    load_data()
    populate_table(students)

    dash.mainloop()


if __name__ == "__main__":
    load_data()
    if students:
        open_dashboard()
    else:
        open_add_student_window()
