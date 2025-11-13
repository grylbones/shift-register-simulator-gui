import tkinter as tk
from tkinter import messagebox

# --- 1. ABSTRACT PARENT CLASS ---
class ShiftRegisterGUI:
    """
    Parent class for all shift register simulations.
    Handles basic Tkinter setup, common drawing utilities, and register state.
    """
    # FIX: Use __init__ instead of _init_
    def __init__(self, master, title, num_bits=4):
        self.master = master
        self.master.title(title)
        self.num_bits = num_bits
        self.register = [0] * num_bits  # Stores the state of Q1, Q2, Q3, Q4...

        # Lists to hold Tkinter canvas IDs for dynamic updating
        self.d_input_labels = []
        self.q_output_labels = []
        self.box_centers = []  # To align the clock line taps

        # --- Common Layout Parameters ---
        self.y_center = 150
        self.y_box_top = self.y_center - 40
        self.y_box_bot = self.y_center + 40
        self.box_width = 80
        self.box_spacing = 60 # Increased spacing for clarity
        self.x_start = 60

        # Calculate canvas width based on number of bits
        canvas_width = self.x_start * 2 + (self.num_bits * self.box_width) + ((self.num_bits -1) * self.box_spacing) + 100
        
        # Initialize the main frames
        self.create_controls_frame()
        self.canvas = tk.Canvas(self.master, width=canvas_width, height=350, bg="#E6E6FA")  # Lavender background
        self.canvas.pack(pady=10, padx=10)

        # Initialization methods (must be defined in children)
        self.create_specific_controls(self.top)
        self.draw_diagram()
        self.update_display()

    def create_controls_frame(self):
        """Creates the frame for controls, common to all register types."""
        self.top = tk.Frame(self.master, padx=10, pady=5, bg="#DCDCDC")
        self.top.pack(pady=10, fill=tk.X)
        tk.Button(self.top, text="Close Simulation", command=self.master.destroy,
                  bg="#FF6347", fg="white", activebackground="#CD5C5C").pack(side=tk.RIGHT, padx=15)

    def draw_flip_flop(self, i, x_pos):
        """Helper function to draw a single Flip-Flop box."""
        box_x1 = x_pos
        box_x2 = box_x1 + self.box_width
        self.canvas.create_rectangle(box_x1, self.y_box_top, box_x2, self.y_box_bot,
                                     outline="#4682B4", width=2, fill="#F0F8FF")
        self.canvas.create_text((box_x1 + box_x2) / 2, self.y_box_top - 15,
                                text=f"FF {i + 1}", fill="#4682B4", font=("Arial", 10, "bold"))
        self.box_centers.append((box_x1 + box_x2) / 2)
        return box_x1, box_x2

    def draw_common_clock(self):
        """Draws the common clock line connecting all flip-flops."""
        if not self.box_centers: return
        clock_y = self.y_box_bot + 60
        # Horizontal bus line
        self.canvas.create_line(self.box_centers[0] - 20, clock_y, self.box_centers[-1] + 20, clock_y,
                                fill="#800080", width=2)
        self.canvas.create_text(self.box_centers[0] - 30, clock_y, text="CLK", anchor="e", fill="#800080", font=("Arial", 10, "bold"))
        # Vertical taps
        for center_x in self.box_centers:
            # Drawing the clock triangle symbol at the input of the FF (simplified)
            self.canvas.create_line(center_x, self.y_box_bot, center_x, self.y_box_bot + 10, fill="#800080", width=1)
            self.canvas.create_polygon(center_x, self.y_box_bot + 10, center_x + 6, self.y_box_bot + 20,
                                       center_x - 6, self.y_box_bot + 20, fill="#800080")
            self.canvas.create_line(center_x, self.y_box_bot + 20, center_x, clock_y, fill="#800080", width=1)


    # --- ABSTRACT METHODS (To be implemented by children) ---
    def create_specific_controls(self, parent_frame):
        raise NotImplementedError("Subclass must implement create_specific_controls")

    def draw_diagram(self):
        raise NotImplementedError("Subclass must implement draw_diagram")

    def clock_pulse(self):
        raise NotImplementedError("Subclass must implement clock_pulse")

    def update_display(self):
        """Updates the D/Q labels on the canvas. Overridden by children for specific logic."""
        # Update all Q labels (Common for all registers)
        for i in range(self.num_bits):
            if i < len(self.q_output_labels): # Defensive check
                q_val = self.register[i]
                self.canvas.itemconfig(self.q_output_labels[i], text=f"Q{i+1}={q_val}")

# --- 2. CHILD CLASS: SERIAL IN, SERIAL OUT (SISO) ---

class SISO_Register(ShiftRegisterGUI):
    # FIX: Use __init__ instead of _init_
    def __init__(self, master):
        self.input_bits = []
        self.serial_input_entry = None
        self.input_label_id = None
        self.output_label_id = None
        self.next_serial_in = '0' # Tracks the next bit to enter D1
        super().__init__(master, "4-bit Serial-In, Serial-Out (SISO)")

    def create_specific_controls(self, parent_frame):
        tk.Label(parent_frame, text="Serial Input (e.g. 1010):", bg="#DCDCDC").pack(side=tk.LEFT, padx=5)
        self.serial_input_entry = tk.Entry(parent_frame, width=12)
        self.serial_input_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(parent_frame, text="Load String", command=self.load_input_string, bg="#A9A9A9").pack(side=tk.LEFT, padx=5)
        tk.Button(parent_frame, text="Clock (Shift)", command=self.clock_pulse, bg="#90EE90").pack(side=tk.LEFT, padx=15)

    def load_input_string(self):
        bits = self.serial_input_entry.get().strip()
        if not bits or not all(b in "01" for b in bits):
            messagebox.showerror("Invalid Input", "Input must be a non-empty string of 0s and 1s.")
            self.serial_input_entry.delete(0, tk.END)
            return
            
        self.input_bits = list(bits)
        self.register = [0] * self.num_bits
        self.next_serial_in = self.input_bits[0]
        self.update_display()

    def clock_pulse(self):
        new_bit = int(self.input_bits.pop(0)) if self.input_bits else 0
        self.register = [new_bit] + self.register[:-1]
        self.next_serial_in = self.input_bits[0] if self.input_bits else '0'
        self.update_display()

    def draw_diagram(self):
        # --- Serial Input Line ---
        self.canvas.create_line(self.x_start - 40, self.y_center, self.x_start, self.y_center, arrow=tk.LAST, fill="green", width=2)
        self.input_label_id = self.canvas.create_text(self.x_start - 45, self.y_center - 15, text="D1=0", anchor="w", fill="blue")

        # --- Draw all components sequentially ---
        for i in range(self.num_bits):
            # FIX: Standardized calculation for x_pos for consistent spacing
            x_pos = self.x_start + i * (self.box_width + self.box_spacing)
            box_x1, box_x2 = self.draw_flip_flop(i, x_pos)
            
            # Q Output Label (stored value)
            q_x_center = (box_x1 + box_x2) / 2
            
            # FIX: Moved Q label inside the box to prevent overlap with the clock line.
            self.q_output_labels.append(
                self.canvas.create_text(q_x_center, self.y_center, text=f"Q{i+1}=0", fill="#DC143C", font=("Arial", 12, "bold"))
            )
            
            # Connecting wire (Q[i] -> D[i+1])
            if i < self.num_bits - 1:
                line_start_x = box_x2
                line_end_x = line_start_x + self.box_spacing
                self.canvas.create_line(line_start_x, self.y_center, line_end_x, self.y_center, arrow=tk.LAST, fill="green", width=2)
                
                # D Label (for next flip-flop)
                d_x_center = line_start_x + self.box_spacing / 2
                self.d_input_labels.append(
                    self.canvas.create_text(d_x_center, self.y_center - 15, text=f"D{i+2}=0", fill="blue", font=("Arial", 9))
                )
                
        # --- Serial Output ---
        last_box_x2 = self.x_start + (self.num_bits - 1) * (self.box_width + self.box_spacing) + self.box_width
        output_end_x = last_box_x2 + 60
        self.canvas.create_line(last_box_x2, self.y_center, output_end_x, self.y_center, arrow=tk.LAST, fill="red", width=2)
        self.output_label_id = self.canvas.create_text(output_end_x + 5, self.y_center, text="0", anchor="w", fill="black", font=("Arial", 10, "bold"))
        self.canvas.create_text(output_end_x + 5, self.y_center - 15, text="Serial Out", anchor="w", fill="black", font=("Arial", 8))
        
        self.draw_common_clock()

    def update_display(self):
        super().update_display() # Updates Q labels
        # Update D1 (Serial Input)
        self.canvas.itemconfig(self.input_label_id, text=f"D1={self.next_serial_in}")
        # Update D2, D3, D4
        for i in range(len(self.d_input_labels)):
            self.canvas.itemconfig(self.d_input_labels[i], text=f"D{i+2}={self.register[i]}")
        # Update Serial Output (Q4)
        self.canvas.itemconfig(self.output_label_id, text=f"{self.register[self.num_bits - 1]}")


# --- 3. CHILD CLASS: SERIAL IN, PARALLEL OUT (SIPO) ---
class SIPO_Register(SISO_Register): # Inherits logic from SISO
    # FIX: Use __init__ instead of _init_
    def __init__(self, master):
        # FIX: Call parent __init__ using standard super()
        super().__init__(master)
        self.master.title("4-bit Serial-In, Parallel-Out (SIPO)")
        
    def draw_diagram(self):
        # --- Serial Input Line ---
        self.canvas.create_line(self.x_start - 40, self.y_center, self.x_start, self.y_center, arrow=tk.LAST, fill="green", width=2)
        self.input_label_id = self.canvas.create_text(self.x_start - 45, self.y_center - 15, text="D1=0", anchor="w", fill="blue")

        for i in range(self.num_bits):
            x_pos = self.x_start + i * (self.box_width + self.box_spacing)
            box_x1, box_x2 = self.draw_flip_flop(i, x_pos)
            
            q_x_center = (box_x1 + box_x2) / 2
            # Q Output Label (stored value) - placed inside FF for clarity
            self.q_output_labels.append(
                self.canvas.create_text(q_x_center, self.y_center, text=f"Q{i+1}=0", fill="#DC143C", font=("Arial", 12, "bold"))
            )
            
            # PARALLEL OUTPUT lines
            self.canvas.create_line(q_x_center, self.y_box_bot, q_x_center, self.y_box_bot + 40, arrow=tk.LAST, fill="red", width=2)
            
            # Connecting wire (Q[i] -> D[i+1])
            if i < self.num_bits - 1:
                line_start_x = box_x2
                line_end_x = line_start_x + self.box_spacing
                self.canvas.create_line(line_start_x, self.y_center, line_end_x, self.y_center, arrow=tk.LAST, fill="green", width=2)
                
                d_x_center = line_start_x + self.box_spacing / 2
                self.d_input_labels.append(
                    self.canvas.create_text(d_x_center, self.y_center - 15, text=f"D{i+2}=0", fill="blue", font=("Arial", 9))
                )
        self.draw_common_clock()
    
    def update_display(self):
        # Inherits logic from SISO, which is correct for SIPO's shifting and input display.
        # The Q labels are automatically updated by the super().update_display() call.
        super().update_display()


# --- 4. CHILD CLASS: PARALLEL IN, SERIAL OUT (PISO) ---
class PISO_Register(ShiftRegisterGUI):
    def __init__(self, master):
        self.parallel_vars = [tk.StringVar(value='0') for _ in range(4)]
        self.load_shift_mode = tk.StringVar(value="Load")
        self.serial_in_var = tk.StringVar(value='0') 
        self.output_label_id = None
        super().__init__(master, "4-bit Parallel-In, Serial-Out (PISO)")

    def create_specific_controls(self, parent_frame):
        # --- Parallel Input Controls ---
        tk.Label(parent_frame, text="Parallel Data:", bg="#DCDCDC").pack(side=tk.LEFT, padx=(5, 10))
        for i in range(self.num_bits):
            tk.Checkbutton(parent_frame, text=f"D{i+1}", variable=self.parallel_vars[i], onvalue='1', offvalue='0',
                           command=self.update_display, bg="#DCDCDC").pack(side=tk.LEFT)
        
        # --- Mode and Clock Controls ---
        tk.Button(parent_frame, text="Clock (Load/Shift)", command=self.clock_pulse, bg="#ADD8E6").pack(side=tk.LEFT, padx=15)
        tk.Label(parent_frame, text="Mode:", bg="#DCDCDC").pack(side=tk.LEFT)
        tk.Label(parent_frame, textvariable=self.load_shift_mode, font=("Arial", 10, "bold"), fg="#FF4500", bg="#DCDCDC").pack(side=tk.LEFT)
        
        # --- Serial Input Control ---
        separator = tk.Frame(parent_frame, bg="gray", width=2, height=20)
        separator.pack(side=tk.LEFT, padx=10, fill='y')
        tk.Checkbutton(parent_frame, text="Serial In", variable=self.serial_in_var, onvalue='1', offvalue='0',
                       command=self.update_display, bg="#DCDCDC").pack(side=tk.LEFT)

    def clock_pulse(self):
        if self.load_shift_mode.get() == "Load":
            self.register = [int(var.get()) for var in self.parallel_vars]
            self.load_shift_mode.set("Shift")
            messagebox.showinfo("Mode Change", "Data loaded. Register is now in SHIFT mode.")
        else: # Shift mode
            new_bit = int(self.serial_in_var.get())
            self.register = [new_bit] + self.register[:-1]
        self.update_display()

    # FIX 1: Override draw_flip_flop specifically for PISO
    def draw_flip_flop(self, i, x_pos):
        """Overrides parent method to draw the FF label inside the box."""
        box_x1 = x_pos
        box_x2 = box_x1 + self.box_width
        self.canvas.create_rectangle(box_x1, self.y_box_top, box_x2, self.y_box_bot,
                                     outline="#4682B4", width=2, fill="#F0F8FF")
        # Draw the "FF n" label INSIDE the box at the top to avoid all overlaps
        self.canvas.create_text((box_x1 + box_x2) / 2, self.y_box_top + 15,
                                text=f"FF {i + 1}", fill="#4682B4", font=("Arial", 10, "bold"))
        self.box_centers.append((box_x1 + box_x2) / 2)
        return box_x1, box_x2

    # FIX 2: Cleaned up draw_diagram to use the new method
    def draw_diagram(self):
        self.canvas.create_text(self.x_start - 35, self.y_center, text="Serial\nInput", fill="blue", justify=tk.CENTER)
        
        for i in range(self.num_bits):
            x_pos = self.x_start + i * (self.box_width + self.box_spacing)
            
            # This now calls the PISO-specific draw_flip_flop method above
            box_x1, box_x2 = self.draw_flip_flop(i, x_pos)
            
            d_x_center = (box_x1 + box_x2) / 2

            # D Input Line (PARALLEL INPUT from above)
            self.canvas.create_line(d_x_center, self.y_box_top, d_x_center, self.y_box_top - 30, arrow=tk.LAST, fill="blue", width=2)
            self.d_input_labels.append(
                self.canvas.create_text(d_x_center, self.y_box_top - 45, text=f"D{i+1}=0", fill="blue", font=("Arial", 9))
            )

            # Q Output Label (stored bit) is placed in the center of the box
            self.q_output_labels.append(
                self.canvas.create_text(d_x_center, self.y_center + 10, text=f"Q{i+1}=0", fill="#DC143C", font=("Arial", 12, "bold"))
            )
            
            # Connecting wire (for SHIFTING)
            if i < self.num_bits - 1:
                line_start_x = box_x2
                line_end_x = line_start_x + self.box_spacing
                self.canvas.create_line(line_start_x, self.y_center, line_end_x, self.y_center, arrow=tk.LAST, fill="green", width=2)
        
        # Serial Output
        last_box_x2 = self.x_start + (self.num_bits - 1) * (self.box_width + self.box_spacing) + self.box_width
        output_end_x = last_box_x2 + 60
        self.canvas.create_line(last_box_x2, self.y_center, output_end_x, self.y_center, arrow=tk.LAST, fill="red", width=2)
        self.output_label_id = self.canvas.create_text(output_end_x + 5, self.y_center, text="0", anchor="w", fill="black", font=("Arial", 10, "bold"))
        self.canvas.create_text(output_end_x + 5, self.y_center - 15, text="Serial Out", anchor="w", fill="black", font=("Arial", 8))

        self.draw_common_clock()

    def update_display(self):
        # Update Q labels
        for i in range(self.num_bits):
            self.canvas.itemconfig(self.q_output_labels[i], text=f"Q{i+1}={self.register[i]}")

        # Update D labels based on mode
        if self.load_shift_mode.get() == "Load":
            for i in range(self.num_bits):
                d_val = self.parallel_vars[i].get()
                self.canvas.itemconfig(self.d_input_labels[i], text=f"D{i+1}={d_val}")
        else: # Shift Mode
            serial_in_val = self.serial_in_var.get()
            self.canvas.itemconfig(self.d_input_labels[0], text=f"D1={serial_in_val}")
            for i in range(1, self.num_bits):
                self.canvas.itemconfig(self.d_input_labels[i], text=f"D{i+1}={self.register[i-1]}")
                
        # Update Serial Output label (always shows Q4)
        self.canvas.itemconfig(self.output_label_id, text=f"{self.register[self.num_bits - 1]}")
# --- 5. CHILD CLASS: PARALLEL IN, PARALLEL OUT (PIPO) ---
# --- 5. CHILD CLASS: PARALLEL IN, PARALLEL OUT (PIPO) ---
class PIPO_Register(ShiftRegisterGUI):
    def __init__(self, master):
        self.parallel_vars = [tk.StringVar(value='0') for _ in range(4)]
        super().__init__(master, "4-bit Parallel-In, Parallel-Out (PIPO)")

    def create_specific_controls(self, parent_frame):
        tk.Label(parent_frame, text="Parallel Data:", bg="#DCDCDC").pack(side=tk.LEFT, padx=(5, 10))
        for i in range(self.num_bits):
            tk.Checkbutton(parent_frame, text=f"D{i+1}", variable=self.parallel_vars[i], onvalue='1', offvalue='0',
                           command=self.update_display, bg="#DCDCDC").pack(side=tk.LEFT)
        tk.Button(parent_frame, text="Clock (Load)", command=self.clock_pulse, bg="#ADD8E6").pack(side=tk.LEFT, padx=20)

    def clock_pulse(self):
        self.register = [int(var.get()) for var in self.parallel_vars]
        self.update_display()

    # FIX 1: Override draw_flip_flop to move the "FF n" label inside.
    def draw_flip_flop(self, i, x_pos):
        """Overrides parent method to draw the FF label inside the box."""
        box_x1 = x_pos
        box_x2 = box_x1 + self.box_width
        self.canvas.create_rectangle(box_x1, self.y_box_top, box_x2, self.y_box_bot,
                                     outline="#4682B4", width=2, fill="#F0F8FF")
        # Draw the "FF n" label INSIDE the box at the top to avoid all overlaps
        self.canvas.create_text((box_x1 + box_x2) / 2, self.y_box_top + 15,
                                text=f"FF {i + 1}", fill="#4682B4", font=("Arial", 10, "bold"))
        self.box_centers.append((box_x1 + box_x2) / 2)
        return box_x1, box_x2

    # FIX 2: Cleaned up draw_diagram for clarity and correctness.
    def draw_diagram(self):
        for i in range(self.num_bits):
            x_pos = self.x_start + i * (self.box_width + self.box_spacing)
            # Calls the PIPO-specific draw_flip_flop method above
            box_x1, box_x2 = self.draw_flip_flop(i, x_pos)
            d_x_center = (box_x1 + box_x2) / 2

            # D Input Line (PARALLEL INPUT) - Arrow points down into the box.
            self.canvas.create_line(d_x_center, self.y_box_top - 30, d_x_center, self.y_box_top, arrow=tk.LAST, fill="blue", width=2)
            self.d_input_labels.append(
                self.canvas.create_text(d_x_center, self.y_box_top - 45, text=f"D{i+1}=0", fill="blue", font=("Arial", 9))
            )
            
            # Q Output Label (stored bit)
            self.q_output_labels.append(
                self.canvas.create_text(d_x_center, self.y_center + 10, text=f"Q{i+1}=0", fill="#DC143C", font=("Arial", 12, "bold"))
            )
            
            # FIX 3: Draw PARALLEL OUTPUT lines. Arrow points down, away from the box.
            self.canvas.create_line(d_x_center, self.y_box_bot, d_x_center, self.y_box_bot + 40, arrow=tk.LAST, fill="red", width=2)
        
        self.draw_common_clock()

    def update_display(self):
        super().update_display() # Updates Q labels
        # Update D labels from checkbuttons
        for i in range(self.num_bits):
            d_val = self.parallel_vars[i].get()
            self.canvas.itemconfig(self.d_input_labels[i], text=f"D{i+1}={d_val}")

# --- 6. MAIN MENU CLASS ---
class MainMenu:
    # FIX: Use __init__ instead of _init_
    def __init__(self, master):
        self.master = master
        self.master.title("Shift Register Simulator")
        self.master.geometry("400x300")
        self.master.config(bg="#F0F0F0")

        tk.Label(master, text="Select Shift Register Type",
                 font=("Arial", 16, "bold"), bg="#F0F0F0").pack(pady=20)

        self.register_types = {
            "Serial-In, Serial-Out (SISO)": SISO_Register,
            "Serial-In, Parallel-Out (SIPO)": SIPO_Register,
            "Parallel-In, Serial-Out (PISO)": PISO_Register,
            "Parallel-In, Parallel-Out (PIPO)": PIPO_Register
        }

        for name, cls in self.register_types.items():
            tk.Button(master, text=name, command=lambda c=cls: self.open_simulation(c),
                      width=30, height=2, bg="#FFFFFF", relief=tk.RAISED, bd=2).pack(pady=5)

    def open_simulation(self, RegisterClass):
        new_window = tk.Toplevel(self.master)
        app = RegisterClass(new_window)

# FIX: Use __name__ and __main__
if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()
