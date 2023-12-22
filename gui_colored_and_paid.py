from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, ttk, Canvas, Entry, Text, Button, PhotoImage, Label, Frame, Scrollbar
from tkinter import PanedWindow, Toplevel, messagebox, Scale
import tkinter as tk
import tkinter.font as tkFont
from collections import Counter
from PIL import Image, ImageTk

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
output_file = "output2.txt" # can choose output txt file here !

total=0
service_scale = None 

def reload():
    global total
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
def pay():
    p_window = Toplevel(window)
    p_window.geometry(f"+{window.winfo_x() + window.winfo_width()}+{window.winfo_y()}")
    
    amount_paid_label = Label(p_window, text="Amount Paid:", font=("Comic Sans MS", 12))
    amount_paid_label.pack(anchor='w')

    amount_paid_entry = Entry(p_window, font=("Comic Sans MS", 12))
    amount_paid_entry.pack()

    calculate_change_button = tk.Button(
        p_window,
        text="Paid !",
        font=("Comic Sans MS", 12),  # Updated font
        command=lambda: calculate_change(amount_paid_entry.get(), p_window)
    )
    calculate_change_button.pack()

def calculate_change(amount_paid, p_window):
    try:
        global total
        amount_paid = float(amount_paid)
        change = amount_paid - total

        if change < 0:
            tk.messagebox.showwarning("Insufficient Payment!", "The amount paid is not enough.")
            change_label = tk.Label(p_window, text="Insufficient Payment!", font=("Comic Sans MS", 14))
            change_label.pack(anchor='w')

        else:
            change_label = tk.Label(p_window, text=f"Give back: ${change:.2f}", font=("Comic Sans MS", 14))
            change_label.pack(anchor='w')

            rt_score = tk.IntVar()
            rt_score.set(0)

            def show_score(v):
                service_rating_label.config(text=f"Service Rating: {rt_score.get()}/10")

            def show_image(event=None):
                original_image = Image.open(relative_to_assets("thanku.png"))
                resized_image = original_image.resize((150, 150))
                tk_img = ImageTk.PhotoImage(resized_image)
                label_thanku = tk.Label(p_window, image=tk_img, width=130, height=130, anchor='center')
                label_thanku.image = tk_img  # Keep a reference to the image
                label_thanku.pack()

                exit_button = tk.Button(p_window, text="Exit", command=p_window.destroy, font=("Comic Sans MS", 12))
                exit_button.pack()

            service_scale = Scale(p_window, from_=0, to=10, orient=tk.HORIZONTAL, length=200, variable=rt_score, command=show_score)
            service_scale.pack()
            service_scale.bind("<ButtonRelease-1>", show_image)  # Use "<ButtonRelease-1>" for the left mouse button

            service_rating_label = tk.Label(p_window, text=f"Service Rating: {rt_score.get()}/10", font=("Comic Sans MS", 12))
            service_rating_label.pack(anchor='w')

    except ValueError:
        tk.messagebox.showerror("Invalid Input", "Please enter a valid amount.")
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

window.resizable(False, False)
window.mainloop()
