import warnings
import pandas as pd
import streamlit as st

from st_aggrid import AgGrid, GridUpdateMode, ColumnsAutoSizeMode, GridOptionsBuilder
from utils import (
    set_page_config,
    sidebar_image,
    set_css,
    home_page,
    get_cell_style,
    author_link,
    back_button,
)


def page_info():
    st.markdown(
        "<h2 style='text-align: left; color: #7A3777;'><strong>MTBC barcoding SNPs</strong></h2>",
        unsafe_allow_html=True,
    )
    st.caption("Curated list of barcoding SNPs")
    dataset = load_dataset()
    long_df = load_long_levels()

    tsv = convert_df_to_tsv(dataset)
    csv = convert_df_to_csv(dataset)

    long_df_tsv = convert_df_to_tsv(long_df)
    long_df_csv = convert_df_to_csv(long_df)

    with st.expander("Download"):
        dwn1, dwn2, dwn3, dwn4, mock = st.columns([3, 3, 5, 5, 7])

        with dwn1:
            st.download_button(
                label="💾 Download TSV",
                data=tsv,
                file_name="snp_barcode.tsv",
                mime="text/csv",
            )
        with dwn2:
            st.download_button(
                label="💾 Download CSV",
                data=csv,
                file_name="snp_barcode.csv",
                mime="text/csv",
            )
        with dwn3:
            st.download_button(
                label="💾 Download TSV (long format)",
                data=long_df_tsv,
                file_name="snp_barcode_long.tsv",
                mime="text/csv",
            )
        with dwn4:
            st.download_button(
                label="💾 Download CSV (long format)",
                data=long_df_csv,
                file_name="snp_barcode_long.tsv",
                mime="text/csv",
            )
        with mock:
            pass


@st.experimental_memo
def load_dataset():
    df = pd.read_csv("./data/snp_barcode.tsv", sep="\t")
    return df


@st.experimental_memo
def load_long_levels():
    df = pd.read_csv("./data/levels.tsv", sep="\t")
    return df


@st.experimental_memo()
def convert_df_to_tsv(df):
    return df.to_csv(sep="\t", index=False).encode("utf-8")


@st.experimental_memo(show_spinner=False)
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")


def show_dataset():
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=FutureWarning)

        dataset = load_dataset()
        cellstyle_jscode = get_cell_style()

        gd = GridOptionsBuilder.from_dataframe(
            dataset,
            enableRowGroup=True,
            enableValue=True,
            enablePivot=True,
        )
        gd.configure_grid_options(domLayout="autoHeight", enableRangeSelection=True)
        gd.configure_selection(selection_mode="multiple", use_checkbox=False)
        gd.configure_default_column(
            editable=False,
            groupable=True,
        )
        gd.configure_columns(dataset, cellStyle=cellstyle_jscode)

        grid = AgGrid(
            dataset,
            gridOptions=gd.build(),
            enable_enterprise_modules=False,
            allowDragFromColumnsToolPanel=True,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
            allow_unsafe_jscode=True,
            theme="streamlit",
        )
        return grid


if __name__ == "__main__":
    set_page_config()
    sidebar_image()
    set_css()
    home_page()
    author_link()
    page_info()
    show_dataset()
    back_button("mtbc-barcoding-snps")
