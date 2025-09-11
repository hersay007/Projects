import tkinter as tk

class MemoryManagementSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Management Simulator")
        self.root.configure(bg="#1e1e2e")

        self.memory_size = 100  # Total memory size in MB
        self.process_list = []  # Stores running processes (ID, Size, Start Address)
        self.memory_holes = [(20, self.memory_size)] 
        self.process_counter = 1 

        self.setup_ui()

    def setup_ui(self):
        self.left_frame = tk.Frame(self.root, bg="#282a36", padx=10, pady=10, bd=2, relief="ridge")
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.process_label = tk.Label(self.left_frame, text="Processes in Memory:", fg="cyan", bg="#282a36", font=("Arial", 12, "bold"))
        self.process_label.pack()

        self.process_listbox = tk.Listbox(self.left_frame, height=10, width=30, bg="#44475a", fg="white", font=("Arial", 10), selectbackground="cyan")
        self.process_listbox.pack(pady=5)

        self.remove_process_btn = tk.Button(self.left_frame, text="Remove Selected", command=self.remove_selected_process,
                                            bg="#ff5555", fg="white", font=("Arial", 10, "bold"), bd=0, padx=10, pady=5, relief="flat")
        self.remove_process_btn.pack(pady=5)

        self.swap_out_btn = tk.Button(self.left_frame, text="Swap Out", command=self.swap_out_process,
                                      bg="#ffb86c", fg="black", font=("Arial", 10, "bold"), bd=0, padx=10, pady=5, relief="flat")
        self.swap_out_btn.pack(pady=5)

        # Memory Display
        self.canvas = tk.Canvas(self.root, width=400, height=600, bg="#44475a", bd=0, highlightthickness=2, highlightbackground="cyan")
        self.canvas.pack(side=tk.RIGHT, padx=10, pady=10)
        self.draw_memory()

        # Center Log Panel
        self.log_frame = tk.Frame(self.root, bg="#282a36", pady=10)
        self.log_frame.pack(side=tk.TOP, fill=tk.X, padx=150)

        self.log_label = tk.Label(self.log_frame, text="Event Log:", fg="cyan", bg="#282a36", font=("Arial", 12, "bold"))
        self.log_label.pack()

        self.log_text = tk.Text(self.log_frame, height=10, width=80, bg="#44475a", fg="white", font=("Arial", 10), state=tk.DISABLED)
        self.log_text.pack(padx=20, pady=5)

        # Bottom Control Panel
        self.control_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.control_frame.pack(side=tk.BOTTOM, pady=10)

        self.process_size_entry = tk.Entry(self.control_frame, width=10, font=("Arial", 12), bg="#6272a4", fg="white", bd=2, relief="solid")
        self.process_size_entry.pack(side=tk.LEFT, padx=5)

        self.add_process_btn = tk.Button(self.control_frame, text="Add Process", command=self.add_process,
                                         bg="#50fa7b", fg="black", font=("Arial", 10, "bold"), bd=0, padx=10, pady=5, relief="flat")
        self.add_process_btn.pack(side=tk.LEFT, padx=5)

        self.compact_btn = tk.Button(self.control_frame, text="Compact Memory", command=self.compact_memory,
                                     bg="#8be9fd", fg="black", font=("Arial", 10, "bold"), bd=0, padx=10, pady=5, relief="flat")
        self.compact_btn.pack(side=tk.LEFT, padx=5)

    def update_log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.yview(tk.END)

    def draw_memory(self):
        self.canvas.delete("all")
        self.canvas.create_text(200, 10, text="Memory Block", font=("Arial", 14, "bold"), fill="white")

        for process in self.process_list:
            self.canvas.create_rectangle(50, process[2], 350, process[2] + process[1] * 5, fill="#50fa7b", outline="white")
            self.canvas.create_text(200, process[2] + 10, text=f"P{process[0]} ({process[1]}MB)", fill="black")

        for hole in self.memory_holes:
            self.canvas.create_rectangle(50, hole[0], 350, hole[0] + hole[1] * 5, fill="#ff5555", outline="white")
            self.canvas.create_text(200, hole[0] + 10, text=f"Hole: {hole[1]}MB", fill="white")

        available_memory = self.get_available_memory()
        self.canvas.create_text(200, 580, text=f"Available Memory: {available_memory}MB", fill="cyan")

    def get_available_memory(self):
        return sum(hole[1] for hole in self.memory_holes)

    def add_process(self):
        process_size = self.process_size_entry.get()
        if not process_size.isdigit():
            self.update_log("Error: Invalid process size.")
            return
        process_size = int(process_size)

        allocated = False
        for index, hole in enumerate(self.memory_holes):
            if hole[1] * 5 >= process_size * 5:
                self.process_list.append((self.process_counter, process_size, hole[0]))
                self.process_listbox.insert(tk.END, f"P{self.process_counter} - {process_size}MB")

                if hole[1] == process_size:
                    del self.memory_holes[index]
                else:
                    self.memory_holes[index] = (hole[0] + process_size * 5, hole[1] - process_size)

                self.process_counter += 1
                allocated = True
                break

        if allocated:
            self.update_log(f"Process P{self.process_counter - 1} added ({process_size}MB).")
        else:
            self.update_log("Warning: Process cannot be allocated. Consider compacting memory.")

        self.draw_memory()

    def remove_selected_process(self):
        selected_index = self.process_listbox.curselection()
        if not selected_index:
            self.update_log("Warning: No process selected.")
            return
        process_to_remove = self.process_list.pop(selected_index[0])
        self.process_listbox.delete(selected_index[0])
        self.memory_holes.append((process_to_remove[2], process_to_remove[1]))
        self.merge_holes()
        self.update_log(f"Process P{process_to_remove[0]} removed.")
        self.draw_memory()

    def swap_out_process(self):
        if not self.process_list:
            self.update_log("Warning: No processes to swap out.")
            return
        earliest_process = self.process_list.pop(0)
        self.process_listbox.delete(0)
        self.memory_holes.append((earliest_process[2], earliest_process[1]))
        self.merge_holes()
        self.update_log(f"Process P{earliest_process[0]} swapped out.")
        self.draw_memory()

    def compact_memory(self):
        self.process_list.sort(key=lambda x: x[2])
        y = 20
        for i in range(len(self.process_list)):
            self.process_list[i] = (self.process_list[i][0], self.process_list[i][1], y)
            y += self.process_list[i][1] * 5

        used_memory = sum(p[1] for p in self.process_list)
        self.memory_holes = [(y, self.memory_size - used_memory)]
        self.update_log("Memory compacted successfully.")
        self.draw_memory()

    def merge_holes(self):
        self.memory_holes.sort()
        merged_holes = []
        for hole in self.memory_holes:
            if merged_holes and merged_holes[-1][0] + merged_holes[-1][1] * 5 == hole[0]:
                merged_holes[-1] = (merged_holes[-1][0], merged_holes[-1][1] + hole[1])
            else:
                merged_holes.append(hole)
        self.memory_holes = merged_holes

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryManagementSimulator(root)
    root.mainloop()
