# Marketing Attribution — Spend & Pray

Interactive Streamlit + Plotly storytelling dashboard for Team 8.

## Run locally

1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Install dependencies:

   pip install -r requirements.txt

4. Run:

   streamlit run app.py

5. Open the local URL Streamlit shows (usually http://localhost:8501).

## Publish

The easiest free route is Streamlit Community Cloud:
- Put these files in a GitHub repository.
- Create a new Streamlit app.
- Select `app.py`.
- Deploy.

The app uses only the included synthetic CSV extracts and does not require a database.

## Story structure

01 Sales
02 Marketing
03 Timing
04 Engagement
05 Attribution gap
06 Measure & improve

The dashboard intentionally does not claim channel attribution, CAC, ROAS, channel profit, or causal lift because the current-state dataset does not contain reliable order-to-channel linkage.
