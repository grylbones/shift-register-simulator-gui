# Shift Register Simulator (Python OOP + Tkinter)

A visual, interactive simulator for 4-bit shift registers built using Object-Oriented Programming and Tkinter.

This project implements and visualizes:

- SISO – Serial-In Serial-Out  
- SIPO – Serial-In Parallel-Out  
- PISO – Parallel-In Serial-Out  
- PIPO – Parallel-In Parallel-Out  

Each register type is structured using an abstract base class and multiple polymorphic child classes.

---

## Features

- Interactive Tkinter GUI  
- Real-time D/Q updates  
- Clock pulse simulation  
- Serial and parallel input modes  
- Hardware-style block diagram visualization  
- Clean OOP architecture (inheritance and polymorphism)  
- Main menu for selecting register type  

---

## Tech Stack

- Python  
- Tkinter  
- Object-Oriented Programming  

---

## Screenshots

### Main Menu
<img width="506" height="525" src="https://github.com/user-attachments/assets/82540577-555f-4d4f-ab5c-086defc5e855" />

### SISO Register
<img width="741" height="465" src="https://github.com/user-attachments/assets/84461033-4896-42dc-903f-de3f6a798009" />

### SIPO Register
<img width="745" height="471" src="https://github.com/user-attachments/assets/1da49365-0678-4fb4-b807-27de0cadaabc" />

### PISO Register
<img width="824" height="465" src="https://github.com/user-attachments/assets/678fa9de-ec03-4a39-bfcd-922bfbc29b9d" />

### PIPO Register
<img width="745" height="471" src="https://github.com/user-attachments/assets/a12750e4-b0d0-475b-8762-a54e81cefc41" />

---

## How It Works

- A base class handles GUI layout, drawing, and shared register logic  
- Each register type extends the base class and implements its specific loading and shifting behavior  
- Clock pulses update the register state and refresh the GUI  
- Polymorphism ensures each design has its own functionality while sharing a unified structure  

---

## Concepts Demonstrated

- Digital logic design  
- Shift register behavior  
- GUI application structure  
- Abstraction and reusable class design  
- State updates and event-driven programming  

---

## Author
-  Chinnagundam Harsha <br>
-  Shashank Dorbala <br>
-  Rishi Chitturi <br>
Project developed out of interest in digital electronics, OOP, and GUI design.
