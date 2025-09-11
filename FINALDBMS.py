import itertools
import tkinter as tk
from tkinter import scrolledtext, ttk

class NormalizationTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Normalization Tool - Candidate Keys and Normal Forms")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Input Section
        input_frame = tk.LabelFrame(root, text="Input", font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)
        input_frame.pack(pady=10, padx=10, fill="both")

        tk.Label(input_frame, text="Enter Relation (comma-separated attributes):", font=("Arial", 10), bg="white").pack()
        self.relation_entry = tk.Entry(input_frame, width=60)
        self.relation_entry.pack(pady=5)

        tk.Label(input_frame, text="Enter Functional Dependencies (A->B, B->C):", font=("Arial", 10), bg="white").pack()
        self.fd_entry = tk.Entry(input_frame, width=60)
        self.fd_entry.pack(pady=5)

        # Dropdown for Normal Form Selection
        tk.Label(input_frame, text="Choose Decomposition Level:", font=("Arial", 10), bg="white").pack()
        self.nf_choice = ttk.Combobox(input_frame, values=["2NF", "3NF", "BCNF"], state="readonly")
        self.nf_choice.pack(pady=5)
        self.nf_choice.current(0)

        # Analyze Button
        tk.Button(input_frame, text="Analyze", command=self.analyze, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white").pack(pady=10)

        # Output Section
        output_frame = tk.LabelFrame(root, text="Output", font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)
        output_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.result_text = scrolledtext.ScrolledText(output_frame, width=90, height=20, wrap=tk.WORD)
        self.result_text.pack()

    def parse_input(self):
        attributes = set(self.relation_entry.get().replace(" ", "").split(","))
        fds = [fd.replace(" ", "").split("->") for fd in self.fd_entry.get().split(",")]
        fds = [(set(fd[0]), set(fd[1])) for fd in fds]
        return attributes, fds

    def closure(self, attrs, fds):
        closure_set = set(attrs)
        while True:
            new_elements = set()
            for lhs, rhs in fds:
                if lhs.issubset(closure_set):
                    new_elements.update(rhs)
            if new_elements.issubset(closure_set):
                break
            closure_set.update(new_elements)
        return closure_set

    def find_candidate_keys(self, attributes, fds):
        all_attrs = set(attributes)
        minimal_superkeys = []
        for subset_size in range(1, len(all_attrs) + 1):
            for subset in itertools.combinations(all_attrs, subset_size):
                subset = set(subset)
                if self.closure(subset, fds) == all_attrs:
                    if not any(set(ck).issubset(subset) for ck in minimal_superkeys):
                        minimal_superkeys.append(subset)
        return minimal_superkeys

    def analyze(self):
        self.result_text.delete(1.0, tk.END)  # Clear previous output
        attributes, fds = self.parse_input()
        candidate_keys = self.find_candidate_keys(attributes, fds)

        # Display candidate keys
        self.result_text.insert(tk.END, f"Candidate Keys: {', '.join([''.join(sorted(ck)) for ck in candidate_keys])}\n\n", "green")

        # Check normal forms
        self.check_normal_forms(attributes, fds, candidate_keys)

    def check_normal_forms(self, attributes, fds, candidate_keys):
        nf_level = self.nf_choice.get()

        # 1NF Check
        self.result_text.insert(tk.END, "✔ 1NF: Relation is in 1NF (all attributes are atomic).\n", "green")

        # 2NF Check
        violating_fds_2nf = []
        for lhs, rhs in fds:
            for ck in candidate_keys:
                if lhs.issubset(ck) and not rhs.issubset(ck) and len(lhs) < len(ck):
                    violating_fds_2nf.append((lhs, rhs))
                    break

        if violating_fds_2nf:
            self.result_text.insert(tk.END, "❌ 2NF Violation:\n", "red")
            for lhs, rhs in violating_fds_2nf:
                self.result_text.insert(tk.END, f"  {''.join(sorted(lhs))} -> {''.join(sorted(rhs))}\n", "red")
            if nf_level == "2NF":
                self.decompose("2NF", attributes, fds, violating_fds_2nf)
                return
        else:
            self.result_text.insert(tk.END, "✔ 2NF: Relation is in 2NF.\n", "green")

        # 3NF Check
        violating_fds_3nf = []
        for lhs, rhs in fds:
            if not any(rhs.issubset(ck) for ck in candidate_keys):
                violating_fds_3nf.append((lhs, rhs))

        if violating_fds_3nf:
            self.result_text.insert(tk.END, "❌ 3NF Violation:\n", "red")
            for lhs, rhs in violating_fds_3nf:
                self.result_text.insert(tk.END, f"  {''.join(sorted(lhs))} -> {''.join(sorted(rhs))}\n", "red")
            if nf_level == "3NF":
                self.decompose("3NF", attributes, fds, violating_fds_3nf)
                return
        else:
            self.result_text.insert(tk.END, "✔ 3NF: Relation is in 3NF.\n", "green")

        # BCNF Check
        violating_fds_bcnf = []
        for lhs, rhs in fds:
            if not any(lhs.issuperset(ck) for ck in candidate_keys):
                violating_fds_bcnf.append((lhs, rhs))

        if violating_fds_bcnf:
            self.result_text.insert(tk.END, "❌ BCNF Violation:\n", "red")
            for lhs, rhs in violating_fds_bcnf:
                self.result_text.insert(tk.END, f"  {''.join(sorted(lhs))} -> {''.join(sorted(rhs))}\n", "red")
            if nf_level == "BCNF":
                self.decompose("BCNF", attributes, fds, violating_fds_bcnf)
                return
        else:
            self.result_text.insert(tk.END, "✔ BCNF: Relation is in BCNF.\n", "green")

    def decompose(self, level, attributes, fds, violating_fds):
        self.result_text.insert(tk.END, f"\n🔹 Decomposing into {level}...\n", "blue")
        new_relations = []
        for lhs, rhs in violating_fds:
            new_relations.append(lhs | rhs)
        remaining_attrs = attributes.copy()
        for rel in new_relations:
            remaining_attrs -= rel
        if remaining_attrs:
            new_relations.append(remaining_attrs)
        for i, rel in enumerate(new_relations):
            self.result_text.insert(tk.END, f"  R{i+1}: {', '.join(sorted(rel))}\n", "blue")

if __name__ == "__main__":
    root = tk.Tk()
    app = NormalizationTool(root)

    # Styling for color-coded output
    app.result_text.tag_config("green", foreground="green")
    app.result_text.tag_config("red", foreground="red")
    app.result_text.tag_config("blue", foreground="blue")

    root.mainloop()
