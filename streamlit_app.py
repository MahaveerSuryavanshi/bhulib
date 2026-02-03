import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV → HTML Snippet Generator", layout="wide")

st.title("📄 CSV to HTML Scholarly Publications Generator")
st.write("Upload Scopus-style CSV and get a single HTML snippet (copy–paste ready).")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

def format_authors(author_str):
    if pd.isna(author_str):
        return ""

    authors = [a.strip() for a in author_str.split(";") if a.strip()]

    if len(authors) == 1:
        return authors[0]
    elif len(authors) == 2:
        return f"{authors[0]} &amp; {authors[1]}"
    else:
        return ", ".join(authors[:-1]) + ", &amp; " + authors[-1]

def build_entry(idx, row):
    authors = format_authors(row["Authors"])
    year = row["Year"]
    title = row["Title"]
    journal = row["Source title"]
    volume = row["Volume"]
    issue = row["Issue"]
    page_start = row["Page start"]
    page_end = row["Page end"]
    doi = row["DOI"]

    pages = ""
    if pd.notna(page_start) and pd.notna(page_end):
        pages = f", {int(page_start)}–{int(page_end)}"

    issue_part = f"({int(issue)})" if pd.notna(issue) else ""

    html = f"""
<p style="font-family:Lucida Sans Unicode,Lucida Grande,sans-serif;">
<strong>{idx}.</strong>
{authors} ({int(year)}). {title}.
<em>{journal}</em>, <em>{volume}</em>{issue_part}{pages}.
<a href="https://doi.org/{doi}" target="_blank">https://doi.org/{doi}</a>
</p>
<p style="font-family:Lucida Sans Unicode,Lucida Grande,sans-serif;">&nbsp;</p>
"""
    return html

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    required_cols = [
        "Authors", "Year", "Title",
        "Source title", "Volume",
        "Issue", "Page start", "Page end", "DOI"
    ]

    df = df[required_cols]
    df = df.dropna(subset=["Authors", "Title", "Year"])

    output_html = ""
    for i, row in df.iterrows():
        output_html += build_entry(len(output_html.split("<strong>")), row)

    st.subheader("Generated HTML (Copy & Paste)")
    st.text_area(
        "Final HTML Snippet",
        output_html,
        height=600
    )

    st.download_button(
        label="⬇ Download HTML File",
        data=output_html,
        file_name="scholarly_publications.html",
        mime="text/html"
    )
