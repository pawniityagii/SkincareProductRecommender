import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from PIL import Image, ImageTk

# Load skincare products from CSV or use default data
try:
    df = pd.read_csv("skincare_products.csv")
except FileNotFoundError:
    df = pd.DataFrame({
        "Product": ["Hydrating Cleanser", "Oil-Free Moisturizer", "Acne Control Serum", "Sunscreen SPF 50"],
        "Skin Type": ["Dry", "Oily", "Combination", "All"],
        "Concern": ["Dryness", "Oiliness", "Acne", "Sun Protection"],
        "Price": [500, 700, 1200, 900]
    })

def recommend_products():
    skin_type = skin_type_var.get()
    concern = concern_var.get()
    budget = budget_var.get()
    
    if not skin_type or not concern or not budget:
        messagebox.showerror("Error", "Please fill in all fields")
        return
    
    try:
        budget = int(budget)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for budget")
        return
    
    filtered_df = df[(df["Skin Type"] == skin_type) | (df["Skin Type"] == "All")]
    filtered_df = filtered_df[filtered_df["Concern"] == concern]
    filtered_df = filtered_df[filtered_df["Price"] <= budget]
    
    results_frame.delete(*results_frame.get_children())
    if not filtered_df.empty:
        for _, row in filtered_df.iterrows():
            results_frame.insert("", "end", values=(row["Product"], row["Price"]))
    else:
        messagebox.showinfo("No Matches", "No products found in your budget.")

# Create main application window
root = tk.Tk()
root.title("Skincare Product Recommender")
root.geometry("800x600")

# Load and set background image
bg_image = Image.open("skin.jpg")  # Ensure you have a background image file
bg_image = bg_image.resize((800, 600), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Transparent frame to hold widgets
frame = tk.Frame(root, bg="white", bd=0, highlightthickness=0)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Title label
title_label = ttk.Label(frame, text="🌿 Skincare Product Recommender 🌸", font=("Helvetica", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Skin type selection
ttk.Label(frame, text="Select Your Skin Type:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
skin_type_var = tk.StringVar()
skin_types = ["Dry", "Oily", "Combination", "Acne-Prone", "Normal", "All"]
skin_type_menu = ttk.Combobox(frame, textvariable=skin_type_var, values=skin_types)
skin_type_menu.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

# Concern selection
ttk.Label(frame, text="Select Your Concern:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
concern_var = tk.StringVar()
concerns = ["Dryness", "Oiliness", "Acne", "Sun Protection", "Aging", "Brightening", "Exfoliation", "Hydration", "Pores", "Sensitive Skin"]
concern_menu = ttk.Combobox(frame, textvariable=concern_var, values=concerns)
concern_menu.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

# Budget entry
ttk.Label(frame, text="Enter Your Budget (INR):").grid(row=3, column=0, sticky="w", padx=10, pady=5)
budget_var = tk.StringVar()
budget_entry = ttk.Entry(frame, textvariable=budget_var)
budget_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

# Recommend button
recommend_button = ttk.Button(frame, text="Find Products", command=recommend_products)
recommend_button.grid(row=4, column=0, columnspan=2, pady=10)

# Recommended products label
ttk.Label(frame, text="Recommended Products:").grid(row=5, column=0, columnspan=2, pady=5)

# Results frame
columns = ("Product", "Price")
results_frame = ttk.Treeview(frame, columns=columns, show="headings")
for col in columns:
    results_frame.heading(col, text=col)
    results_frame.column(col, anchor="center", width=200)
results_frame.grid(row=6, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

# Start the main loop
root.mainloop()
