import tkinter as tk
from tkinter import Menu, messagebox
import requests
from geopy.geocoders import Nominatim

# api kulcs
API_KEY = "853541cee3bc747831cf348682355b04"

# function data
def get_precipitation_data():
    location = location_entry.get()
    if not location:
        messagebox.showerror("Error", "Próbáld mégegyszer")
        return

    # Geocoding 
    geolocator = Nominatim(user_agent="precipitation_app")
    try:
        location_info = geolocator.geocode(location, timeout=10)
    except Exception as e:
        messagebox.showerror("Error", f"Geocoding error: {str(e)}")
        return

    if location_info:
        lat, lon = location_info.latitude, location_info.longitude
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}"

        try:
            response = requests.get(url)
            data = response.json()
            hour = data["list"][0]["dt_txt"].split()[1][:2]  # ideőbeállitás
            total_precipitation = 0

            # időlebontás
            for entry in data["list"]:
                if entry["dt_txt"].split()[1][:2] == hour:
                    total_precipitation += entry.get("rain", {}).get("3h", 0)

            # eredmény
            result_label.config(text=f"Csapadék az elkövetkező egy órában: {total_precipitation} mm")
        except Exception as e:
            messagebox.showerror("Error", f"API error: {str(e)}")
    else:
        messagebox.showerror("Error", "A helység nem található.")

# mentés
def save_result():
    result = result_label.cget("text")
    if result:
        with open("precipitation_result.txt", "w") as file:
            file.write(result)
        messagebox.showinfo("Sikeres mentés.", "Mentve: 'előrejelzés_eredmény.txt'.")

# gui
root = tk.Tk()
root.title("Csapadék előrejelzés")
root.geometry('600x200')
# háttér gui
root.configure(background='')

# menü
menu = Menu(root)
root.config(menu=menu)
file_menu = Menu(menu)
menu.add_cascade(label="Fájl", menu=file_menu)
file_menu.add_command(label="Eredmény mentése", command=save_result)
file_menu.add_command(label="Kilépés", command=root.quit)

# Create and pack widgets
location_label = tk.Label(root, text="Helység:")
location_label.pack()
location_entry = tk.Entry(root)
location_entry.pack()
get_data_button = tk.Button(root, text="Elemzés", command=get_precipitation_data)
get_data_button.pack()
result_label = tk.Label(root, text="", font=("Helvetica", 14))
result_label.pack()

root.mainloop()
