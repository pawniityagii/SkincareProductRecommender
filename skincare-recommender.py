import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

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

root = tk.Tk()
root.title("Skincare Product Recommender")
root.state("zoomed")
root.configure(bg="#2e1a47")

ttk.Style().configure("TButton", font=("Helvetica", 12, "bold"), background="#5a3d7d", foreground="white")
ttk.Style().configure("TLabel", font=("Helvetica", 11), background="#2e1a47", foreground="white")
ttk.Style().configure("TEntry", font=("Helvetica", 11), fieldbackground="#44355b", foreground="white")
ttk.Style().configure("Treeview", background="#2e1a47", foreground="white", fieldbackground="#2e1a47")
ttk.Style().configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#5a3d7d", foreground="white")

title_label = ttk.Label(root, text="🌿 Skincare Product Recommender 🌸", font=("Helvetica", 16, "bold"), background="#2e1a47", foreground="#d8b5ff")
title_label.pack(pady=10)

ttk.Label(root, text="Select Your Skin Type:").pack(pady=5)
skin_type_var = tk.StringVar()
skin_types = ["Dry", "Oily", "Combination", "Acne-Prone", "Normal", "All"]
skin_type_menu = ttk.Combobox(root, textvariable=skin_type_var, values=skin_types, font=("Helvetica", 11))
skin_type_menu.pack(pady=5)

ttk.Label(root, text="Select Your Concern:").pack(pady=5)
concern_var = tk.StringVar()
concerns = ["Dryness", "Oiliness", "Acne", "Sun Protection", "Aging", "Brightening", "Exfoliation", "Hydration", "Pores", "Sensitive Skin"]
concern_menu = ttk.Combobox(root, textvariable=concern_var, values=concerns, font=("Helvetica", 11))
concern_menu.pack(pady=5)

ttk.Label(root, text="Enter Your Budget (INR):").pack(pady=5)
budget_var = tk.StringVar()
budget_entry = ttk.Entry(root, textvariable=budget_var, font=("Helvetica", 11))
budget_entry.pack(pady=5)

recommend_button = ttk.Button(root, text="Find Products", command=recommend_products)
recommend_button.pack(pady=10)

ttk.Label(root, text="Recommended Products:").pack(pady=5)
columns = ("Product", "Price")
results_frame = ttk.Treeview(root, columns=columns, show="headings", style="mystyle.Treeview")
for col in columns:
    results_frame.heading(col, text=col)
    results_frame.column(col, anchor="center", width=200)
results_frame.pack(pady=10, fill="both", expand=True)

root.mainloop()
