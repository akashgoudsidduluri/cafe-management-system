# ☕ Café Management System (Python CLI)

A clean, beginner-friendly **command-line Café Management System** built using Python.  
Place orders, generate bills, save them, and visualize sales — all from the terminal.

---

## ✨ Features

✔ Interactive ordering system  
✔ Input validation  
✔ Auto-calculated totals  
✔ Beautiful bill formatting with **PrettyTable**  
✔ Save bills to `cafe_bill.txt`  
✔ Sales chart using **Matplotlib**  
✔ Simple & readable OOP design  

---

## 🧩 Technologies Used
- **Python 3**
- **PrettyTable**
- **Matplotlib**

---

## 📦 Install Dependencies

pip install prettytable matplotlib

▶️ Run the Program
python cafe_management.py

🧾 Program Menu
![Main Menu](menu.PNG)

📄 Bill Example
![Bill](bill.PNG)

📊 Sales Visualization
![Visualization](visualization.PNG)

🧩 Usage Flow
When you run the program, you will see:

markdown
Copy code
1. Place Order
2. Generate Bill
3. Save Bill to File
4. Visualize Sales
5. Exit
1️⃣ Place Order
Enter:

Item number

Quantity

Enter 0 to stop ordering.

2️⃣ Generate Bill
Displays a formatted itemized bill with totals.

3️⃣ Save Bill to File
Creates:

Copy code
cafe_bill.txt
4️⃣ Visualize Sales
Displays a bar chart of ordered items.

5️⃣ Exit
Closes the program.

mathematica
Copy code
+-------------+----------+-----------+-----------+
| Item Name   | Quantity | Price (₹) | Total (₹) |
+-------------+----------+-----------+-----------+
| Coffee      |    2     |    50     |    100    |
| Sandwich    |    6     |   100     |    600    |
| Cold Coffee |    5     |    90     |    450    |
+-------------+----------+-----------+-----------+
Total Amount: ₹1780
⚠ Limitations
Orders reset each run

Menu is static

No database storage

CLI based

🚀 Future Enhancements
GST / discounts

Remove / edit orders

Customer info

Persistent storage (CSV / DB)

GUI / Web version

📄 License
Free to use and modify.
