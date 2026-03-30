
# AI Smart Traffic Control System using Fuzzy Logic

## Overview
This project implements an **AI-based Smart Traffic Control System** using **Fuzzy Logic** to dynamically allocate green signal time based on traffic density at different roads of a junction.

The system provides a **Graphical User Interface (GUI)** built with Tkinter that allows users to simulate traffic conditions and visualize signal operations.

---

## Features
- Supports **2-way, 4-way, and 6-way junctions**
- Uses **Fuzzy Logic** to determine signal timing
- Interactive **GUI simulation**
- **Traffic signal visualization** with red, yellow, and green lights
- **Random traffic generator**
- **Emergency mode** for priority vehicles
- **Graph visualization** of green signal time allocation
- Displays **traffic condition analysis** (Low, Moderate, Heavy)

---

## Technologies Used
- Python
- Tkinter (GUI)
- NumPy
- Scikit-Fuzzy
- Matplotlib
<img width="900" height="85" alt="image" src="https://github.com/user-attachments/assets/2a977a6f-3baf-4753-bc5a-81565d8d68a5" />

---

## Installation

Install required libraries:

```bash
pip install numpy scikit-fuzzy matplotlib
````

---

## How to Run

Run the Python program:

```bash
python fuzzy_logic.py
```

---

## How It Works

1. User selects junction type (2-way, 4-way, or 6-way).
2. User enters traffic density values (0–100).
3. The fuzzy logic system evaluates traffic conditions.
4. Green signal time is allocated accordingly.
5. Traffic lights simulation and graph are displayed.

---

## Example Scenario

| Road | Traffic Density |
| ---- | --------------- |
| A    | 20              |
| B    | 80              |
| C    | 40              |
| D    | 60              |
<img width="1002" height="793" alt="image" src="https://github.com/user-attachments/assets/8f247b96-a47a-48bb-a6c2-2923c843b820" />
<img width="1903" height="1112" alt="image" src="https://github.com/user-attachments/assets/bde8624c-9ceb-4430-8103-2fd3df75de42" />
<img width="1909" height="1115" alt="image" src="https://github.com/user-attachments/assets/5cf1b6da-b882-4088-87e5-ba9102cf5d0e" />
<img width="1915" height="1127" alt="image" src="https://github.com/user-attachments/assets/8f824c96-cce3-491f-916e-af3b0bbd459f" />

The system calculates optimal **green signal timing** for each road based on density.

---

## Output

* Traffic signal simulation
* Priority road identification
* Graph showing green time allocation
* Traffic condition status

---

## Future Improvements

* Integration with real-time traffic sensors
* Camera-based vehicle detection
* IoT traffic management system
* Smart city traffic integration

---

## Author

Jyoshna Chereddy




---

If you want, I can also make a **much better professional README with diagrams and screenshots (looks impressive on GitHub projects).**
