import tkinter as tk
from tkinter import filedialog

ALLOWED_CHARACTERS = ".XSGE"

class MapGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Map Generator")
        master.geometry("500x400")

        # Settings Frame
        settings_frame = tk.Frame(master)
        settings_frame.pack()

        tk.Label(settings_frame, text="Width:").grid(row=0, column=0)
        self.width_entry = tk.Entry(settings_frame)
        self.width_entry.insert(0, "10") 
        self.width_entry.grid(row=0, column=1)

        tk.Label(settings_frame, text="Height:").grid(row=1, column=0)
        self.height_entry = tk.Entry(settings_frame)
        self.height_entry.insert(0, "10")  
        self.height_entry.grid(row=1, column=1)

        # Add the Update Grid Button to the settings frame
        tk.Button(settings_frame, text="Update Grid", command=self.update_grid).grid(row=0, column=2, rowspan=2)


        # Button Frame
        button_frame = tk.Frame(master)
        button_frame.pack()

        tk.Button(button_frame, text="Fill All", command=self.fill_all).pack(side=tk.LEFT)

        self.selected_char = tk.StringVar(value=".")  # Currently selected character
        chars = ".EXGS"
        for char in chars:
            tk.Radiobutton(
                button_frame, 
                text=char, 
                variable=self.selected_char, 
                value=char
            ).pack(side=tk.LEFT)

        # Map Frame 
        self.map_frame = tk.Frame(master)
        self.map_frame.pack()

        self.build_map()  # Initialize the map

        # Create a frame specifically for Save and Load buttons
        file_buttons_frame = tk.Frame(master)
        file_buttons_frame.pack()

        # Place the buttons within the new frame
        tk.Button(file_buttons_frame, text="Load Map", command=self.load_map).pack(side=tk.LEFT)
        tk.Button(file_buttons_frame, text="Save Map", command=self.save_map).pack(side=tk.LEFT)

    def fill_all(self):
        selected = self.selected_char.get()
        for row in range(self.height):
            for col in range(self.width):
                self.map_labels[row][col]['text'] = selected

    def build_map(self):
        self.width = int(self.width_entry.get())
        self.height = int(self.height_entry.get())

        # Clear existing map frame
        for widget in self.map_frame.winfo_children():
            widget.destroy()

        # Create grid of labels
        self.map_labels = []
        for row in range(self.height):
            row_labels = []
            for col in range(self.width):
                label = tk.Label(self.map_frame, text=".", width=2, borderwidth=1, relief="sunken")
                label.grid(row=row, column=col)
                label.bind("<Button-1>", lambda event, r=row, c=col: self.update_tile(event, r, c))
                row_labels.append(label)
            self.map_labels.append(row_labels)

    def load_map(self):
        filename = filedialog.askopenfilename(defaultextension=".txt")
        if filename:
            try:
                with open(filename, "r") as f:
                    new_map = f.readlines()

                new_width = len(new_map[0].strip())  # Get width from the file
                new_height = len(new_map)

                # Update dimensions
                self.width_entry.delete(0, tk.END)
                self.width_entry.insert(0, new_width)
                self.height_entry.delete(0, tk.END)
                self.height_entry.insert(0, new_height)

                self.update_grid() # Update grid with new dimensions

                # Basic validation
                if any(len(line.strip()) != self.width for line in new_map):
                    print("Error: Map width doesn't match.")
                    return

                self.height = len(new_map)
                self.build_map()  # Recreate the grid

                # Load the map data
                for row, line in enumerate(new_map):
                    for col, char in enumerate(line.strip()):
                        self.map_labels[row][col]['text'] = char

            except (FileNotFoundError, ValueError):  # Handle potential errors
                print("Error loading the map file.")

    def update_grid(self):
        try:
            new_width = int(self.width_entry.get())
            new_height = int(self.height_entry.get())

            if new_width > 0 and new_height > 0:
                # Store existing map data
                old_map = []
                for row in self.map_labels:
                    old_map.append([label['text'] for label in row])

                # Resize and rebuild the grid
                self.width = new_width
                self.height = new_height
                self.build_map()  

                # Restore non-'.' characters
                for row in range(min(new_height, len(old_map))):  
                    for col in range(min(new_width, len(old_map[0]))): 
                        if old_map[row][col] != '.':
                            self.map_labels[row][col]['text'] = old_map[row][col] 

        except ValueError:
            print("Invalid width or height")

    def update_tile(self, event, row, col):
        current_char = self.map_labels[row][col]['text']
        chars = ALLOWED_CHARACTERS  # Allowed characters
        index = (chars.index(current_char) + 1) % len(chars)
        self.map_labels[row][col]['text'] = self.selected_char.get()

    def save_map(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt")
        if filename:
            with open(filename, "w") as f:
                for row in self.map_labels:
                    line = "".join(label['text'] for label in row) + "\n"
                    f.write(line)

root = tk.Tk()
map_generator = MapGenerator(root)


root.mainloop()