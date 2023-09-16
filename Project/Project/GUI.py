import tkinter as tk

root = tk.Tk()

output_area = tk.Text(root, height=10, width=50)
output_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_area.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=output_area.yview)

output_area.insert(tk.END, "Hello, world!")

root.mainloop()