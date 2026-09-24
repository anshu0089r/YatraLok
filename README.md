# 🛡️ YatraLok

### Smart Tourist Safety Monitoring & Incident Response System

YatraLok is a tourist safety and incident-response platform designed to connect **Tourists, Police, and Administrators** through a unified system.

The platform enables tourists to travel using **Trip Mode**, receive warnings when entering unsafe geo-fenced areas, share live locations during active trips, and send emergency SOS alerts. These alerts are delivered to the Police Dashboard in real time, where officers can manage an incident through its complete lifecycle—from creation to closure.

---

## 🎯 Project Objective

The objective of YatraLok is to build a complete tourist safety ecosystem rather than only an SOS or location-tracking application.

The core system flow is:

```text
Tourist
   ↓
Trip & Location Monitoring
   ↓
Risk / Geo-fence Detection
   ↓
SOS Alert
   ↓
Police Dashboard
   ↓
Police Response
   ↓
Incident Resolution
   ↓
Records & Analytics
```

---

## ✨ Core Features

### 📱 Tourist Application

* Tourist Registration and Login
* Unique Digital Tourist ID
* Tourist Profile
* Emergency Contacts
* Start / End Trip Mode
* Live GPS Location Tracking
* Map Integration
* Circular Geo-fence Detection
* Unsafe Zone Warning
* One-Tap SOS
* Travel History
* Last Known Location
* Offline Location Caching and Synchronization

### 👮 Police Dashboard

* Police Authentication
* View Active Tourists
* View Tourist Location
* Receive Real-Time SOS Alerts
* View Incident Details
* Access Tourist Emergency Contacts
* Assign Officers
* Update Incident Status
* Add Incident Notes
* Resolve and Close Incidents
* View Maps and Unsafe Zones

### 🛠️ Admin Dashboard

* Admin Authentication
* Manage Police Accounts
* Manage Tourists
* Create Unsafe / Restricted Zones
* Edit and Delete Zones
* View Incidents
* View Analytics
* View Audit Logs
* System Configuration

---

## 🚨 Incident Management

YatraLok uses a structured incident-response lifecycle.

```text
New
 ↓
Acknowledged
 ↓
Assigned
 ↓
En Route
 ↓
Resolved
 ↓
Closed
```

This ensures that an emergency is tracked throughout the complete response process instead of being treated as only a read/unread notification.

---

## 📍 Trip Mode

YatraLok does not use continuous always-on location tracking.

Location tracking starts only when the tourist activates:

```text
Start Trip / Trip Mode ON
```

and stops when:

```text
End Trip / Trip Mode OFF
```

During an active trip, the system can store:

* Start Time
* End Time
* Destination
* Location Points
* Trip Status
* Associated Incidents

This approach helps improve both **privacy and battery efficiency**.

---

## 🌍 Geo-Fencing

Administrators can create unsafe or restricted geographical zones.

The current implementation uses **Circular Geo-Fencing** defined using:

```text
Latitude
Longitude
Radius
```

The backend uses the **Haversine Distance Formula** to calculate the distance between the tourist and the defined zone.

```text
Tourist Distance ≤ Zone Radius
             ↓
       Unsafe Zone
             ↓
      Warning Generated
```

Polygon-based geo-fencing is outside the current project scope.

---

## 🆘 SOS System

When a tourist presses the SOS button, the system sends important information to the backend, including:

* Tourist ID
* Tourist Name
* GPS Location
* Timestamp
* Active Trip Information
* Emergency Contact Information

The backend creates an incident and uses **Socket.IO** to deliver the emergency alert to the Police Dashboard in real time.

```text
Tourist
   ↓
SOS
   ↓
Backend
   ↓
Incident Created
   ↓
Socket.IO
   ↓
Police Dashboard
```

---

## 🏗️ System Architecture

```text
                 ┌─────────────────────┐
                 │   Tourist Mobile    │
                 │        App          │
                 │    React Native     │
                 └──────────┬──────────┘
                            │
                            │ REST API / Socket.IO
                            ↓
                 ┌─────────────────────┐
                 │      Backend        │
                 │ Node.js + Express.js│
                 └──────────┬──────────┘
                            │
                            ↓
                 ┌─────────────────────┐
                 │       MySQL         │
                 │      Database       │
                 └─────────────────────┘
                            ↑
                            │
                            │ REST API / Socket.IO
                 ┌──────────┴──────────┐
                 │ Police / Admin Web  │
                 │      Dashboard      │
                 │       React.js      │
                 └─────────────────────┘
```

---

## 💻 Technology Stack

| Component               | Technology                 |
| ----------------------- | -------------------------- |
| Tourist Mobile App      | React Native               |
| Police/Admin Dashboard  | React.js                   |
| Backend                 | Node.js + Express.js       |
| Database                | MySQL                      |
| Real-Time Communication | Socket.IO                  |
| Authentication          | JWT                        |
| Maps & Location         | Maps/GPS API               |
| Geo-Fencing             | Haversine Distance Formula |
| Machine Learning        | Python / ML Libraries      |
| Version Control         | Git                        |
| Repository              | GitHub                     |

---

## 📁 Repository Structure

```text
YatraLok/
│
├── Frontend/
│   ├── Tourist-Mobile-App/
│   └── Police-Admin-Dashboard/
│
├── Backend/
│
├── Database/
│
├── ML/
│
├── docs/
│
├── .gitignore
└── README.md
```

### `Frontend/`

Contains the user-facing applications:

* Tourist Mobile Application
* Police/Admin Web Dashboard

### `Backend/`

Contains the Node.js + Express.js server, APIs, authentication, authorization, trip management, geo-fencing, SOS processing, incident management, Socket.IO integration, audit logs, and analytics APIs.

### `Database/`

Contains MySQL-related files such as:

* Database Schema
* Table Creation Scripts
* Relationships
* Sample Data
* ER Diagram

### `ML/`

Contains machine-learning development work such as:

* Datasets
* Data Preprocessing
* Exploratory Data Analysis
* Experiments
* Jupyter Notebooks
* Trained Models
* Prediction Scripts
* Model Evaluation

> AI-based risk scoring and suspicious movement detection are planned as later-phase features and should not be considered implemented until their models have been developed and integrated.

### `docs/`

Contains project documentation, architecture diagrams, workflows, API documentation, and other supporting resources.

---

## 🗄️ Main Database Entities

The planned database includes the following major entities:

```text
users
tourists
police_officers
trips
emergency_contacts
geo_zones
location_points
incidents
incident_status_history
audit_logs
notifications
```

The database design will maintain separate roles for:

```text
TOURIST
POLICE
ADMIN
```

---

## 🔐 Security & Privacy

YatraLok is designed with security and privacy considerations including:

* JWT-based authentication
* Role-based authorization
* Separate Tourist, Police, and Admin permissions
* Location tracking only during active Trip Mode
* Audit logging for sensitive actions
* Controlled access to tourist information
* Passwords must never be stored as plain text

Sensitive credentials and environment variables must not be committed to GitHub.

---

## 📊 Analytics

The dashboard is planned to provide basic operational analytics such as:

* Total Active Tourists
* Total Incidents
* Incidents by Status
* Incidents by Zone
* Daily / Weekly SOS Trends
* Average Response Time

---

## 🔮 Future Scope

The following features are currently considered future scope:

* AI-Based Risk Scoring
* Suspicious Movement Detection
* SMS SOS Fallback
* Automatic SMS / Call to Emergency Contacts
* Polygon Geo-Fencing
* Government Emergency-System Integration
* Multi-Language Support

These features should not be presented as implemented until they are actually developed and integrated.

---

# 🌿 Git & GitHub Workflow

YatraLok is developed collaboratively.

The `main` branch should contain stable and reviewed code.

Team members should **not directly develop features on `main`**.

Each member should create a separate feature branch.

Example:

```text
main
│
├── frontend
├── backend
├── database
└── ml
```

More specific branches can also be created as the project grows:

```text
feature/tourist-login
feature/trip-mode
feature/sos
feature/geo-fencing
feature/incident-management
feature/risk-prediction
```

---

## 👨‍💻 Working on a Feature

First update your local `main` branch:

```bash
git checkout main
git pull origin main
```

Create your feature branch:

```bash
git checkout -b feature/your-feature-name
```

Example:

```bash
git checkout -b feature/risk-prediction
```

Work on your feature and then check the changes:

```bash
git status
```

Add the changes:

```bash
git add .
```

Commit:

```bash
git commit -m "feat: add risk prediction module"
```

Push your branch:

```bash
git push -u origin feature/risk-prediction
```

Then create a **Pull Request** on GitHub to merge the feature branch into `main`.

---

## ⚠️ Contribution Rules

Before contributing:

1. Do not directly push feature development to `main`.
2. Create a separate branch for your work.
3. Pull the latest `main` before starting new work.
4. Write meaningful commit messages.
5. Do not commit passwords, API keys, database credentials, or `.env` files.
6. Test your feature before creating a Pull Request.
7. Create a Pull Request after completing your feature.
8. Review changes before merging into `main`.

---

## 📝 Commit Message Examples

```text
feat: add tourist registration
feat: implement SOS functionality
feat: add geo-fence detection
feat: add incident management
feat: add risk prediction model

fix: resolve login authentication issue
fix: correct location calculation

docs: update README
docs: add API documentation

refactor: restructure backend routes

test: add authentication tests
```

---

## 🚀 Development Roadmap

```text
Phase 1  → Planning
Phase 2  → Authentication
Phase 3  → Tourist Registration & Profile
Phase 4  → Trip & GPS Tracking
Phase 5  → Geo-Fencing
Phase 6  → SOS + Socket.IO
Phase 7  → Incident Management
Phase 8  → Travel History + Offline Sync
Phase 9  → Audit Logs + Analytics
Phase 10 → UI Polish + Testing + Demo
```

The priority is to make the complete end-to-end safety and incident-response flow functional before focusing on additional UI polish and advanced features.

---

## 🎬 Target Demo Flow

```text
Tourist Registration
        ↓
Digital Tourist ID Generated
        ↓
Emergency Contacts Added
        ↓
Trip Started
        ↓
GPS Tracking Started
        ↓
Tourist Enters Unsafe Zone
        ↓
Geo-Fence Warning
        ↓
Tourist Presses SOS
        ↓
Incident Created
        ↓
Real-Time Socket.IO Alert
        ↓
Police Dashboard
        ↓
Acknowledged
        ↓
Assigned
        ↓
En Route
        ↓
Resolved
        ↓
Closed
        ↓
Trip & Incident Saved
        ↓
Analytics & Audit Logs Updated
```

---

## 👥 Contributors

YatraLok is being developed collaboratively by the project team.

| Responsibility   | Module                                    |
| ---------------- | ----------------------------------------- |
| Frontend         | Tourist App & Police/Admin Dashboard      |
| Backend          | APIs, Authentication & Real-Time Services |
| Database         | MySQL Database Design & Management        |
| Machine Learning | Data Analysis & ML Models                 |

Team member names and individual responsibilities can be updated as development progresses.

---

## 📌 Project Status

🚧 **Currently Under Development**

YatraLok is being actively developed. Features and documentation may change as individual modules are implemented, tested, and integrated.

---

## 📄 License

This project is being developed for academic and educational purposes.

---

## 🛡️ YatraLok

**Safer Journeys. Faster Response. Smarter Tourist Safety.**
