import streamlit as st
import os
import base64
from core.main import main as run_scraper

st.set_page_config(page_title="OddsPortal Scraper", layout="wide")

if 'saved_files' not in st.session_state:
    st.session_state.saved_files = []

# --- DARK THEME + FIXED NAVBAR/HERO/FOOTER LAYOUT ---
st.markdown("""
<style>
    body {
        font-family: 'Segoe UI', sans-serif;
        background-color: #0f172a;
        color: #f1f5f9;
    }

    /* NAVBAR */
    .navbar {
        background-color: #1e293b;
        padding: 16px 32px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #334155;
    }

    .navbar-title {
        font-size: 20px;
        font-weight: bold;
        color: #38bdf8;
    }

    .navbar-links {
        font-size: 14px;
        color: #cbd5e1;
    }

    /* HERO SECTION */
    .hero {
        background: linear-gradient(120deg, #1e293b, #0f172a);
        padding: 60px 30px;
        text-align: center;
        color: white;
        border-bottom: 1px solid #334155;
        margin-top: 12px; /* Space below navbar */
        margin-bottom: 32px;
        border-radius: 8px;
    }

    .hero h1 {
        font-size: 42px;
        margin-bottom: 12px;
        color: #38bdf8;
    }

    .hero p {
        font-size: 18px;
        color: #e2e8f0;
        max-width: 700px;
        margin: 0 auto;
    }

    /* CATEGORY TITLE */
    .category-name {
        font-size: 22px;
        font-weight: 600;
        color: #f1f5f9;
        margin: 40px 0 10px;
        text-align: center;
    }

    .subfolder-title {
        font-size: 16px;
        color: #cbd5e1;
        margin: 16px 0 6px;
    }

    /* DOWNLOAD LINK */
    .download-link {
        display: block;
        margin: 4px auto;
        padding: 10px 16px;
        background-color: #1d4ed8;
        width: fit-content;
        border-radius: 8px;
        color: #ffffff;
        font-size: 14px;
        font-weight: 600;
        text-decoration: none;
        transition: background-color 0.2s ease;
    }

    .download-link:hover {
        background-color: #3b82f6;
        color: #f8fafc;
    }

    /* FOOTER */
    .footer {
        background-color: #1e293b;
        text-align: center;
        font-size: 13px;
        color: #94a3b8;
        margin-top: 50px;
        padding: 20px;
        border-top: 1px solid #334155;
    }

    /* BUTTONS */
    .stButton button {
        background-color: #38bdf8;
        color: #0f172a;
        font-weight: 600;
        padding: 0.5rem 1.2rem;
        border-radius: 8px;
        border: none;
        transition: 0.3s ease-in-out;
    }

    .stButton button:hover {
        background-color: #0ea5e9;
    }

    /* HEADINGS */
    h3 {
        color: #f8fafc;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- NAVBAR ---
st.markdown("""
<div class="navbar">
    <div class="navbar-title">⚽ OddsPortal Scraper</div>
    <div class="navbar-links">Get odds for the next 24 hours in CSV, JSON & more</div>
</div>
""", unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown("""
<div class="hero">
    <h1>Scrape Sports Betting Odds with Ease</h1>
    <p>
        OddsPortal Scraper collects football match odds from OddsPortal.<br>
        Supports CSV, JSON, and more formats for matches in the next 24 hours.
    </p>
</div>
""", unsafe_allow_html=True)

# --- HOW IT WORKS SECTION ---
st.markdown("""
### ⚙️ How It Works
1. Click **Start Scraping** to begin retrieving match data.
2. The scraper gathers football match odds from OddsPortal for the next 24 hours.
3. Output is automatically organized by sport/category.
4. Download files in `.csv`, `.json`, and more.

---
""")

# --- SCRAPE BUTTON ---
if st.button("Start Scraping"):
    try:
        run_scraper()
        st.success("✅ Scraping completed and files saved!")

        st.session_state.saved_files.clear()
        output_dir = "output"

        for root, _, files in os.walk(output_dir):
            for file in files:
                st.session_state.saved_files.append(os.path.join(root, file))

    except Exception as e:
        st.error(f"An error occurred during scraping: {e}")

# --- FILE GROUPING ---


def group_files_by_category(files):
    grouped = {}
    for f in files:
        rel_path = os.path.relpath(f, 'output')
        parts = rel_path.split(os.sep)
        category = parts[0]
        subfolder = '/'.join(parts[1:-1]) if len(parts) > 2 else ''
        grouped.setdefault(category, {}).setdefault(subfolder, []).append(f)
    return grouped


def file_to_download_link(filepath):
    try:
        with open(filepath, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        filename = os.path.basename(filepath)
        return f'<a href="data:file/txt;base64,{b64}" download="{filename}" class="download-link">📄 {filename}</a>'
    except:
        return ""


# --- FILE DISPLAY ---
if st.session_state.saved_files:
    st.markdown("### 📁 Files by Category")
    grouped = group_files_by_category(st.session_state.saved_files)

    for category, subfolders in grouped.items():
        st.markdown(
            f'<div class="category-name">📂 {category.capitalize()}</div>', unsafe_allow_html=True)

        for subfolder, files in subfolders.items():
            if subfolder:
                st.markdown(
                    f'<div class="subfolder-title">📁 {subfolder}</div>', unsafe_allow_html=True)

            for f in files:
                st.markdown(file_to_download_link(f), unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div class="footer">
    Built for data analysts, bettors & sports traders.<br>
    &copy; 2025 OddsPortal Scraper
</div>
""", unsafe_allow_html=True)
