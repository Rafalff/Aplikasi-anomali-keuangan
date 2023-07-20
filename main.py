import numpy as np
import pandas as pd
from tkinter import *
from tkinter import filedialog, messagebox
from sklearn.ensemble import IsolationForest

# Declare entry_contamination as a global variable
entry_contamination = None

def detect_anomalies(data, contamination=0.05):
    # Membuat DataFrame dari data
    df = pd.DataFrame(data, columns=["Amount"])
    
    # Membagi data menjadi fitur (X)
    X = df[["Amount"]]

    # Membuat model Isolation Forest
    isolation_forest = IsolationForest(contamination=contamination, random_state=42)

    # Melatih model pada data fitur X
    isolation_forest.fit(X)

    # Prediksi anomali menggunakan model
    df["Predicted_Label"] = isolation_forest.predict(X)
    
    return df

def on_open_file_button_click():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        try:
            data = pd.read_excel(file_path)

            # Check if 'Jumlah' column exists, otherwise, use 'Amount'
            column_to_use = 'Jumlah' if 'Jumlah' in data.columns else 'Amount'
            if column_to_use in data.columns:
                entry_samples.delete(0, END)
                entry_samples.insert(END, len(data))
                for amount in data[column_to_use]:
                    entry = Entry(frame_data_input)
                    entry.insert(END, amount)
                    entry.pack()
                    entries.append(entry)
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat membaca file:\n{str(e)}")

def on_add_button_click():
    n_samples = int(entry_samples.get())
    for i in range(n_samples):
        entry = Entry(frame_data_input)
        entry.pack()
        entries.append(entry)

def on_detect_button_click():
    try:
        data = []
        for entry in entries:
            amount = float(entry.get())
            data.append([amount])

        contamination = float(entry_contamination.get())

        result_df = detect_anomalies(data, contamination)

        # Create a new window for displaying the result
        result_window = Toplevel(root)
        result_window.title("Hasil Deteksi Anomali")
        result_window.geometry("300x200")

        # Create a scrollbar
        scrollbar = Scrollbar(result_window)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Create a text widget to display the result
        result_text = Text(result_window, height=10, width=40, yscrollcommand=scrollbar.set)
        result_text.pack()

        # Configure the scrollbar to work with the text widget
        scrollbar.config(command=result_text.yview)

        # Insert the result into the text widget
        result_text.insert(END, result_df.to_string())

        anomalous_df = result_df[result_df["Predicted_Label"] == -1]
        if len(anomalous_df) > 0:
            messagebox.showinfo("Hasil Deteksi", "Ditemukan data anomali!")
        else:
            messagebox.showinfo("Hasil Deteksi", "Tidak ada data anomali yang ditemukan.")
    except ValueError:
        messagebox.showerror("Error", "Pastikan input valid. Jumlah data transaksi harus berupa bilangan bulat dan nilai transaksi harus berupa bilangan desimal.")

def set_default_contamination():
    entry_contamination.delete(0, END)
    entry_contamination.insert(END, '0.01')

if __name__ == "__main__":
    root = Tk()
    root.title("Deteksi Anomali Transaksi Keuangan")
    root.geometry("400x500")

    # Create a frame to center all widgets
    center_frame = Frame(root)
    center_frame.pack(expand=True)

    label_samples = Label(center_frame, text="Masukkan jumlah data transaksi:")
    label_samples.pack()

    entry_samples = Entry(center_frame)
    entry_samples.pack()

    add_button = Button(center_frame, text="Tambah Data Transaksi", command=on_add_button_click)
    add_button.pack()

    frame_data_input = Frame(center_frame)
    frame_data_input.pack()

    entries = []

    open_file_button = Button(center_frame, text="Buka File Excel", command=on_open_file_button_click)
    open_file_button.pack()

    # Set default contamination to 0.01
    set_default_contamination()

    label_contamination = Label(center_frame, text="Masukkan tingkat kontaminasi (biasanya 0.01 - 0.1):")
    label_contamination.pack()

    entry_contamination = Entry(center_frame)
    entry_contamination.pack()

    detect_button = Button(center_frame, text="Deteksi Anomali", command=on_detect_button_click)
    detect_button.pack()

    root.mainloop()
