import pandas as pd
import geopandas
import pickle
import streamlit as st
import leafmap.kepler as leafmap

from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_extras.add_vertical_space import add_vertical_space
from utils import set_page_config, sidebar_image, set_css

set_page_config()
sidebar_image()
set_css()

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


def get_map_config(input):
    with open(input, "rb") as f:
        config = pickle.load(f)
    return config


dataset = get_data("./data/samples_data.tsv")
country_shapes = get_country_shapes("./data/world_countries.json")
map_config = get_map_config("./data/config.pkl")

# Calculate mean SNPs values
no_vars = (
    dataset[["level 1", "no. of SNPs"]]
    .groupby(["level 1"])
    .mean()
    .reset_index()
    .rename(columns={"level 1": "Main lineage", "no. of SNPs": "Number of SNPs"})
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
    .drop(columns=["id", "Country of isolation"])
    .rename(columns={"name": "Country"})
)

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
        enable_enterprise_modules=True,
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

# Plot two barplots side by side
fig_col1, fig_col2 = st.columns(2, gap="large")

with fig_col1:
    st.markdown("### Mean number of SNPs per lineage")
    st.bar_chart(no_vars, x="Main lineage", y="Number of SNPs")

# with fig_col2:
#     st.markdown("### Total Number of SNPs per Drug Resistance Type")
#     st.bar_chart(dr_snps, x="DR type", y="Total number of SNPs")

# Plot a map
"### Maps Showing the Distributions of Samples "
m = leafmap.Map()
m.add_data(data=cnt_samples_poly, name="Number of Samples")
m.config = map_config

tab1, tab2, tab3 = st.tabs(
    [
        "Distribution of the Analyzed Samples per Country of Isolation",
        "test #1",
        "test #2",
    ]
)

with tab1:
    m.to_streamlit()


# import folium
# from streamlit_folium import st_folium

# url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
# country_shapes = f'{url}/world-countries.json'

# country = pd.read_csv('/Volumes/Extreme_SSD/Work/RNF/TB_app/data/countries.csv').dropna()

# cn_samples = dataset[['Sample', 'country of isolation']] \
#     .groupby(['country of isolation']) \
#         .count() \
#             .reset_index() \
#                 .rename(columns={'Sample': 'Number of Samples', 'country of isolation': 'Country of Isolation'})

# m = folium.Map()

# folium.Choropleth(
#     #The GeoJSON data to represent the world country
#     geo_data=country_shapes,
#     name='choropleth TB samples',
#     data=cn_samples,
#     #The column aceppting list with 2 value; The country name and  the numerical value
#     columns=['Country of Isolation', 'Number of Samples'],
#     key_on='feature.properties.name',
#     fill_color='PuRd',
#     nan_fill_color='white'
# ).add_to(m)

# for lat, lon, name in   zip(country['latitude'],country['longitude'],country['name']):
#     #Creating the marker
#     folium.Marker(
#     #Coordinate of the country
#     location=[lat, lon],
#     #The popup that show up if click the marker
#     popup=name
#     ).add_to(m)

# st_data = st_folium(m, width=1000)
