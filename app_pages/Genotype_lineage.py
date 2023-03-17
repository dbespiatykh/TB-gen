import os
import time
import numpy as np
import pandas as pd
import streamlit as st

from typing import TextIO
from gzip import BadGzipFile
from gzip import open as gzopen
from tempfile import NamedTemporaryFile
from utils import (
    set_page_config,
    sidebar_image,
    set_css,
    home_page,
    lottie_success,
    lottie_error,
    lottie_warning,
    lottie_arrow,
    lottie_spinner,
)


def page_info():
    st.markdown(
        """
        <h2 style="text-align: left; color: #7a3777">
        <strong>Genotype lineage from VCF file</strong>
        </h2>
        <hr
        style="
            height: 2px;
            border-width: 0;
            color: #A9A5D1;
            background-color: #A9A5D1;
        "
        />
        """,
        unsafe_allow_html=True,
    )


def info_box():
    box = st.empty()
    with box.container():
        st.markdown(
            """
            Use your own **:blue[.VCF]** or **:blue[.VCF.GZ]** files as input to call lineage  \n
            - You can use both **:green[single-]** or **:green[multi-sample]** **:blue[.VCF]** files
            - Accepts **:green[multiple]** **:blue[.VCF]** files at a time
            - Variants should be called by mapping to the [NC_000962.3](https://www.ncbi.nlm.nih.gov/nuccore/NC_000962.3/) _M. tuberculosis_ H37Rv genome
            - It is preferable for variants to be filtered and contain only high quality calls
            """
        )
        st.markdown(
            """
            <p style="color: #737a7c">
            <sub
                >Example .VCF file can be downloaded from the
                <a
                target="_self"
                href="/Reference%20dataset"
                style="color: #a65aa3; text-decoration: none"
                >
                Reference dataset</a
                >
                page</sub
            >
            </p>
            """,
            unsafe_allow_html=True,
        )
    return box


def lottie_container(message_string, message_type, icon, lottie_function):
    with st.container():
        if icon is None:
            if message_type == "info":
                st.info(message_string)
            elif message_type == "warning":
                st.warning(message_string)
            elif message_type == "error":
                st.error(message_string)
        else:
            if message_type == "info":
                st.info(message_string, icon=icon)
            elif message_type == "warning":
                st.warning(message_string, icon=icon)
            elif message_type == "error":
                st.error(message_string, icon=icon)

        col1, col2 = st.columns([1, 10])

        with col1:
            lottie_function()
        with col2:
            pass


@st.cache_data()
def convert_df_to_file(df, file_format="csv", sep=","):
    if file_format == "csv":
        return df.to_csv(sep=sep, index=False).encode("utf-8")
    elif file_format == "tsv":
        return df.to_csv(sep="\t", index=False).encode("utf-8")
    else:
        raise ValueError(f"Unsupported file format: {file_format}")


@st.cache_data()
def get_levels_data():
    temp_df = pd.read_csv("./data/levels.tsv", sep="\t")
    uniqueLevels = temp_df["level"].unique()
    levelsDict = {}

    # For each unique level value, extract the relevant data and store it in the dictionary
    for elem in uniqueLevels:
        levelsDict[elem] = temp_df[temp_df["level"] == elem][
            ["POS", "REF", "ALT", "lineage"]
        ]

    # Create a tuple of NumPy arrays, where each array contains the data for a different level
    # Each array contains the positional data, the reference allele, the alternate allele,
    # and the lineage (i.e., the level value) for each row in the data
    # The tuple contains data for levels 1 through 5
    levels_data = tuple(
        levelsDict.get(i, pd.DataFrame())[["POS", "REF", "ALT", "lineage"]].to_numpy().T
        for i in range(1, 6)
    )

    pos = temp_df["POS"].values

    return levels_data, pos


@st.cache_data(show_spinner=False)
def vcf_to_dataframe(file: TextIO):
    pos_all = get_levels_data()[1]

    # Remove all header lines from the input file
    lines = [line.strip() for line in file if not line.startswith("##")]

    # Extract the sample names from the first header line
    header = lines.pop(0).split("\t")[9:]

    # Extract data from each line of the input file and convert it to a list
    data = []
    for line in lines:
        fields = line.split("\t")
        pos, ref, alt = fields[1], fields[3], fields[4]
        alleles = [ref] + alt.split(",")
        genotypes = [genotype.split(":") for genotype in fields[9:]]
        for i, gt in enumerate(genotypes):
            if gt[0] == "." or gt[0] == "./." or gt[0] == ".|.":
                allele = np.nan
            elif "/" in gt[0]:
                alleles_list = [
                    alleles[int(x)] if x != "." else np.nan for x in gt[0].split("/")
                ]
                allele = "/".join([x for x in alleles_list if str(x) != "nan"])
            elif "|" in gt[0]:
                alleles_list = [
                    alleles[int(x)] if x != "." else np.nan for x in gt[0].split("|")
                ]
                allele = "|".join([x for x in alleles_list if str(x) != "nan"])
            else:
                allele = alleles[int(gt[0])]
            data.append([header[i], pos, ref, allele])

    # Convert the list of data to a Pandas DataFrame
    df = pd.DataFrame(data, columns=["Sample", "POS", "REF", "ALT"])

    # Set the data types for each column in the DataFrame
    df = df.astype(
        {"Sample": "object", "REF": "object", "ALT": "object", "POS": "int64"}
    )

    # Strip "/" and "|"
    df["ALT"] = df["ALT"].str.split(r"[/|]").str[-1]

    # Filter the DataFrame to only include rows with positions in the pos_all list
    df = df.loc[df["POS"].isin(pos_all)]

    # Return the filtered DataFrame
    return df


# This function takes a list of calls and a lineage as input and returns a new list
# that either removes the lineage if it exists in the call or adds the lineage to the
# call twice if it does not exist in the call.
@st.cache_data(show_spinner=False)
def lineage4_decision(call_list, lin):
    altList = []
    for item in call_list:
        if any(i in item for i in lin):
            item = [x for x in item if x not in lin]
        else:
            item.extend([lin[0] for i in range(2)])
        altList.append(item)
    return altList


# This function takes a list of calls as input and returns a new list with each call
# count and formatted as a string. If a prefix is provided, it only includes calls that
# start with the prefix in the output.
@st.cache_data(show_spinner=False)
def count_variants(call_list, prefix=None):
    d = {}
    for item in call_list:
        if item:
            caseless = item.casefold()
            if caseless in d:
                d[caseless][1] += 1
            else:
                d[caseless] = [item, 1]

    call_list = []
    for item, count in d.values():
        if not item.startswith(prefix) if prefix else True:
            item = (
                f"{item}" if count > 1 else f"{item} [warning! only 1/2 snp is present]"
            )
        call_list.append(item)

    return call_list


# This function takes a list of calls as input and returns a new list that either
# removes the lineage "L2.2 (modern)" and "L2.2 (ancient)" if both exist in the call
# or adds the lineage "L2.2 (modern)" if the call contains "L2.2 (ancient)".
@st.cache_data(show_spinner=False)
def lineage2_decision(call_list):
    lin2 = ["L2.2 (modern)", "L2.2 (ancient)"]
    altList = []
    for item in call_list:
        if all(i in item for i in lin2):
            item = list(set(item) - set(lin2))
            item.append(lin2[0])
        altList.append(item)
    return altList


# This function takes a VCF file as input and returns a DataFrame with barcoding information.
@st.cache_data(show_spinner=False)
def barcoding(uploaded_vcf):
    # Convert VCF to DataFrame
    df = vcf_to_dataframe(uploaded_vcf)

    # Get levels dictionary and create a list of level names
    levels = get_levels_data()[0]
    level_names = [f"level_{i+1}" for i in range(len(levels))]

    # Define a function to compute the level of each sample
    def compute_level(level):
        exp = (
            df["POS"].values[:, None],
            df["REF"].values[:, None],
            df["ALT"].values[:, None],
        )
        mask = np.logical_and.reduce(
            [
                np.equal(exp[0], level[0]),
                np.equal(exp[1], level[1]),
                np.equal(exp[2], level[2]),
            ]
        )
        return np.dot(mask, level[3])

    # Compute the level of each sample for each level
    for i, level in enumerate(levels):
        df[level_names[i]] = compute_level(level)

    # Drop the columns REF, ALT, and POS and replace empty strings with NaN
    df.drop(["REF", "ALT", "POS"], axis=1, inplace=True)
    df.replace("", np.nan, inplace=True)

    # Group the data by sample and concatenate the level columns into comma-separated strings
    df = df.groupby(["Sample"]).agg(lambda x: ",".join(x.dropna())).reset_index()

    # Split the first two level columns into lists and apply lineage decision and count variants functions
    df[level_names[:2]] = df[level_names[:2]].applymap(lambda x: x.split(","))
    df[level_names[0]] = lineage4_decision(df[level_names[0]], ["L4"])
    df[level_names[1]] = lineage4_decision(df[level_names[1]], ["L4.9"])
    df[level_names[0]] = df[level_names[0]].apply(count_variants, prefix="L8")
    df[level_names[1]] = df[level_names[1]].apply(
        count_variants, prefix=("L2.2 (modern)", "L2.2 (ancient)")
    )
    df[level_names[1]] = lineage2_decision(df[level_names[1]])

    # Convert the first two level columns back to comma-separated strings
    df[level_names[:2]] = df[level_names[:2]].applymap(lambda x: ", ".join(map(str, x)))

    # Sort the dataframe by level and reset the index
    df.sort_values(level_names, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Return the final dataframe
    return df


def temporary_vcf_gz(uploaded_file):
    with NamedTemporaryFile(
        dir=".",
        suffix=".vcf.gz",
        delete=False,
    ) as temp_vcf:
        temp_vcf.write(uploaded_file.getbuffer())

    return temp_vcf.name


def temporary_vcf(uploaded_file):
    with NamedTemporaryFile(
        dir=".",
        suffix=".vcf",
        delete=False,
    ) as temp_vcf:
        temp_vcf.write(uploaded_file.getbuffer())

    return temp_vcf.name


@st.cache_data(show_spinner=False)
def genotype_lineages(uploaded_file):
    uploaded_extension = uploaded_file.name.split(".")[-1]

    if uploaded_extension == "gz":
        try:
            temp_vcf = temporary_vcf_gz(uploaded_file)
            uploaded_vcf = gzopen(temp_vcf, "rt")
            result = barcoding(uploaded_vcf)
        finally:
            os.remove(temp_vcf)
    else:
        try:
            temp_vcf = temporary_vcf(uploaded_file)
            uploaded_vcf = open(temp_vcf)
            result = barcoding(uploaded_vcf)
        finally:
            os.remove(temp_vcf)
    return result


def get_uploaded_files():
    with st.sidebar.container():
        uploaded_files = st.file_uploader(
            "**Upload** **:blue[.VCF]** **file**",
            type=["vcf", "vcf.gz"],
            accept_multiple_files=True,
        )
    return uploaded_files


def main():
    set_page_config()
    sidebar_image()
    set_css()
    home_page()
    page_info()

    info_ct = info_box()
    uploaded_files = get_uploaded_files()

    if st.sidebar.button("Genotype lineage", type="primary"):
        if len(uploaded_files) == 0:
            message = "No data was uploaded!"
            icon = "warning"
            symbol = "⚠️"
            animation = lottie_warning
            lottie_container(message, icon, symbol, animation)

        else:
            try:
                t_start = time.perf_counter()
                results_list = []

                for uploaded_file in uploaded_files:
                    with lottie_spinner():
                        info_ct.empty()
                        out = genotype_lineages(uploaded_file)
                        results_list.append(out)

                results = pd.concat(results_list).reset_index(drop=True)

            except (ValueError, BadGzipFile, StopIteration, IndexError) as e:
                error_messages = {
                    ValueError: "Wrong file type!",
                    BadGzipFile: "File is not gzipped!",
                    StopIteration: "VCF file is malformed!",
                    IndexError: "VCF file is malformed!",
                }
                message = error_messages.get(type(e), "An unknown error occurred")
                icon = "error"
                symbol = "❗️"
                animation = lottie_error
                info_box()
                lottie_container(message, icon, symbol, animation)

            else:
                if (
                    results.empty
                    or all(
                        results.loc[:, results.columns != "Sample"]
                        .replace("", np.nan)
                        .isna()
                        .all()
                    )
                    is True
                ):
                    message = "No genotypes were called"
                    icon = "warning"
                    symbol = "⚠️"
                    animation = lottie_warning
                    info_box()
                    lottie_container(message, icon, symbol, animation)

                else:
                    t_end = time.perf_counter()
                    hours, rem = divmod(t_end - t_start, 3600)
                    minutes, seconds = divmod(rem, 60)
                    elapsed = f"{int(hours):0>2}:{int(minutes):0>2}:{seconds:05.2f}"

                    placeholder = st.empty()
                    with placeholder.container():
                        lottie_success()
                        time.sleep(1.6)
                    placeholder.empty()

                    st.dataframe(results, width=900)
                    st.success(f"Done! ⏱️ {elapsed}")

                    tsv = convert_df_to_file(results, file_format="tsv")
                    csv = convert_df_to_file(results)

                    dwn1, dwn2, mock = st.columns([1, 1, 4])

                    with dwn1:
                        st.download_button(
                            label="💾 Download data as TSV",
                            data=tsv,
                            file_name="lineage.tsv",
                            mime="text/csv",
                        )

                    with dwn2:
                        st.download_button(
                            label="💾 Download data as CSV",
                            data=csv,
                            file_name="lineage.csv",
                            mime="text/csv",
                        )

                    with mock:
                        pass

    elif len(uploaded_files) != 0:
        message = "Press the <Genotype lineage> button!"
        icon = "info"
        symbol = None
        animation = lottie_arrow
        lottie_container(message, icon, symbol, animation)

    elif len(uploaded_files) == 0:
        message = "Upload input data in the sidebar to start!"
        icon = "info"
        symbol = None
        animation = lottie_arrow
        lottie_container(message, icon, symbol, animation)


if __name__ == "__main__":
    main()
