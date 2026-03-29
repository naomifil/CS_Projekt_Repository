# Overview
 
## Technologies
- Main Language: Python
- Framework: Streamlit
- Database: SQLite
- API: Amadeus Self-Service
- ML Dataset: [Kaggle Datasets](https://www.kaggle.com/datasets/lunthu/european-airlines-routes)
- ML: **TBD**
 
## Todo's
### Phase 1
 
- ✅ Lock concept, formulate busniess problem
- 🔁 Fix routes, travel class
  - ZHR - LHR?
  - ➡️ Decide when decided on dataset
 
### Phase 2
- ✅ Setup Github env
- ✅ Setup Streamlit env
- 🔁 Define project steps
- ✅ Setup project scaffold
  - `app_main_file.py`
  - `data/`
  - `models/`
  - `database/`
  - `utils/`
- Add `requirements.txt` and clearly define technical requirements (imported packages, apis, blabla) in a quick summary.
- Add a `README.md` for other team members. Formate this for coding agents or other developers to gather context as well.
 
### Phase 3
- Register for Amadeus developer account
- Get API key + secret
- Write one Python script that:
  - authenticates
  - queries one route
  - prints response
- Convert result into a pandas DataFrame
- Keep only fields needed for the app:
  - airline
  - departure time
  - arrival time
  - duration
  - stops
  - price
  - currency
- ‼️**DO NOT COMMIT ANY API KEYS IN GIT** ‼️
  - research what `.env` files are and how to use them -> AI helps
- Write guide for other team members to use
 
### Phase 4
- Create SQLite DB
- Create DB schema
- Save successful API results to DB
 
### Phase 5
- Download historic flight dataset
- Clean data and import it into the database
- Create features, train simple model
  - Save model as `.pkl`
- Use model in app
 
### Phase 6
- Create website layout
- Route visualizer
  - Maybe with cards?
- Button to "search flights"
- Main page
  - KPI cards
  - Data Table visualizations
  - Recommendation box
  - Charts
- Interaction: Choose prefered flights