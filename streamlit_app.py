import streamlit as st
import base64

from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.add_vertical_space import add_vertical_space
from utils import set_page_config, sidebar_image, set_css, author_link, set_pages


def page_info():
    st.markdown(
        "<h1 style='text-align: center; color: #7A3777;'><strong>Explore <em>Mycobacterium tuberculosis</em> complex</strong></h1>",
        unsafe_allow_html=True,
    )


@st.experimental_memo(experimental_allow_widgets=True, show_spinner=False)
def buttons():
    bt1, bt2, bt3, bt4, bt5, bt6 = st.columns([3, 1, 1, 1, 1, 3])

    with bt1:
        pass
    with bt2:
        genotype_user_data = st.button("Genotype VCF")
    with bt3:
        phylogeny = st.button("Explore Phylogeny")
    with bt4:
        dataset = st.button("Reference Dataset")
    with bt5:
        barcodes = st.button("Barcoding SNPs")
    with bt6:
        pass

    if genotype_user_data:
        switch_page("genotype lineage")
    if phylogeny:
        switch_page("phylogeny")
    if dataset:
        switch_page("reference dataset")
    if barcodes:
        switch_page("barcoding snps")


@st.experimental_memo(show_spinner=False)
def show_svg_tree():
    with open("./assets/mtbc_tree.svg", "rb") as f:
        base64_svg = base64.b64encode(f.read()).decode("utf-8")
    svg_display = f'<center><iframe src="data:image/svg+xml;base64,{base64_svg}" width="750" height="750"></iframe></center>'
    st.markdown(svg_display, unsafe_allow_html=True)


if __name__ == "__main__":
    set_page_config()
    sidebar_image()
    set_css()
    author_link()
    set_pages()
    page_info()
    add_vertical_space(1)
    buttons()
    add_vertical_space(2)
    show_svg_tree()
