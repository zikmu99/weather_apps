import tkinter as tk
import requests
import csv
from datetime import datetime, timedelta

# api kulcs
API_KEY = '853541cee3bc747831cf348682355b04'

# funkció
def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()
    precipitation = [0] * 4  
    current_time = datetime.utcnow()
    
    for entry in data['list']:
        dt = datetime.utcfromtimestamp(entry['dt'])
        if current_time < dt <= current_time + timedelta(hours=1):
            # idő
            quarter = (dt.minute // 15)
            precipitation[quarter] += entry.get('rain', {}).get('3h', 0)
    
    return precipitation

# csv mentés
def save_to_csv(city, precipitation):
    filename = f'{city}_csapadek.csv'
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Quarter-Hour', 'Precipitation (mm)'])
        for i, p in enumerate(precipitation):
            writer.writerow([f'Q{i+1}', p])

# Function to display weather data
def display_weather():
    city = city_entry.get()
    precipitation = get_weather(city)
    save_to_csv(city, precipitation)
    
    result_text.config(text=f'Csapadék mennyisége {city} (következő 1 órában):\n'
                            f'Q1: {precipitation[0]} mm\n'
                            f'Q2: {precipitation[1]} mm\n'
                            f'Q3: {precipitation[2]} mm\n'
                            f'Q4: {precipitation[3]} mm\n'
                            'Eredmény mentve CSV-be..')

# Create the GUI
app = tk.Tk()
app.title('Időjárás App')
app.geometry('400x400')

city_label = tk.Label(app, text='Város neve:')
city_label.pack()

city_entry = tk.Entry(app)
city_entry.pack()

get_weather_button = tk.Button(app, text='Lekérdezés', command=display_weather)
get_weather_button.pack()

result_text = tk.Label(app, text='')
result_text.pack()

app.mainloop()
