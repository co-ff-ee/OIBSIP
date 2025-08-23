import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
from datetime import datetime, timedelta

# API key
API_KEY = "715ddb24f6a0e8108de45cc690ab2fe0"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Function to update background based on temperature
def update_background(temp_celsius):
    if temp_celsius >= 30:
        root.config(bg="#FF7043")  
    elif 15 <= temp_celsius < 30:
        root.config(bg="#81D4FA")  
    else:
        root.config(bg="#B3E5FC")  

# Function to display high-quality weather icon
def display_icon(icon_code):
    try:
        url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"  # High-res icon
        response = requests.get(url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((120, 120))  # Bigger & sharper
        icon_image = ImageTk.PhotoImage(img)
        icon_label.config(image=icon_image)
        icon_label.image = icon_image
    except Exception as e:
        print("Error loading icon:", e)

# Function to fetch weather data
def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Input Error", "Please enter a city name.")
        return

    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data["cod"] != 200:
        messagebox.showerror("Error", f"City '{city}' not found!")
        return

    # Extract data
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"].title()
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    feels_like = data["main"]["feels_like"]
    icon_code = data["weather"][0]["icon"]
    timezone_offset = data["timezone"]

    # Calculate local time (formatted nicely)
    utc_now = datetime.utcnow()
    local_time = utc_now + timedelta(seconds=timezone_offset)
    local_time_str = local_time.strftime("%A, %d %B %Y - %I:%M %p")

    # Update UI
    update_background(temp)
    temp_label.config(text=f"{temp}°C", bg=root["bg"])
    desc_label.config(text=desc, bg=root["bg"])
    time_label.config(text=f"Local Time: {local_time_str}", bg=root["bg"])
    extra_label.config(
        text=f"Humidity: {humidity}%\nWind Speed: {wind_speed} m/s\nFeels Like: {feels_like}°C",
        bg=root["bg"]
    )
    display_icon(icon_code)

# Create main window
root = tk.Tk()
root.title("Advanced Weather App")
root.geometry("420x550")
root.resizable(False, False)
root.config(bg="#B3E5FC")

# Title
title_label = tk.Label(root, text="Advanced Weather App", font=("Helvetica", 18, "bold"), bg=root["bg"])
title_label.pack(pady=10)

# City input
city_entry = tk.Entry(root, font=("Helvetica", 14))
city_entry.pack(pady=5)

# Search button
search_button = tk.Button(root, text="Search Weather", font=("Helvetica", 12, "bold"), command=get_weather)
search_button.pack(pady=5)

# Weather icon
icon_label = tk.Label(root, bg=root["bg"])
icon_label.pack(pady=10)

# Temperature
temp_label = tk.Label(root, text="", font=("Helvetica", 20, "bold"), bg=root["bg"])
temp_label.pack()

# Description
desc_label = tk.Label(root, text="", font=("Helvetica", 14), bg=root["bg"])
desc_label.pack()

# Local time
time_label = tk.Label(root, text="", font=("Helvetica", 12, "italic"), bg=root["bg"])
time_label.pack(pady=5)

# Extra details
extra_label = tk.Label(root, text="", font=("Helvetica", 12), bg=root["bg"])
extra_label.pack(pady=10)

root.mainloop()
