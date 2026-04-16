import tkinter as tk
from tkinter import messagebox
import queries as q
from PIL import Image, ImageTk
import threading
from queries import generate_full_world_graph

root = tk.Tk()
root.title("World Builder")
root.geometry("900x700")

def open_create_person():
    win = tk.Toplevel(root)
    win.title("Create Person")

    # Fields
    tk.Label(win, text="Name").grid(row=0, column=0)
    name_entry = tk.Entry(win)
    name_entry.grid(row=0, column=1)

    tk.Label(win, text="Race").grid(row=1, column=0)
    race_entry = tk.Entry(win)
    race_entry.grid(row=1, column=1)

    tk.Label(win, text="Age").grid(row=2, column=0)
    age_entry = tk.Entry(win)
    age_entry.grid(row=2, column=1)

    tk.Label(win, text="Home Continent").grid(row=3, column=0)
    cont_entry = tk.Entry(win)
    cont_entry.grid(row=3, column=1)

    tk.Label(win, text="God").grid(row=4, column=0)
    god_entry = tk.Entry(win)
    god_entry.grid(row=4, column=1)

    tk.Label(win, text="Hometown ID").grid(row=5, column=0)
    town_entry = tk.Entry(win)
    town_entry.grid(row=5, column=1)

    def submit():
        try:
            q.create_person(
                name_entry.get(),
                race_entry.get(),
                int(age_entry.get()),
                cont_entry.get(),
                god_entry.get(),
                int(town_entry.get()) if town_entry.get() else None
            )

            # Get the last inserted person
            person = q.get_all(q.person)[-1]
            person_id = person["PersonID"]

            is_adv = messagebox.askyesno("Adventurer", "Is this person an adventurer?")

            if is_adv:
                adv_win = open_create_adventurer(person_id)
                win.wait_window(adv_win)

            messagebox.showinfo("Success", f"Person created with ID {person_id}")
            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Create", command=submit).grid(row=6, columnspan=2)

def open_create_adventurer(person_id=None):
    win = tk.Toplevel(root)
    win.title("Create Adventurer")

    tk.Label(win, text=f"Person ID: {person_id}").grid(row=0, columnspan=2)

    tk.Label(win, text="Class").grid(row=1, column=0)
    class_entry = tk.Entry(win)
    class_entry.grid(row=1, column=1)

    tk.Label(win, text="Level").grid(row=2, column=0)
    level_entry = tk.Entry(win)
    level_entry.grid(row=2, column=1)
    

    def submit():
        try:
            pid = person_id if person_id else int(input_id.get())

            q.create_adventurer(pid, class_entry.get(), int(level_entry.get()))

            messagebox.showinfo("Success", "Adventurer created")
            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    if person_id is None:
        tk.Label(win, text="Person ID").grid(row=3, column=0)
        input_id = tk.Entry(win)
        input_id.grid(row=3, column=1)

    tk.Button(win, text="Create", command=submit).grid(row=4, columnspan=2)
    return win

def open_create_continent():
    win = tk.Toplevel(root)
    win.title("Create Continent")

    tk.Label(win, text="Name").grid(row=0, column=0)
    name_entry = tk.Entry(win)
    name_entry.grid(row=0, column=1)

    tk.Label(win, text="Climate").grid(row=1, column=0)
    climate_entry = tk.Entry(win)
    climate_entry.grid(row=1, column=1)

    def submit():
        try:
            q.create_continent(name_entry.get(), climate_entry.get())
            messagebox.showinfo("Success", "Continent created")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Create", command=submit).grid(row=2, columnspan=2)

def open_create_town():
    win = tk.Toplevel(root)
    win.title("Create Town")

    tk.Label(win, text="Name").grid(row=0, column=0)
    name_entry = tk.Entry(win)
    name_entry.grid(row=0, column=1)

    tk.Label(win, text="Country ID").grid(row=1, column=0)
    country_entry = tk.Entry(win)
    country_entry.grid(row=1, column=1)

    tk.Label(win, text="Leader ID").grid(row=2, column=0)
    leader_entry = tk.Entry(win)
    leader_entry.grid(row=2, column=1)

    def submit():
        try:
            q.create_town(
                name_entry.get(),
                int(country_entry.get()) if country_entry.get() else None,
                int(leader_entry.get()) if leader_entry.get() else None
            )
            messagebox.showinfo("Success", "Town created")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Create", command=submit).grid(row=3, columnspan=2)

def open_create_country():
    win = tk.Toplevel(root)
    win.title("Create Country")

    tk.Label(win, text="Name").grid(row=0, column=0)
    name_entry = tk.Entry(win)
    name_entry.grid(row=0, column=1)

    tk.Label(win, text="Ruler ID").grid(row=1, column=0)
    ruler_entry = tk.Entry(win)
    ruler_entry.grid(row=1, column=1)

    tk.Label(win, text="Continent ID").grid(row=2, column=0)
    cont_entry = tk.Entry(win)
    cont_entry.grid(row=2, column=1)

    def submit():
        try:
            q.create_country(
                name_entry.get(),
                int(ruler_entry.get()) if ruler_entry.get() else None,
                int(cont_entry.get()) if cont_entry.get() else None
            )
            messagebox.showinfo("Success", "Country created")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Create", command=submit).grid(row=3, columnspan=2)

def open_create_relationship():
    win = tk.Toplevel(root)
    win.title("Create Relationship")

    tk.Label(win, text="Person 1 ID").grid(row=0, column=0)
    p1_entry = tk.Entry(win)
    p1_entry.grid(row=0, column=1)

    tk.Label(win, text="Person 2 ID").grid(row=1, column=0)
    p2_entry = tk.Entry(win)
    p2_entry.grid(row=1, column=1)

    tk.Label(win, text="Relationship Type").grid(row=2, column=0)
    rel_entry = tk.Entry(win)
    rel_entry.grid(row=2, column=1)

    def submit():
        try:
            q.create_relationship(
                int(p1_entry.get()),
                int(p2_entry.get()),
                rel_entry.get()
            )
            messagebox.showinfo("Success", "Relationship created")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Create", command=submit).grid(row=3, columnspan=2)

def open_create_god():
    win = tk.Toplevel(root)
    win.title("Create God")

    tk.Label(win, text="Name").grid(row=0, column=0)
    name_entry = tk.Entry(win)
    name_entry.grid(row=0, column=1)

    tk.Label(win, text="Pantheon ID").grid(row=1, column=0)
    pantheon_entry = tk.Entry(win)
    pantheon_entry.grid(row=1, column=1)

    def submit():
        try:
            q.create_god(
                name_entry.get(),
                int(pantheon_entry.get()) if pantheon_entry.get() else None
            )
            messagebox.showinfo("Success", "God created")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Create", command=submit).grid(row=2, columnspan=2)


def open_create_pantheon():
    win = tk.Toplevel(root)
    win.title("Create Pantheon")

    tk.Label(win, text="Name").grid(row=0, column=0)
    name_entry = tk.Entry(win)
    name_entry.grid(row=0, column=1)

    def submit():
        try:
            q.create_pantheon(name_entry.get())
            messagebox.showinfo("Success", "Pantheon created")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Create", command=submit).grid(row=1, columnspan=2)

def show_results(title, data):
    win = tk.Toplevel(root)
    win.title(title)

    text = tk.Text(
    win,
    wrap="word",
    width=70,
    height=20,
    bg="#fdf6e3",
    fg=TEXT_COLOR,
    font=("Courier", 10),
    bd=2,
    relief="ridge"
    )
    text.pack()

    if not data:
        text.insert(tk.END, "No results found.")
        return

    def format_row(row):
        if isinstance(row, dict):
            d = row
        else:
            d = dict(row._mapping)

        formatted = ""

        for key, value in d.items():
            if isinstance(value, dict):
                formatted += f"{key}:\n"
                for subk, subv in value.items():
                    formatted += f"  {subk}: {subv}\n"
            else:
                formatted += f"{key}: {value}\n"

        return formatted

    if isinstance(data, list):
        for i, row in enumerate(data, 1):
            text.insert(tk.END, f"--- Result {i} ---\n")
            text.insert(tk.END, format_row(row))
            text.insert(tk.END, "\n")
    else:
        text.insert(tk.END, format_row(data))

def open_search_person():
    win = tk.Toplevel(root)
    win.title("Search Person")

    tk.Label(win, text="Search by Name or ID").grid(row=0, columnspan=2)

    entry = tk.Entry(win)
    entry.grid(row=1, columnspan=2)

    def search():
        val = entry.get()

        try:
            if val.isdigit():
                person = q.get_person_by_id(int(val))
                if not person:
                    show_results("Result", None)
                    return

                adv = q.get_adventurer_by_person(person.PersonID)

                result = dict(person._mapping)
                if adv:
                    result["Adventurer"] = dict(adv._mapping)

                show_results("Person Result", result)

            else:
                people = q.get_person_by_name(val)

                results = []
                for p in people:
                    data = dict(p._mapping)
                    adv = q.get_adventurer_by_person(p.PersonID)
                    if adv:
                        data["Adventurer"] = dict(adv._mapping)
                    results.append(data)

                show_results("Person Results", results)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Search", command=search).grid(row=2, columnspan=2)

def open_generic_search(title, table, id_col, name_col):
    win = tk.Toplevel(root)
    win.title(title)

    tk.Label(win, text="Search by Name or ID").grid(row=0, columnspan=2)

    entry = tk.Entry(win)
    entry.grid(row=1, columnspan=2)

    def search():
        val = entry.get()

        try:
            if val.isdigit():
                result = q.get_by_id(table, id_col, int(val))
                show_results(title, result)
            else:
                results = q.get_by_name(table, name_col, val)
                show_results(title, results)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Search", command=search).grid(row=2, columnspan=2)

def open_search_pantheon():
    win = tk.Toplevel(root)
    win.title("Search Pantheon")

    entry = tk.Entry(win)
    entry.grid(row=0, columnspan=2)

    def search():
        val = entry.get()

        try:
            if val.isdigit():
                pan = q.get_by_id(q.pantheon, q.pantheon.c.PantheonID, int(val))
                results = [pan] if pan else []
            else:
                results = q.get_by_name(q.pantheon, q.pantheon.c.Name, val)

            if not results:
                show_results("Pantheon", None)
                return

            show_results("Pantheon", results)

            show_gods = messagebox.askyesno("Gods", "Show gods in this pantheon?")

            if show_gods:
                for p in results:
                    gods = q.get_gods_in_pantheon(p.PantheonID)
                    show_results(f"Gods in {p.Name}", gods)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Search", command=search).grid(row=1, columnspan=2)

def open_delete_window(title, delete_func, table, id_column, id_label):
    win = tk.Toplevel(root)
    win.title(f"Delete {title}")

    tk.Label(win, text=f"{id_label} ID").grid(row=0, column=0)
    id_entry = tk.Entry(win)
    id_entry.grid(row=0, column=1)

    def submit():
        try:
            val = id_entry.get()

            if not val.isdigit():
                messagebox.showerror("Error", "Please enter a valid numeric ID")
                return

            entity_id = int(val)

            # ✅ CHECK IF EXISTS
            existing = q.get_by_id(table, id_column, entity_id)

            if not existing:
                messagebox.showerror("Error", f"{title} ID {entity_id} does not exist")
                return

            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete {title} ID {entity_id}?"
            )

            if not confirm:
                return

            delete_func(entity_id)

            messagebox.showinfo("Success", f"{title} deleted successfully")
            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Delete", command=submit).grid(row=1, columnspan=2)

def open_update_window(title, table, id_column, update_func):
    win = tk.Toplevel(root)
    win.title(f"Update {title}")

    tk.Label(win, text=f"{title} ID").grid(row=0, column=0)
    id_entry = tk.Entry(win)
    id_entry.grid(row=0, column=1)

    fields = {}
    entries = {}

    def load_data():
        val = id_entry.get()

        if not val.isdigit():
            messagebox.showerror("Error", "Enter valid ID")
            return

        entity_id = int(val)

        row = q.get_by_id(table, id_column, entity_id)

        if not row:
            messagebox.showerror("Error", f"{title} not found")
            return

        data = dict(row._mapping)

        # Remove primary key from editable fields
        data.pop(id_column.name, None)

        # Clear previous fields if reloading
        for widget in win.grid_slaves():
            if int(widget.grid_info()["row"]) > 1:
                widget.destroy()

        entries.clear()

        # Create input fields dynamically
        for i, (key, value) in enumerate(data.items(), start=2):
            tk.Label(win, text=key).grid(row=i, column=0)

            entry = tk.Entry(win)
            entry.insert(0, "" if value is None else str(value))
            entry.grid(row=i, column=1)

            entries[key] = entry

        # Submit button
        tk.Button(win, text="Update",
                  command=lambda: submit(entity_id)).grid(row=i+1, columnspan=2)

    def submit(entity_id):
        try:
            update_data = {}

            for key, entry in entries.items():
                val = entry.get()

                if val == "":
                    update_data[key] = None
                elif val.isdigit():
                    update_data[key] = int(val)
                else:
                    update_data[key] = val

            update_func(entity_id, **update_data)

            messagebox.showinfo("Success", f"{title} updated")
            win.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Load", command=load_data).grid(row=1, columnspan=2)

def open_population_lookup(title, func):
    win = tk.Toplevel(root)
    win.title(title)

    tk.Label(win, text=f"{title} ID").grid(row=0, column=0)
    entry = tk.Entry(win)
    entry.grid(row=0, column=1)

    def submit():
        try:
            val = int(entry.get())
            result = func(val)
            messagebox.showinfo("Population", f"{title} Population: {result}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Find", command=submit).grid(row=1, columnspan=2)

def show_avg_ages():
    win = tk.Toplevel(root)
    win.title("Average Ages")

    text = tk.Text(win, width=60, height=20)
    text.pack()

    def format_rows(rows, label):
        text.insert(tk.END, f"\n--- {label} ---\n")
        for r in rows:
            text.insert(tk.END, f"{r[0]}: {round(r[1],2)}\n")

    format_rows(q.get_avg_age_by_town(), "Town Average Age")
    format_rows(q.get_avg_age_by_country(), "Country Average Age")
    format_rows(q.get_avg_age_by_continent(), "Continent Average Age")

def show_total_adventurers():
    count = q.get_total_adventurers()
    messagebox.showinfo("Adventurers", f"Total Adventurers: {count}")

def show_population_extremes():
    data = q.get_population_extremes()

    msg = ""

    for key in ["continent", "country", "town"]:
        max_val, min_val = data[key]

        msg += f"\n--- {key.capitalize()} ---\n"
        msg += f"Max: {max_val.Name} ({max_val.pop})\n"
        msg += f"Min: {min_val.Name} ({min_val.pop})\n"

    messagebox.showinfo("Population Extremes", msg)

def update_value_menu(*args):
    scope = scope_var.get()

    menu = value_menu["menu"]
    menu.delete(0, "end")

    options = []

    if scope == "Continent":
        options = [c["Name"] for c in q.get_all(q.continent)]
    elif scope == "Country":
        options = [c["Name"] for c in q.get_all(q.country)]
    elif scope == "Town":
        options = [t["Name"] for t in q.get_all(q.town)]

    # Disable dropdown if World
    if scope == "World":
        value_menu.config(state="disabled")
        value_var.set("")
        return
    else:
        value_menu.config(state="normal")

    if not options:
        options = [""]

    value_var.set(options[0])

    for opt in options:
        menu.add_command(label=opt, command=lambda v=opt: value_var.set(v))

def show_world_graph():
    def task():
        try:
            scope = scope_var.get()
            value = value_var.get() if scope != "World" else None

            path = generate_full_world_graph(scope=scope, value=value)

            win = tk.Toplevel(root)
            win.title("World Graph")

            img = Image.open(path)
            img = img.resize((1000, 750))

            tk_img = ImageTk.PhotoImage(img)

            label = tk.Label(win, image=tk_img)
            label.image = tk_img
            label.pack()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    threading.Thread(target=task).start()



# -------------------- THEME --------------------
BG_COLOR = "#f4ecd8"        # parchment
FRAME_COLOR = "#e6dcc4"     # slightly darker parchment
ACCENT_COLOR = "#5a3e2b"    # dark brown ink
BTN_COLOR = "#c2a878"       # wood button
BTN_HOVER = "#a68b5b"
TEXT_COLOR = "#2b1d14"

FONT_TITLE = ("Georgia", 16, "bold")
FONT_HEADER = ("Georgia", 11, "bold")
FONT_BODY = ("Garamond", 10)

root.configure(bg=BG_COLOR)
main_frame = tk.Frame(root, bg=BG_COLOR)
for i in range(5):
    main_frame.grid_columnconfigure(i, weight=1, uniform="col")
main_frame.pack(pady=10)
main_frame.grid_columnconfigure(0, pad=10)
main_frame.grid_columnconfigure(1, pad=10)
main_frame.grid_columnconfigure(2, pad=10)
main_frame.grid_columnconfigure(3, pad=10)
main_frame.grid_columnconfigure(4, pad=10)
agg_frame = tk.Frame(main_frame, bg=FRAME_COLOR, bd=2, relief="ridge")
agg_frame.grid(row=10, column=0, columnspan=5, pady=20)
def styled_button(parent, text, cmd, row, col):
    btn = tk.Button(
        parent,
        text=text,
        command=cmd,
        bg=BTN_COLOR,
        fg=TEXT_COLOR,
        activebackground=BTN_HOVER,
        relief="flat",
        bd=1,
        width=12,
        font=FONT_BODY,
        cursor="hand2"
    )
    btn.grid(row=row, column=col, padx=4, pady=4)

    # Hover effect
    btn.bind("<Enter>", lambda e: btn.config(bg=BTN_HOVER))
    btn.bind("<Leave>", lambda e: btn.config(bg=BTN_COLOR))

    return btn
def add_crud_row(parent, row, label, create_cmd, search_cmd, update_cmd, delete_cmd):
    tk.Label(
        parent,
        text=label,
        anchor="w",
        bg=BG_COLOR,
        fg=TEXT_COLOR,
        font=FONT_HEADER
    ).grid(row=row, column=0, padx=8, pady=6, sticky="w")

    def placeholder(col):
        tk.Label(
            parent,
            text="-",
            bg=BG_COLOR,
            fg="#888",
            width=12  # 🔥 MATCH BUTTON WIDTH
        ).grid(row=row, column=col, padx=4, pady=4)

    if create_cmd:
        styled_button(parent, "Create", create_cmd, row, 1)
    else:
        placeholder(1)

    if search_cmd:
        styled_button(parent, "Search", search_cmd, row, 2)
    else:
        placeholder(2)

    if update_cmd:
        styled_button(parent, "Update", update_cmd, row, 3)
    else:
        placeholder(3)

    if delete_cmd:
        styled_button(parent, "Delete", delete_cmd, row, 4)
    else:
        placeholder(4)
add_crud_row(
    main_frame, 1, "Person",
    open_create_person,
    open_search_person,
    lambda: open_update_window("Person", q.person, q.person.c.PersonID, q.update_person),
    lambda: open_delete_window("Person", q.delete_person, q.person, q.person.c.PersonID, "Person")
)
add_crud_row(
    main_frame, 2, "Town",
    open_create_town,
    lambda: open_generic_search("Town", q.town, q.town.c.TownID, q.town.c.Name),
    lambda: open_update_window("Town", q.town, q.town.c.TownID, q.update_town),
    lambda: open_delete_window("Town", q.delete_town, q.town, q.town.c.TownID, "Town")
)
add_crud_row(
    main_frame, 3, "Country",
    open_create_country,
    lambda: open_generic_search("Country", q.country, q.country.c.CountryID, q.country.c.Name),
    lambda: open_update_window("Country", q.country, q.country.c.CountryID, q.update_country),
    lambda: open_delete_window("Country", q.delete_country, q.country, q.country.c.CountryID, "Country")
)
add_crud_row(
    main_frame, 4, "Continent",
    open_create_continent,
    lambda: open_generic_search("Continent", q.continent, q.continent.c.ContinentID, q.continent.c.Name),
    lambda: open_update_window("Continent", q.continent, q.continent.c.ContinentID, q.update_continent),
    lambda: open_delete_window("Continent", q.delete_continent, q.continent, q.continent.c.ContinentID, "Continent")
)
add_crud_row(
    main_frame, 5, "God",
    open_create_god,  # if you don’t have create UI yet
    lambda: open_generic_search("God", q.god, q.god.c.GodID, q.god.c.Name),
    lambda: open_update_window("God", q.god, q.god.c.GodID, q.update_god),
    lambda: open_delete_window("God", q.delete_god, q.god, q.god.c.GodID, "God")
)
add_crud_row(
    main_frame, 6, "Pantheon",
    open_create_pantheon,
    open_search_pantheon,
    lambda: open_update_window("Pantheon", q.pantheon, q.pantheon.c.PantheonID, q.update_pantheon),
    lambda: open_delete_window("Pantheon", q.delete_pantheon, q.pantheon, q.pantheon.c.PantheonID, "Pantheon")
)
add_crud_row(
    main_frame, 7, "Adventurer",
    open_create_adventurer,
    None,
    lambda: open_update_window("Adventurer", q.adventurer, q.adventurer.c.PersonID, q.update_adventurer),
    lambda: open_delete_window("Adventurer", q.delete_adventurer, q.adventurer, q.adventurer.c.PersonID, "Person")
)
add_crud_row(
    main_frame, 8, "Relationship",
    open_create_relationship,
    None,
    lambda: open_update_window("Relationship", q.relationship, q.relationship.c.RelationshipID, q.update_relationship),
    lambda: open_delete_window("Relationship", q.delete_relationship, q.relationship, q.relationship.c.RelationshipID, "Relationship")
)

tk.Label(agg_frame, text="Population", bg=FRAME_COLOR, fg=ACCENT_COLOR, font=FONT_HEADER).grid(row=1, column=0, padx=5)
styled_button(agg_frame, "Continent",
    lambda: open_population_lookup("Continent", q.get_population_by_continent), 1, 1)

styled_button(agg_frame, "Country",
    lambda: open_population_lookup("Country", q.get_population_by_country), 1, 2)

styled_button(agg_frame, "Town",
    lambda: open_population_lookup("Town", q.get_population_by_town), 1, 3)


tk.Label(agg_frame, text="Average Age", bg=FRAME_COLOR, fg=ACCENT_COLOR, font=FONT_HEADER).grid(row=2, column=0, padx=5)

styled_button(agg_frame, "Show All", show_avg_ages, 2, 1)

tk.Label(agg_frame, text="Adventurers", bg=FRAME_COLOR, fg=ACCENT_COLOR, font=FONT_HEADER).grid(row=3, column=0, padx=5)

styled_button(agg_frame, "Total Count", show_total_adventurers, 3, 1)

tk.Label(agg_frame, text="Population Extremes", bg=FRAME_COLOR, fg=ACCENT_COLOR, font=FONT_HEADER).grid(row=4, column=0, padx=5)

styled_button(agg_frame, "Find Max/Min", show_population_extremes, 4, 1)

headers = ["", "Create", "Search", "Update", "Delete"]
scope_var = tk.StringVar(value="World")
value_var = tk.StringVar()

scope_var.trace_add("write", update_value_menu)
scope_menu = tk.OptionMenu(agg_frame, scope_var, "World", "Continent", "Country", "Town")
value_menu = tk.OptionMenu(agg_frame, value_var, "")
scope_menu.config(bg=BTN_COLOR, fg=TEXT_COLOR, font=FONT_BODY)
value_menu.config(bg=BTN_COLOR, fg=TEXT_COLOR, font=FONT_BODY)
tk.Label(agg_frame, text="Scope", bg=FRAME_COLOR, fg=ACCENT_COLOR, font=FONT_HEADER).grid(row=6, column=0)
tk.Label(agg_frame, text="Filter", bg=FRAME_COLOR, fg=ACCENT_COLOR, font=FONT_HEADER).grid(row=6, column=1)
scope_menu.grid(row=7, column=0, padx=5)
value_menu.grid(row=7, column=1, padx=5)

styled_button(agg_frame, "Generate World Graph", show_world_graph, 8, 1)
update_value_menu()

for col, text in enumerate(headers):
    tk.Label(main_frame, text=text, bg=BG_COLOR, fg=ACCENT_COLOR, font=FONT_HEADER).grid(row=0, column=col, padx=5, pady=5)
    
tk.Label(agg_frame, text="Aggregations", bg=FRAME_COLOR, fg=ACCENT_COLOR, font=FONT_HEADER).grid(row=0, column=0, columnspan=4, pady=10)

separator = tk.Frame(main_frame, height=2, bd=1, relief="sunken")
separator.grid(row=9, column=0, columnspan=5, sticky="we", pady=10)
root.mainloop()