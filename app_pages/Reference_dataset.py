import pandas as pd
import numpy as np
import geopandas
import streamlit as st
import leafmap.foliumap as leafmap
import altair as alt

from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.stoggle import stoggle
from utils import set_page_config, sidebar_image, set_css, home_page

set_page_config()
sidebar_image()
set_css()
home_page()

st.title("Reference dataset of _Mycobacterium tuberculosis_ complex isolates")

st.markdown("---")


@st.experimental_memo
def get_data(input):
    df = pd.read_csv(input, sep="\t")
    return df


@st.experimental_memo
def get_country_shapes(input):
    df = geopandas.read_file(input)
    return df


@st.experimental_memo
def get_regions(input):
    df = pd.read_csv(input, usecols=["name", "region"]).rename(
        columns={"region": "Region"}
    )
    return df


@st.experimental_memo
def get_countries(input):
    df = pd.read_csv(input)
    return df


dataset = get_data("./data/samples_data.tsv")


@st.experimental_memo
def get_mapping_data():
    dataset = get_data("./data/samples_data.tsv")
    country_shapes = get_country_shapes("./data/world_countries.json")
    regions = get_regions("./data/regions.csv")
    countries = get_countries("./data/countries.csv")
    smp_data = pd.merge(
        dataset[
            [
                "Sample",
                "Country of isolation",
                "level 1",
                "level 2",
                "level 3",
                "level 4",
                "level 5",
            ]
        ],
        countries,
        how="left",
        left_on="Country of isolation",
        right_on="name",
    ).drop(columns=["country"])
    smp_data = smp_data[smp_data["name"].notna()]
    smp_data = pd.merge(left=smp_data, right=regions, how="left", on="name").drop(
        columns=["name"]
    )
    # Calculate number of samples per country
    cnt_samples = (
        dataset[["Sample", "Country of isolation"]]
        .groupby(["Country of isolation"])
        .count()
        .reset_index()
        .rename(columns={"Sample": "Number of Samples", "country of isolation": "name"})
    )
    # Merge country shapes and counts data
    cnt_samples_poly = (
        pd.merge(
            country_shapes,
            cnt_samples,
            left_on="name",
            right_on="Country of isolation",
            how="left",
        )
        .dropna()
        .drop(columns=["id", "Country of isolation"])
        .rename(columns={"name": "Country"})
    )
    cnt_samples_poly["Number of Samples"] = cnt_samples_poly[
        "Number of Samples"
    ].astype(np.int64)
    return smp_data, cnt_samples_poly


def get_map():
    smp_data, cnt_samples_poly = get_mapping_data()
    m = leafmap.Map(
        layers_control=False,
        draw_control=False,
        measure_control=False,
        fullscreen_control=False,
        attribution_control=True,
    )
    m.add_basemap("CartoDB.PositronNoLabels")
    m.add_data(
        data=cnt_samples_poly,
        column="Number of Samples",
        layer_name="Number of Samples",
        k=9,
        add_legend=False,
    )
    m.add_points_from_xy(
        smp_data,
        layer_name="Samples",
        x="longitude",
        y="latitude",
        popup=[
            "Sample",
            "Country of isolation",
            "Region",
            "level 1",
            "level 2",
            "level 3",
            "level 4",
            "level 5",
        ],
        color_column="Region",
        icon_names=["star"],
        spin=True,
        add_legend=False,
    )
    return m


sm1, mk = st.columns([2, 5])
sm1.metric(
    label="Total Samples",
    value=int(dataset["Sample"].count()),
    help="""Number of currently availible samples in the dataset
        """,
)

####################################################################################################################
# st.markdown("## Dataset")
gd = GridOptionsBuilder.from_dataframe(
    dataset, enableRowGroup=True, enableValue=True, enablePivot=True
)
gd.configure_grid_options(domLayout="normal")
gd.configure_selection(selection_mode="multiple", use_checkbox=True)
gd.configure_default_column(editable=True, groupable=True)
# gd.configure_pagination(enabled=True, paginationPageSize=100)
gd.configure_side_bar()

if st.checkbox("Show Dataset"):
    # st.subheader('Dataset')
    # st.dataframe(dataset)
    grid1 = AgGrid(
        dataset,
        gridOptions=gd.build(),
        enable_enterprise_modules=False,
        allowDragFromColumnsToolPanel=True,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        allow_unsafe_jscode=True,
        height=400,
        width="100%",
        theme="streamlit",
    )
    sel_row = grid1["selected_rows"]
    dataset_sel = pd.DataFrame(sel_row)
    st.subheader("Selected Samples")
    # Grid 2
    builder = GridOptionsBuilder.from_dataframe(dataset_sel)
    builder.configure_column("_selectedRowNodeInfo", hide=True)
    go = builder.build()
    grid2 = AgGrid(
        dataset_sel,
        gridOptions=go,
        height=150,
        theme="streamlit",
        enable_enterprise_modules=False,
    )


add_vertical_space(3)


def sample_stats(dataset):
    # Dataframe filter
    sample_filter = st.selectbox("Select Sample", pd.unique(dataset["Sample"]))
    dataset = dataset[dataset["Sample"] == sample_filter]

    # Create six columns
    sd1, sd2, sd3, sd4, sd5, sd6 = st.columns(6, gap="small")

    # Fill columns with Sample metics
    sd1.metric(
        label="SNPs",
        value=int(dataset["no. of SNPs"]),
        help="""Number of single nucteotide polymorphisms (SNPs) 
                relative to the _M. tuberculosis_ H37Rv genome 
               (GenBank accession no. [NC_000962.3](https://www.ncbi.nlm.nih.gov/nuccore/NC_000962.3/)
            """,
    )

    sd2.metric(
        label="GC %",
        value=int(dataset["%GC"]),
        help="""GC-content (guanine-cytosine content) in the sample
            """,
    )

    sd3.metric(label="Total Sequences", value=int(dataset["Total sequences"]))

    sd4.metric(
        label="Average sequence length",
        value=float(round(dataset["Average sequence length"], 2)),
    )

    sd5.metric(
        label="Mapped Reads %",
        value=float(round(dataset["%Reads mapped"], 2)),
        help="""Percenatege of the reads mapped to the _M. tuberculosis_ H37Rv genome 
            (GenBank accession no. [NC_000962.3](https://www.ncbi.nlm.nih.gov/nuccore/NC_000962.3/)
            """,
    )

    sd6.metric(
        label="Average coverage depth",
        value=float(round(dataset["Average coverage depth"], 2)),
        help="""Mean depth of the sample mapped to the _M. tuberculosis_ H37Rv genome 
            (GenBank accession no. [NC_000962.3](https://www.ncbi.nlm.nih.gov/nuccore/NC_000962.3/)
            """,
    )

    # Create another six columns
    sd7, sd8, sd9, sd10, sd11, sd12 = st.columns(6, gap="small")

    sd7.metric(
        label="Country of Isolation", value=str(dataset["Country of isolation"].item())
    )

    sd8.metric(label="Level 1", value=str(dataset["level 1"].item()))
    sd9.metric(label="Level 2", value=str(dataset["level 2"].item()))
    sd10.metric(label="Level 3", value=str(dataset["level 3"].item()))
    sd11.metric(label="Level 4", value=str(dataset["level 4"].item()))
    sd12.metric(label="Level 5", value=str(dataset["level 5"].item()))


sample_stats(dataset)

# expander = st.expander("†")
# expander.write("""
#     All metrics relative to reference
#     _M. tuberculosis_ H37Rv genome
#     (GenBank accession no. [NC_000962.3](https://www.ncbi.nlm.nih.gov/nuccore/NC_000962.3/))
# """)

add_vertical_space(5)


@st.experimental_memo
def get_chart():
    # Calculate mean SNPs values
    no_vars = (
        get_data("./data/samples_data.tsv")[["level 1", "no. of SNPs"]]
        .groupby(["level 1"])
        .mean()
        .reset_index()
        .rename(columns={"level 1": "Main lineage", "no. of SNPs": "Number of SNPs"})
    )

    no_samples = (
        get_data("./data/samples_data.tsv")[["level 1", "Sample"]]
        .groupby(["level 1"])
        .count()
        .reset_index()
        .rename(columns={"Sample": "Number of Samples", "level 1": "Main lineage"})
    )

    snp_chart = (
        alt.Chart(no_vars)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            x=alt.X("Main lineage", axis=alt.Axis(title="")),
            y="Number of SNPs",
            color=alt.value("#A65AA3"),
        )
    )

    sample_chart = (
        alt.Chart(no_samples)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            x=alt.X("Main lineage", axis=alt.Axis(title="")),
            y="Number of Samples",
            color=alt.value("#88AAC7"),
        )
    )

    fig_col1, fig_col2 = st.columns(2, gap="large")

    with fig_col2:
        st.markdown("### Average Number of SNPs per Lineage")
        st.altair_chart(snp_chart, theme="streamlit", use_container_width=True)

    with fig_col1:
        st.markdown("### Total Number of Samples per Lineage")
        st.altair_chart(sample_chart, theme="streamlit", use_container_width=True)


get_chart()

add_vertical_space(5)

# Plot a map
"### Map Showing the Distribution of Samples"
get_map().to_streamlit(height=700)

stoggle(
    "Note",
    """ℹ️ Samples without information about the country of isolation are not shown""",
)
