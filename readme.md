# ABU Zaria Smart Campus Navigation System  
![Project Banner](https://via.placeholder.com/800x200.png?text=ABU+Zaria+Smart+Campus+Navigation)  

**COEN545 Artificial Intelligence Applications Project**  
*Developed by Group 9*  

---

## 📖 Table of Contents  
- [Introduction](#-introduction)  
- [Features](#-features)  
- [Installation](#-installation)  
- [Usage](#-usage)  
- [Technologies](#-technologies)  
- [Team](#-team)  
- [License](#-license)  
- [Acknowledgements](#-acknowledgements)  
- [Contact](#-contact)  

---

## 🌟 Introduction  
A web-based AI-powered navigation system for Ahmadu Bello University (ABU) Zaria. This project provides:  
- Interactive campus map with 18+ key locations  
- Voice-guided search functionality  
- Real-time walking route optimization  
- Live campus updates (e.g., closures, events)  
- User feedback system  

**Problem Solved**: Addresses navigation challenges for students, staff, and visitors on the large ABU Zaria campus.  

---

## 🚀 Features  
- **Interactive Map**: Google Maps integration with custom markers  
- **Voice Search**: Speech-to-text for hands-free navigation  
- **Route Optimization**: AI-powered shortest-path calculation  
- **Real-Time Updates**: Simulated live alerts about campus status  
- **Feedback System**: SQLite database for user input  

---

## ⚙️ Installation  

### Prerequisites  
- Python 3.8+  
- Google Chrome/Firefox  
- OpenRouteService API Key ([Get Here](https://openrouteservice.org/))  

### Steps  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/Alhibb/COEN545-Artificial-Intelligence-Applications.git  
   cd COEN545-Artificial-Intelligence-Applications  
   ```  

2. Create a virtual environment:  
   ```bash  
   python -m venv venv  
   source venv/bin/activate  # Linux/Mac  
   venv\Scripts\activate     # Windows  
   ```  

3. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  

4. Replace API keys in `app.py`:  
   ```python  
   ORS_API_KEY = 'your_ors_key_here'   
   ```  

5. Initialize the database:  
   ```bash  
   python init_db.py  
   ```  

---

## 🖥️ Usage  
1. Start the Flask server:  
   ```bash  
   python app.py  
   ```  

2. Open in browser:  
   ```  
   http://localhost:5000  
   ```  

3. Use the system:  
   - Allow location access for route calculation  
   - Type or speak your destination  
   - View real-time walking directions  

![Interface Demo](https://via.placeholder.com/600x400.png?text=Map+Interface+Demo)  

---

## 💻 Technologies  
- **Backend**: Flask, SQLite  
- **Mapping**: Folium, Google Maps tiles  
- **AI Components**:  
  - OpenRouteService (Route optimization)  
  - SpeechRecognition (Voice search)  
- **Frontend**: HTML5, Bootstrap, JavaScript  

---

## 👥 Team  
| Name                      | Role                          | GitHub                          |  
|---------------------------|-------------------------------|---------------------------------|  
| Usman Gambo Lawal         | Backend & API Integration     | [@UsmanGL](https://github.com/) |  
| Ibrahim Rabiu             | Mapping Logic                 | [@IbrahimR](https://github.com/alhibb)|  
| Ibrahim AbdulJabbar Hamid | Voice Search Implementation   | [@IbrahimH](https://github.com/)|  
| Maryam Abdulkadir         | Frontend Design               | [@MaryamA](https://github.com/) |  
| Maryam D. Shabbal         | Database & Documentation      | [@MaryamS](https://github.com/) |  

---

## 📜 License  
This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.  

---

## 🙏 Acknowledgements  
- OpenRouteService for routing API  
- Folium team for mapping tools  
- Google for speech-to-text API  

---

## 📧 Contact  
For queries or contributions:  
- **GitHub**: [https://github.com/Alhibb/COEN545-Artificial-Intelligence-Applications](https://github.com/Alhibb/COEN545-Artificial-Intelligence-Applications)  
- **Team Lead**: Usman Gambo Lawal - u19co20@abu.edu.ng  

--- 

*Developed for COEN545 Artificial Intelligence Applications, ABU Zaria - 2023*  
```

**Note**: Replace placeholder images (`via.placeholder.com`) with actual screenshots of your application for the final version.