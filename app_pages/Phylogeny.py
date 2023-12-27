import streamlit as st
import streamlit.components.v1 as components

from utils import (
    set_page_config,
    sidebar_image,
    set_css,
    home_page,
    author_link,
    # back_button,
)


def page_info():
    st.markdown(
        """
        <h2 style="text-align: left; color: #7a3777">
        <strong><em>Mycobacterium tuberculosis</em> complex phylogeny</strong>
        </h2>
        """,
        unsafe_allow_html=True,
    )
    st.caption(
        """
        <p>
        The exterior vertical bars and names indicate lineage:
        </br>
        <span style="color: #333333; font-weight: bold"> black</span> –
        <a href="https://doi.org/10.1128/msphere.00169-23" style="color: #333333; text-decoration: none">
            Shitikov & Bespiatykh (2023)</a
        >
        </br>
        <span style="color: #be9a5a; font-weight: bold"> golden</span> –
        <a href="https://doi.org/10.1186/S13073-020-00817-3" style="color: #be9a5a; text-decoration: none">
            Napier <em>et al.</em> (2020)</a
        >
        </p>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def show_lineage1_tree():
    HtmlTree = open("./data/trees/lineage.1.tree.html", encoding="utf-8")
    source_code = HtmlTree.read()
    components.html(source_code, height=1000, width=1800, scrolling=True)


@st.cache_data
def show_lineage2_tree():
    HtmlTree = open("./data/trees/lineage.2.tree.html", encoding="utf-8")
    source_code = HtmlTree.read()
    components.html(source_code, height=1000, width=1800, scrolling=True)


@st.cache_data
def show_lineage3_tree():
    HtmlTree = open("./data/trees/lineage.3.tree.html", encoding="utf-8")
    source_code = HtmlTree.read()
    components.html(source_code, height=1000, width=1800, scrolling=True)


@st.cache_data
def show_lineage4_tree():
    HtmlTree = open("./data/trees/lineage.4.tree.html", encoding="utf-8")
    source_code = HtmlTree.read()
    components.html(source_code, height=1000, width=1800, scrolling=True)


@st.cache_data
def show_lineage5_tree():
    HtmlTree = open("./data/trees/lineage.5.Animal.tree.html", encoding="utf-8")
    source_code = HtmlTree.read()
    components.html(source_code, height=1000, width=1600, scrolling=True)


def arrange_tabs():
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "Lineage 1",
            "Lineage 2",
            "Lineage 3",
            "Lineage 4",
            "Lineage 5-Animal",
        ]
    )

    with tab1:
        show_lineage1_tree()

    with tab2:
        show_lineage2_tree()

    with tab3:
        show_lineage3_tree()

    with tab4:
        show_lineage4_tree()

    with tab5:
        show_lineage5_tree()


def main():
    set_page_config()
    sidebar_image()
    set_css()
    author_link()
    home_page()
    page_info()
    arrange_tabs()
    # back_button("mycobacterium-tuberculosis-complex-phylogeny")


if __name__ == "__main__":
    main()
