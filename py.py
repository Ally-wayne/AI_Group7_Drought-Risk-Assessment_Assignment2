import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os

# CSV file to store data
CSV_FILE = "drought_data.csv"

def assess_drought(rainfall, soil_moisture, temperature, water_availability):
    """Rule-based expert system for drought risk assessment."""
    try:
        rainfall = float(rainfall)
        soil_moisture = float(soil_moisture)
        temperature = float(temperature)
        water_availability = float(water_availability)
        
        # Drought assessment rules
        if rainfall < 50 and soil_moisture < 30:
            return "Moderate Drought: Implement water conservation measures and monitor conditions."
        elif rainfall < 20 and temperature > 35 and soil_moisture < 20:
            return "Severe Drought: Immediate irrigation and emergency relief are required."
        elif water_availability < 40 and soil_moisture < 15 and temperature > 38:
            return "Extreme Drought: Government intervention, water rationing, and food aid necessary."
        elif rainfall > 200 and temperature < 25 and soil_moisture > 70:
            return "No Drought: Adequate rainfall and soil conditions. Monitor for waterlogging."
        elif temperature > 40 and water_availability < 30:
            return "High Heat Risk: Extreme temperatures may lead to drought conditions soon."
        else:
            return "No significant drought risk detected. Maintain regular water management."

    except ValueError:
        return "Invalid input! Please enter numeric values."

def save_to_csv(data):
    """Save user input and assessment result to a CSV file."""
    file_exists = os.path.isfile(CSV_FILE)
    
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Rainfall (mm)", "Soil Moisture (%)", "Temperature (°C)", "Water Availability (%)", "Assessment Result"])
        writer.writerow(data)

def evaluate_drought():
    """Get user input, assess drought risk, and save data."""
    rainfall = entry_rainfall.get()
    soil_moisture = entry_soil.get()
    temperature = entry_temp.get()
    water_availability = entry_water.get()

    result = assess_drought(rainfall, soil_moisture, temperature, water_availability)
    save_to_csv([rainfall, soil_moisture, temperature, water_availability, result])

    # Display result in messagebox and result label
    messagebox.showinfo("Drought Assessment Result", result)
    result_label.config(text=f"Result: {result}", fg="darkred")

def display_saved_data():
    """Display the saved drought data in a new window."""
    if not os.path.isfile(CSV_FILE):
        messagebox.showinfo("No Data", "No data available. Please assess drought first.")
        return

    # Create a new window for displaying data
    data_window = tk.Toplevel(root)
    data_window.title("Saved Drought Data")
    data_window.geometry("700x400")
    data_window.configure(bg="skyblue")

    # Table for displaying data
    tree = ttk.Treeview(data_window)
    tree["columns"] = ("Rainfall", "Soil Moisture", "Temperature", "Water Availability", "Result")
    tree.heading("#0", text="ID")
    tree.column("#0", width=50)
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    # Read CSV and display rows
    with open(CSV_FILE, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for i, row in enumerate(reader, 1):
            tree.insert("", "end", text=i, values=row)

    tree.pack(fill="both", expand=True)

# Main Tkinter window
root = tk.Tk()
root.title("Drought Risk Assessment System")
root.geometry("500x600")
root.configure(bg="skyblue")

# Title label
tk.Label(root, text="Drought Risk Assessment", font=("Arial", 20, "bold"), bg="skyblue").pack(pady=10)

# Input fields
tk.Label(root, text="Rainfall (mm):", bg="skyblue").pack()
entry_rainfall = tk.Entry(root)
entry_rainfall.pack()

tk.Label(root, text="Soil Moisture (%):", bg="skyblue").pack()
entry_soil = tk.Entry(root)
entry_soil.pack()

tk.Label(root, text="Temperature (°C):", bg="skyblue").pack()
entry_temp = tk.Entry(root)
entry_temp.pack()

tk.Label(root, text="Water Availability (%):", bg="skyblue").pack()
entry_water = tk.Entry(root)
entry_water.pack()

# Buttons
tk.Button(root, text="Assess Drought", command=evaluate_drought, bg="green", fg="white").pack(pady=5)
tk.Button(root, text="View Saved Data", command=display_saved_data, bg="blue", fg="white").pack(pady=5)

# Result display
result_label = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="skyblue")
result_label.pack(pady=10)

# Run the main loop
root.mainloop()