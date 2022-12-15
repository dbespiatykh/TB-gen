import base64
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Phylogeny",
    page_icon="favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("_Mycobacterium tuberculosis_ phylogeny")

st.markdown("---")

st.write(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300&display=swap');
html, body, [class*="css"]  {
   font-family: 'Montserrat';
}
</style>
""",
    unsafe_allow_html=True,
)


def sidebar_background_image(image):

    image_extension = "svg+xml"

    st.markdown(
        f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{image_extension};base64,{base64.b64encode(open(image, "rb").read()).decode()});
          padding-top: 80px;
          background-size: 200px;
          background-repeat: no-repeat;
          background-position: 20px 20px;
      }}
      </style>
      """,
        unsafe_allow_html=True,
    )


sidebar_background_image("logo.svg")


def show_svg(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    pdf_display = f'<iframe src="data:image/svg+xml;base64,{base64_pdf}" width="1100" height="900" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Lineage 1",
        "Lineage 2",
        "Lineage 3",
        "Lineage 4",
        "MTBC",
    ]
)

with tab1:
    show_svg("./data/trees/lineage1_tree.svg")

with tab2:
    show_svg("./data/trees/lineage2_tree.svg")

with tab3:
    show_svg("./data/trees/lineage3_tree.svg")

with tab4:
    show_svg("./data/trees/lineage4_tree.svg")

with tab5:
    show_svg("./data/trees/mtbc_tree.svg")

# # TREE TEST

# HtmlTree = open("./data/tree-plot.html", "r", encoding="utf-8")
# source_code = HtmlTree.read()
# components.html(source_code, height=1500, scrolling=True)
