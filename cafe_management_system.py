from prettytable import PrettyTable
import matplotlib.pyplot as plt
# Menu Data (stored in a dictionary)
menu = {
    1: {"name": "Coffee", "price": 50},
    2: {"name": "Tea", "price": 30},
    3: {"name": "Sandwich", "price": 100},
    4: {"name": "Cake", "price": 80},
}

# Class to handle the cafe management
class CafeManagementSystem:
    def __init__(self):
        self.orders = []

    def display_menu(self):
        table = PrettyTable()
        table.field_names = ["Item No.", "Item Name", "Price (₹)"]

        for item_id, details in menu.items():
            table.add_row([item_id, details["name"], details["price"]])

        print("\n--- Menu ---")
        print(table)

    def take_order(self):
        try:
            self.display_menu()
            order_id = int(input("\nEnter the item number to order (or 0 to finish): "))
            if order_id == 0:
                return False
            if order_id not in menu:
                raise ValueError("Invalid item number!")
            quantity = int(input(f"Enter quantity for {menu[order_id]['name']}: "))
            if quantity <= 0:
                raise ValueError("Quantity must be greater than 0!")
            self.orders.append({"item": menu[order_id], "quantity": quantity})
            print(f"Added {quantity} x {menu[order_id]['name']} to the order.")
            return True
        except ValueError as e:
            print(f"Error: {e}")
            return True

    def calculate_total(self):
        return sum(order["item"]["price"] * order["quantity"] for order in self.orders)

    def generate_bill(self):
        if not self.orders:
            print("\nNo orders placed!")
            return

        table = PrettyTable()
        table.field_names = ["Item Name", "Quantity", "Price (₹)", "Total (₹)"]

        total = 0
        for order in self.orders:
            item_total = order["item"]["price"] * order["quantity"]
            total += item_total
            table.add_row([order["item"]["name"], order["quantity"], order["item"]["price"], item_total])

        print("\n--- Bill ---")
        print(table)
        print(f"Total Amount: ₹{total}")

    def save_to_file(self):
        try:
            with open("cafe_bill.txt", "w") as file:
                file.write("--- Bill ---\n")
                for order in self.orders:
                    item_total = order["item"]["price"] * order["quantity"]
                    file.write(
                        f"{order['item']['name']} x {order['quantity']} = ₹{item_total}\n"
                    )
                file.write(f"Total Amount: ₹{self.calculate_total()}\n")
            print("\nBill saved to 'cafe_bill.txt'")
        except Exception as e:
            print(f"Error saving file: {e}")

    def visualize_sales(self):
        if not self.orders:
            print("\nNo orders placed to visualize!")
            return

        # Prepare data for visualization
        item_names = [order["item"]["name"] for order in self.orders]
        quantities = [order["quantity"] for order in self.orders]

        # Plotting the bar chart
        plt.bar(item_names, quantities, color="skyblue")
        plt.title("Café Sales Visualization")
        plt.xlabel("Items")
        plt.ylabel("Quantities Ordered")
        plt.show()


def choice():
    system = CafeManagementSystem()
    print("\nWelcome to the Café Management System!")
    while True:
        try:
            print("\n1. Place Order")
            print("2. Generate Bill")
            print("3. Save Bill to File")
            print("4. Visualize Sales")
            print("5. Exit")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                while system.take_order():
                    pass
            elif choice == 2:
                system.generate_bill()
            elif choice == 3:
                system.save_to_file()
            elif choice == 4:
                system.visualize_sales()
            elif choice == 5:
                print("Thank you for using the Café Management System!")
                break
            else:
                print("Invalid choice! Please try again.")
        except ValueError:
            print("Error: Please enter a valid number!")


# Run the system
choice()