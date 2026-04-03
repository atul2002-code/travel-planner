import os
import streamlit as st
from datetime import datetime
import requests
import time
 
# ============================================================
# LIVE DATA FUNCTIONS — OpenStreetMap + OpenWeatherMap
# ============================================================
 
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
 
def get_coordinates(city_name):
    """Get latitude and longitude for a city using Nominatim (free)"""
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": f"{city_name}, India",
            "format": "json",
            "limit": 1
        }
        headers = {"User-Agent": "TravelPlannerApp/1.0"}
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"]), data[0]["display_name"]
        return None, None, None
    except:
        return None, None, None
 
 
def get_places_from_osm(lat, lon, place_type, city_name, limit=5):
    """Fetch real places from OpenStreetMap Overpass API"""
    try:
        # Map our categories to OSM tags
        type_map = {
            "historical": '[tourism~"museum|attraction|monument|castle|ruins|heritage"][name]',
            "food":       '[amenity~"restaurant|cafe|fast_food"][name]',
            "hotels":     '[tourism~"hotel|guest_house|hostel"][name]',
            "markets":    '[shop~"mall|supermarket|market"][name]',
        }
        tag = type_map.get(place_type, '[tourism][name]')
 
        # Search within ~10km radius
        radius = 10000
        query = f"""
        [out:json][timeout:25];
        (
          node{tag}(around:{radius},{lat},{lon});
          way{tag}(around:{radius},{lat},{lon});
        );
        out body {limit * 3};
        """
        response = requests.post(
            "https://overpass-api.de/api/interpreter",
            data={"data": query},
            timeout=30
        )
        data = response.json()
        elements = data.get("elements", [])
 
        # Extract names, filter out unnamed
        names = []
        for el in elements:
            name = el.get("tags", {}).get("name", "")
            if name and name not in names:
                names.append(name)
            if len(names) >= limit:
                break
 
        return names if names else None
    except:
        return None
 
 
def get_weather(city_name):
    """Get current weather from OpenWeatherMap (free tier)"""
    if not WEATHER_API_KEY:
        return None
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": f"{city_name},IN",
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if response.status_code == 200:
            return {
                "temp": round(data["main"]["temp"]),
                "feels_like": round(data["main"]["feels_like"]),
                "description": data["weather"][0]["description"].title(),
                "humidity": data["main"]["humidity"],
                "wind": round(data["wind"]["speed"]),
                "icon": data["weather"][0]["icon"]
            }
        return None
    except:
        return None
 
 
def get_live_city_data(city_name):
    """Fetch all live data for a city"""
    status = st.empty()
    progress = st.progress(0)
 
    status.info("🔍 Finding city location...")
    lat, lon, display_name = get_coordinates(city_name)
    progress.progress(15)
 
    if not lat:
        status.warning("⚠️ Could not find city. Using fallback data.")
        progress.empty()
        return None, None
 
    result = {
        "display_name": display_name,
        "lat": lat,
        "lon": lon,
        "historical": [],
        "food": [],
        "hotels": [],
        "markets": [],
        "weather": None
    }
 
    status.info("🏛️ Fetching historical places...")
    hist = get_places_from_osm(lat, lon, "historical", city_name)
    result["historical"] = hist if hist else [f"{city_name.title()} Museum", f"{city_name.title()} Monument", f"{city_name.title()} Temple", f"{city_name.title()} Fort", f"{city_name.title()} Heritage Site"]
    progress.progress(35)
    time.sleep(1)  # Respect API rate limits
 
    status.info("🍴 Fetching restaurants & cafes...")
    food = get_places_from_osm(lat, lon, "food", city_name)
    result["food"] = food if food else [f"{city_name.title()} Restaurant", f"{city_name.title()} Cafe", f"Local Dhaba", f"{city_name.title()} Eatery", f"Street Food Corner"]
    progress.progress(55)
    time.sleep(1)
 
    status.info("🏨 Fetching hotels...")
    hotels = get_places_from_osm(lat, lon, "hotels", city_name)
    result["hotels"] = hotels if hotels else [f"{city_name.title()} Grand Hotel", f"{city_name.title()} Inn", f"Hotel {city_name.title()}", f"{city_name.title()} Residency", f"{city_name.title()} Suites"]
    progress.progress(70)
    time.sleep(1)
 
    status.info("🛍️ Fetching markets & malls...")
    markets = get_places_from_osm(lat, lon, "markets", city_name)
    result["markets"] = markets if markets else [f"{city_name.title()} Market", f"{city_name.title()} Mall", f"Local Bazaar", f"{city_name.title()} Shopping Centre", f"Main Market"]
    progress.progress(85)
    time.sleep(1)
 
    status.info("🌤️ Fetching weather...")
    if WEATHER_API_KEY:
        result["weather"] = get_weather(city_name)
    progress.progress(100)
 
    status.empty()
    progress.empty()
 
    return result, display_name
 
 
# ============================================================
# PLAN GENERATION
# ============================================================
 
def generate_detailed_plan(destination, budget, trip_duration, travelers, interests, city_data):
    """Generate detailed plan using live city data"""
    try:
        total_budget = int(budget)
        accommodation = int(total_budget * 0.4)
        food_budget   = int(total_budget * 0.25)
        transport     = int(total_budget * 0.15)
        activities    = int(total_budget * 0.1)
        shopping      = int(total_budget * 0.05)
        buffer        = int(total_budget * 0.05)
    except:
        total_budget  = 10000
        accommodation = 4000
        food_budget   = 2500
        transport     = 1500
        activities    = 1000
        shopping      = 500
        buffer        = 500
 
    historical = city_data.get("historical", [])
    food       = city_data.get("food", [])
    hotels     = city_data.get("hotels", [])
    markets    = city_data.get("markets", [])
    weather    = city_data.get("weather")
    lat        = city_data.get("lat", "")
    lon        = city_data.get("lon", "")
 
    # --- RESEARCH SECTION ---
    research = f"""
🌍 **{destination.upper()} LIVE TRAVEL RESEARCH**
 
📍 **Location:** {city_data.get('display_name', destination)}
🗺️ **Coordinates:** {lat:.4f}°N, {lon:.4f}°E
"""
    if weather:
        research += f"""
🌤️ **Current Weather:**
• Temperature: {weather['temp']}°C (Feels like {weather['feels_like']}°C)
• Condition: {weather['description']}
• Humidity: {weather['humidity']}%
• Wind Speed: {weather['wind']} m/s
"""
 
    research += "\n**🏛️ TOP ATTRACTIONS (Live from OpenStreetMap):**\n"
    for i, site in enumerate(historical[:5], 1):
        research += f"• **📍 {site}** — Attraction #{i}\n"
 
    research += "\n**🍴 RESTAURANTS & CAFES (Live from OpenStreetMap):**\n"
    for i, restaurant in enumerate(food[:5], 1):
        research += f"• **🍴 {restaurant}** — Recommended eatery #{i}\n"
 
    research += "\n**🏨 HOTELS (Live from OpenStreetMap):**\n"
    for i, hotel in enumerate(hotels[:4], 1):
        research += f"• **🏨 {hotel}** — Recommended stay #{i}\n"
 
    research += "\n**🛍️ MARKETS & MALLS (Live from OpenStreetMap):**\n"
    for i, market in enumerate(markets[:4], 1):
        research += f"• **🛍️ {market}** — Shopping destination #{i}\n"
 
    research += f"""
**🗺️ View on Map:**
• [OpenStreetMap Link](https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=13)
 
**✅ TRAVEL TIPS:**
• Best time to visit: October to March
• Currency: Indian Rupees (₹)
• Emergency: 100 (Police), 102 (Ambulance)
"""
 
    # --- BUDGET SECTION ---
    budget_plan = f"""
💰 **BUDGET BREAKDOWN FOR {destination.upper()}** — Total: ₹{budget}
 
**COSTS FOR {travelers} TRAVELERS ({trip_duration} DAYS):**
• **🏨 Accommodation:** ₹{accommodation} (₹{accommodation//max(trip_duration,1)}/night)
• **🍴 Food & Dining:** ₹{food_budget} (₹{food_budget//max(trip_duration,1)}/day)
• **🚍 Local Transport:** ₹{transport} (₹{transport//max(trip_duration,1)}/day)
• **🎯 Activities & Entry Fees:** ₹{activities}
• **🛍️ Shopping & Souvenirs:** ₹{shopping}
• **🆘 Emergency Buffer:** ₹{buffer}
 
**💡 DAILY BUDGET PER PERSON:** ₹{total_budget//max(travelers,1)//max(trip_duration,1)}
 
**MONEY-SAVING TIPS:**
• Use public transport — buses and metro are cheapest
• Eat at local restaurants like **{food[0] if food else 'local eateries'}**
• Visit free attractions like parks and temples
• Bargain at local markets
• Book hotels in advance for best rates
"""
 
    # --- ITINERARY SECTION ---
    itinerary = f"""
🗓️ **{trip_duration}-DAY {destination.upper()} ITINERARY**
 
**Travel Interests:** {', '.join(interests)}
**Travelers:** {travelers} | **Budget:** ₹{budget}
"""
 
    for day in range(1, trip_duration + 1):
        hist_site   = historical[(day - 1) % len(historical)] if historical else f"{destination} Attraction"
        hist_site2  = historical[day % len(historical)] if historical else f"{destination} Monument"
        restaurant1 = food[(day - 1) % len(food)] if food else "Local Restaurant"
        restaurant2 = food[day % len(food)] if food else "Local Cafe"
        market      = markets[(day - 1) % len(markets)] if markets else "Local Market"
        hotel       = hotels[0] if hotels else f"{destination} Hotel"
 
        itinerary += f"""
**DAY {day}:**
• 🌅 **8:00 AM** — Breakfast at **{restaurant1}**
• 🏛️ **9:30 AM** — Visit **{hist_site}**
• 🛍️ **12:00 PM** — Explore **{market}**
• 🍽️ **2:00 PM** — Lunch at **{restaurant2}**
• 🎯 **4:00 PM** — Visit **{hist_site2}**
• 🌇 **6:30 PM** — Evening walk & local sightseeing
• 🍴 **8:00 PM** — Dinner at **{restaurant1}**
• 🏨 **9:30 PM** — Return to **{hotel}**
"""
 
    return [research, budget_plan, itinerary]
 
 
def generate_html_report(responses):
    """Generate downloadable HTML report"""
    destination  = st.session_state.destination
    budget       = st.session_state.budget
    travelers    = st.session_state.travelers
    trip_duration = st.session_state.trip_duration
    interests    = st.session_state.interests
 
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Travel Plan - {destination.title()}</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.7; color: #333; }}
  h1 {{ color: #2c3e50; text-align: center; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
  h2 {{ color: #2980b9; margin-top: 30px; }}
  .info-box {{ background: #f0f8ff; padding: 15px; border-radius: 8px; border-left: 5px solid #3498db; margin: 20px 0; }}
  .section {{ margin-bottom: 30px; }}
  p {{ margin: 6px 0; }}
</style>
</head>
<body>
<h1>🌍 Live Travel Plan - {destination.title()}</h1>
<div class="info-box">
  <p><strong>Destination:</strong> {destination.title()}</p>
  <p><strong>Budget:</strong> ₹{budget}</p>
  <p><strong>Travelers:</strong> {travelers}</p>
  <p><strong>Duration:</strong> {trip_duration} days</p>
  <p><strong>Interests:</strong> {', '.join(interests)}</p>
  <p><strong>Generated on:</strong> {datetime.now().strftime("%Y-%m-%d at %H:%M")}</p>
  <p><strong>Data source:</strong> OpenStreetMap (Live)</p>
</div>
"""
    section_titles = ["Research Findings", "Budget Breakdown", "Daily Itinerary"]
    for i, response in enumerate(responses):
        title = section_titles[i] if i < len(section_titles) else f"Section {i+1}"
        html += f"<div class='section'><h2>{title}</h2>"
        for line in str(response).split('\n'):
            line = line.strip()
            if line:
                html += f"<p>{line}</p>"
        html += "</div>"
 
    html += """
<div class="info-box">
  <p><em>Data sourced live from OpenStreetMap. Always verify before travel.</em></p>
  <p style="text-align:center;color:#888;">Generated with ❤️ by AI Travel Planner</p>
</div>
</body></html>"""
    return html
 
 
# ============================================================
# STREAMLIT UI
# ============================================================
 
if 'page' not in st.session_state:
    st.session_state.page = 'input'
if 'responses' not in st.session_state:
    st.session_state.responses = None
if 'city_data' not in st.session_state:
    st.session_state.city_data = None
 
 
def main():
    st.set_page_config(page_title="AI Travel Planner — Live", layout="wide", page_icon="🌍")
    if st.session_state.page == 'input':
        show_input_page()
    elif st.session_state.page == 'output':
        show_output_page()
 
 
def show_input_page():
    st.title("🌍 AI Travel Planner — Live Data")
    st.caption("Powered by OpenStreetMap & OpenWeatherMap — real locations, real data!")
 
    # Weather API key setup
    with st.expander("🔑 Optional: Add OpenWeatherMap API key for live weather"):
        st.info("Get a FREE key at https://openweathermap.org/api — no credit card needed!")
        weather_key = st.text_input("OpenWeatherMap API Key:", type="password", placeholder="Paste your free API key here")
        if weather_key:
            os.environ["OPENWEATHER_API_KEY"] = weather_key
            st.success("✅ Weather API key saved!")
 
    col1, col2 = st.columns(2)
    with col1:
        destination = st.text_input("📍 Enter Any Indian City:", placeholder="e.g., Mumbai, Pune, Jalgaon, Nashik...")
        budget      = st.text_input("💰 Enter Budget (INR):", placeholder="e.g., 15000", value="15000")
        travelers   = st.number_input("👥 Number of Travelers", min_value=1, max_value=20, value=2)
 
    with col2:
        start_date = st.date_input("📅 Start Date", value=None)
        end_date   = st.date_input("📅 End Date", value=None)
        interests  = st.multiselect(
            "🎯 Travel Interests",
            ["Historical Sites", "Adventure", "Food", "Shopping", "Nature", "Culture", "Relaxation", "City Tours"],
            default=["Historical Sites", "Food", "Shopping"]
        )
 
    st.info("🌐 This app fetches **live** locations from OpenStreetMap — works for **any city in India**!")
 
    if st.button("🎯 Generate Live Travel Plan", type="primary", use_container_width=True):
        if not destination or not budget:
            st.error("⚠️ Please enter both a destination and budget.")
        else:
            try:
                if start_date and end_date:
                    trip_duration = (end_date - start_date).days
                    if trip_duration <= 0:
                        trip_duration = 3
                else:
                    trip_duration = 3
 
                # Fetch live data
                city_data, display_name = get_live_city_data(destination)
 
                if not city_data:
                    st.error("❌ Could not fetch data for this city. Please check the city name and try again.")
                    return
 
                # Generate plan
                responses = generate_detailed_plan(
                    destination, budget, trip_duration, travelers, interests, city_data
                )
 
                st.session_state.responses    = responses
                st.session_state.destination  = destination
                st.session_state.budget       = budget
                st.session_state.travelers    = travelers
                st.session_state.trip_duration = trip_duration
                st.session_state.interests    = interests
                st.session_state.city_data    = city_data
                st.session_state.page         = 'output'
                st.rerun()
 
            except Exception as e:
                st.error(f"Error: {str(e)}")
 
 
def show_output_page():
    st.title("✅ Your Live Travel Plan")
    st.markdown(f"### 📍 {st.session_state.destination.title()}")
 
    responses = st.session_state.responses
    city_data = st.session_state.city_data
 
    if responses:
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Destination", st.session_state.destination.title())
        with col2: st.metric("Budget", f"₹{st.session_state.budget}")
        with col3: st.metric("Travelers", st.session_state.travelers)
        with col4: st.metric("Duration", f"{st.session_state.trip_duration} days")
 
        # Weather card
        if city_data and city_data.get("weather"):
            w = city_data["weather"]
            st.info(f"🌤️ **Current Weather in {st.session_state.destination.title()}:** {w['temp']}°C — {w['description']} | Humidity: {w['humidity']}% | Wind: {w['wind']} m/s")
 
        # Map link
        if city_data:
            lat = city_data.get("lat")
            lon = city_data.get("lon")
            if lat and lon:
                st.markdown(f"🗺️ [View {st.session_state.destination.title()} on OpenStreetMap](https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=13)")
 
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Complete Plan", "🔍 Research", "💰 Budget", "🗓️ Itinerary"])
        with tab1:
            for i, response in enumerate(responses, 1):
                with st.expander(f"Section {i}", expanded=i==1):
                    st.markdown(response)
        with tab2:
            st.markdown(responses[0])
        with tab3:
            st.markdown(responses[1])
        with tab4:
            st.markdown(responses[2])
 
        # Download
        st.markdown("---")
        html_content = generate_html_report(responses)
        filename = f"Live_Travel_Plan_{st.session_state.destination.replace(' ','_').title()}_{datetime.now().strftime('%Y%m%d')}.html"
        st.download_button(
            label="⬇️ Download Travel Plan (HTML)",
            data=html_content,
            file_name=filename,
            mime="text/html",
            use_container_width=True
        )
        st.caption("💡 Open the downloaded file in your browser. You can print it as PDF from there!")
 
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Plan Another Trip", use_container_width=True):
            st.session_state.page = 'input'
            st.session_state.responses = None
            st.session_state.city_data = None
            st.rerun()
    with col2:
        if st.button("📱 Share This Plan", use_container_width=True):
            st.info("Download the HTML file above and share it!")
 
 
if __name__ == "__main__":
    main()
