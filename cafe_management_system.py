import os
import json
import logging
from datetime import datetime
from prettytable import PrettyTable
import matplotlib.pyplot as plt

DEFAULT_MENU = {
    1: {"name": "Coffee", "price": 50},
    2: {"name": "Tea", "price": 30},
    3: {"name": "Sandwich", "price": 100},
    4: {"name": "Cake", "price": 80},
}


def safe_int(prompt, allow_zero=False):
    try:
        value = int(input(prompt))
        if not allow_zero and value <= 0:
            raise ValueError
        return value
    except ValueError:
        return None


class CafeManagementSystem:
    def __init__(self, data_path=None):
        self.data_path = data_path or os.path.join(os.getcwd(), "cafe_data.json")
        self.menu = {}
        self.orders = []
        self._load_data()

    def _load_data(self):
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.menu = {int(k): v for k, v in data.get("menu", {}).items()} if data else {}
            except Exception:
                logging.warning("Could not read data file; falling back to default menu.")
                self.menu = DEFAULT_MENU.copy()
        else:
            self.menu = DEFAULT_MENU.copy()

    def _save_data(self):
        data = {"menu": {str(k): v for k, v in self.menu.items()}}
        os.makedirs(os.path.dirname(self.data_path) or ".", exist_ok=True)
        try:
            with open(self.data_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logging.error("Failed to save data: %s", e)

    def display_menu(self):
        table = PrettyTable()
        table.field_names = ["Item No.", "Item Name", "Price (₹)"]
        for item_id, details in sorted(self.menu.items()):
            table.add_row([item_id, details["name"], details["price"]])
        print("\n--- Menu ---")
        print(table)

    def add_menu_item(self):
        name = input("Item name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        price = safe_int("Price (integer): ")
        if price is None:
            print("Invalid price.")
            return
        next_id = max(self.menu.keys(), default=0) + 1
        self.menu[next_id] = {"name": name, "price": price}
        self._save_data()
        print(f"Added {name} (#{next_id}) for ₹{price}.")

    def update_menu_item(self):
        self.display_menu()
        item_no = safe_int("Enter item number to update: ")
        if item_no is None or item_no not in self.menu:
            print("Invalid item number.")
            return
        name = input(f"New name (leave blank to keep '{self.menu[item_no]['name']}'): ").strip()
        price = input(f"New price (leave blank to keep {self.menu[item_no]['price']}): ").strip()
        if name:
            self.menu[item_no]["name"] = name
        if price:
            try:
                p = int(price)
                self.menu[item_no]["price"] = p
            except ValueError:
                print("Invalid price; keeping old value.")
        self._save_data()
        print("Menu updated.")

    def remove_menu_item(self):
        self.display_menu()
        item_no = safe_int("Enter item number to remove: ")
        if item_no is None or item_no not in self.menu:
            print("Invalid item number.")
            return
        removed = self.menu.pop(item_no)
        self._save_data()
        print(f"Removed {removed['name']}.")

    def take_order(self):
        self.display_menu()
        while True:
            order_id = safe_int("Enter the item number to order (or 0 to finish): ", allow_zero=True)
            if order_id is None:
                print("Please enter a valid integer (0 to finish).")
                continue
            if order_id == 0:
                break
            if order_id not in self.menu:
                print("Invalid item number.")
                continue
            quantity = safe_int(f"Enter quantity for {self.menu[order_id]['name']}: ")
            if quantity is None:
                print("Invalid quantity.")
                continue
            self.orders.append({"item": self.menu[order_id], "quantity": quantity})
            print(f"Added {quantity} x {self.menu[order_id]['name']}")

    def calculate_total(self):
        return sum(order["item"]["price"] * order["quantity"] for order in self.orders)

    def generate_bill(self, print_only=True):
        if not self.orders:
            print("\nNo orders placed!")
            return None
        table = PrettyTable()
        table.field_names = ["Item Name", "Quantity", "Price (₹)", "Total (₹)"]
        total = 0
        for order in self.orders:
            item_total = order["item"]["price"] * order["quantity"]
            total += item_total
            table.add_row([order["item"]["name"], order["quantity"], order["item"]["price"], item_total])
        if print_only:
            print("\n--- Bill ---")
            print(table)
            print(f"Total Amount: ₹{total}")
        return {"table": table, "total": total}

    def save_bill_to_file(self, directory="."):
        bill = self.generate_bill(print_only=False)
        if bill is None:
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(directory, f"cafe_bill_{timestamp}.txt")
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("--- Bill ---\n")
                for order in self.orders:
                    item_total = order["item"]["price"] * order["quantity"]
                    f.write(f"{order['item']['name']} x {order['quantity']} = ₹{item_total}\n")
                f.write(f"Total Amount: ₹{bill['total']}\n")
            print(f"Bill saved to '{filename}'")
        except Exception as e:
            print(f"Error saving file: {e}")

    def visualize_sales(self):
        if not self.orders:
            print("\nNo orders placed to visualize!")
            return
        # aggregate quantities per item name
        agg = {}
        for order in self.orders:
            name = order["item"]["name"]
            agg[name] = agg.get(name, 0) + order["quantity"]
        names = list(agg.keys())
        quantities = list(agg.values())
        plt.bar(names, quantities, color="skyblue")
        plt.title("Café Sales Visualization")
        plt.xlabel("Items")
        plt.ylabel("Quantities Ordered")
        plt.tight_layout()
        plt.show()

    def manage_menu_interactive(self):
        while True:
            print("\nMenu Management:\n1. View Menu\n2. Add Item\n3. Update Item\n4. Remove Item\n5. Back")
            choice = safe_int("Choose: ", allow_zero=True)
            if choice == 1:
                self.display_menu()
            elif choice == 2:
                self.add_menu_item()
            elif choice == 3:
                self.update_menu_item()
            elif choice == 4:
                self.remove_menu_item()
            elif choice == 5 or choice == 0:
                break
            else:
                print("Invalid choice.")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Cafe Management System")
    parser.add_argument("--data", help="path to data file (JSON)", default=None)
    args = parser.parse_args()

    system = CafeManagementSystem(data_path=args.data)

    print("\nWelcome to the Café Management System!")
    while True:
        print("\n1. Place Order\n2. Generate Bill\n3. Save Bill to File\n4. Visualize Sales\n5. Manage Menu\n6. Exit")
        choice = safe_int("Enter your choice: ", allow_zero=True)
        if choice is None:
            print("Please enter a valid number.")
            continue
        if choice == 1:
            system.take_order()
        elif choice == 2:
            system.generate_bill()
        elif choice == 3:
            system.save_bill_to_file()
        elif choice == 4:
            system.visualize_sales()
        elif choice == 5:
            system.manage_menu_interactive()
        elif choice == 6 or choice == 0:
            print("Thank you for using the Café Management System!")
            break
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
