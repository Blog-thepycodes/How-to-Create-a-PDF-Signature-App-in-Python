import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk




def add_signature(input_pdf: str, output_pdf: str, image_path: str,
                 x: int, y: int, width: int, height: int, pages: tuple = None):
   pdf = fitz.open(input_pdf)
   for page_num in range(pdf.page_count):
       if pages and (page_num + 1) not in pages:
           continue
       page = pdf[page_num]
       rect = fitz.Rect(x, y, x + width, y + height)
       page.insert_image(rect, filename=image_path)
   pdf.save(output_pdf)
   pdf.close()




def browse_pdf():
   file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
   if file_path:
       pdf_path_entry.delete(0, tk.END)
       pdf_path_entry.insert(0, file_path)




def browse_image():
   file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg")])
   if file_path:
       img_path_entry.delete(0, tk.END)
       img_path_entry.insert(0, file_path)
       update_preview(file_path)




def browse_output():
   file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
   if file_path:
       output_path_entry.delete(0, tk.END)
       output_path_entry.insert(0, file_path)




def sign_pdf():
   input_pdf = pdf_path_entry.get()
   image_path = img_path_entry.get()
   output_pdf = output_path_entry.get() or (input_pdf.replace(".pdf", "_signed.pdf"))
   try:
       x = int(x_coord_entry.get())
       y = int(y_coord_entry.get())
       width = int(width_entry.get())
       height = int(height_entry.get())


       # Determine pages based on the selected option
       if page_option.get() == "all":
           pages = None  # Sign all pages
       elif page_option.get() == "range":
           start, end = map(int, page_range_entry.get().split("-"))
           pages = tuple(range(start, end + 1))
       elif page_option.get() == "specific":
           pages = tuple(map(int, specific_pages_entry.get().split(",")))
       else:
           pages = None


       add_signature(input_pdf, output_pdf, image_path, x, y, width, height, pages)
       messagebox.showinfo("Success", f"Signed PDF saved as {output_pdf}")
   except Exception as e:
       messagebox.showerror("Error", f"Failed to sign PDF: {e}")




def update_preview(image_path):
   try:
       img = Image.open(image_path)
       img.thumbnail((200, 200))  # Adjust preview size
       img_preview = ImageTk.PhotoImage(img)
       preview_label.config(image=img_preview)
       preview_label.image = img_preview
   except Exception as e:
       messagebox.showerror("Error", f"Failed to load preview: {e}")




def drag_and_drop(event):
   file_path = event.data.strip('{}')  # Handle spaces in paths
   if file_path.endswith(".pdf"):
       pdf_path_entry.delete(0, tk.END)
       pdf_path_entry.insert(0, file_path)
   elif file_path.endswith((".png", ".jpg")):
       img_path_entry.delete(0, tk.END)
       img_path_entry.insert(0, file_path)
       update_preview(file_path)




# Initialize the TkinterDnD window
root = TkinterDnD.Tk()
root.title("PDF Signature Tool - The Pycodes")
root.geometry("500x700")


# Instructions Label
tk.Label(root, text="Drag and Drop PDF/Image or use Browse Buttons", font=("Arial", 12, "bold")).pack(pady=10)


# PDF File Selection
tk.Label(root, text="Select PDF File").pack()
pdf_path_entry = tk.Entry(root, width=60)
pdf_path_entry.pack(pady=5)
tk.Button(root, text="Browse PDF", command=browse_pdf).pack()


# Image Selection and Preview
tk.Label(root, text="Select Signature Image").pack()
img_path_entry = tk.Entry(root, width=60)
img_path_entry.pack(pady=5)
tk.Button(root, text="Browse Image", command=browse_image).pack()


preview_label = tk.Label(root, text="Signature Preview will appear here", relief="sunken", width=20, height=10)
preview_label.pack(pady=10)


# Coordinates and Size
coord_frame = tk.Frame(root)
coord_frame.pack(pady=5)


tk.Label(coord_frame, text="X Coordinate").grid(row=0, column=0)
x_coord_entry = tk.Entry(coord_frame, width=10)
x_coord_entry.grid(row=0, column=1, padx=5)


tk.Label(coord_frame, text="Y Coordinate").grid(row=0, column=2)
y_coord_entry = tk.Entry(coord_frame, width=10)
y_coord_entry.grid(row=0, column=3, padx=5)


tk.Label(coord_frame, text="Width").grid(row=1, column=0)
width_entry = tk.Entry(coord_frame, width=10)
width_entry.grid(row=1, column=1, padx=5)


tk.Label(coord_frame, text="Height").grid(row=1, column=2)
height_entry = tk.Entry(coord_frame, width=10)
height_entry.grid(row=1, column=3, padx=5)


# Page Selection Options
tk.Label(root, text="Select Pages to Sign").pack(pady=5)
page_option = tk.StringVar(value="all")


all_pages_rb = tk.Radiobutton(root, text="All Pages", variable=page_option, value="all")
all_pages_rb.pack()


range_pages_rb = tk.Radiobutton(root, text="Range (e.g., 1-5)", variable=page_option, value="range")
range_pages_rb.pack()


page_range_entry = tk.Entry(root, width=20, state="normal")
page_range_entry.pack(pady=5)


specific_pages_rb = tk.Radiobutton(root, text="Specific Pages (e.g., 1,3,5)", variable=page_option, value="specific")
specific_pages_rb.pack()


specific_pages_entry = tk.Entry(root, width=20, state="normal")
specific_pages_entry.pack(pady=5)


# Output Path Selection
tk.Label(root, text="Output PDF Path").pack()
output_path_entry = tk.Entry(root, width=60)
output_path_entry.pack(pady=5)
tk.Button(root, text="Browse Output Path", command=browse_output).pack()


# Sign Button
sign_button = tk.Button(root, text="Sign PDF", command=sign_pdf, bg="blue", fg="white")
sign_button.pack(pady=20)


# Drag-and-Drop bindings
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drag_and_drop)


# Run the Tkinter event loop
root.mainloop()
