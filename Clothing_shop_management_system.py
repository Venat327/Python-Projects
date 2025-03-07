import pandas as pd
import os
# Define the file path for the inventory data
EXCEL_FILE = "shop_data.xlsx"
# Check if the file exists, if not, create it with some columns (Item, Category, Price, Quantity)
if not os.path.exists(EXCEL_FILE):
    # Create a new empty DataFrame with the required columns
    df = pd.DataFrame(columns=["Item", "Category", "Price", "Quantity"])
    # Save this empty DataFrame to the Excel file
    df.to_excel(EXCEL_FILE, index=False)
else:
    # If the file already exists, we load the existing data into the DataFrame
    df = pd.read_excel(EXCEL_FILE)
# A dictionary to define discount percentages based on item categories
DISCOUNTS = {"ladies": 10, "kids": 15}  # 10% off for 'ladies', 15% off for 'kids'
# Function to load the data from the Excel file
def load_data():
    # Load the data from the Excel file into a DataFrame
    return pd.read_excel(EXCEL_FILE)
# Function to save the updated data to the Excel file
def save_data(df):
    # Write the DataFrame (df) back into the Excel file
    df.to_excel(EXCEL_FILE, index=False)
# Function to add a new item to the inventory
def add_item():
    # Load the current inventory data into df
    df = load_data()
    # Ask the user for details about the new item
    item = input("Enter item name: ")
    category = input("Enter category (men/ladies/kids): ").lower()
    price = float(input("Enter price: "))
    quantity = int(input("Enter quantity: "))
    # Add the new item to the DataFrame
    new_item = {"Item": item, "Category": category, "Price": price, "Quantity": quantity}
    df = df.append(new_item, ignore_index=True)
    # Save the updated DataFrame back to the Excel file
    save_data(df)
    print(f"{item} added successfully!\n")
# Function to view the current inventory
def view_inventory():
    # Load the current inventory data into df
    df = load_data()
    # If the DataFrame is empty, print a message saying no items are in the inventory
    if df.empty:
        print("No items in inventory.\n")
    else:
        # Otherwise, print the entire inventory
        print("\nInventory:")
        print(df)
        print()
# Function to update an existing item in the inventory
def update_item():
    # Load the current inventory data into df
    df = load_data()
    # Show the current inventory
    view_inventory()
    # Ask the user for the item they want to update
    item = input("Enter item name to update: ")
    # Check if the item exists in the inventory
    if item in df["Item"].values:
        # If the item exists, ask the user for new price and quantity
        new_price = float(input("Enter new price: "))
        new_quantity = int(input("Enter new quantity: "))
        # Update the price and quantity of the item
        df.loc[df["Item"] == item, ["Price", "Quantity"]] = [new_price, new_quantity]
        # Save the updated inventory back to the Excel file
        save_data(df)
        print(f"{item} updated successfully!\n")
    else:
        print("Item not found.\n")
# Function to delete an item from the inventory
def delete_item():
    # Load the current inventory data into df
    df = load_data()
    # Show the current inventory
    view_inventory()
    # Ask the user for the item they want to delete
    item = input("Enter item name to delete: ")
    # Check if the item exists in the inventory
    if item in df["Item"].values:
        # If the item exists, remove it from the DataFrame
        df = df[df["Item"] != item]
        # Save the updated inventory back to the Excel file
        save_data(df)
        print(f"{item} deleted successfully!\n")
    else:
        print("Item not found.\n")
# Function to generate a bill for a customer
def generate_bill():
    # Load the current inventory data into df
    df = load_data()
    # Initialize total bill amount and a list to store purchased items
    total = 0
    bill_items = []
    # Loop to let the user buy items until they type 'done'
    while True:
        # Show the current inventory
        view_inventory()
        # Ask the user for the item they want to buy
        item = input("Enter item name to buy (or type 'done' to finish): ").lower()
        # If the user types 'done', break out of the loop
        if item == "done":
            break
        # Check if the item exists in the inventory
        if item in df["Item"].values:
            # If the item exists, get the details (price, available quantity, category)
            row = df[df["Item"] == item]
            available_quantity = int(row["Quantity"].values[0])
            price = float(row["Price"].values[0])
            category = row["Category"].values[0]
            # Ask the user how many of the item they want to buy
            quantity = int(input(f"Enter quantity (Available: {available_quantity}): "))
            # Check if there's enough stock
            if quantity > available_quantity:
                print("Not enough stock available.\n")
                continue
            # Calculate the discounted price based on the category
            discount = DISCOUNTS.get(category, 0)  # Get the discount for the category (default is 0 if not found)
            discounted_price = price - (price * discount / 100)
            # Add the item's cost to the total bill
            total += discounted_price * quantity
            # Add the item details to the bill items list
            bill_items.append(f"{item} (x{quantity}) - ${discounted_price:.2f} each")
            # Update the quantity in the inventory (subtract the bought items)
            df.loc[df["Item"] == item, "Quantity"] -= quantity
        else:
            print("Item not found.\n")
    # Save the updated inventory after the purchase
    save_data(df)
    # Print the bill summary
    print("\n===== Bill Summary =====")
    for b_item in bill_items:
        print(b_item)
    print(f"Total Amount: ${total:.2f}\n")
# Main program loop
while True:
    # Display the menu options
    print("\n========= Clothing Shop Management =========")
    print("1. Add Item")
    print("2. View Inventory")
    print("3. Update Item")
    print("4. Delete Item")
    print("5. Generate Bill")
    print("6. Exit")
    # Ask the user to choose an option
    choice = input("Enter your choice: ")
    # Call the corresponding function based on the user's choice
    if choice == '1':
        add_item()
    elif choice == '2':
        view_inventory()
    elif choice == '3':
        update_item()
    elif choice == '4':
        delete_item()
    elif choice == '5':
        generate_bill()
    elif choice == '6':
        print("Exiting... Thank you for using the Clothing Shop Management System!")
        break
    else:
        print("Invalid choice. Try again.\n")