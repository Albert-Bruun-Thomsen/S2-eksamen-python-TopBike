import tkinter as tk
from tkinter import ttk
import topbike_data as tbd
import topbike_sql as tbsql
import topbike_func as tbf
from tkinter import messagebox

padx = 8
pady = 4
rowheight = 24
treeview_background = "#eeeeee"
treeview_foreground = "#000000"
treeview_selected = "#4D4D4D"
oddrow = "#dddddd"
evenrow = "#cccccc"


# team function start region
def read_team_entries():  #  reads all team entries
    return entry_team_id.get(), entry_team_skill_level.get(), entry_team_team_size.get()


def clear_team_entries():  #  clear all team entries
    entry_team_id.delete(0, tk.END)
    entry_team_skill_level.delete(0, tk.END)
    entry_team_team_size.delete(0, tk.END)


def write_team_entries(values):
    entry_team_id.insert(0, values[0])
    entry_team_skill_level.insert(0, values[1])
    entry_team_team_size.insert(0, values[2])


def edit_team(event, tree):
    index_selected = tree.focus()
    values = tree.item(index_selected, "values")
    clear_team_entries()
    write_team_entries(values)


def create_team(tree, record):
    team = tbd.Team.convert_from_tuple(record)
    tbsql.create_record(team)
    clear_team_entries()
    refresh_treeview(tree, tbd.Team)


def update_team(tree, record):
    team = tbd.Team.convert_from_tuple(record)
    tbsql.update_team(team)
    clear_team_entries()
    refresh_treeview(tree, tbd.Team)


def delete_team(tree, record):
    team = tbd.Team.convert_from_tuple(record)
    tbsql.update_team(team)
    clear_team_entries()
    refresh_treeview(tree, tbd.Team)

# team function end region------------------------------
# lane function start region


def read_lane_entries():
    return entry_booking_id.get(), entry_booking_date.get(), entry_booking_team_id.get()


def clear_lane_entries():
    entry_booking_id.delete(0, tk.END)
    entry_booking_date.delete(0, tk.END)
    entry_booking_team_id.delete(0, tk.END)


def write_lane_entries(values):
    entry_lane_id.insert(0, values[0])
    entry_lane_date.insert(0, values[1])
    entry_lane_team_id.insert(0, values[2])


def edit_lane(event, tree):
    index_selected = tree.focus()
    values = tree.item(index_selected, "values")
    clear_lane_entries()
    write_lane_entries(values)


def create_lane(tree, record):
    lane = tbd.Lane.convert_from_tuple(record)
    tbsql.create_record(lane)
    clear_lane_entries()
    refresh_treeview(tree, tbd.Lane)


def update_lane(tree, record):
    lane = tbd.Lane.convert_from_tuple(record)
    tbsql.update_lane(lane)
    clear_lane_entries()
    refresh_treeview(tree, tbd.Lane)


def delete_lane(tree, record):
    lane = tbd.Lane.convert_from_tuple(record)
    tbsql.soft_delete_lane(lane)
    clear_lane_entries()
    refresh_treeview()

#  end region lane functions
# start region booking functions


def read_booking_entries():
    return entry_booking_id.get(), entry_booking_date.get(), entry_booking_team_id.get(), entry_booking_lane_id.get()


def clear_booking_entries():
    entry_booking_id.delete(0, tk.END)
    entry_booking_date.delete(0, tk.END)
    entry_booking_team_id.delete(0, tk.END)
    entry_booking_lane_id.delete(0, tk.END)


def write_booking_entries(values):
    entry_booking_id.insert(0, values[0])
    entry_booking_date.insert(0, values[1])
    entry_booking_team_id.insert(0, values[2])
    entry_booking_lane_id.insert(0, values[3])


def edit_booking(event,tree):
    index_selected = tree.focus()
    values = tree.item(index_selected, "values")
    clear_booking_entries()
    write_booking_entries(values)


def create_booking(tree, record):
    booking = tbd.Booking.convert_from_tuple(record)
    print(booking)
    lane_available = tbf.lane_available(tbsql.get_record(tbd.Lane, booking.lane_id), booking.date)
    capacity_ok = tbf.capacity_ok(tbsql.get_record(tbd.Lane, booking.lane_id), tbsql.get_record(tbd.Team, booking.team_id))
    if lane_available: # checks if land is available
        if capacity_ok: # checks if the max capacity has been reached
            tbsql.create_record(booking)
            clear_booking_entries()
            refresh_treeview(tree, tbd.Booking)
        else:
            messagebox.showwarning("", "Team size is too big for the Lane!")
    else:
        messagebox.showwarning("", "Lane is already booked on that date!")

def update_booking(tree, record):
    booking = tbd.Booking.convert_from_tuple(record)
    print(booking)
    lane_available = tbf.lane_available(tbsql.get_record(tbd.Lane, booking.lane_id), booking.date)
    capacity_ok = tbf.capacity_ok(tbsql.get_record(tbd.Lane, booking.lane_id), tbsql.get_record(tbd.Team, booking.team_id))
    if lane_available: # checks if land is available
        if capacity_ok: # checks if the max capacity has been reached
            tbsql.update_booking(booking)
            clear_booking_entries()
            refresh_treeview(tree, tbd.Booking)
        else:
            messagebox.showwarning("", "Team size is too big for the Lane!")
    else:
        messagebox.showwarning("", "Lane is already booked on that date!")

def delete_booking(tree, record):
    booking = tbd.Booking.convert_from_tuple(record)
    tbsql.soft_delete_booking(booking)
    clear_booking_entries()
    refresh_treeview(tree, tbd.Booking)

# endregion booking functions

def read_table(tree, class_):  # fill tree from database
    count = 0  # Used to keep track of odd and even rows, because these will be colored differently.
    result = tbsql.select_all(class_)  # Read all containers from database
    for record in result:
        if record.valid():  # this condition excludes soft deleted records from being shown in the data table
            if count % 2 == 0:  # even
                tree.insert(parent='', index='end', iid=str(count), text='', values=record.convert_to_tuple(), tags=('evenrow',))  # Insert one row into the data table
            else:  # odd
                tree.insert(parent='', index='end', iid=str(count), text='', values=record.convert_to_tuple(), tags=('oddrow',))  # Insert one row into the data table
            count += 1


def refresh_treeview(tree, class_):
    empty_treeview(tree)
    read_table(tree, class_)


def empty_treeview(tree):
    tree.delete(*tree.get_children())

main_window = tk.Tk()  # Define the main window
main_window.title('Topbike')  # Text shown in the top window bar
main_window.geometry("1100x500")  # window size first is width second is height

style = ttk.Style()
style.theme_use('default')

style.configure("Treeview", background=treeview_background, foreground=treeview_foreground, rowheight=rowheight, fieldbackground=treeview_background)
style.map('Treeview', background=[('selected', treeview_selected)])


# team region
frame_teams = tk.LabelFrame(main_window, text="Teams")  # labelframe for teams
frame_teams.grid(row=0, column=0, padx=padx, pady=pady, sticky=tk.N)  # place frame top left


tree_frame_teams = tk.Frame(frame_teams)
tree_frame_teams.grid(row=0, column=0, padx=padx, pady=pady)
tree_scroll_teams = tk.Scrollbar(tree_frame_teams)
tree_scroll_teams.grid(row=0, column=1, padx=0, pady=pady, sticky='ns')
tree_teams = ttk.Treeview(tree_frame_teams, yscrollcommand=tree_scroll_teams.set, selectmode="browse")
tree_teams.grid(row=0, column=0, padx=0, pady=pady)
tree_scroll_teams.config(command=tree_teams.yview)

tree_teams['columns'] = ("id", "skill_level", "team_size")  # Define columns
tree_teams.column("#0", width=0, stretch=tk.NO)  # Format columns. Suppress the irritating first empty column.
tree_teams.column("id", anchor=tk.E, width=40)  # "E" stands for East, meaning Right. Possible anchors are N, NE, E, SE, S, SW, W, NW and CENTER
tree_teams.column("skill_level", anchor=tk.CENTER, width=100)
tree_teams.column("team_size", anchor=tk.CENTER, width=100)
tree_teams.heading("#0", text="", anchor=tk.W)  # Create column headings
tree_teams.heading("id", text="Id", anchor=tk.CENTER)
tree_teams.heading("skill_level", text="Skill level", anchor=tk.CENTER)
tree_teams.heading("team_size", text="Team size", anchor=tk.CENTER)
tree_teams.tag_configure('oddrow', background=oddrow)  # Create tags for rows in 2 different colors
tree_teams.tag_configure('evenrow', background=evenrow)

# make rows clickable and call a function
tree_teams.bind("<ButtonRelease-1>", lambda event: edit_team(event, tree_teams))

# Define Frame containing labels, entries and buttons
controls_frame_teams = tk.Frame(frame_teams)
controls_frame_teams.grid(row=3, column=0, padx=padx, pady=pady)

# define frame containing labels and entries
edit_frame_teams = tk.Frame(controls_frame_teams)  # Add tuple entry boxes
edit_frame_teams.grid(row=0, column=0, padx=padx, pady=pady)

label_team_id = tk.Label(edit_frame_teams, text="Id")  # https://www.tutorialspoint.com/python/tk_label.htm
label_team_id.grid(row=0, column=0, padx=padx, pady=pady)
entry_team_id = tk.Entry(edit_frame_teams, width=4, justify="center")  # https://www.tutorialspoint.com/python/tk_entry.htm
entry_team_id.grid(row=1, column=0, padx=padx, pady=pady)

label_team_skill_level = tk.Label(edit_frame_teams, text="Skill level")
label_team_skill_level.grid(row=0, column=1, padx=padx, pady=pady)
entry_team_skill_level = tk.Entry(edit_frame_teams, width=10, justify="center")
entry_team_skill_level.grid(row=1, column=1, padx=padx, pady=pady)

label_team_team_size = tk.Label(edit_frame_teams, text="Team size")
label_team_team_size.grid(row=0, column=2, padx=padx, pady=pady)
entry_team_team_size = tk.Entry(edit_frame_teams, width=10, justify="center")
entry_team_team_size.grid(row=1, column=2, padx=padx, pady=pady)

# Define Frame containing buttons
button_frame_teams = tk.Frame(controls_frame_teams)
button_frame_teams.grid(row=1, column=0, padx=padx, pady=pady)

# Define buttons
button_create_team = tk.Button(button_frame_teams, text="Create", command=lambda: create_team(tree_teams, read_team_entries()))
button_create_team.grid(row=0, column=1, padx=padx, pady=pady)
button_update_team = tk.Button(button_frame_teams, text="Update", command=lambda: update_team(tree_teams, read_team_entries()))
button_update_team.grid(row=0, column=2, padx=padx, pady=pady)
button_delete_team = tk.Button(button_frame_teams, text="Delete", command=lambda: delete_team(tree_teams, read_team_entries()))
button_delete_team.grid(row=0, column=3, padx=padx, pady=pady)
button_clear_team_entries = tk.Button(button_frame_teams, text="Clear Entry Boxes", command=clear_team_entries)
button_clear_team_entries.grid(row=0, column=4, padx=padx, pady=pady)

# team end region-------------------------------------------------------------------------------
# lane start region--------------------------------------------------------------------------------

frame_lanes = tk.LabelFrame(main_window, text="Lanes")  # labelframe for lanes
frame_lanes.grid(row=0, column=1, padx=padx, pady=pady, sticky=tk.N)


tree_frame_lanes = tk.Frame(frame_lanes)
tree_frame_lanes.grid(row=0, column=0, padx=padx, pady=pady)
tree_scroll_lanes = tk.Scrollbar(tree_frame_lanes)
tree_scroll_lanes.grid(row=0, column=1, padx=0, pady=pady, sticky='ns')
tree_lanes = ttk.Treeview(tree_frame_lanes, yscrollcommand=tree_scroll_lanes.set, selectmode="browse")
tree_lanes.grid(row=0, column=0, padx=0, pady=pady)
tree_scroll_lanes.config(command=tree_lanes.yview)

tree_lanes['columns'] = ("id", "max_capacity", "difficulty")  # Define columns
tree_lanes.column("#0", width=0, stretch=tk.NO)  # Format columns. Suppress the irritating first empty column.
tree_lanes.column("id", anchor=tk.E, width=40)  # "E" stands for East, meaning Right. Possible anchors are N, NE, E, SE, S, SW, W, NW and CENTER
tree_lanes.column("max_capacity", anchor=tk.CENTER, width=100)
tree_lanes.column("difficulty", anchor=tk.CENTER, width=100)
tree_lanes.heading("#0", text="", anchor=tk.W)  # Create column headings
tree_lanes.heading("id", text="Id", anchor=tk.CENTER)
tree_lanes.heading("max_capacity", text="Max capacity", anchor=tk.CENTER)
tree_lanes.heading("difficulty", text="Difficulty", anchor=tk.CENTER)
tree_lanes.tag_configure('oddrow', background=oddrow)  # Create tags for rows in 2 different colors
tree_lanes.tag_configure('evenrow', background=evenrow)

# make rows clickable and call a function
tree_lanes.bind("<ButtonRelease-1>", lambda event: edit_lane(event, tree_lanes))

# Define Frame containing labels, entries and buttons
controls_frame_lanes = tk.Frame(frame_lanes)
controls_frame_lanes.grid(row=3, column=0, padx=padx, pady=pady)

# define frame containing labels and entries
edit_frame_lanes = tk.Frame(controls_frame_lanes)  # Add tuple entry boxes
edit_frame_lanes.grid(row=0, column=0, padx=padx, pady=pady)

label_lane_id = tk.Label(edit_frame_lanes, text="Id")
label_lane_id.grid(row=0, column=0, padx=padx, pady=pady)
entry_lane_id = tk.Entry(edit_frame_lanes, width=4, justify="center")
entry_lane_id.grid(row=1, column=0, padx=padx, pady=pady)

label_lane_date = tk.Label(edit_frame_lanes, text="Max capacity")
label_lane_date.grid(row=0, column=1, padx=padx, pady=pady)
entry_lane_date = tk.Entry(edit_frame_lanes, width=10, justify="center")
entry_lane_date.grid(row=1, column=1, padx=padx, pady=pady)

label_lane_team_id = tk.Label(edit_frame_lanes, text="Difficulty")
label_lane_team_id.grid(row=0, column=2, padx=padx, pady=pady)
entry_lane_team_id = tk.Entry(edit_frame_lanes, width=10, justify="center")
entry_lane_team_id.grid(row=1, column=2, padx=padx, pady=pady)

# Define Frame containing buttons
button_frame_lanes = tk.Frame(controls_frame_lanes)
button_frame_lanes.grid(row=1, column=0, padx=padx, pady=pady)

# Define buttons
button_create_lane = tk.Button(button_frame_lanes, text="Create", command=lambda: create_lane(tree_lanes, read_lane_entries()))
button_create_lane.grid(row=0, column=1, padx=padx, pady=pady)
button_update_lane = tk.Button(button_frame_lanes, text="Update", command=lambda: update_lane(tree_lanes, read_lane_entries()))
button_update_lane.grid(row=0, column=2, padx=padx, pady=pady)
button_delete_lane = tk.Button(button_frame_lanes, text="Delete", command=lambda: delete_lane(tree_lanes, read_lane_entries()))
button_delete_lane.grid(row=0, column=3, padx=padx, pady=pady)
button_clear_lane_entries = tk.Button(button_frame_lanes, text="Clear Entry Boxes", command=clear_team_entries)
button_clear_lane_entries.grid(row=0, column=4, padx=padx, pady=pady)

# lane end region
# booking start region

frame_bookings = tk.LabelFrame(main_window, text="Bookings")  # labelframe for Bookings
frame_bookings.grid(row=0, column=2, padx=padx, pady=pady, sticky=tk.N)


tree_frame_bookings = tk.Frame(frame_bookings)
tree_frame_bookings.grid(row=0, column=0, padx=padx, pady=pady)
tree_scroll_bookings = tk.Scrollbar(tree_frame_bookings)
tree_scroll_bookings.grid(row=0, column=1, padx=0, pady=pady, sticky='ns')
tree_bookings = ttk.Treeview(tree_frame_bookings, yscrollcommand=tree_scroll_bookings.set, selectmode="browse")
tree_bookings.grid(row=0, column=0, padx=0, pady=pady)
tree_scroll_bookings.config(command=tree_bookings.yview)

tree_bookings['columns'] = ("id", "date", "team_id", "lane_id")  # Define columns
tree_bookings.column("#0", width=0, stretch=tk.NO)  # Format columns. Suppress the irritating first empty column.
tree_bookings.column("id", anchor=tk.E, width=40)  # "E" stands for East, meaning Right. Possible anchors are N, NE, E, SE, S, SW, W, NW and CENTER
tree_bookings.column("date", anchor=tk.CENTER, width=100)
tree_bookings.column("team_id", anchor=tk.CENTER, width=100)
tree_bookings.column("lane_id", anchor=tk.CENTER, width=100)

tree_bookings.heading("#0", text="", anchor=tk.W)  # Create column headings
tree_bookings.heading("id", text="Id", anchor=tk.CENTER)
tree_bookings.heading("date", text="Date", anchor=tk.CENTER)
tree_bookings.heading("team_id", text="Team id", anchor=tk.CENTER)
tree_bookings.heading("lane_id", text="Lane id", anchor=tk.CENTER)
tree_bookings.tag_configure('oddrow', background=oddrow)  # Create tags for rows in 2 different colors
tree_bookings.tag_configure('evenrow', background=evenrow)

# make rows clickable and call a function
tree_bookings.bind("<ButtonRelease-1>", lambda event: edit_booking(event, tree_bookings))

# Define Frame containing labels, entries and buttons
controls_frame_bookings = tk.Frame(frame_bookings)
controls_frame_bookings.grid(row=3, column=0, padx=padx, pady=pady)

# define frame containing labels and entries
edit_frame_bookings = tk.Frame(controls_frame_bookings)  # Add tuple entry boxes
edit_frame_bookings.grid(row=0, column=0, padx=padx, pady=pady)

label_booking_id = tk.Label(edit_frame_bookings, text="Id")
label_booking_id.grid(row=0, column=0, padx=padx, pady=pady)
entry_booking_id = tk.Entry(edit_frame_bookings, width=4, justify="center")
entry_booking_id.grid(row=1, column=0, padx=padx, pady=pady)

label_booking_date = tk.Label(edit_frame_bookings, text="Date")
label_booking_date.grid(row=0, column=1, padx=padx, pady=pady)
entry_booking_date = tk.Entry(edit_frame_bookings, width=10, justify="center")
entry_booking_date.grid(row=1, column=1, padx=padx, pady=pady)

label_booking_team_id = tk.Label(edit_frame_bookings, text="Team id")
label_booking_team_id.grid(row=0, column=2, padx=padx, pady=pady)
entry_booking_team_id = tk.Entry(edit_frame_bookings, width=10, justify="center")
entry_booking_team_id.grid(row=1, column=2, padx=padx, pady=pady)

label_booking_lane_id = tk.Label(edit_frame_bookings, text="Lane id")
label_booking_lane_id.grid(row=0, column=3, padx=padx, pady=pady)
entry_booking_lane_id = tk.Entry(edit_frame_bookings, width=10, justify="center")
entry_booking_lane_id.grid(row=1, column=3, padx=padx, pady=pady)

# Define Frame containing buttons
button_frame_bookings = tk.Frame(controls_frame_bookings)
button_frame_bookings.grid(row=1, column=0, padx=padx, pady=pady)

# Define buttons
button_create_booking = tk.Button(button_frame_bookings, text="Create", command=lambda: create_booking(tree_bookings, read_booking_entries()))
button_create_booking.grid(row=0, column=1, padx=padx, pady=pady)
button_update_booking = tk.Button(button_frame_bookings, text="Update", command=lambda: update_booking(tree_bookings, read_booking_entries()))
button_update_booking.grid(row=0, column=2, padx=padx, pady=pady)
button_delete_booking = tk.Button(button_frame_bookings, text="Delete", command=lambda: delete_booking(tree_bookings, read_booking_entries()))
button_delete_booking.grid(row=0, column=3, padx=padx, pady=pady)
button_clear_booking_entries = tk.Button(button_frame_bookings, text="Clear Entry Boxes", command=clear_team_entries)
button_clear_booking_entries.grid(row=0, column=4, padx=padx, pady=pady)

if __name__ == "__main__":
    refresh_treeview(tree_teams, tbd.Team)
    refresh_treeview(tree_lanes, tbd.Lane)
    refresh_treeview(tree_bookings, tbd.Booking)
    main_window.mainloop()