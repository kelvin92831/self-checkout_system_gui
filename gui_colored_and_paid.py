from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, ttk, Canvas, Entry, Text, Button, PhotoImage, Label, Frame, Scrollbar
from tkinter import PanedWindow, Toplevel, messagebox
import tkinter as tk
import tkinter.font as tkFont
from collections import Counter

OUTPUT_PATH = Path(__file__).parent
print(OUTPUT_PATH)
ASSETS_PATH = OUTPUT_PATH / "assets/frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


item_data = {
    "donat": {"name": "甜甜圈", "price": 20},
    "grape": {"name": "葡萄乾麵包", "price": 40},
    "square": {"name": "大理石磚麵包", "price": 50},
    "strawberry": {"name": "草莓麵包", "price": 25},
    "pudding": {"name": "布丁麵包", "price": 25},
    "meat_floss": {"name": "肉鬆麵包", "price": 30},
    "pizza": {"name": "披薩麵包", "price": 40},
    "matcha": {"name": "抹茶麵包", "price": 35},
    "sugar": {"name": "糖霜麵包", "price": 30},
    "strawberry_donat": {"name": "草莓甜甜圈", "price": 30},
    "black_eye": {"name": "黑岩豆豆麵包", "price": 35},

}

# item_num = 5
output_file = r"C:\Users\安\Desktop\self-checkout_system_gui-main\output2.txt" # can choose output txt file here !

def reload():
    try:
        for i in list(item_data.keys()):
            canvas.delete(f"item_text_{i}")
        canvas.delete("items_n")
        canvas.delete("total")        

        with open(output_file, "r") as file:
            lines = file.readlines()
            item_ids = [line.split()[0] for line in lines]

            # 使用 Counter 計算每個 ID 的出現次數
            id_counts = Counter(item_ids)
            cnt=0
            total=0
            for item_id, count in id_counts.items():
                cnt+=1
                # 取得字典中對應的項目資料
                item_info = item_data.get(item_id, {"name": "Unknown", "price": "N/A"})
                
                # 格式化要顯示的文字
                text_content = [f"{item_info['name']}", f"*{count}", f"$ {item_info['price']*count}"]
                total += item_info['price'] * count

                # 清除先前的文字
                scroll_canvas.delete(f"item_text_{item_id}")
 
                # 在 Canvas 上顯示文字
                
                offsets = [30, 170, 250]
                for el in range(3):
                    scroll_canvas.create_text(
                        offsets[el], cnt * 30,  # 位置 (x, y)，每個項目間隔 50 個像素
                        anchor="nw",
                        text=text_content[el],
                        fill="#000000",
                        font=("Comic Sans MS", 15),
                        tag=f"item_text_{item_id}"  # 使用 tag 以便稍後清除
                    )
            scroll_canvas.configure(scrollregion = scroll_canvas.bbox("all"))
                
            canvas.create_text(
                255.0,
                271.0,
                anchor="nw",
                text=f"{len(item_ids)} items",
                fill="#000000",
                font=("Comic Sans MS", 20 * -1),
                tags="items_n"
            )
            canvas.create_text(
                425.0,
                77.0,
                anchor="nw",
                text=f"$ {total}",
                fill="#000000",
                font=("Comic Sans MS", 32 * -1),
                tags="total"
            )
                

    except FileNotFoundError:
        # 清除先前的文字
        canvas.delete("item_text")
        
        # 在 Canvas 上顯示錯誤訊息
        canvas.create_text(
            10, 10,  # 位置 (x, y)
            anchor="nw",
            text="File not found",
            fill="#000000",
            font=("Comic Sans MS", 24),
            tag="item_text"  # 使用 tag 以便稍後清除
        )

#####################
sel_price=0

def pay(): 
   
    global sel_price
    sel_price = 0  # Reset sel_price

    # Create a new Toplevel window for checkboxes
    checkbox_window = Toplevel(window)   
    checkbox_window.geometry(f"+{window.winfo_x() + window.winfo_width()}+{window.winfo_y()-50}")

    # Iterate through item_data and create checkboxes
    for item_id, item_info in item_data.items():
        var = tk.IntVar()
        checkbox = tk.Checkbutton(
            checkbox_window,
            text=item_info["name"],
            variable=var,
            command=lambda i=item_id, v=var: on_checkbox_toggle(i, v)
        )
        checkbox.pack(anchor=tk.W, pady=2)
        checkboxes[item_id] = {"checkbox": checkbox, "var": var}

    # Create an Entry widget for the amount paid
    amount_paid_label = tk.Label(checkbox_window, text="You Paid:")
    amount_paid_label.pack()
    amount_paid_entry = Entry(checkbox_window)
    amount_paid_entry.pack()

    # Button to calculate change
    calculate_change_button = tk.Button(
        checkbox_window,
        text="paid!",
        command=lambda: calculate_change(amount_paid_entry.get(), checkbox_window)
    )
    calculate_change_button.pack()

def on_checkbox_toggle(item_id, var):
    global sel_price
    item_info = item_data.get(item_id, {"name": "Unknown", "price": 0})

    # Calculate the updated total price based on the checkboxes
    sel_price = sum(item_data[item_id]["price"] for item_id, data in checkboxes.items() if data["var"].get())

    # Display the updated total price
    update_total_price()


# update the total price on the canvas
def update_total_price():
    canvas.delete("total")  # Clear previous total price
    canvas.create_text(
        425.0,
        77.0,
        anchor="nw",
        text=f"$ {sel_price}",
        fill="#000000",
        font=("Comic Sans MS", 32 * -1),
        tags="total"
    )

def calculate_change(amount_paid, checkbox_window):
    try:
        amount_paid = float(amount_paid)
        change = amount_paid - sel_price

        if change >= 0:
            change_label = tk.Label(checkbox_window, text=f"Give back: ${change:.2f}")
            change_label.pack()
        else:
            tk.messagebox.showwarning("Insufficient Payment!", "The amount paid is not enough.")
            change_label = tk.Label(checkbox_window, text="Insufficient Payment!")
            change_label.pack()

        exit_button = tk.Button(checkbox_window, text="Exit", command=checkbox_window.destroy)
        exit_button.pack()

    except ValueError:
        tk.messagebox.showerror("Error", "Invalid input for Amount Paid. Please enter a valid number.")

#######################

window = Tk()
window.geometry("532x314")
window.configure(bg ="#FDFDBD") 

canvas = Canvas(
    window,
    bg = "#ADD1FC",
    height = 314,
    width = 532,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge",
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    532.0,
    314.0,
    fill="#DFF4F3",
    outline="")

canvas.create_rectangle(
    0.0,
    0.0,
    532.0,
    43.0,
    fill="#EDB1F1",
    outline="")

canvas.create_rectangle( 
    340.0,
    49.0,
    523.0,
    131.0,
    fill="#CBBCF6",
    outline="")

canvas.create_text(
    18.0,
    11.0,
    anchor="nw",
    text="Self-checkout System",
    fill="#000000",
    font=("Comic Sans MS", 20 * -1)
)

canvas.create_text(
    27.0,
    58.0,
    anchor="nw",
    text="Item:",
    fill="#000000",
    font=("Comic Sans MS", 20 * -1)
)

canvas.create_text(
    354.0,
    58.0,
    anchor="nw",
    text="Total:",
    fill="#000000",
    font=("Comic Sans MS", 20 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    #image=button_image_1,
    text="pay",
    bg = "#E9B2BC",
    borderwidth=0,
    font=("Comic Sans MS", int(16.0)),
    highlightthickness=0,
    #command=lambda: print("button_1 clicked"),
    command=pay,
    relief="flat"
)
button_1.place(
    x=440.0,
    y=265.0,
    width=82.71424865722656,
    height=35.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    #image=button_image_2,
    text="reload",
    bg = "#E9B2BC",
    font=("Comic Sans MS", int(16.0)),
    borderwidth=0,
    highlightthickness=0,
    command=lambda: reload(),
    relief="flat"
)
button_2.place(
    x=347.0,
    y=265.0,
    width=82.71424865722656,
    height=35.0
)

canvas.create_rectangle( #line
    7.0,
    262.4906397712401,
    330.99843223643694,
    265.5093504925284,
    fill="#000000",
    outline="")

_canvas = Canvas(
    window,
    bg = "#B5DEFF",
    height = 205,
    width = 324,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
_canvas.place(x = 8, y = 49)
scroll_frame = Frame(_canvas, bg = "#ffffff")
scroll_frame.pack()
scroll_canvas = Canvas(
    scroll_frame,
    bg = "#CBBCF6",
    height = 205,
    width = 324,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge",
    scrollregion=(0,0,0,0)
)
scrollY = Scrollbar(scroll_frame, orient='vertical')
scrollY.pack(side='right', fill='y')
scrollY.config(command=scroll_canvas.yview)
scroll_canvas.config(yscrollcommand=scrollY.set)
scroll_canvas.pack()

################
checkbox_panedwindow = PanedWindow(window, orient=tk.VERTICAL)
checkboxes = {}

for idx, (item_id, item_info) in enumerate(item_data.items()):
    var = tk.IntVar()
    checkbox = tk.Checkbutton(
        checkbox_panedwindow,
        text=item_info["name"],
        command=lambda i=item_id, v=var: on_checkbox_toggle(i, v)
    )
    checkbox.pack()
    checkboxes[item_id] = {"checkbox": checkbox, "var": var, "count": 0}
##################

window.resizable(False, False)
window.mainloop()
