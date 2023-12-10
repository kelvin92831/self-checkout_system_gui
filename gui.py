from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label, Frame, Scrollbar
from collections import Counter
OUTPUT_PATH = Path(__file__).parent
print(OUTPUT_PATH)
ASSETS_PATH = OUTPUT_PATH / "assets/frame0"  #modifiled

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

item_data = {
    0: {"name": "strawberry", "price": 50},
    1: {"name": "berry", "price": 20},
    2: {"name": "apple", "price": 10},
    3: {"name": "banana", "price": 15},
    4: {"name": "cheery", "price": 20}
}

item_num = 5

def reload():
    try:
        for i in range(0, item_num):
            canvas.delete(f"item_text_{i}")
        canvas.delete("items_n")
        canvas.delete("total")        

        with open("output.txt", "r") as file:
            lines = file.readlines()
            item_ids = [line.split()[0] for line in lines]

            # 使用 Counter 計算每個 ID 的出現次數
            id_counts = Counter(item_ids)
            cnt=0
            total=0
            for item_id, count in id_counts.items():
                cnt+=1
                # 取得字典中對應的項目資料
                item_info = item_data.get(int(item_id), {"name": "Unknown", "price": "N/A"})
                
                # 格式化要顯示的文字
                text_content = [f"{item_info['name']}", f"*{count}", f"$ {item_info['price']*count}"]
                total += item_info['price'] * count

                # 清除先前的文字
                canvas.delete(f"item_text_{item_id}")
 
                # 在 Canvas 上顯示文字
                offsets = [30, 170, 250]
                for el in range(3):
                    canvas.create_text(
                        offsets[el], 70 + cnt * 30,  # 位置 (x, y)，每個項目間隔 50 個像素
                        anchor="nw",
                        text=text_content[el],
                        fill="#000000",
                        font=("Inter Bold", 16),
                        tag=f"item_text_{item_id}"  # 使用 tag 以便稍後清除
                    )

            canvas.create_text(
                255.0,
                271.0,
                anchor="nw",
                text=f"{len(item_ids)} items",
                fill="#000000",
                font=("Inter", 20 * -1),
                tags="items_n"
            )
            canvas.create_text(
                432.0,
                77.0,
                anchor="nw",
                text=f"$ {total}",
                fill="#000000",
                font=("Inter", 32 * -1),
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
            font=("Inter Bold", 24),
            tag="item_text"  # 使用 tag 以便稍後清除
        )




window = Tk()

window.geometry("532x314")
window.configure(bg = "#FFFFFF")

frame = Frame(window)
frame.pack(pady=10)

item_text = Label(frame, text="hello", font=("Inter Bold", 36))
item_text.pack()

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 314,
    width = 532,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    532.0,
    314.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    0.0,
    4.0,
    532.0,
    43.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    27.0,
    58.0,
    anchor="nw",
    text="Item:",
    fill="#000000",
    font=("Inter Bold", 20 * -1)
)

canvas.create_rectangle(
    8.0,
    49.0,
    331.0,
    304.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    340.0,
    49.0,
    523.0,
    131.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    18.0,
    11.0,
    anchor="nw",
    text="Self-checkout System",
    fill="#000000",
    font=("Inter SemiBold", 20 * -1)
)

canvas.create_text(
    354.0,
    58.0,
    anchor="nw",
    text="Total:",
    fill="#000000",
    font=("Inter Bold", 20 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
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
    image=button_image_2,
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



canvas.create_rectangle(
    7.0,
    262.4906397712401,
    330.99843223643694,
    265.5093504925284,
    fill="#000000",
    outline="")

window.resizable(False, False)
window.mainloop()
