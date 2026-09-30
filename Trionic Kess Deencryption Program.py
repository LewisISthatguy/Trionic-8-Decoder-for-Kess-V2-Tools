import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

def flip_16bit_words(data):
    """
    Swap every pair of bytes.

    Example:
        AA BB CC DD
    becomes:
        BB AA DD CC
    """

    if len(data) % 2 != 0:
        raise ValueError(
            "The selected file has an odd number of bytes.\n\n"
            "It cannot be cleanly processed as 16-bit words."
        )

    output = bytearray()

    for i in range(0, len(data), 2):
        output.extend(data[i:i + 2][::-1])

    return bytes(output)


def select_input():
    global input_file

    filename = filedialog.askopenfilename(
        title="Select BIN file",
        filetypes=[
            ("BIN files", "*.bin"),
            ("All files", "*.*")
        ]
    )

    if filename:
        input_file = Path(filename)

        input_label.config(
            text=f"Input:\n{input_file}"
        )

        status_label.config(
            text="BIN loaded. Choose where to save the converted file."
        )


def convert_and_save():
    if input_file is None:
        messagebox.showwarning(
            "No file selected",
            "Please select a BIN file first."
        )
        return

    try:
        original = input_file.read_bytes()

        converted = flip_16bit_words(original)
        
        if input_file.stem.endswith(" Bit Flip"):
            suggested_name = (
                input_file.stem[:-8].rstrip() + ".bin"
            )
        else:
            suggested_name = (
                input_file.stem + " Bit Flip.bin"
            )

        output_file = filedialog.asksaveasfilename(
            title="Save converted BIN",
            defaultextension=".bin",
            initialfile=suggested_name,
            filetypes=[
                ("BIN files", "*.bin"),
                ("All files", "*.*")
            ]
        )

        if not output_file:
            status_label.config(
                text="Save cancelled."
            )
            return

        output_file = Path(output_file)

        if output_file.resolve() == input_file.resolve():
            overwrite = messagebox.askyesno(
                "Overwrite original?",
                "You're trying to overwrite the original BIN.\n\n"
                "Are you sure you want to do this?"
            )

            if not overwrite:
                status_label.config(
                    text="Save cancelled."
                )
                return

        output_file.write_bytes(converted)

        status_label.config(
            text=f"Done! Saved:\n{output_file}"
        )

        messagebox.showinfo(
            "Conversion complete",
            f"16-bit word swap complete!\n\n"
            f"Input:\n{input_file.name}\n\n"
            f"Output:\n{output_file.name}\n\n"
            f"Input size:  {len(original):,} bytes\n"
            f"Output size: {len(converted):,} bytes"
        )

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"Something went wrong:\n\n{error}"
        )

input_file = None

root = tk.Tk()

root.title("Trionic 8 - Kess BIN Dump Decoder")
root.geometry("650x400")
root.resizable(False, False)


title_label = tk.Label(
    root,
    text="Trionic 8 - Kess BIN Dump Decoder",
    font=("Segoe UI", 16, "bold")
)

title_label.pack(pady=(20, 5))


description_label = tk.Label(
    root,
    text="This Swaps every bit on every 16 bit line.",
    font=("Segoe UI", 10)
)

description_label.pack(pady=(0, 20))


input_button = tk.Button(
    root,
    text="📂 Select BIN File",
    command=select_input,
    width=25,
    height=2
)

input_button.pack()


input_label = tk.Label(
    root,
    text="No file selected.",
    wraplength=600,
    justify="center"
)

input_label.pack(pady=10)


convert_button = tk.Button(
    root,
    text="🔄 Convert & Save As...",
    command=convert_and_save,
    width=25,
    height=2
)

convert_button.pack(pady=5)


status_label = tk.Label(
    root,
    text="Select a BIN file to begin.",
    wraplength=600,
    justify="center"
)

status_label.pack(pady=15)


root.mainloop()
