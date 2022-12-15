import base64
import pandas as pd
import geopandas
import pickle
import streamlit as st
import leafmap.kepler as leafmap

from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(
    page_title="Global Mycobacterium tuberculosis data",
    page_icon=":earth_africa:",
    layout="wide",
    initial_sidebar_state="expanded",
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

st.sidebar.success("Select a page above")

st.sidebar.header("Header `ver 1`")
st.sidebar.subheader("Sunheader")

st.markdown("# Global _Mycobacterium tuberculosis_ data")
st.markdown(
    """
Streamlit is an open-source app framework built specifically for
Machine Learning and Data Science projects.
**👈 Select a demo from the sidebar** to see some examples
of what Streamlit can do!
### Want to learn more?
- Check out [streamlit.io](https://streamlit.io)
- Jump into our [documentation](https://docs.streamlit.io)
- Ask a question in our [community
    forums](https://discuss.streamlit.io)
### See more complex demos
- Use a neural net to [analyze the Udacity Self-driving Car Image
    Dataset](https://github.com/streamlit/demo-self-driving)
- Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)


genotype_user_data = st.button("Genotype VCF")
if genotype_user_data:
    switch_page("genotype lineage")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.write(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto');
html, body, [class*="css"]  {
   font-family: 'Roboto';
}
</style>
""",
    unsafe_allow_html=True,
)


main_dataset = "./data/tb_data.csv"


@st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_csv(main_dataset)


df = get_data()

# Calculate mean DR SNPs values
dr_vars = (
    df[["DR_type", "num_dr_variants"]]
    .groupby(["DR_type"])
    .mean()
    .reset_index()
    .rename(columns={"DR_type": "DR type", "num_dr_variants": "Number of DR SNPs"})
)

# Calculate mean ALL SNPs values
dr_snps = (
    df[["DR_type", "SNPs"]]
    .groupby(["DR_type"])
    .mean()
    .reset_index()
    .rename(columns={"DR_type": "DR type", "SNPs": "Total number of SNPs"})
)

# Load Country Shapes file
# country_url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
# country_shapes = f'{country_url}/world-countries.json'
country_shapes = "./data/world_countries.json"
country = geopandas.read_file(country_shapes)

# Calculate number of samples per country
cnt_samples = (
    df[["Sample", "country of isolation"]]
    .groupby(["country of isolation"])
    .count()
    .reset_index()
    .rename(columns={"Sample": "Number of Samples", "country of isolation": "name"})
)

# Merge country shapes and counts data
cnt_samples_poly = (
    country.merge(cnt_samples, on="name")
    .drop(columns=["id"])
    .rename(columns={"name": "Country"})
)

# Load configuration file for kepler
with open("./data/config.pkl", "rb") as f:
    config = pickle.load(f)

####################################################################################################################
# st.markdown("## Dataset")
gd = GridOptionsBuilder.from_dataframe(
    df, enableRowGroup=True, enableValue=True, enablePivot=True
)
gd.configure_grid_options(domLayout="normal")
gd.configure_selection(selection_mode="multiple", use_checkbox=True)
gd.configure_default_column(editable=True, groupable=True)
# gd.configure_pagination(enabled=True, paginationPageSize=100)
gd.configure_side_bar()

if st.checkbox("Show Dataset"):
    # st.subheader('Dataset')
    # st.dataframe(df)
    grid1 = AgGrid(
        df,
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
    df_sel = pd.DataFrame(sel_row)
    st.subheader("Selected Samples")
    # Grid 2
    builder = GridOptionsBuilder.from_dataframe(df_sel)
    builder.configure_column("_selectedRowNodeInfo", hide=True)
    go = builder.build()
    grid2 = AgGrid(df_sel, gridOptions=go, height=150, theme="streamlit")

sm1, mk = st.columns([2, 5])
sm1.metric(
    label="Total Samples",
    value=int(df["Sample"].count()),
    help="""Number of currently availible samples in the database
        """,
)


def sample_stats(df):
    # Dataframe filter
    sample_filter = st.selectbox("Select Sample", pd.unique(df["Sample"]))
    df = df[df["Sample"] == sample_filter]

    # Create six columns
    sd1, sd2, sd3, sd4, sd5, sd6 = st.columns(6, gap="small")

    # Fill columns with Sample metics
    sd1.metric(
        label="SNPs",
        value=int(df["SNPs"]),
        help="""Number of single nucteotide polymorphisms (SNPs) 
                relative to the _M. tuberculosis_ H37Rv genome 
               (GenBank accession no. [NC_000962.3](https://www.ncbi.nlm.nih.gov/nuccore/NC_000962.3/)
            """,
    )

    sd2.metric(
        label="GC %",
        value=int(df["%GC"]),
        help="""GC-content (guanine-cytosine content) in the sample
            """,
    )

    sd3.metric(label="Total Sequences", value=int(df["Total Sequences"]))

    sd4.metric(
        label="Average Sequence Length",
        value=float(round(df["avg_sequence_length"], 2)),
    )

    sd5.metric(
        label="Mapped Reads %",
        value=float(round(df["reads_mapped_percent"], 2)),
        help="""Percenatege of the reads mapped to the _M. tuberculosis_ H37Rv genome 
            (GenBank accession no. [NC_000962.3](https://www.ncbi.nlm.nih.gov/nuccore/NC_000962.3/)
            """,
    )

    sd6.metric(
        label="Mean depth",
        value=float(round(df["Mean depth"], 2)),
        help="""Mean depth of the sample mapped to the _M. tuberculosis_ H37Rv genome 
            (GenBank accession no. [NC_000962.3](https://www.ncbi.nlm.nih.gov/nuccore/NC_000962.3/)
            """,
    )

    # Create another six columns
    sd7, sd8, sd9, sd10, sd11, sd12 = st.columns(6, gap="small")

    sd7.metric(label="Project", value=str(df["Collection"].item()))

    sd8.metric(
        label="Country of Isolation", value=str(df["country of isolation"].item())
    )

    sd9.metric(
        label="UN Geographic Region",
        value=str(df["United Nations Geographic Region"].item()),
    )

    sd10.metric(label="Main Lineage", value=str(df["main_lineage"].item()))

    sd11.metric(label="Sublineage", value=str(df["sub_lineage"].item()))

    sd12.metric(label="Drug Resistance Type", value=str(df["DR_type"].item()))

    sd13, sd14 = st.columns((7, 3.5), gap="small")

    sd13.metric(label="Spoligotype pattern", value=str(df["Spoligo Binary"].item()))

    sd14.metric(
        label="SITVIT2 Lineage", value=str(df["Curated lineage (SITVIT2)"].item())
    )

    # st.metric(
    #     label="Spoligotype pattern",
    #     value=str(df['Spoligo Binary'].item())
    #     )

    # st.metric(
    #     label="SITVIT2 Lineage",
    #     value=str(df['Curated lineage (SITVIT2)'].item())
    #     )


sample_stats(df)

# expander = st.expander("†")
# expander.write("""
#     All metrics relative to reference
#     _M. tuberculosis_ H37Rv genome
#     (GenBank accession no. [NC_000962.3](https://www.ncbi.nlm.nih.gov/nuccore/NC_000962.3/))
# """)

# Plot two barplots side by side
fig_col1, fig_col2 = st.columns(2, gap="large")

with fig_col1:
    st.markdown("### Number of Drug Resistand SNPs")
    st.bar_chart(dr_vars, x="DR type", y="Number of DR SNPs")

with fig_col2:
    st.markdown("### Total Number of SNPs per Drug Resistance Type")
    st.bar_chart(dr_snps, x="DR type", y="Total number of SNPs")

# Plot a map
"### Maps Showing the Distributions of Samples "
m = leafmap.Map()
m.add_data(data=cnt_samples_poly, name="Number of Samples")
m.config = config

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

# cn_samples = df[['Sample', 'country of isolation']] \
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
