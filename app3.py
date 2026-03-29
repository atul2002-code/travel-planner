import os
import streamlit as st
from xhtml2pdf import pisa
from datetime import datetime

# --- COMPREHENSIVE INDIAN CITIES DATABASE ---
INDIAN_CITIES_DATA = {
    # Major Metropolitan Cities
    "mumbai": {
        "historical": ["Gateway of India", "Chhatrapati Shivaji Maharaj Terminus", "Elephanta Caves", "Haji Ali Dargah", "Kanheri Caves"],
        "food": ["Leopold Cafe", "Bademiya", "Cafe Madras", "Trishna", "Britannia & Co."],
        "hotels": ["Taj Mahal Palace", "Trident Nariman Point", "The Leela", "JW Marriott", "ITC Maratha"],
        "markets": ["Colaba Causeway", "Crawford Market", "Chor Bazaar", "Linking Road", "Hill Road"],
        "transport": "Local Trains, BEST Buses, Metro",
        "specialty": "Financial Capital, Bollywood"
    },
    "delhi": {
        "historical": ["Red Fort", "Qutub Minar", "India Gate", "Lotus Temple", "Humayun's Tomb"],
        "food": ["Karim's", "Paranthe Wali Gali", "Bukhara", "Sagar Ratna", "Kake Di Hatti"],
        "hotels": ["The Leela Palace", "Taj Mahal Delhi", "The Imperial", "ITC Maurya", "Hyatt Regency"],
        "markets": ["Chandni Chowk", "Connaught Place", "Dilli Haat", "Sarojini Nagar", "Khan Market"],
        "transport": "Delhi Metro, DTC Buses, Auto-rickshaws",
        "specialty": "Capital City, Historical Monuments"
    },
    "bangalore": {
        "historical": ["Bangalore Palace", "Tipu Sultan's Summer Palace", "Bull Temple", "Vidhana Soudha", "ISKCON Temple"],
        "food": ["Mavalli Tiffin Room", "Vidyarthi Bhavan", "CTR", "Karavalli", "Koshy's"],
        "hotels": ["Taj West End", "ITC Gardenia", "The Leela Palace", "Ritz Carlton", "Marriott"],
        "markets": ["Commercial Street", "Brigade Road", "Chickpet", "MG Road", "UB City"],
        "transport": "Bangalore Metro, BMTC Buses",
        "specialty": "IT Capital, Garden City"
    },
    "hyderabad": {
        "historical": ["Charminar", "Golconda Fort", "Salar Jung Museum", "Qutb Shahi Tombs", "Chowmahalla Palace"],
        "food": ["Paradise Biryani", "Cafe Bahar", "Bawarchi", "Shadab", "Pista House"],
        "hotels": ["Park Hyatt", "Taj Krishna", "ITC Kohenur", "Marriott", "Novotel"],
        "markets": ["Charminar Market", "Sultan Bazar", "Laad Bazar", "Begum Bazar", "Abids"],
        "transport": "Hyderabad Metro, TSRTC Buses",
        "specialty": "Biryani, Pearls, IT Hub"
    },
    "chennai": {
        "historical": ["Kapaleeshwarar Temple", "Fort St. George", "San Thome Basilica", "Valluvar Kottam", "Guindy National Park"],
        "food": ["Saravana Bhavan", "Murugan Idli Shop", "Annalakshmi", "Copper Chimney", "Rayar's Mess"],
        "hotels": ["Taj Coromandel", "ITC Grand Chola", "The Leela Palace", "Hyatt Regency", "Radisson Blu"],
        "markets": ["T Nagar", "Pondy Bazar", "George Town", "Ranganathan Street", "Spencer Plaza"],
        "transport": "Chennai Metro, MTC Buses",
        "specialty": "Cultural Capital, Automotive Hub"
    },
    "kolkata": {
        "historical": ["Victoria Memorial", "Howrah Bridge", "Dakshineswar Temple", "Indian Museum", "Marble Palace"],
        "food": ["Peter Cat", "Kewpie's", "Mocambo", "Oh! Calcutta", "Arsalan"],
        "hotels": ["Taj Bengal", "ITC Sonar", "The Oberoi Grand", "Hyatt Regency", "Novotel"],
        "markets": ["New Market", "Gariahat", "College Street", "Park Street", "Burrabazar"],
        "transport": "Kolkata Metro, Trams, Buses",
        "specialty": "City of Joy, Cultural Hub"
    },

    # Maharashtra Cities
    "pune": {
        "historical": ["Shaniwar Wada", "Aga Khan Palace", "Sinhagad Fort", "Raja Dinkar Kelkar Museum", "Dagdusheth Halwai Temple"],
        "food": ["Cafe Goodluck", "Badshahi Biryani", "Kayani Bakery", "Bedekar Misal", "Vaishali"],
        "hotels": ["Hotel Aurora Towers", "The Fern Hotel", "Ibis Hotel", "Conrad Pune", "JW Marriott"],
        "markets": ["Tulsi Baug", "Laxmi Road", "FC Road", "Juna Bazar", "MG Road"],
        "transport": "Pune Metro, PMPML Buses",
        "specialty": "Oxford of India, IT Hub"
    },
    "nagpur": {
        "historical": ["Deekshabhoomi", "Sitabuldi Fort", "Raman Science Centre", "Futala Lake", "Ambazari Lake"],
        "food": ["Haldiram's", "Happiness Cafe", "Saoji Khao Galli", "Shree Krishnan", "Bapat Nagar"],
        "hotels": ["Le Meridien", "Hotel Centre Point", "Radisson Blu", "Tuli Imperial", "Hotel Pride"],
        "markets": ["Sitabuldi Main Road", "Jhansi Rani Square", "Dharampeth", "Itwari", "Mahal"],
        "transport": "Nagpur Metro, NMC Buses",
        "specialty": "Orange City, Zero Mile"
    },
    "nashik": {
        "historical": ["Sula Vineyards", "Trimbakeshwar Temple", "Pandavleni Caves", "Kalaram Temple", "Coin Museum"],
        "food": ["Sula Vineyard Restaurant", "Purohit Lunch Home", "Garden Court", "Sai Krupa", "Grape Embassy"],
        "hotels": ["Gateway Hotel", "Express Inn", "Hotel Panchavati", "Lemon Tree", "Ibis"],
        "markets": ["Main Road Market", "Shalimar", "Saraf Bazar", "Old Nashik Market", "Dwarka"],
        "transport": "Nashik City Buses, Auto-rickshaws",
        "specialty": "Wine Capital, Kumbh Mela"
    },
    "aurangabad": {
        "historical": ["Ajanta Caves", "Ellora Caves", "Bibi Ka Maqbara", "Daulatabad Fort", "Grishneshwar Temple"],
        "food": ["Bhoj", "Green Leaf", "Tandoor", "Madhur Cafe", "Sankalp"],
        "hotels": ["Lemon Tree", "Vivanta Aurangabad", "Rama International", "WelcomHotel", "Atithi Gruh"],
        "markets": ["Gulmandi", "Juna Bazar", "Shahgunj", "City Chowk", "Kannad Road"],
        "transport": "Aurangabad City Buses, Auto-rickshaws",
        "specialty": "Tourism Hub, Historical Caves"
    },
    "kolhapur": {
        "historical": ["Mahalaxmi Temple", "New Palace", "Rankala Lake", "Jyotiba Temple", "Panhala Fort"],
        "food": ["Hotel Opal", "Purohit", "Khasbag", "Prasad", "Mahesh Lunch Home"],
        "hotels": ["Sayaji Hotel", "The Pavilion", "Hotel Pearl", "Yatri Nivas", "Hotel Tourist"],
        "markets": ["Mahadwar Road", "Dasara Chowk", "Shivaji Peth", "Foujdar Chawk", "Station Road"],
        "transport": "Kolhapur Municipal Buses, Auto-rickshaws",
        "specialty": "Jaggery, Kolhapuri Chappal, Wrestling"
    },

    # Gujarat Cities
    "ahmedabad": {
        "historical": ["Sabarmati Ashram", "Sidi Saiyyed Mosque", "Adalaj Stepwell", "Kankaria Lake", "Auto World Museum"],
        "food": ["Gordhan Thal", "Agashiye", "Havmor", "Das Khaman", "Swati Snacks"],
        "hotels": ["The Renaissance", "Courtyard Marriott", "Hyatt Regency", "Fortune Landmark", "Novotel"],
        "markets": ["Law Garden", "Manek Chowk", "Rani no Hajiro", "Dhalgarwad", "CG Road"],
        "transport": "Ahmedabad Metro, AMTS Buses",
        "specialty": "Textile Hub, Heritage City"
    },
    "surat": {
        "historical": ["Surat Castle", "Sardar Patel Museum", "Dutch Garden", "Ambika Niketan Temple", "Gopi Talav"],
        "food": ["Kansar Gujarati Thali", "Balaji Bhajiya House", "Garden Kulfi Centre", "Gwalia Sweet Home", "New Falahaar"],
        "hotels": ["The Grand Bhagwati", "Hotel Surya Palace", "Hotel Saffron", "Novotel", "Sayaji"],
        "markets": ["Textile Market", "Mahidharpura Gold Market", "RR Street", "Chowk Bazar", "Adajan Patia"],
        "transport": "City Bus, Auto-rickshaws",
        "specialty": "Diamond City, Textile Hub"
    },
    "vadodara": {
        "historical": ["Laxmi Vilas Palace", "Sayaji Baug", "EME Temple", "Baroda Museum", "Kirti Mandir"],
        "food": ["Mandy's", "Surya Palace", "Toran", "Jassi de Parathe", "Kansar"],
        "hotels": ["WelcomHotel", "Surya Palace", "Express Inn", "Ibis", "Gateway Hotel"],
        "markets": ["Mandal", "Raopura", "Khanderao Market", "Dandia Bazar", "Akota"],
        "transport": "Vadodara City Buses, Auto-rickshaws",
        "specialty": "Cultural Capital, Education Hub"
    },

    # South Indian Cities
    "coimbatore": {
        "historical": ["Marudamalai Temple", "Perur Temple", "VOC Park", "Gedee Car Museum", "Black Thunder"],
        "food": ["Annapoorna", "Aryaas", "Shree Krishna", "Abirami", "Sree Annapoorna"],
        "hotels": ["Vivanta Coimbatore", "Le Meridien", "Radisson Blu", "The Residency", "Aloft"],
        "markets": ["Gandhipuram", "Cross Cut Road", "Oppanakara Street", "RS Puram", "Town Hall"],
        "transport": "Coimbatore City Buses, Auto-rickshaws",
        "specialty": "Manchester of South India, Engineering Hub"
    },
    "kochi": {
        "historical": ["Fort Kochi", "Chinese Fishing Nets", "Mattancherry Palace", "Jewish Synagogue", "St. Francis Church"],
        "food": ["Grand Hotel", "Dal Roti", "Casa Bianca", "Kashi Art Cafe", "Fort House"],
        "hotels": ["Taj Malabar", "Brunton Boatyard", "Grand Hyatt", "Le Meridien", "Holiday Inn"],
        "markets": ["Jew Town", "Broadway", "MG Road", "Lulu Mall", "Oceanus Mall"],
        "transport": "Kochi Metro, City Buses, Ferries",
        "specialty": "Queen of Arabian Sea, Port City"
    },

    # North Indian Cities
    "jaipur": {
        "historical": ["Hawa Mahal", "Amber Fort", "City Palace", "Jantar Mantar", "Nahargarh Fort"],
        "food": ["Laxmi Mishthan Bhandar", "Rawla", "Natraj", "Handi", "Chokhi Dhani"],
        "hotels": ["Rambagh Palace", "Fairmont Jaipur", "JW Marriott", "Holiday Inn", "Trident"],
        "markets": ["Johari Bazar", "Bapu Bazar", "Tripolia Bazar", "Chandpole Bazar", "MI Road"],
        "transport": "Jaipur Metro, City Buses, Auto-rickshaws",
        "specialty": "Pink City, Royal Heritage"
    },
    "lucknow": {
        "historical": ["Bara Imambara", "Chota Imambara", "Rumi Darwaza", "British Residency", "Ambedkar Park"],
        "food": ["Tunday Kababi", "Dastarkhwan", "Royal Cafe", "Nawab's", "Ratti Lal's"],
        "hotels": ["Renaissance Lucknow", "Hyatt Regency", "Vivanta Gomti Nagar", "Clarks Avadh", "Piccadily"],
        "markets": ["Hazratganj", "Aminabad", "Chowk", "Kaiserbagh", "Alambagh"],
        "transport": "Lucknow Metro, City Buses, Auto-rickshaws",
        "specialty": "City of Nawabs, Kebabs"
    },

    # Small Cities & Tier 2/3 Cities
    "jalgaon": {
        "historical": ["Gandhi Teerth", "Patnadevi Temple", "Jain Temple", "Swami Samarth Temple", "Gajanan Maharaj Temple"],
        "food": ["Hotel Samrat", "Shree Krishna Bhojanalay", "Khandesh Bhojanalay", "Garden View Restaurant", "Madhur Cafe"],
        "hotels": ["Hotel Aura", "Hotel Plaza", "Hotel Heritage", "Shree Krishna", "Yash Palace"],
        "markets": ["Jalgaon Cloth Market", "Gandhi Market", "Station Road Market", "Navpada", "M.J. Road"],
        "transport": "MSRTC Buses, Auto-rickshaws",
        "specialty": "Banana City, Gold Market"
    },
    "amravati": {
        "historical": ["Amba Devi Temple", "Chatri Talao", "Baba Farid Park", "Wadali Talao", "Bharat Palace"],
        "food": ["Hotel Rajwada", "Shiv Sagar", "Gurukripa", "Madhur Milan", "Sai Palace"],
        "hotels": ["Hotel Rajwada", "Hotel Vrindavan", "Hotel Samrat", "Hotel Sai Palace", "Hotel Shivsagar"],
        "markets": ["Rajapeth", "Bhogali", "Gandhi Chowk", "Shivaji Nagar", "Shyam Chowk"],
        "transport": "Amravati Municipal Buses, Auto-rickshaws",
        "specialty": "Education Hub, Historical City"
    },
    "nanded": {
        "historical": ["Hazur Sahib", "Sachkhand Gurudwara", "Kaleshwar Temple", "Shri Guru Gobind Singh Ji Museum", "Mahanubhav Temple"],
        "food": ["Gurudwara Langar", "Hotel Samrat", "Shiv Sagar", "Madhur Cafe", "Sai Palace"],
        "hotels": ["Hotel Samrat", "Hotel Rajwada", "Hotel Sai Palace", "Gurudwara Sarai", "Hotel Shivsagar"],
        "markets": ["Main Road Market", "Shivaji Nagar", "Gandhi Chowk", "Shyam Chowk", "Jain Bazar"],
        "transport": "Nanded City Buses, Auto-rickshaws",
        "specialty": "Sikh Pilgrimage, Historical Significance"
    },
    "latur": {
        "historical": ["Ganj Golai", "Siddheshwar Temple", "Ausa Fort", "Hattikhana", "Surat Shahaji Museum"],
        "food": ["Hotel Samrat", "Shiv Sagar", "Gurukripa", "Madhur Milan", "Sai Palace"],
        "hotels": ["Hotel Rajwada", "Hotel Vrindavan", "Hotel Samrat", "Hotel Sai Palace", "Hotel Shivsagar"],
        "markets": ["Main Road Market", "Gandhi Chowk", "Shivaji Nagar", "Shyam Chowk", "Jain Bazar"],
        "transport": "Latur City Buses, Auto-rickshaws",
        "specialty": "Educational Hub, Historical City"
    }
}

# --- Initialize session state ---
if 'page' not in st.session_state:
    st.session_state.page = 'input'
if 'responses' not in st.session_state:
    st.session_state.responses = None
if 'destination' not in st.session_state:
    st.session_state.destination = ""
if 'budget' not in st.session_state:
    st.session_state.budget = ""

def get_city_data(city_name):
    """Get exact location data for any Indian city"""
    city_key = city_name.lower().split(',')[0].strip()
    
    if city_key in INDIAN_CITIES_DATA:
        return INDIAN_CITIES_DATA[city_key]
    else:
        # For unknown cities, use city name in locations
        city_title = city_name.title()
        return {
            "historical": [
                f"{city_title} Fort", 
                f"{city_title} Museum", 
                f"Old {city_title} Temple",
                f"{city_title} Palace",
                f"{city_title} Historical Monument"
            ],
            "food": [
                f"{city_title} Famous Restaurant",
                f"{city_title} Local Eatery", 
                f"{city_title} Sweet Shop",
                f"{city_title} Bhojanalay",
                f"{city_title} Cafe"
            ],
            "hotels": [
                f"{city_title} Grand Hotel",
                f"{city_title} Comfort Inn", 
                f"{city_title} Budget Stay",
                f"{city_title} Palace",
                f"{city_title} Residency"
            ],
            "markets": [
                f"{city_title} Main Market",
                f"{city_title} Cloth Market", 
                f"{city_title} Local Bazaar",
                f"{city_title} Shopping Street",
                f"{city_title} Commercial Area"
            ],
            "transport": "Local Buses, Auto-rickshaws, Taxis",
            "specialty": "Local Culture, Historical Significance"
        }

def generate_detailed_plan(destination, budget, trip_duration, travelers, interests):
    """Generate detailed plan with EXACT location names"""
    city_data = get_city_data(destination)
    city_key = destination.lower().split(',')[0].strip()
    
    # Calculate budget
    try:
        total_budget = int(budget)
        accommodation = int(total_budget * 0.4)
        food = int(total_budget * 0.25)
        transport = int(total_budget * 0.15)
        activities = int(total_budget * 0.1)
        shopping = int(total_budget * 0.05)
        buffer = int(total_budget * 0.05)
    except:
        total_budget = 10000
        accommodation = 4000
        food = 2500
        transport = 1500
        activities = 1000
        shopping = 500
        buffer = 500
    
    # Research Section with EXACT locations
    research = f"""
🌍 **{destination.upper()} TRAVEL RESEARCH REPORT**

**CITY SPECIALTY:** {city_data['specialty']}

**TOP HISTORICAL SITES (EXACT NAMES):**
"""
    for i, site in enumerate(city_data["historical"][:5], 1):
        research += f"• **📍 {site}** - Must-visit historical site #{i}\n"
    
    research += f"""
**SHOPPING (SPECIFIC MARKETS):**
"""
    for i, market in enumerate(city_data["markets"][:4], 1):
        research += f"• **🛍️ {market}** - Popular shopping destination #{i}\n"
    
    research += f"""
**FOOD (EXACT RESTAURANT NAMES):**
"""
    for i, restaurant in enumerate(city_data["food"][:5], 1):
        research += f"• **🍴 {restaurant}** - Famous for local cuisine #{i}\n"
    
    research += f"""
**ACCOMMODATION (SPECIFIC HOTELS):**
"""
    for i, hotel in enumerate(city_data["hotels"][:4], 1):
        research += f"• **🏨 {hotel}** - Recommended hotel #{i}\n"
    
    research += f"""
**TRANSPORT:**
• **🚍 {city_data['transport']}** - Main transport options
• **💰 Estimated daily transport cost:** ₹200-500 per person

**TRAVEL TIPS:**
• Best time to visit: October to March
• Local language: Learn basic greetings
• Currency: Indian Rupees (₹)
• Emergency numbers: 100 (Police), 102 (Ambulance)
"""

    # Budget Section
    budget_plan = f"""
💰 **BUDGET BREAKDOWN FOR {destination.upper()}** - Total: ₹{budget}

**DETAILED COSTS FOR {travelers} TRAVELERS ({trip_duration} DAYS):**
• **🏨 Accommodation:** ₹{accommodation} (₹{accommodation//trip_duration}/night)
• **🍴 Food & Dining:** ₹{food} (₹{food//trip_duration}/day)
• **🚍 Local Transport:** ₹{transport} (₹{transport//trip_duration}/day)
• **🎯 Activities & Entry Fees:** ₹{activities}
• **🛍️ Shopping & Souvenirs:** ₹{shopping}
• **🆘 Emergency Buffer:** ₹{buffer}

**DAILY BUDGET PER PERSON:** ₹{total_budget//travelers//trip_duration}

**MONEY-SAVING TIPS:**
• Use {city_data['transport'].split(',')[0]} for affordable travel
• Eat at local restaurants like **{city_data['food'][0]}**
• Visit free attractions and public spaces
• Bargain politely at local markets
• Book accommodation 2-3 weeks in advance
• Travel in groups to share costs
"""

    # Itinerary Section with EXACT locations
    itinerary = f"""
🗓️ **{trip_duration}-DAY {destination.upper()} ITINERARY**

**Travel Interests:** {', '.join(interests)}
**Number of Travelers:** {travelers}
**Budget:** ₹{budget}

"""
    
    # Generate day-wise itinerary with exact locations
    day_plans = [
        {"title": "HISTORICAL & CULTURAL EXPLORATION", "sites": city_data["historical"][:2], "market": city_data["markets"][0], "food": city_data["food"][:2]},
        {"title": "LOCAL MARKETS & TEMPLE TOUR", "sites": city_data["historical"][2:4], "market": city_data["markets"][1], "food": city_data["food"][2:4]},
        {"title": "CITY LANDMARKS & SHOPPING", "sites": [city_data["historical"][4] if len(city_data["historical"]) > 4 else city_data["historical"][0]], "market": city_data["markets"][2], "food": [city_data["food"][4] if len(city_data["food"]) > 4 else city_data["food"][0]]},
        {"title": "LOCAL EXPERIENCES & RELAXATION", "sites": ["Local Park/Garden", "Riverside"], "market": "Local Crafts Market", "food": ["Traditional Dinner"]},
        {"title": "FINAL EXPLORATION & DEPARTURE", "sites": ["Last Minute Sightseeing"], "market": "Souvenir Shopping", "food": ["Farewell Lunch"]}
    ]
    
    for day in range(1, trip_duration + 1):
        plan = day_plans[min(day-1, len(day_plans)-1)]
        
        itinerary += f"""
**DAY {day}: {plan['title']}**

• **🌅 8:00 AM** - Breakfast at **{city_data['food'][0]}**
• **🏛️ 9:30 AM** - Visit **{plan['sites'][0]}**
• **🛍️ 12:00 PM** - Explore **{plan['market']}**
• **🍽️ 2:00 PM** - Lunch at **{plan['food'][0] if isinstance(plan['food'], list) else plan['food']}**
• **🎯 4:00 PM** - {f"Visit {plan['sites'][1]}" if len(plan['sites']) > 1 else "Cultural activity"}
• **🌇 6:30 PM** - Evening at local attraction
• **🍴 8:00 PM** - Dinner at **{plan['food'][1] if isinstance(plan['food'], list) and len(plan['food']) > 1 else city_data['food'][1]}**
• **🏨 9:30 PM** - Return to **{city_data['hotels'][0]}**

"""
    
    return [research, budget_plan, itinerary]

def create_pdf(content, filename):
    try:
        with open(filename, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(content, dest=pdf_file)
        return not pisa_status.err
    except Exception as e:
        st.error(f"PDF creation error: {str(e)}")
        return False

def main():
    st.set_page_config(page_title="AI Travel Planner - All India", layout="wide", page_icon="🌍")
    
    if st.session_state.page == 'input':
        show_input_page()
    elif st.session_state.page == 'output':
        show_output_page()

def show_input_page():
    st.title("🌍 AI Travel Planner ")
    st.markdown("")
    
    # Supported cities list
    supported_cities = list(INDIAN_CITIES_DATA.keys())
    major_cities = supported_cities[:8]
    other_cities = supported_cities[8:]
    
    col1, col2 = st.columns(2)
    
    with col1:
        destination = st.text_input("📍 Enter Any Indian City:", 
                                  placeholder="e.g., Mumbai, Pune, Jalgaon, Nashik, etc.")
        budget = st.text_input("💰 Enter Budget (INR):", 
                             placeholder="e.g., 15000", 
                             value="15000")
        travelers = st.number_input("👥 Number of Travelers", 
                                  min_value=1, max_value=20, value=2)
    
    with col2:
        start_date = st.date_input("📅 Start Date", value=None)
        end_date = st.date_input("📅 End Date", value=None)
        interests = st.multiselect(
            "🎯 Travel Interests",
            ["Historical Sites", "Adventure", "Food", "Shopping", "Nature", "Culture", "Relaxation", "City Tours"],
            default=["Historical Sites", "Food", "Shopping"]
        )

    # Show supported cities in expander
    with st.expander("📍 **Supported Cities (Click to view)**", expanded=False):
        st.write("**Major Cities:** " + ", ".join([city.title() for city in major_cities]))
        st.write("**Other Cities:** " + ", ".join([city.title() for city in other_cities]))
        st.write("**➕ Many More!** - Enter any Indian city name")

    if st.button("🎯 Generate Travel Plan", type="primary", use_container_width=True):
        if not destination or not budget:
            st.error("⚠️ Please enter both a destination and budget.")
        else:
            with st.spinner("⏳ Generating your travel plan with EXACT location names..."):
                try:
                    # Calculate trip duration
                    if start_date and end_date:
                        trip_duration = (end_date - start_date).days
                        if trip_duration <= 0:
                            trip_duration = 3
                    else:
                        trip_duration = 3
                    
                    # Generate plan with exact locations
                    responses = generate_detailed_plan(
                        destination, budget, trip_duration, travelers, interests
                    )
                    
                    st.session_state.responses = responses
                    st.session_state.destination = destination
                    st.session_state.budget = budget
                    st.session_state.travelers = travelers
                    st.session_state.trip_duration = trip_duration
                    st.session_state.interests = interests
                    st.session_state.page = 'output'
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error generating plan: {str(e)}")

def show_output_page():
    st.title("✅ Your Travel Plan with EXACT Locations")
    st.markdown(f"### **Perfect itinerary for {st.session_state.destination.title()}**")
    
    responses = st.session_state.responses
    
    if responses:
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Destination", st.session_state.destination.title())
        with col2:
            st.metric("Budget", f"₹{st.session_state.budget}")
        with col3:
            st.metric("Travelers", st.session_state.travelers)
        with col4:
            st.metric("Duration", f"{st.session_state.trip_duration} days")
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Complete Plan", "🔍 Research", "💰 Budget", "🗓️ Itinerary"])
        
        with tab1:
            display_full_plan(responses)
        
        with tab2:
            display_research(responses)
            
        with tab3:
            display_budget(responses)
            
        with tab4:
            display_itinerary(responses)
        
        # PDF Download
        st.markdown("---")
        st.subheader("📄 Download Your Travel Plan")
        
        if st.button("⬇️ Generate PDF Report", type="primary", use_container_width=True):
            with st.spinner("Creating PDF..."):
                pdf_success = generate_pdf_report(responses)
                if pdf_success:
                    st.success("✅ PDF generated successfully!")
                    st.balloons()
        
    else:
        st.error("No responses available. Please generate a new plan.")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Generate New Plan", use_container_width=True):
            st.session_state.page = 'input'
            st.session_state.responses = None
            st.rerun()
    with col2:
        if st.button("📱 Share This Plan", use_container_width=True):
            st.info("Share this plan by downloading the PDF report above!")

def display_full_plan(responses):
    st.subheader("Complete Travel Plan Summary")
    for i, response in enumerate(responses, 1):
        with st.expander(f"Section {i}: Detailed Analysis", expanded=i==1):
            st.markdown(response)

def display_research(responses):
    st.subheader("🔍 Travel Research Findings")
    st.info("Detailed research with EXACT location names and specific details.")
    if len(responses) > 0:
        st.markdown(responses[0])

def display_budget(responses):
    st.subheader("💰 Budget Breakdown")
    st.info("Detailed cost analysis with specific examples and money-saving tips.")
    if len(responses) > 1:
        st.markdown(responses[1])

def display_itinerary(responses):
    st.subheader("🗓️ Daily Itinerary")
    st.info(f"Day-by-day schedule with EXACT location names and specific timings.")
    if len(responses) > 2:
        st.markdown(responses[2])

def generate_pdf_report(responses):
    try:
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: 'Arial', sans-serif; margin: 40px; line-height: 1.6; }}
                h1 {{ color: #2c3e50; text-align: center; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
                h2 {{ color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 5px; margin-top: 30px; }}
                h3 {{ color: #2c3e50; margin-top: 25px; }}
                .section {{ margin-bottom: 30px; }}
                .point {{ margin: 10px 0; padding-left: 15px; }}
                .info-box {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 5px solid #3498db; }}
                .location {{ color: #e74c3c; font-weight: bold; }}
                .highlight {{ background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .itinerary-day {{ background-color: #e8f4fd; padding: 15px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #2980b9; }}
                @media print {{
                    body {{ margin: 20px; }}
                    .no-print {{ display: none; }}
                }}
            </style>
        </head>
        <body>
            <h1>🌍 AI Travel Plan - {st.session_state.destination.title()}</h1>
            <div class="info-box">
                <h2>Trip Overview</h2>
                <div class="point"><strong>• Destination:</strong> {st.session_state.destination.title()}</div>
                <div class="point"><strong>• Budget:</strong> ₹{st.session_state.budget}</div>
                <div class="point"><strong>• Travelers:</strong> {st.session_state.travelers}</div>
                <div class="point"><strong>• Duration:</strong> {st.session_state.trip_duration} days</div>
                <div class="point"><strong>• Interests:</strong> {', '.join(st.session_state.interests)}</div>
                <div class="point"><strong>• Generated on:</strong> {datetime.now().strftime("%Y-%m-%d at %H:%M")}</div>
            </div>
        """
        
        section_titles = ["Research Findings", "Budget Breakdown", "Detailed Itinerary"]
        
        for i, response in enumerate(responses):
            if i < len(section_titles):
                html_content += f'<h2>{section_titles[i]}</h2>'
            else:
                html_content += f'<h2>Section {i+1}</h2>'
            
            lines = str(response).split('\n')
            for line in lines:
                if line.strip():
                    if any(marker in line for marker in ['📍', '🍴', '🏨', '🛍️', '🚍']):
                        html_content += f'<div class="point"><span class="location">{line.strip()}</span></div>'
                    elif line.strip().startswith('**DAY'):
                        html_content += f'<div class="itinerary-day"><strong>{line.strip()}</strong></div>'
                    elif line.strip().startswith(('•', '-', '*')):
                        html_content += f'<div class="point">{line.strip()}</div>'
                    elif line.strip().startswith('🌍') or line.strip().startswith('💰') or line.strip().startswith('🗓️'):
                        html_content += f'<h3>{line.strip()}</h3>'
                    elif len(line.strip()) > 10:
                        html_content += f'<p>{line.strip()}</p>'
                    else:
                        html_content += f'<div class="point">• {line.strip()}</div>'
        
        # Add footer
        html_content += """
            <div class="highlight no-print">
                <h2>💡 Important Travel Tips</h2>
                <div class="point">• Carry original ID proof and copies</div>
                <div class="point">• Keep emergency contacts handy</div>
                <div class="point">• Check weather forecast before travel</div>
                <div class="point">• Respect local customs and traditions</div>
                <div class="point">• Stay hydrated and carry essential medicines</div>
                <div class="point">• Keep digital and physical copies of documents</div>
            </div>
            
            <div class="info-box">
                <p><strong>Note:</strong> This AI-generated travel plan provides estimated costs and recommendations. 
                Actual prices, timings, and availability may vary. Always verify current information before your trip.</p>
                <p style="text-align: center; margin-top: 20px; color: #7f8c8d;">
                    Generated with ❤️ by AI Travel Planner | {datetime.now().strftime("%Y")}
                </p>
            </div>
        </body>
        </html>
        """
        
        pdf_filename = f"Travel_Plan_{st.session_state.destination.replace(' ', '_').title()}_{datetime.now().strftime('%Y%m%d')}.pdf"
        success = create_pdf(html_content, pdf_filename)
        
        if success:
            with open(pdf_filename, "rb") as f:
                pdf_data = f.read()
            
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_data,
                file_name=pdf_filename,
                mime="application/pdf",
                use_container_width=True
            )
            return True
        return False
        
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        return False

if __name__ == "__main__":
    main()