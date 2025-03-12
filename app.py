from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import folium
from folium.raster_layers import TileLayer
import sqlite3
import speech_recognition as sr
import os
import openrouteservice
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database Setup
DATABASE = 'feedback.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = sqlite3.connect(DATABASE)
    with open('schema.sql', 'r') as f:
        conn.cursor().executescript(f.read())
    conn.commit()
    conn.close()

if not os.path.exists(DATABASE):
    init_db()

# Speech Recognition Setup
def transcribe_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        return None

# API Clients
ORS_API_KEY = 'Your-Open-Route-API-KEY'  # From openrouteservice.org
client = openrouteservice.Client(key=ORS_API_KEY)

# ABU Zaria Coordinates
MAP_CENTER_LAT = 11.1496
MAP_CENTER_LON = 7.6565
CAMPUS_NAME = "ABU Zaria"

# Campus Locations
locations = {
    "main_gate": (11.1496, 7.6565, "Main Gate"),
    "library": (11.1502, 7.6571, "University Library"),
    "lecture_hall": (11.1489, 7.6553, "Lecture Hall Complex"),
    "sport_complex": (11.1510, 7.6582, "Sports Complex"),
    "senate_building": (11.1492, 7.6560, "Senate Building"),
    "faculty_of_engineering": (11.1485, 7.6550, "Faculty of Engineering"),
    "faculty_of_sciences": (11.1505, 7.6575, "Faculty of Sciences"),
    "medical_center": (11.1512, 7.6585, "Medical Center")
}
location_names = [loc[2] for loc in locations.values()]

def create_map(center=None, zoom=16):
    if not center:
        center = [MAP_CENTER_LAT, MAP_CENTER_LON]
    
    campus_map = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles=None,
        control_scale=True
    )
    
    # Add Google Maps layer
    TileLayer(
        tiles='https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
        tiles=f'https://{{s}}.google.com/vt/lyrs=s&x={{x}}&y={{y}}&z={{z}}&key=YOUR-GOOGLE-API-KEY-', #Only when you need Satelite View
        subdomains=['mt0','mt1','mt2','mt3'],
        attr='Google',
        name='Google Maps',
        overlay=False,
        control=False,
        show=True
    ).add_to(campus_map)
    
    return campus_map

@app.route('/')
def index():
    campus_map = create_map()
    for name, (lat, lon, popup) in locations.items():
        folium.Marker([lat, lon], popup=popup, icon=folium.Icon(color="blue")).add_to(campus_map)
    map_html = campus_map._repr_html_()
    return render_template('index.html', campus_name=CAMPUS_NAME, map_html=map_html, location_names=location_names)

@app.route('/search', methods=['POST'])
def search():
    current_lat = request.form.get('current_lat')
    current_lon = request.form.get('current_lon')
    search_term = request.form.get('query', '').lower()

    if not search_term:
        flash('Please enter a search term.', 'error')
        return redirect(url_for('index'))

    campus_map = create_map()
    found = False
    searched_coords = None

    for name, (lat, lon, popup) in locations.items():
        if search_term in name.lower() or search_term in popup.lower():
            searched_coords = [lat, lon]
            found = True
            break

    if found:
        mid_point = [
            (float(current_lat) + searched_coords[0])/2 if current_lat else searched_coords[0],
            (float(current_lon) + searched_coords[1])/2 if current_lon else searched_coords[1]
        ]
        
        campus_map = create_map(center=mid_point, zoom=18)
        
        # Add destination marker
        folium.Marker(
            searched_coords,
            popup=popup,
            icon=folium.Icon(color="red", icon="flag")
        ).add_to(campus_map)

        if current_lat and current_lon:
            try:
                current_coords = [float(current_lat), float(current_lon)]
                folium.Marker(
                    current_coords,
                    popup="Your Location",
                    icon=folium.Icon(color="green", icon="user")
                ).add_to(campus_map)

                # Get route data
                route = client.directions(
                    coordinates=[current_coords[::-1], searched_coords[::-1]],
                    profile='foot-walking',
                    format='geojson'
                )
                
                # Add route to map
                folium.PolyLine(
                    locations=[list(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']],
                    color='#0047ab',
                    weight=5
                ).add_to(campus_map)
                
            except Exception as e:
                flash(f"Routing error: {str(e)}", 'error')

    # Add all other markers
    for name, (lat, lon, popup) in locations.items():
        folium.Marker([lat, lon], popup=popup, icon=folium.Icon(color="blue")).add_to(campus_map)

    if not found:
        flash('Location not found!', 'error')
    
    map_html = campus_map._repr_html_()
    return render_template('index.html', campus_name=CAMPUS_NAME, map_html=map_html, location_names=location_names)


@app.route('/voice_search', methods=['POST'])
def voice_search():
    spoken_text = transcribe_speech()
    if not spoken_text:
        flash('Could not understand audio. Please try again.', 'error')
        return redirect(url_for('index'))

    current_lat = request.form.get('current_lat')
    current_lon = request.form.get('current_lon')
    spoken_text = spoken_text.lower()
    campus_map = folium.Map(location=[MAP_CENTER_LAT, MAP_CENTER_LON], zoom_start=15, tiles="OpenStreetMap")
    found = False
    searched_coords = None
    for name, (lat, lon, popup) in locations.items():
        if spoken_text in name.lower() or spoken_text in popup.lower():
            searched_coords = [lat, lon]
            mid_lat = (float(current_lat) + lat) / 2 if current_lat else lat
            mid_lon = (float(current_lon) + lon) / 2 if current_lon else lon
            campus_map = folium.Map(location=[mid_lat, mid_lon], zoom_start=18, tiles="OpenStreetMap")
            folium.Marker([lat, lon], popup=popup, icon=folium.Icon(color="red")).add_to(campus_map)
            if current_lat and current_lon:
                try:
                    current_coords = [float(current_lat), float(current_lon)]
                    route = client.directions([current_coords, searched_coords], profile='foot-walking')
                    route_coords = [(coord[1], coord[0]) for coord in route['features'][0]['geometry']['coordinates']]
                    folium.PolyLine(route_coords, color="blue", weight=5).add_to(campus_map)
                    folium.Marker(current_coords, popup="Your Location", icon=folium.Icon(color="green")).add_to(campus_map)
                except Exception as e:
                    flash(f"Could not calculate route: {e}", 'error')
            found = True
            break
        folium.Marker([lat, lon], popup=popup, icon=folium.Icon(color="blue")).add_to(campus_map)

    if not found:
        flash('Location not found!', 'error')
    map_html = campus_map._repr_html_()
    return render_template('index.html', campus_name=CAMPUS_NAME, map_html=map_html, location_names=location_names)

@app.route('/updates')
def updates():
    try:
        messages = ["No closures reported.", "Lecture Hall closed for maintenance.", "Sports Complex open until 8 PM."]
        return jsonify({"message": random.choice(messages)})
    except Exception as e:
        return jsonify({"message": f"Error fetching updates: {str(e)}"}), 500

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        feedback_text = request.form['feedback']

        if not name or not email or not feedback_text:
            flash('Please fill in all fields.', 'error')
            return render_template('feedback.html')

        conn = get_db_connection()
        conn.execute('INSERT INTO feedback (name, email, feedback_text) VALUES (?, ?, ?)',
                     (name, email, feedback_text))
        conn.commit()
        conn.close()

        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('feedback'))
    return render_template('feedback.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)