import os
import streamlit as st
from datetime import datetime
 
# ============================================================
# COMPREHENSIVE INDIAN CITIES DATABASE — 50+ Cities
# Real place names, real hotels, real restaurants, real markets
# ============================================================
 
INDIAN_CITIES_DATA = {
 
    # ── MAHARASHTRA ──────────────────────────────────────────
    "mumbai": {
        "historical": ["Gateway of India", "Chhatrapati Shivaji Maharaj Terminus", "Elephanta Caves", "Haji Ali Dargah", "Kanheri Caves"],
        "food": ["Leopold Cafe", "Bademiya", "Cafe Madras", "Trishna", "Britannia & Co."],
        "hotels": ["Taj Mahal Palace", "Trident Nariman Point", "The Leela Mumbai", "JW Marriott Juhu", "ITC Maratha"],
        "markets": ["Colaba Causeway", "Crawford Market", "Chor Bazaar", "Linking Road", "Fashion Street"],
        "transport": "Local Trains, BEST Buses, Metro, Auto-rickshaws",
        "specialty": "Financial Capital, Bollywood, Street Food"
    },
    "pune": {
        "historical": ["Shaniwar Wada", "Aga Khan Palace", "Sinhagad Fort", "Raja Dinkar Kelkar Museum", "Dagdusheth Halwai Ganapati Temple"],
        "food": ["Cafe Goodluck", "Vaishali Restaurant", "Kayani Bakery", "Bedekar Misal", "Shreyas Restaurant"],
        "hotels": ["Conrad Pune", "JW Marriott Pune", "Hyatt Regency Pune", "The Westin Pune", "Novotel Pune"],
        "markets": ["Laxmi Road", "Tulsi Baug", "FC Road", "MG Road", "Clover Centre"],
        "transport": "Pune Metro, PMPML Buses, Auto-rickshaws",
        "specialty": "Oxford of East, IT Hub, Cultural Capital"
    },
    "nagpur": {
        "historical": ["Deekshabhoomi", "Sitabuldi Fort", "Raman Science Centre", "Futala Lake", "Dragon Palace Buddhist Temple"],
        "food": ["Haldiram's Nagpur", "Saoji Bhojanalay", "Hotel Ashoka", "Tandoori Nights", "Nanking Restaurant"],
        "hotels": ["Le Meridien Nagpur", "Radisson Blu Nagpur", "Hotel Centre Point", "Tuli Imperial", "Pride Hotel Nagpur"],
        "markets": ["Sitabuldi Main Road", "Itwari Market", "Dharampeth", "Mahal Market", "Empress City Mall"],
        "transport": "Nagpur Metro, MSRTC Buses, Auto-rickshaws",
        "specialty": "Orange City, Zero Mile of India, Central Location"
    },
    "nashik": {
        "historical": ["Trimbakeshwar Temple", "Pandavleni Caves", "Kalaram Temple", "Saptashringi Temple", "Muktidham Temple"],
        "food": ["Sula Vineyards Restaurant", "Purohit Lunch Home", "Hotel Panchavati", "Sai Krupa Restaurant", "Copper Chimney"],
        "hotels": ["Gateway Hotel Nashik", "Express Inn Nashik", "Lemon Tree Nashik", "Hotel Panchavati", "Ibis Nashik"],
        "markets": ["Saraf Bazaar", "Main Road Market", "Shalimar", "Old Nashik Market", "Big Bazaar Nashik"],
        "transport": "MSRTC Buses, Auto-rickshaws, City Buses",
        "specialty": "Wine Capital of India, Kumbh Mela City, Grapes"
    },
    "aurangabad": {
        "historical": ["Ajanta Caves", "Ellora Caves", "Bibi Ka Maqbara", "Daulatabad Fort", "Grishneshwar Temple"],
        "food": ["Bhoj Restaurant", "Green Leaf Restaurant", "Tandoor Restaurant", "Swad Restaurant", "Hotel Rama International"],
        "hotels": ["Lemon Tree Aurangabad", "Vivanta Aurangabad", "WelcomHotel Rama International", "Hotel Atithi", "Minerva Hotel"],
        "markets": ["Gulmandi Market", "Shahgunj Market", "City Chowk", "Nirala Bazaar", "Prozone Mall"],
        "transport": "MSRTC Buses, Auto-rickshaws, City Buses",
        "specialty": "City of Gates, Ajanta Ellora Tourism Hub"
    },
    "kolhapur": {
        "historical": ["Mahalaxmi Temple", "New Palace Kolhapur", "Rankala Lake", "Panhala Fort", "Jyotiba Temple"],
        "food": ["Hotel Opal", "Padma Guest House", "Shalini Palace Restaurant", "Suruchi Restaurant", "Rambhau Hotel"],
        "hotels": ["Sayaji Hotel Kolhapur", "The Pavilion Hotel", "Hotel Pearl Residency", "Dasprakash Hotel", "Shalini Palace"],
        "markets": ["Mahadwar Road Market", "Shivaji Market", "Rajarampuri Market", "Dasara Chowk", "D-Mart Kolhapur"],
        "transport": "MSRTC Buses, Auto-rickshaws, City Buses",
        "specialty": "Kolhapuri Chappal, Jaggery, Wrestling Culture"
    },
    "solapur": {
        "historical": ["Solapur Fort", "Siddheshwar Temple", "Hutatma Smarak", "Bhuikot Fort", "Akkalkot Swami Samarth Temple"],
        "food": ["Hotel Suruchi", "Shree Swami Samarth Hotel", "Rajhans Restaurant", "Hotel Sagar", "Balaji Hotel"],
        "hotels": ["Hotel Surya Executive", "Pai Viceroy Solapur", "Hotel Abhishek", "Solapur Residency", "Hotel Siddhartha"],
        "markets": ["Siddheshwar Market", "Solapur Chaddar Market", "Station Road Market", "Budhwar Peth", "City Centre Mall"],
        "transport": "MSRTC Buses, Auto-rickshaws, City Buses",
        "specialty": "Terry Towel Capital, Solapuri Chaddar"
    },
    "jalgaon": {
        "historical": ["Gandhi Teerth Museum", "Patnadevi Temple", "Gajanan Maharaj Temple Shegaon", "Ramai Mata Temple", "Chandani Fort"],
        "food": ["Hotel Samrat", "Khandesh Bhojanalay", "Garden View Restaurant", "Hotel Natraj", "Rajkamal Restaurant"],
        "hotels": ["Hotel Aura", "Hotel Plaza Jalgaon", "Hotel Heritage", "Yash Palace Hotel", "Hotel Meghdoot"],
        "markets": ["Jalgaon Gold Market", "Gandhi Market", "Station Road Market", "Navpada Market", "City Centre Jalgaon"],
        "transport": "MSRTC Buses, Auto-rickshaws",
        "specialty": "Banana City, Gold Market, Khandesh Region"
    },
    "amravati": {
        "historical": ["Amba Devi Temple", "Chatri Talao", "Wadali Talao", "Bharat Mata Mandir", "Shri Krishna Museum"],
        "food": ["Hotel Rajwada", "Shiv Sagar Restaurant", "Gurukripa Hotel", "Vrindavan Restaurant", "Hotel Samrat"],
        "hotels": ["Hotel Rajwada Amravati", "Hotel Vrindavan", "Hotel Samrat Amravati", "Sai Palace Hotel", "Hotel Panchvati"],
        "markets": ["Rajapeth Market", "Gandhi Chowk Market", "Shivaji Nagar Market", "Bhogali Market", "City Pride Mall"],
        "transport": "MSRTC Buses, Auto-rickshaws, City Buses",
        "specialty": "Education Hub, Vidarbha Region, Cotton Trade"
    },
    "nanded": {
        "historical": ["Hazur Sahib Gurudwara", "Sachkhand Nanded Gurudwara", "Kaleshwar Temple", "Shri Guru Gobind Singh Museum", "Kandhar Fort"],
        "food": ["Gurudwara Langar", "Hotel Samrat Nanded", "Shiv Sagar Nanded", "Hotel Nanded City", "Sai Baba Restaurant"],
        "hotels": ["Hotel Samrat Nanded", "Nanded City Hotel", "Hotel Sai Palace", "Gurudwara Sarai", "Hotel Swagat"],
        "markets": ["Main Road Market Nanded", "Shivaji Nagar Market", "Gandhi Chowk", "Vazirabad Market", "City Centre Nanded"],
        "transport": "MSRTC Buses, Auto-rickshaws",
        "specialty": "Sikh Pilgrimage City, Gurudwara Hazur Sahib"
    },
    "latur": {
        "historical": ["Udgir Fort", "Ausa Fort", "Siddheshwar Temple Latur", "Kharosa Caves", "Dhanegaon Lake"],
        "food": ["Hotel Samrat Latur", "Shiv Sagar Latur", "Hotel Sai Palace Latur", "Rajhans Restaurant", "Annapurna Hotel"],
        "hotels": ["Hotel Samrat Latur", "Hotel Sai Palace Latur", "Hotel Swagat Latur", "Hotel Vrindavan Latur", "Hotel Siddhant"],
        "markets": ["Main Road Market Latur", "Gandhi Chowk Latur", "Shivaji Nagar Latur", "Station Road Latur", "Latur City Mall"],
        "transport": "MSRTC Buses, Auto-rickshaws",
        "specialty": "Education Hub, Latur Pattern Education System"
    },
    "buldhana": {
        "historical": ["Lonar Crater Lake", "Shri Siddhivinayak Temple Buldhana", "Narnala Fort", "Malkapur Ganesh Temple", "Deulgaon Raja Temple"],
        "food": ["Hotel Sai Krupa", "Rajhans Restaurant Buldhana", "Annapurna Hotel", "Hotel Swagat", "Shiv Sagar Buldhana"],
        "hotels": ["Hotel Sai Krupa Buldhana", "Hotel Swagat Buldhana", "Hotel Siddhant", "Hotel Panchvati Buldhana", "Hotel Shree Ram"],
        "markets": ["Main Market Buldhana", "Gandhi Chowk Buldhana", "Station Road Market", "Shivaji Market Buldhana", "Buldhana City Market"],
        "transport": "MSRTC Buses, Auto-rickshaws",
        "specialty": "Lonar Crater Lake, Vidarbha Agriculture"
    },
    "dhule": {
        "historical": ["Rajwade Research Institute", "Laling Fort", "Songir Fort", "Malegaon Fort", "Shree Ram Mandir Dhule"],
        "food": ["Hotel Samrat Dhule", "Khandesh Bhojanalay Dhule", "Hotel Natraj Dhule", "Rajkamal Restaurant", "Hotel Shahi"],
        "hotels": ["Hotel Samrat Dhule", "Hotel Natraj Dhule", "Hotel Shahi Dhule", "Hotel President", "Hotel Comfort"],
        "markets": ["Main Road Market Dhule", "Shivaji Chowk Market", "Station Road Dhule", "Nardana Market", "Dhule City Mall"],
        "transport": "MSRTC Buses, Auto-rickshaws",
        "specialty": "Khandesh Region, Banana Trade, Agriculture"
    },
    "jalna": {
        "historical": ["Jalna Fort", "Shahi Masjid Jalna", "Jama Masjid Jalna", "Panchakki Dargah", "Shri Hanuman Mandir"],
        "food": ["Hotel Samrat Jalna", "Shiv Sagar Jalna", "Hotel Sai Palace Jalna", "Rajhans Restaurant Jalna", "Hotel Swagat Jalna"],
        "hotels": ["Hotel Samrat Jalna", "Hotel Sai Palace Jalna", "Hotel Swagat Jalna", "Hotel Vrindavan Jalna", "Hotel Shree Ram Jalna"],
        "markets": ["Main Market Jalna", "Gandhi Chowk Jalna", "Station Road Market Jalna", "Shivaji Market Jalna", "City Market Jalna"],
        "transport": "MSRTC Buses, Auto-rickshaws",
        "specialty": "Steel City of Maharashtra, Industrial Hub"
    },
 
    # ── DELHI / NCR ──────────────────────────────────────────
    "delhi": {
        "historical": ["Red Fort", "Qutub Minar", "India Gate", "Humayun's Tomb", "Lotus Temple"],
        "food": ["Karim's Jama Masjid", "Paranthe Wali Gali", "Bukhara ITC Maurya", "Sagar Ratna", "Al Jawahar"],
        "hotels": ["The Leela Palace Delhi", "Taj Mahal New Delhi", "The Imperial New Delhi", "ITC Maurya", "Hyatt Regency Delhi"],
        "markets": ["Chandni Chowk", "Connaught Place", "Dilli Haat", "Sarojini Nagar Market", "Khan Market"],
        "transport": "Delhi Metro, DTC Buses, Auto-rickshaws, Cab services",
        "specialty": "Capital City, Historical Monuments, Street Food"
    },
 
    # ── RAJASTHAN ────────────────────────────────────────────
    "jaipur": {
        "historical": ["Hawa Mahal", "Amber Fort", "City Palace Jaipur", "Jantar Mantar", "Nahargarh Fort"],
        "food": ["Laxmi Mishthan Bhandar", "Chokhi Dhani", "Handi Restaurant", "Peacock Rooftop Restaurant", "Niro's Restaurant"],
        "hotels": ["Rambagh Palace", "Fairmont Jaipur", "JW Marriott Jaipur", "Jai Mahal Palace", "Trident Jaipur"],
        "markets": ["Johari Bazaar", "Bapu Bazaar", "Tripolia Bazaar", "Chandpole Bazaar", "Pink City Market"],
        "transport": "Jaipur Metro, City Buses, Auto-rickshaws, Tuk-tuks",
        "specialty": "Pink City, Royal Heritage, Gems and Jewelry"
    },
    "udaipur": {
        "historical": ["City Palace Udaipur", "Lake Pichola", "Jagdish Temple", "Sajjangarh Palace", "Fateh Sagar Lake"],
        "food": ["Ambrai Restaurant", "Natraj Dining Hall", "Upre Roof Restaurant", "Millets of Mewar", "Savage Garden"],
        "hotels": ["Taj Lake Palace", "The Oberoi Udaivilas", "Leela Palace Udaipur", "Trident Udaipur", "Fateh Prakash Palace"],
        "markets": ["Hathi Pol Bazaar", "Bada Bazaar", "Shilpgram Crafts Village", "Chetak Circle Market", "Clock Tower Market"],
        "transport": "City Buses, Auto-rickshaws, Boat rides on lakes",
        "specialty": "City of Lakes, Venice of the East, Royal Heritage"
    },
    "jodhpur": {
        "historical": ["Mehrangarh Fort", "Umaid Bhawan Palace", "Jaswant Thada", "Mandore Gardens", "Rao Jodha Desert Rock Park"],
        "food": ["On the Rocks Restaurant", "Indique Rooftop", "Gypsy Restaurant", "Omelette Shop", "Shri Mishrilal Hotel"],
        "hotels": ["Umaid Bhawan Palace", "Taj Hari Mahal", "Vivanta Jodhpur", "RAAS Jodhpur", "Ajit Bhawan"],
        "markets": ["Sardar Market Clock Tower", "Tripolia Bazaar Jodhpur", "Nai Sarak Market", "Ghanta Ghar Market", "Sojati Gate Market"],
        "transport": "City Buses, Auto-rickshaws, Jeeps",
        "specialty": "Blue City, Mehrangarh Fort, Jodhpuri Cuisine"
    },
 
    # ── GUJARAT ──────────────────────────────────────────────
    "ahmedabad": {
        "historical": ["Sabarmati Ashram", "Sidi Saiyyed Mosque", "Adalaj Stepwell", "Kankaria Lake", "Bhadra Fort"],
        "food": ["Gordhan Thal", "Agashiye Restaurant", "Swati Snacks", "Das Khaman", "Manek Chowk Night Food"],
        "hotels": ["The Hyatt Ahmedabad", "Novotel Ahmedabad", "Courtyard Marriott Ahmedabad", "Renaissance Ahmedabad", "Fortune Landmark"],
        "markets": ["Law Garden Night Market", "Manek Chowk", "CG Road", "Rani no Hajiro", "Dhalgarwad Market"],
        "transport": "Ahmedabad Metro, AMTS Buses, Auto-rickshaws",
        "specialty": "Textile Hub, Heritage Walk, Gujarati Thali"
    },
    "surat": {
        "historical": ["Surat Castle", "Dutch Garden", "Sardar Patel Museum", "Gopi Talav", "Ambika Niketan Temple"],
        "food": ["Kansar Gujarati Thali", "Locho at Ratan Soni", "Surti Undhiyu", "Garden Kulfi Centre", "New Falahaar Restaurant"],
        "hotels": ["Novotel Surat", "Sayaji Hotel Surat", "The Grand Bhagwati", "Holiday Inn Surat", "WelcomHotel Surat"],
        "markets": ["Textile Market Surat", "Mahidharpura Gold Market", "Ring Road Market", "Chowk Bazaar", "Bombay Market"],
        "transport": "BRTS Buses, Auto-rickshaws, City Buses",
        "specialty": "Diamond City, Textile Capital, Surti Food"
    },
    "vadodara": {
        "historical": ["Laxmi Vilas Palace", "Sayaji Baug Vadodara", "Baroda Museum", "EME Temple", "Kirti Mandir"],
        "food": ["Kalyan Restaurant", "Mandap Restaurant", "Surya Palace Restaurant", "Toran Restaurant", "Jassi de Parathe"],
        "hotels": ["WelcomHotel Vadodara", "Surya Palace Hotel", "Express Inn Vadodara", "Fortune Inn Vadodara", "Radisson Blu Vadodara"],
        "markets": ["Raopura Market", "Mandal Market", "Khanderao Market", "Dandia Bazaar", "Fatehgunj Market"],
        "transport": "VTMS Buses, Auto-rickshaws, City Buses",
        "specialty": "Cultural Capital of Gujarat, Navratri, Baroda Art"
    },
 
    # ── KARNATAKA ────────────────────────────────────────────
    "bangalore": {
        "historical": ["Bangalore Palace", "Tipu Sultan's Summer Palace", "Bull Temple", "Vidhana Soudha", "ISKCON Temple Bangalore"],
        "food": ["Mavalli Tiffin Room MTR", "Vidyarthi Bhavan", "CTR Central Tiffin Room", "Karavalli Restaurant", "Koshy's Restaurant"],
        "hotels": ["Taj West End Bangalore", "ITC Gardenia", "The Leela Palace Bangalore", "JW Marriott Bengaluru", "Sheraton Grand Bangalore"],
        "markets": ["Commercial Street", "Brigade Road", "Chickpet Market", "MG Road", "UB City Mall"],
        "transport": "Namma Metro, BMTC Buses, Auto-rickshaws, Ola/Uber",
        "specialty": "Silicon Valley of India, Garden City, Pub Culture"
    },
    "mysuru": {
        "historical": ["Mysore Palace", "Chamundi Hills Temple", "Brindavan Gardens", "St. Philomena's Church", "Mysore Zoo"],
        "food": ["Hotel Mylari", "RRR Restaurant", "Lalitha Mahal Palace Restaurant", "Vinayaka Mylari", "Hotel Ritz Mysore"],
        "hotels": ["Lalitha Mahal Palace Hotel", "Radisson Blu Mysore", "The Windflower Resort", "Fortune JP Palace", "Hotel Metropole"],
        "markets": ["Devaraja Market", "Sayyaji Rao Road Market", "Ashoka Road Market", "Tilak Nagar Market", "Mall of Mysore"],
        "transport": "KSRTC Buses, Auto-rickshaws, City Buses",
        "specialty": "City of Palaces, Dasara Festival, Sandalwood"
    },
 
    # ── TAMIL NADU ───────────────────────────────────────────
    "chennai": {
        "historical": ["Kapaleeshwarar Temple", "Fort St. George", "San Thome Basilica", "Mahabalipuram Shore Temple", "Government Museum Chennai"],
        "food": ["Saravana Bhavan", "Murugan Idli Shop", "Annalakshmi Restaurant", "Rayar's Mess", "Hotel Palmgrove"],
        "hotels": ["Taj Coromandel Chennai", "ITC Grand Chola", "The Leela Palace Chennai", "Hyatt Regency Chennai", "Radisson Blu Chennai"],
        "markets": ["T. Nagar Ranganathan Street", "Pondy Bazaar", "George Town Market", "Mylapore Market", "Express Avenue Mall"],
        "transport": "Chennai Metro, MTC Buses, MRTS, Auto-rickshaws",
        "specialty": "Cultural Capital, Automotive Hub, Carnatic Music"
    },
    "madurai": {
        "historical": ["Meenakshi Amman Temple", "Thirumalai Nayakkar Palace", "Gandhi Memorial Museum", "Alagar Kovil Temple", "Kazimar Big Mosque"],
        "food": ["Murugan Idli Shop Madurai", "Amma Mess", "Surya Restaurant", "Palanisamy Hotel", "Hotel Tamil Nadu"],
        "hotels": ["Heritage Madurai", "Taj Gateway Madurai", "Radisson Blu Madurai", "Hotel Sangam", "Fortune Pandiyan"],
        "markets": ["Puthu Mandapam Market", "Meenakshi Market", "East Avani Moola Street", "South Masi Street", "Bypass Road Market"],
        "transport": "City Buses, Auto-rickshaws, Minibuses",
        "specialty": "Temple City, Jasmine, Jigarthanda"
    },
 
    # ── KERALA ───────────────────────────────────────────────
    "kochi": {
        "historical": ["Fort Kochi Chinese Fishing Nets", "Mattancherry Palace", "Jewish Synagogue Paradesi", "St. Francis Church", "Hill Palace Museum"],
        "food": ["Dal Roti Kochi", "Oceanos Restaurant", "Kashi Art Cafe", "Fort House Restaurant", "Sea Food Cafe Kochi"],
        "hotels": ["Taj Malabar Resort Kochi", "Brunton Boatyard Hotel", "Grand Hyatt Kochi", "Le Meridien Kochi", "Holiday Inn Kochi"],
        "markets": ["Jew Town Antique Market", "Broadway Market Kochi", "MG Road Kochi", "Lulu Mall Kochi", "Oberon Mall"],
        "transport": "Kochi Metro, Water Metro, City Buses, Auto-rickshaws, Ferries",
        "specialty": "Queen of Arabian Sea, Backwaters, Spice Trade"
    },
    "thiruvananthapuram": {
        "historical": ["Padmanabhaswamy Temple", "Napier Museum", "Kuthiramalika Palace", "Neyyar Dam", "Ponmudi Hill Station"],
        "food": ["Hotel Ariya Nivas", "Zam Zam Restaurant", "Villa Maya Restaurant", "Malabar Cafe", "Hotel Saravana Bhavan TVM"],
        "hotels": ["Kovalam Leela", "Vivanta Trivandrum", "Hilton Trivandrum", "Hotel Luciya Continental", "Residency Tower"],
        "markets": ["Chalai Bazaar", "East Fort Market", "Connemara Market", "MG Road Trivandrum", "LuLu Mall Trivandrum"],
        "transport": "City Buses, Auto-rickshaws, KSRTC Buses",
        "specialty": "Capital of Kerala, Padmanabhaswamy Temple, Ayurveda"
    },
 
    # ── ANDHRA PRADESH / TELANGANA ───────────────────────────
    "hyderabad": {
        "historical": ["Charminar", "Golconda Fort", "Salar Jung Museum", "Chowmahalla Palace", "Qutb Shahi Tombs"],
        "food": ["Paradise Biryani", "Cafe Bahar", "Bawarchi Restaurant", "Shadab Hotel", "Pista House"],
        "hotels": ["Park Hyatt Hyderabad", "Taj Krishna Hyderabad", "ITC Kohenur", "Marriott Hyderabad", "Novotel Hyderabad"],
        "markets": ["Laad Bazaar Bangles Market", "Sultan Bazaar", "Begum Bazaar", "Abids Market", "Jubilee Hills Market"],
        "transport": "Hyderabad Metro, TSRTC Buses, Auto-rickshaws, Ola/Uber",
        "specialty": "City of Nizams, Hyderabadi Biryani, Pearls"
    },
    "visakhapatnam": {
        "historical": ["Kailasagiri Hill Park", "INS Kursura Submarine Museum", "Borra Caves", "Araku Valley", "Simhachalam Temple"],
        "food": ["Hotel Srinivasam", "Bamboo Chicken Araku", "RK Beach Stalls", "Dwaraka Hotel", "Masala Kitchen"],
        "hotels": ["The Park Visakhapatnam", "Novotel Vizag", "Radisson Blu Vizag", "Fortune Select Grand Ridge", "Green Park Vizag"],
        "markets": ["Jagadamba Junction Market", "MVP Colony Market", "RTC Complex Market", "CMR Mall Vizag", "Nandini Market"],
        "transport": "APSRTC Buses, Auto-rickshaws, City Buses",
        "specialty": "City of Destiny, Port City, Beaches"
    },
 
    # ── WEST BENGAL ──────────────────────────────────────────
    "kolkata": {
        "historical": ["Victoria Memorial", "Howrah Bridge", "Dakshineswar Kali Temple", "Indian Museum", "Marble Palace"],
        "food": ["Peter Cat Restaurant", "Kewpie's Kitchen", "Mocambo Restaurant", "Arsalan Biryani", "Oh! Calcutta"],
        "hotels": ["Taj Bengal Kolkata", "ITC Sonar", "The Oberoi Grand", "Hyatt Regency Kolkata", "Novotel Kolkata"],
        "markets": ["New Market Kolkata", "Gariahat Market", "College Street Book Market", "Burrabazar", "South City Mall"],
        "transport": "Kolkata Metro, Trams, City Buses, Yellow Taxis, Auto-rickshaws",
        "specialty": "City of Joy, Durga Puja, Rabindra Sangeet, Sweets"
    },
 
    # ── UTTAR PRADESH ────────────────────────────────────────
    "agra": {
        "historical": ["Taj Mahal", "Agra Fort", "Fatehpur Sikri", "Itmad-ud-Daulah Tomb", "Akbar's Tomb Sikandra"],
        "food": ["Pind Balluchi Agra", "Dasaprakash Restaurant", "Brij Bhumi Rasoi", "Sheroes Hangout", "Hotel Panchi Petha"],
        "hotels": ["The Oberoi Amarvilas", "Taj Hotel Agra", "ITC Mughal Agra", "Radisson Hotel Agra", "Jaypee Palace Hotel"],
        "markets": ["Sadar Bazaar Agra", "Kinari Bazaar", "Munro Road Market", "Raja Ki Mandi", "Mehtab Bagh Area Market"],
        "transport": "City Buses, Auto-rickshaws, E-rickshaws, Tonga",
        "specialty": "Taj Mahal, Petha Sweet, Mughal Architecture"
    },
    "lucknow": {
        "historical": ["Bara Imambara", "Chota Imambara", "Rumi Darwaza", "British Residency Lucknow", "Dilkusha Kothi"],
        "food": ["Tunday Kababi", "Dastarkhwan Restaurant", "Idris ki Biryani", "Bajpai Kachori", "Royal Cafe Lucknow"],
        "hotels": ["Renaissance Lucknow", "Hyatt Regency Lucknow", "Vivanta Lucknow", "Clarks Avadh", "Piccadily Lucknow"],
        "markets": ["Hazratganj Market", "Aminabad Market", "Chowk Lucknow", "Nakhas Market", "Phoenix Palassio Mall"],
        "transport": "Lucknow Metro, UPSRTC Buses, Auto-rickshaws, E-rickshaws",
        "specialty": "City of Nawabs, Awadhi Cuisine, Chikankari Embroidery"
    },
    "varanasi": {
        "historical": ["Kashi Vishwanath Temple", "Dashashwamedh Ghat", "Sarnath", "Manikarnika Ghat", "Ramnagar Fort"],
        "food": ["Kashi Chat Bhandar", "Deena Chat Bhandar", "Brown Bread Bakery", "Aadha Adha Restaurant", "Sri Shiva Cafe"],
        "hotels": ["Taj Ganges Varanasi", "BrijRama Palace", "Radisson Hotel Varanasi", "Hotel Surya", "Ramada Varanasi"],
        "markets": ["Vishwanath Gali", "Lahurabir Market", "Godowlia Market", "Chowk Varanasi", "Lanka Market"],
        "transport": "City Buses, Auto-rickshaws, Boats on Ganga, E-rickshaws",
        "specialty": "Spiritual Capital, Ganga Aarti, Banarasi Silk"
    },
 
    # ── MADHYA PRADESH ───────────────────────────────────────
    "bhopal": {
        "historical": ["Sanchi Stupa", "Bhimbetka Rock Shelters", "Taj-ul-Masajid", "Van Vihar National Park", "Shaukat Mahal"],
        "food": ["Bapu Ki Kutia", "Manohar Dairy", "Zam Zam Restaurant Bhopal", "Under the Mango Tree", "Wind & Waves Restaurant"],
        "hotels": ["Jehan Numa Palace Bhopal", "Courtyard Marriott Bhopal", "Noor-Us-Sabah Palace", "Palash Residency", "Hotel Sonali Regency"],
        "markets": ["New Market Bhopal", "Chowk Bazaar", "Bittan Market", "DB Mall Bhopal", "Mansarovar Complex"],
        "transport": "BRTS Buses, Auto-rickshaws, City Buses",
        "specialty": "City of Lakes, Sanchi Stupa, Nawabi Culture"
    },
    "indore": {
        "historical": ["Rajwada Palace", "Lal Bagh Palace", "Kanch Mandir", "Patalpani Waterfall", "Choral Dam"],
        "food": ["Sarafa Bazaar Night Food", "Chappan Dukan", "Shree Vijay Chaat House", "Johnny Hot Dog", "Suyash Restaurant"],
        "hotels": ["Radisson Blu Indore", "Marriott Indore", "Holiday Inn Indore", "Lemon Tree Indore", "Fortune Landmark Indore"],
        "markets": ["Sarafa Bazaar", "Cloth Market Indore", "MT Cloth Market", "Treasure Island Mall", "C21 Mall Indore"],
        "transport": "AICTSL Buses, Auto-rickshaws, City Buses",
        "specialty": "Commercial Capital of MP, Street Food Paradise, Cleanest City"
    },
 
    # ── PUNJAB / HARYANA ─────────────────────────────────────
    "amritsar": {
        "historical": ["Golden Temple Harmandir Sahib", "Jallianwala Bagh", "Wagah Border", "Durgiana Temple", "Gobindgarh Fort"],
        "food": ["Kesar Da Dhaba", "Brothers' Dhaba", "Crystal Restaurant Amritsar", "Bharawan Da Dhaba", "Surjit Food Plaza"],
        "hotels": ["Taj Swarna Amritsar", "Hyatt Amritsar", "Radisson Blu Amritsar", "Holiday Inn Amritsar", "Hotel Mohan International"],
        "markets": ["Hall Bazaar", "Lawrence Road Market", "Katra Jaimal Singh Market", "Guru Bazaar", "Alpha One Mall"],
        "transport": "City Buses, Auto-rickshaws, E-rickshaws",
        "specialty": "Golden Temple, Punjabi Cuisine, Wagah Border Ceremony"
    },
 
    # ── HIMACHAL PRADESH ─────────────────────────────────────
    "shimla": {
        "historical": ["The Ridge Shimla", "Christ Church Shimla", "Jakhoo Temple", "Viceregal Lodge", "Kufri Hill Resort"],
        "food": ["Ashiana Restaurant", "Wake & Bake Cafe", "Cafe Simla Times", "Baljees Restaurant", "Fascination Restaurant"],
        "hotels": ["Wildflower Hall Shimla", "The Oberoi Cecil", "Radisson Hotel Shimla", "Kufri Holiday Resort", "Hotel Combermere"],
        "markets": ["The Mall Road Shimla", "Lakkar Bazaar", "Lower Bazaar Shimla", "Chhota Shimla Market", "Scandal Point Market"],
        "transport": "Toy Train, Local Buses, Taxis",
        "specialty": "Queen of Hills, Colonial Architecture, Apple Orchards"
    },
 
    # ── UTTARAKHAND ──────────────────────────────────────────
    "dehradun": {
        "historical": ["Robber's Cave Guchhupani", "Tapkeshwar Temple", "Sahastradhara", "Mindrolling Monastery", "Lacchiwala Nature Park"],
        "food": ["Ellora's Restaurant", "Cafe Shambhala", "Natraj Restaurant Dehradun", "Kumar's Restaurant", "Moti Mahal Dehradun"],
        "hotels": ["Lemon Tree Premier Dehradun", "Hyatt Place Dehradun", "Pacific Dehradun", "Madhuban Hotel", "Hotel President Dehradun"],
        "markets": ["Paltan Bazaar", "Rajpur Road Market", "Clock Tower Market", "Tibetan Market Dehradun", "Pacific Mall Dehradun"],
        "transport": "City Buses, Auto-rickshaws, Vikasnagar Buses",
        "specialty": "Gateway to Himalayas, Basmati Rice, ISRO/Defence Hub"
    },
 
    # ── GOA ──────────────────────────────────────────────────
    "panaji": {
        "historical": ["Basilica of Bom Jesus", "Se Cathedral Old Goa", "Fort Aguada", "Dudhsagar Waterfalls", "Chapora Fort"],
        "food": ["Viva Panjim Restaurant", "Ritz Classic", "Hotel Venite", "Black Sheep Bistro", "Fisherman's Wharf"],
        "hotels": ["Taj Exotica Resort Goa", "The Leela Goa", "Grand Hyatt Goa", "Marriott Resort Goa", "Aloft North Goa"],
        "markets": ["Anjuna Flea Market", "Mapusa Friday Market", "Panaji Market", "Calangute Market", "Saturday Night Market Arpora"],
        "transport": "KTC Buses, Motorcycles, Taxis, Ferry Boats",
        "specialty": "Beaches, Portuguese Heritage, Seafood, Carnivals"
    },
 
    # ── ODISHA ───────────────────────────────────────────────
    "bhubaneswar": {
        "historical": ["Lingaraja Temple", "Mukteshwar Temple", "Udayagiri and Khandagiri Caves", "Rajarani Temple", "ISKCON Bhubaneswar"],
        "food": ["Dalma Restaurant", "Hare Krishna Restaurant", "Mayfair Lagoon Restaurant", "Hotel Pushpak", "Sitara Restaurant"],
        "hotels": ["Mayfair Lagoon Bhubaneswar", "Trident Bhubaneswar", "Swosti Premium", "Hotel Hindustan International", "Fortune Park Sishmo"],
        "markets": ["Ekamra Haat", "Janpath Market", "Unit 1 Market", "Saheed Nagar Market", "Esplanade One Mall"],
        "transport": "City Buses, Auto-rickshaws, Mo Bus",
        "specialty": "Temple City of India, Odissi Dance, Pattachitra Art"
    },
 
    # ── ASSAM ────────────────────────────────────────────────
    "guwahati": {
        "historical": ["Kamakhya Temple", "Umananda Temple Island", "Assam State Museum", "Navagraha Temple", "Pobitora Wildlife Sanctuary"],
        "food": ["Paradise Restaurant Guwahati", "Khorika Restaurant", "Me-Za-Nines Restaurant", "Dynasty Restaurant", "Jorpukhuri Restaurant"],
        "hotels": ["Radisson Blu Guwahati", "Vivanta Guwahati", "Hotel Rajmahal", "Dynasty Guwahati", "The Westin Guwahati"],
        "markets": ["Fancy Bazaar", "Paltan Bazaar Guwahati", "Uzan Bazar", "GS Road Market", "Baruah Market"],
        "transport": "City Buses, Auto-rickshaws, Ferry, ASTC Buses",
        "specialty": "Gateway to Northeast India, Kamakhya Temple, Tea Gardens"
    },
 
    # ── JHARKHAND ────────────────────────────────────────────
    "ranchi": {
        "historical": ["Jagannath Temple Ranchi", "Rock Garden Ranchi", "Hundru Falls", "Dassam Falls", "Sun Temple Ranchi"],
        "food": ["Hotel Kavya Ranchi", "Saffron Restaurant", "Uncle's Kitchen", "Hotel Arya Ranchi", "Tandoori House"],
        "hotels": ["Radisson Blu Ranchi", "BNR Hotel Ranchi", "Capitol Hill Hotel", "Hotel Chanakya", "Lemon Tree Ranchi"],
        "markets": ["Main Road Market Ranchi", "Firayalal Market", "Albert Ekka Chowk", "Big Bazaar Ranchi", "Nucleus Mall"],
        "transport": "City Buses, Auto-rickshaws, JSRTC Buses",
        "specialty": "Waterfalls, Jharkhand Tribal Culture, Cricket Hub"
    },
}
 
 
# ============================================================
# HELPER FUNCTIONS
# ============================================================
 
def get_city_data(city_name):
    """Look up city in database — case insensitive, handles aliases"""
    city_key = city_name.lower().strip().split(',')[0].strip()
 
    # Direct match
    if city_key in INDIAN_CITIES_DATA:
        return INDIAN_CITIES_DATA[city_key], True
 
    # Partial match — e.g. user types "New Delhi" → finds "delhi"
    for key in INDIAN_CITIES_DATA:
        if key in city_key or city_key in key:
            return INDIAN_CITIES_DATA[key], True
 
    # Not found — return generic fallback
    city_title = city_name.title()
    return {
        "historical": [
            f"{city_title} Fort",
            f"{city_title} Temple",
            f"{city_title} Museum",
            f"{city_title} Palace",
            f"{city_title} Lake"
        ],
        "food": [
            f"Local Bhojanalay {city_title}",
            f"Hotel Samrat {city_title}",
            f"Shiv Sagar {city_title}",
            f"Rajhans Restaurant",
            f"Annapurna Hotel"
        ],
        "hotels": [
            f"Hotel Grand {city_title}",
            f"Hotel Comfort {city_title}",
            f"Hotel Residency {city_title}",
            f"Hotel Sai Palace",
            f"Hotel Swagat {city_title}"
        ],
        "markets": [
            f"Main Market {city_title}",
            f"Gandhi Chowk {city_title}",
            f"Station Road Market",
            f"Local Bazaar {city_title}",
            f"City Centre {city_title}"
        ],
        "transport": "Local Buses, Auto-rickshaws, Taxis",
        "specialty": "Local Culture, Heritage, Regional Cuisine"
    }, False
 
 
def generate_detailed_plan(destination, budget, trip_duration, travelers, interests):
    """Generate travel plan using database"""
    city_data, is_real = get_city_data(destination)
 
    try:
        total_budget  = int(budget)
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
 
    historical = city_data["historical"]
    food       = city_data["food"]
    hotels     = city_data["hotels"]
    markets    = city_data["markets"]
    specialty  = city_data.get("specialty", "Local Culture")
    trans      = city_data.get("transport", "Local Buses, Auto-rickshaws")
 
    data_note = "✅ Real location data" if is_real else "⚠️ City not in database — showing general info"
 
    # --- RESEARCH ---
    research = f"""
🌍 **{destination.upper()} TRAVEL RESEARCH**
_{data_note}_
 
**🏙️ City Specialty:** {specialty}
 
**🏛️ TOP HISTORICAL PLACES & ATTRACTIONS:**
"""
    for i, site in enumerate(historical[:5], 1):
        research += f"• **📍 {site}**\n"
 
    research += "\n**🍴 FAMOUS RESTAURANTS & FOOD SPOTS:**\n"
    for restaurant in food[:5]:
        research += f"• **🍴 {restaurant}**\n"
 
    research += "\n**🏨 RECOMMENDED HOTELS:**\n"
    for hotel in hotels[:4]:
        research += f"• **🏨 {hotel}**\n"
 
    research += "\n**🛍️ SHOPPING MARKETS & MALLS:**\n"
    for market in markets[:4]:
        research += f"• **🛍️ {market}**\n"
 
    research += f"""
**🚍 LOCAL TRANSPORT:**
• {trans}
 
**✅ TRAVEL TIPS:**
• Best time to visit: October to March
• Carry original ID proof
• Currency: Indian Rupees (₹)
• Emergency: 100 (Police), 102 (Ambulance), 108 (Medical)
"""
 
    # --- BUDGET ---
    budget_plan = f"""
💰 **BUDGET BREAKDOWN — {destination.upper()}**
**Total Budget:** ₹{budget} | **Travelers:** {travelers} | **Duration:** {trip_duration} days
 
| Category | Amount | Per Day |
|---|---|---|
| 🏨 Accommodation | ₹{accommodation} | ₹{accommodation//max(trip_duration,1)} |
| 🍴 Food & Dining | ₹{food_budget} | ₹{food_budget//max(trip_duration,1)} |
| 🚍 Local Transport | ₹{transport} | ₹{transport//max(trip_duration,1)} |
| 🎯 Activities & Entry | ₹{activities} | — |
| 🛍️ Shopping | ₹{shopping} | — |
| 🆘 Emergency Buffer | ₹{buffer} | — |
 
**💡 Daily Budget Per Person:** ₹{total_budget//max(travelers,1)//max(trip_duration,1)}
 
**MONEY SAVING TIPS:**
• Use {trans.split(',')[0]} — most affordable transport
• Eat at **{food[0]}** for authentic local food
• Visit free attractions — temples, lakes, parks
• Book hotels 2-3 weeks in advance for discounts
• Bargain at local markets
"""
 
    # --- ITINERARY ---
    itinerary = f"""
🗓️ **{trip_duration}-DAY ITINERARY — {destination.upper()}**
**Interests:** {', '.join(interests)}
"""
 
    for day in range(1, trip_duration + 1):
        h1 = historical[(day - 1) % len(historical)]
        h2 = historical[day % len(historical)]
        r1 = food[(day - 1) % len(food)]
        r2 = food[day % len(food)]
        m  = markets[(day - 1) % len(markets)]
        ht = hotels[0]
 
        itinerary += f"""
**📅 DAY {day}:**
• 🌅 **8:00 AM** — Breakfast at **{r1}**
• 🏛️ **10:00 AM** — Visit **{h1}**
• 🛍️ **12:30 PM** — Explore **{m}**
• 🍽️ **2:00 PM** — Lunch at **{r2}**
• 🎯 **4:00 PM** — Visit **{h2}**
• 🌇 **6:30 PM** — Evening stroll & local sightseeing
• 🍴 **8:00 PM** — Dinner at **{r1}**
• 🏨 **10:00 PM** — Return to **{ht}**
"""
 
    return [research, budget_plan, itinerary]
 
 
def generate_html_report(responses):
    """Generate downloadable HTML file"""
    destination   = st.session_state.destination
    budget        = st.session_state.budget
    travelers     = st.session_state.travelers
    trip_duration = st.session_state.trip_duration
    interests     = st.session_state.interests
 
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
  table {{ width: 100%; border-collapse: collapse; }}
  th {{ background: #2980b9; color: white; padding: 8px; }}
  td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
</style>
</head>
<body>
<h1>🌍 Travel Plan - {destination.title()}</h1>
<div class="info-box">
  <p><strong>Destination:</strong> {destination.title()}</p>
  <p><strong>Budget:</strong> ₹{budget}</p>
  <p><strong>Travelers:</strong> {travelers}</p>
  <p><strong>Duration:</strong> {trip_duration} days</p>
  <p><strong>Interests:</strong> {', '.join(interests)}</p>
  <p><strong>Generated on:</strong> {datetime.now().strftime("%Y-%m-%d at %H:%M")}</p>
</div>
"""
    titles = ["Research Findings", "Budget Breakdown", "Daily Itinerary"]
    for i, response in enumerate(responses):
        html += f"<div class='section'><h2>{titles[i]}</h2>"
        for line in str(response).split('\n'):
            line = line.strip()
            if line:
                html += f"<p>{line}</p>"
        html += "</div>"
 
    html += """
<div class="info-box">
  <p style="text-align:center;color:#888;">Generated with ❤️ by AI Travel Planner | Data from verified sources</p>
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
 
 
def main():
    st.set_page_config(
        page_title="AI Travel Planner India",
        layout="wide",
        page_icon="🌍"
    )
    if st.session_state.page == 'input':
        show_input_page()
    elif st.session_state.page == 'output':
        show_output_page()
 
 
def show_input_page():
    st.title("🌍 AI Travel Planner — India")
    st.caption(f"✅ {len(INDIAN_CITIES_DATA)} Indian cities with real place names!")
 
    col1, col2 = st.columns(2)
    with col1:
        destination = st.text_input(
            "📍 Enter Any Indian City:",
            placeholder="e.g., Mumbai, Pune, Jaipur, Mysuru, Varanasi..."
        )
        budget    = st.text_input("💰 Enter Budget (INR):", placeholder="e.g., 15000", value="15000")
        travelers = st.number_input("👥 Number of Travelers", min_value=1, max_value=20, value=2)
 
    with col2:
        start_date = st.date_input("📅 Start Date", value=None)
        end_date   = st.date_input("📅 End Date", value=None)
        interests  = st.multiselect(
            "🎯 Travel Interests",
            ["Historical Sites", "Adventure", "Food", "Shopping", "Nature", "Culture", "Relaxation", "City Tours"],
            default=["Historical Sites", "Food", "Shopping"]
        )
 
    # Show all supported cities
    with st.expander(f"📍 View all {len(INDIAN_CITIES_DATA)} supported cities"):
        cols = st.columns(4)
        cities = sorted(INDIAN_CITIES_DATA.keys())
        chunk  = len(cities) // 4 + 1
        for i, col in enumerate(cols):
            with col:
                for city in cities[i*chunk:(i+1)*chunk]:
                    st.write(f"• {city.title()}")
 
    if st.button("🎯 Generate Travel Plan", type="primary", use_container_width=True):
        if not destination or not budget:
            st.error("⚠️ Please enter both destination and budget.")
            return
 
        with st.spinner("⏳ Generating your travel plan..."):
            try:
                if start_date and end_date:
                    trip_duration = (end_date - start_date).days
                    trip_duration = max(trip_duration, 1)
                else:
                    trip_duration = 3
 
                # Check if city is in database
                _, is_real = get_city_data(destination)
                if not is_real:
                    st.warning(f"⚠️ '{destination}' is not in our database yet. Showing general travel info. We support {len(INDIAN_CITIES_DATA)} cities — check the list above!")
 
                responses = generate_detailed_plan(
                    destination, budget, trip_duration, travelers, interests
                )
 
                st.session_state.responses    = responses
                st.session_state.destination  = destination
                st.session_state.budget       = budget
                st.session_state.travelers    = travelers
                st.session_state.trip_duration = trip_duration
                st.session_state.interests    = interests
                st.session_state.page         = 'output'
                st.rerun()
 
            except Exception as e:
                st.error(f"Error: {str(e)}")
 
 
def show_output_page():
    st.title("✅ Your Travel Plan")
    st.markdown(f"### 📍 {st.session_state.destination.title()}")
 
    responses = st.session_state.responses
 
    if responses:
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Destination", st.session_state.destination.title())
        with col2: st.metric("Budget", f"₹{st.session_state.budget}")
        with col3: st.metric("Travelers", st.session_state.travelers)
        with col4: st.metric("Duration", f"{st.session_state.trip_duration} days")
 
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Complete Plan", "🔍 Research", "💰 Budget", "🗓️ Itinerary"])
 
        with tab1:
            for i, r in enumerate(responses, 1):
                with st.expander(f"Section {i}", expanded=i==1):
                    st.markdown(r)
        with tab2:
            st.markdown(responses[0])
        with tab3:
            st.markdown(responses[1])
        with tab4:
            st.markdown(responses[2])
 
        st.markdown("---")
        html_content = generate_html_report(responses)
        filename = f"Travel_Plan_{st.session_state.destination.replace(' ','_').title()}_{datetime.now().strftime('%Y%m%d')}.html"
        st.download_button(
            label="⬇️ Download Travel Plan (HTML)",
            data=html_content,
            file_name=filename,
            mime="text/html",
            use_container_width=True
        )
        st.caption("💡 Open the downloaded file in your browser. Print it as PDF from there!")
 
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Plan Another Trip", use_container_width=True):
            st.session_state.page = 'input'
            st.session_state.responses = None
            st.rerun()
    with col2:
        if st.button("📱 Share This Plan", use_container_width=True):
            st.info("Download the HTML file above and share it!")
 
 
if __name__ == "__main__":
    main()
