import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="CSV → HTML Snippet Generator | BHU Home Page",
    layout="wide",
    page_icon="logo.png"
)

# ---------- HEADER ----------
col1, col2 = st.columns([1, 6])

with col1:
    st.image("logo.png", width=200)

with col2:
    st.markdown(
        "<h1 style='margin-top: 30px;'>CSV to HTML Scholarly Publications Generator</h1>",
        unsafe_allow_html=True
    )

st.write(
    "Upload Scopus-style CSV and get a single HTML snippet "
    "(APA 7th, A–Z by first author)."
)
st.write(
    "Step 1. Upload CSV file."
)
st.write(
    "Step 2. Open Admin Dashboard"
)
st.write(
    "Step 3. Copy generated english and hindi template and paste them respectively"
)
# ---------- MONTH & YEAR INPUT ----------
months_en = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

months_hi = {
    "January": "जनवरी", "February": "फ़रवरी", "March": "मार्च",
    "April": "अप्रैल", "May": "मई", "June": "जून",
    "July": "जुलाई", "August": "अगस्त", "September": "सितंबर",
    "October": "अक्टूबर", "November": "नवंबर", "December": "दिसंबर"
}

col_m, col_y = st.columns(2)

with col_m:
    selected_month = st.selectbox("Month", months_en)

with col_y:
    selected_year = st.number_input(
        "Year", min_value=2000, max_value=2100, value=2026, step=1
    )

month_en = selected_month
month_hi = months_hi[selected_month]
year_str = str(selected_year)

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

# ---------- FIXED HTML WRAPPERS ----------

HTML_HEADER_EN = f"""
<div class="container">
    <div class="row" ng-init="GetAboutUs()">
        <div class="col-sm-12 ng-binding" ng-bind-html="trustAsHtml(AboutUsHome)">
            <div class="preview-box active" id="eng4" style="display: block;">
                <p ng-bind-html="trustAsHtml(ApproveBodyContent.BodyContentEng)" class="ng-binding"></p>
                <div style="max-width:100%; overflow:hidden">
                    <iframe frameborder="0" height="1800px" scrolling="no"
                        src="https://dl.bhu.ac.in/newar/" width="100%"></iframe>
                </div>

                <div class="News"
                    style="background-color:#c0392b; border:1px solid; margin:2px auto; max-width:1200px">
                    &nbsp;
                    <p style="margin:14px; text-align:center">
                        <span style="font-size:28px; font-family:Lucida Sans Unicode,Lucida Grande,sans-serif; color:#ffffff">
                            <strong>Recent Scholarly Publications of BHU Researchers</strong>
                        </span><br>
                        <span style="font-size:22px; font-family:Lucida Sans Unicode,Lucida Grande,sans-serif; color:#ffffff">
                            <strong>( {month_en} {year_str} )</strong>
                        </span>
                    </p>
                    &nbsp;

                    <div class="contents"
                        style="background-color:#fbf5f5; border:1px solid #cccccc;
                               color:#222222; font-family:Lucida Sans Unicode,Lucida Grande,sans-serif;
                               font-size:16px; line-height:22px; margin-top:10px;
                               padding:0 20px 20px">
                        <div class="xyz"
                             style="height:300px; overflow-x:hidden; overflow-y:scroll; width:100%">
"""


HTML_HEADER_HI = f"""
<div class="container">
    <div class="row" ng-init="GetAboutUs()">
        <div class="col-sm-12 ng-binding" ng-bind-html="trustAsHtml(AboutUsHome)">
            <div class="container">
                <div class="row">
                    <div class="col-sm-12 ng-binding">
                        <div class="active preview-box" id="eng4" style="display:block">
                            <p>&nbsp;</p>

                            <div style="max-width:100%; overflow:hidden">
                                <iframe frameborder="0" height="1800px" scrolling="no"
                                    src="https://dl.bhu.ac.in/newar/hn/" width="100%"></iframe>
                            </div>

                            <div class="News"
                                style="background-color:#c0392b; border:1px solid; margin:2px auto; max-width:1200px">
                                &nbsp;
                                <p style="margin:14px; text-align:center">
                                    <span style="font-size:28px; font-family:Lucida Sans Unicode,Lucida Grande,sans-serif; color:#ffffff">
                                        <strong>बीएचयू शोधकर्ताओं के हालिया शैक्षणिक प्रकाशन</strong>
                                    </span><br>
                                    <span style="font-size:22px; font-family:Lucida Sans Unicode,Lucida Grande,sans-serif; color:#ffffff">
                                        <strong>( {month_hi} {year_str} )</strong>
                                    </span>
                                </p>
                                &nbsp;

                                <div class="contents"
                                    style="background-color:#fbf5f5; border:1px solid #cccccc;
                                           color:#222222; font-family:Lucida Sans Unicode,Lucida Grande,sans-serif;
                                           font-size:16px; line-height:22px; margin-top:10px;
                                           padding:0 20px 20px">
                                    <div class="xyz"
                                         style="height:300px; overflow-x:hidden; overflow-y:scroll; width:100%">
"""


HTML_FOOTER = """
                        </div>
                    </div>
                </div>
                <p style="font-family:Lucida Sans Unicode,Lucida Grande,sans-serif;"></p>
            </div>
        </div>
    </div>
</div>
"""

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
    pages_part = f", {page_start}–{page_end}" if page_start and page_end else ""

    doi_part = (
        f'<a href="https://doi.org/{doi}" target="_blank">https://doi.org/{doi}</a>'
        if pd.notna(doi) else ""
    )

    return f"""
<p style="font-family:Lucida Sans Unicode,Lucida Grande,sans-serif;">
<strong>{idx}.</strong>
{authors} ({year}). {title}.
<em>{journal}</em>{', ' if volume_part else ''}{volume_part}{issue_part}{pages_part}.
{doi_part}
</p>
<p style="font-family:Lucida Sans Unicode,Lucida Grande,sans-serif;">&nbsp;</p>
"""


def generate_html(header, df):
    df = df.copy()

    required_cols = [
        "Authors", "Year", "Title",
        "Source title", "Volume",
        "Issue", "Page start", "Page end", "DOI"
    ]

    df = df[required_cols]
    df = df.dropna(subset=["Authors", "Title", "Year"])

    df["sort_key"] = df["Authors"].apply(first_author_key)
    df = df.sort_values("sort_key").drop(columns=["sort_key"])

    entries_html = ""
    for idx, (_, row) in enumerate(df.iterrows(), start=1):
        entries_html += build_entry(idx, row)

    return header + entries_html + HTML_FOOTER


# ---------- MAIN (TABS) ----------

if uploaded_file:
    try:
        df_original = pd.read_csv(uploaded_file)
    except pd.errors.EmptyDataError:
        st.error("The uploaded CSV file is empty.")
        st.stop()

    tab_en, tab_hi = st.tabs(["🇬🇧 English", "🇮🇳 हिंदी"])

    for tab, header, label, fname in [
        (tab_en, HTML_HEADER_EN, "English", "scholarly_publications_en.html"),
        (tab_hi, HTML_HEADER_HI, "Hindi", "scholarly_publications_hi.html"),
    ]:
        with tab:
            output_html = generate_html(header, df_original)

            st.subheader(f"Generated HTML ({label})")

            st.text_area(
                "Final HTML Snippet",
                output_html,
                height=600
            )

            escaped_html = (
                output_html
                .replace("\\", "\\\\")
                .replace("`", "\\`")
                .replace("$", "\\$")
            )

            components.html(
                f"""
                <script>
                function copyToClipboard() {{
                    navigator.clipboard.writeText(`{escaped_html}`);
                    alert("HTML copied to clipboard!");
                }}
                </script>

                <button onclick="copyToClipboard()"
                style="background:#4CAF50;color:white;padding:10px 16px;
                       border:none;border-radius:6px;cursor:pointer;font-size:14px;">
                COPY HTML
                </button>
                """,
                height=60
            )
            # download button for cone snippet
            st.download_button(
                f"Download {label} HTML File",
                output_html,
                fname,
                "text/html"
            )
