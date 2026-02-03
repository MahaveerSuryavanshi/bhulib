import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV → HTML Snippet Generator", layout="wide")

st.title("📄 CSV to HTML Scholarly Publications Generator")
st.write("Upload Scopus-style CSV and get a single HTML snippet (A–Z by first author).")

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


def first_author_key(author_str):
    if pd.isna(author_str):
        return ""
    # Use first author only for A–Z sorting
    return author_str.split(";")[0].strip().lower()


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

    return f"""
<p style="font-family:Lucida Sans Unicode,Lucida Grande,sans-serif;">
<strong>{idx}.</strong>
{authors} ({int(year)}). {title}.
<em>{journal}</em>, <em>{volume}</em>{issue_part}{pages}.
<a href="https://doi.org/{doi}" target="_blank">https://doi.org/{doi}</a>
</p>
<p style="font-family:Lucida Sans Unicode,Lucida Grande,sans-serif;">&nbsp;</p>
"""


if uploaded_file:
    df = pd.read_csv(uploaded_file)

    required_cols = [
        "Authors", "Year", "Title",
        "Source title", "Volume",
        "Issue", "Page start", "Page end", "DOI"
    ]

    df = df[required_cols]
    df = df.dropna(subset=["Authors", "Title", "Year"])

    # 🔤 SORT A–Z BY FIRST AUTHOR
    df["sort_key"] = df["Authors"].apply(first_author_key)
    df = df.sort_values("sort_key").drop(columns=["sort_key"])

    output_html = ""
    for idx, (_, row) in enumerate(df.iterrows(), start=1):
        output_html += build_entry(idx, row)

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
