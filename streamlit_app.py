import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import datetime

st.set_page_config(page_title="CSV → HTML Snippet Generator", layout="wide")

st.title("📄 CSV to HTML Scholarly Publications Generator")
st.write("Upload Scopus-style CSV and get a single HTML snippet (A–Z by first author).")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])


# ---------- HELPERS ----------

def clean_number(value):
    if pd.isna(value):
        return ""
    try:
        return str(int(value))
    except Exception:
        return ""


def format_authors(author_str, max_authors=10):
    if pd.isna(author_str):
        return ""

    authors = [a.strip() for a in author_str.split(";") if a.strip()]

    if len(authors) > max_authors:
        authors = authors[:max_authors]
        authors.append("et al.")

    if len(authors) == 1:
        return authors[0]
    elif len(authors) == 2:
        return f"{authors[0]} &amp; {authors[1]}"
    else:
        return ", ".join(authors[:-1]) + ", &amp; " + authors[-1]


def first_author_key(author_str):
    if pd.isna(author_str):
        return ""
    return author_str.split(";")[0].strip().lower()


def build_entry(idx, row):
    authors = format_authors(row["Authors"])
    year = clean_number(row["Year"])
    title = row["Title"]
    journal = row["Source title"]

    volume = clean_number(row["Volume"])
    issue = clean_number(row["Issue"])

    page_start = clean_number(row["Page start"])
    page_end = clean_number(row["Page end"])

    doi = row["DOI"]

    volume_part = f"<em>{volume}</em>" if volume else ""
    issue_part = f"({issue})" if issue else ""

    pages_part = ""
    if page_start and page_end:
        pages_part = f", {page_start}–{page_end}"

    # Get the current date and time
    current_date = datetime.datetime.now()
    
    # Use strftime with "%B" to get the full month name
    full_month_name = current_date.strftime("%B")

    return f"""
<div class="container">
    <div class="row" ng-init="GetAboutUs()">
        <div class="col-sm-12 ng-binding" ng-bind-html="trustAsHtml(AboutUsHome)">

            <div class="preview-box active" id="eng4" style="display: block;">
                <p ng-bind-html="trustAsHtml(ApproveBodyContent.BodyContentEng)" class="ng-binding"></p>
                <div style="max-width:100%; overflow:hidden">
                    <iframe frameborder="0" height="1800px" scrolling="no" src="https://dl.bhu.ac.in/newar/"
                        width="100%"></iframe>
                </div>

                <div class="News"
                    style="background-color:#c0392b; border:1px solid; margin-bottom:2px; margin-left:auto; margin-right:auto; margin-top:2px; max-width:1200px">
                    &nbsp;
                    <p style="margin-left:14px; margin-right:14px; text-align:center">
                        <span style="font-size:28px">
                            <span style="font-family:Lucida Sans Unicode,Lucida Grande,sans-serif">
                                <span style="color:#ffffff"><strong>Recent Scholarly Publications of BHU
                                        Researchers</strong></span>
                            </span>
                        </span>
                        <br>
                        <span style="font-size:22px">
                            <span style="font-family:Lucida Sans Unicode,Lucida Grande,sans-serif">
                            <span style="color:#ffffff"><strong>( {full_month_name} &nbsp;{year}) </strong></span>
                            </span>
                        </span>
                    </p>
                    &nbsp;
                    <!--  Scholarly Publications Starts -->
                    <div class="contents"
                        style="background-color:#fbf5f5; border:1px solid #cccccc; color:#222222; font-family:Lucida Sans Unicode,Lucida Grande,sans-serif; font-size:16px; line-height:22px; margin-top:10px; padding:0 20px 20px">
                        <div class="xyz" style="height:300px; overflow-x:hidden; overflow-y:scroll; width:100%">
                        
<p style="font-family:Lucida Sans Unicode,Lucida Grande,sans-serif;">
<strong>{idx}.</strong>
{authors} ({year}). {title}.
<em>{journal}</em>{', ' if volume_part else ''}{volume_part}{issue_part}{pages_part}.
{'<a href="https://doi.org/' + doi + '" target="_blank">https://doi.org/' + doi + '</a>' if pd.notna(doi) else ''}
</p>
<p style="font-family:Lucida Sans Unicode,Lucida Grande,sans-serif;">&nbsp;</p>

</div>
                    </div>
                    <!--  Scholarly Publications ends -->
                </div>
                <p style="font-family:Lucida Sans Unicode,Lucida Grande,sans-serif;">
                </p>

            </div>
        </div>
    </div>
</div>
"""


# ---------- MAIN ----------

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

    st.subheader("Generated HTML (Copy / Download)")

    st.text_area(
        "Final HTML Snippet",
        output_html,
        height=600,
        key="html_output"
    )

    # ✅ PRE-ESCAPE HTML FOR JAVASCRIPT (CRITICAL FIX)
    escaped_html = (
        output_html
        .replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("$", "\\$")
    )

    # 📋 COPY BUTTON (NO SYNTAX ERROR)
    components.html(
        f"""
        <script>
        function copyToClipboard() {{
            navigator.clipboard.writeText(`{escaped_html}`);
            alert("HTML copied to clipboard!");
        }}
        </script>

        <button onclick="copyToClipboard()"
        style="
            background-color:#4CAF50;
            color:white;
            padding:10px 16px;
            border:none;
            border-radius:6px;
            cursor:pointer;
            font-size:14px;
        ">
        📋 Copy HTML
        </button>
        """,
        height=60
    )

    st.download_button(
        label="⬇ Download HTML File",
        data=output_html,
        file_name="scholarly_publications.html",
        mime="text/html"
    )
