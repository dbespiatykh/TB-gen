import os
import time
import numpy as np
import pandas as pd
import streamlit as st

from vcf import Reader
from gzip import BadGzipFile
from gzip import open as gzopen
from collections import OrderedDict
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
def get_levels_dictionary():
    temp_df = pd.read_csv("./data/levels.tsv", sep="\t")
    uniqueLevels = temp_df["level"].unique()
    levelsDict = {elem: pd.DataFrame() for elem in uniqueLevels}

    for key in levelsDict.keys():
        levelsDict[key] = temp_df[:][temp_df["level"] == key]

    lvl1 = (
        levelsDict[1]["POS"].values,
        levelsDict[1]["REF"].values,
        levelsDict[1]["ALT"].values,
        levelsDict[1]["lineage"].values,
    )
    lvl2 = (
        levelsDict[2]["POS"].values,
        levelsDict[2]["REF"].values,
        levelsDict[2]["ALT"].values,
        levelsDict[2]["lineage"].values,
    )
    lvl3 = (
        levelsDict[3]["POS"].values,
        levelsDict[3]["REF"].values,
        levelsDict[3]["ALT"].values,
        levelsDict[3]["lineage"].values,
    )
    lvl4 = (
        levelsDict[4]["POS"].values,
        levelsDict[4]["REF"].values,
        levelsDict[4]["ALT"].values,
        levelsDict[4]["lineage"].values,
    )
    lvl5 = (
        levelsDict[5]["POS"].values,
        levelsDict[5]["REF"].values,
        levelsDict[5]["ALT"].values,
        levelsDict[5]["lineage"].values,
    )

    return lvl1, lvl2, lvl3, lvl4, lvl5


# @st.cache_data()
# def get_lineage4_positions():
#     temp_df = pd.read_csv("./data/levels.tsv", sep="\t")
#     uniqueLevels = temp_df["level"].unique()
#     levelsDict = {elem: pd.DataFrame() for elem in uniqueLevels}

#     for key in levelsDict.keys():
#         levelsDict[key] = temp_df[:][temp_df["level"] == key]

#     lineage4_pos = np.concatenate(
#         (
#             levelsDict[1].loc[levelsDict[1]["lineage"] == "L4", "POS"].values,
#             levelsDict[2].loc[levelsDict[2]["lineage"] == "L4.9", "POS"].values,
#         )
#     )

#     return lineage4_pos


@st.cache_data()
def get_levels_positions():
    temp_df = pd.read_csv("./data/levels.tsv", sep="\t")
    pos = temp_df["POS"].values
    return pos


@st.cache_data(show_spinner=False)
def vcf_to_dataframe(vcf_file):
    pos_all = get_levels_positions()
    # lineage4_pos = get_lineage4_positions()
    vcf_reader = Reader(vcf_file, "r")
    res = []
    cols = ["Sample", "REF", "ALT", "POS"]

    for rec in vcf_reader:
        x = [rec.end]
        for sample in rec.samples:
            if sample.gt_bases is None:
                # no call
                row = [sample.sample, rec.REF, sample.gt_bases]
            elif rec.REF != sample.gt_bases:
                row = [sample.sample, rec.REF, sample.gt_bases] + x
            else:
                # call is REF
                row = [sample.sample, rec.REF, sample.gt_bases] + x

            res.append(row)

    res = pd.DataFrame(res, columns=cols)
    res = res[~res.POS.isnull()]

    res = res.astype(
        {"Sample": "object", "REF": "object", "ALT": "object", "POS": "int64"}
    )

    res = res.loc[res["POS"].isin(pos_all)]
    # lineage4 = res.loc[res["POS"].isin(lineage4_pos)]
    # lineage4 = lineage4[
    #     ~lineage4.duplicated(["Sample", "POS"], keep=False)
    #     | lineage4["ALT"].ne(lineage4["REF"])
    # ]
    # res = res.drop(res[res["REF"] == res["ALT"]].index)
    # frames = [res, lineage4]
    # res = pd.concat(frames)
    res["ALT"] = res["ALT"].str.split("/").str.get(-1)
    return res


@st.cache_data()
def lineage4_decision(call_list):
    lin4 = ["L4"]
    altList = []

    for item in call_list:
        if any(i in item for i in lin4):
            item = [x for x in item if x not in lin4]

        else:
            item.extend(["L4" for i in range(2)])

        altList.append(item)

    return altList


@st.cache_data()
def lineage4_9_decision(call_list):
    lin4_9 = ["L4.9"]
    altList = []

    for item in call_list:
        if any(i in item for i in lin4_9):
            item = [x for x in item if x not in lin4_9]

        else:
            item.extend(["L4.9" for i in range(2)])

        altList.append(item)

    return altList


@st.cache_data()
def count_level1_variants(call_list):
    d = OrderedDict()

    for item in call_list:
        if not len(item) == 0:
            caseless = item.casefold()
            try:
                d[caseless][1] += 1
            except KeyError:
                d[caseless] = [item, 1]

    call_list = []

    for item, count in d.values():
        if not item.startswith("L8"):
            if count > 1:
                item = f"{item}"
            elif count == 1:
                item = f"{item} [warning! only 1/2 snp is present]"
        call_list.append(item)

    return call_list


@st.cache_data()
def count_level2_variants(call_list):
    d = OrderedDict()

    for item in call_list:
        if not len(item) == 0:
            caseless = item.casefold()
            try:
                d[caseless][1] += 1
            except KeyError:
                d[caseless] = [item, 1]

    call_list = []

    for item, count in d.values():
        if not item.startswith(("L2.2 (modern)", "L2.2 (ancient)")):
            if count > 1:
                item = f"{item}"
            elif count == 1:
                item = f"{item} [warning! only 1/2 snp is present]"
        elif item.startswith(("L2.2 (modern)", "L2.2 (ancient)")):
            if count > 1:
                item = f"{item}"
            elif count == 1:
                if not item.startswith("L2.2 (modern)"):
                    item = f"{item} [warning! only 1/2 snp is present]"
                if item.startswith("L2.2 (modern)"):
                    item = f"{item}"
        call_list.append(item)

    return call_list


@st.cache_data()
def lineage2_decision(call_list):
    lin2 = ["L2.2 (modern)", "L2.2 (ancient)"]
    altList = []

    for item in call_list:
        if all(i in item for i in lin2) is True:
            item = list(set(item) - set(lin2))
            item.append("L2.2 (modern)")
        else:
            item = item

        altList.append(item)

    return altList


@st.cache_data()
def convert_df_to_tsv(df):
    return df.to_csv(sep="\t", index=False).encode("utf-8")


@st.cache_data()
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")


@st.cache_data(show_spinner=False)
def barcoding(uploaded_vcf):
    df = vcf_to_dataframe(uploaded_vcf)
    lvl1, lvl2, lvl3, lvl4, lvl5 = get_levels_dictionary()

    exp = (
        df["POS"].values[:, None],
        df["REF"].values[:, None],
        df["ALT"].values[:, None],
    )

    df["level_1"] = np.dot(
        np.logical_and.reduce(
            [
                np.equal(exp[0], lvl1[0]),
                np.equal(exp[1], lvl1[1]),
                np.equal(exp[2], lvl1[2]),
            ]
        ),
        lvl1[3],
    )

    df["level_2"] = np.dot(
        np.logical_and.reduce(
            [
                np.equal(exp[0], lvl2[0]),
                np.equal(exp[1], lvl2[1]),
                np.equal(exp[2], lvl2[2]),
            ]
        ),
        lvl2[3],
    )

    df["level_3"] = np.dot(
        np.logical_and.reduce(
            [
                np.equal(exp[0], lvl3[0]),
                np.equal(exp[1], lvl3[1]),
                np.equal(exp[2], lvl3[2]),
            ]
        ),
        lvl3[3],
    )

    df["level_4"] = np.dot(
        np.logical_and.reduce(
            [
                np.equal(exp[0], lvl4[0]),
                np.equal(exp[1], lvl4[1]),
                np.equal(exp[2], lvl4[2]),
            ]
        ),
        lvl4[3],
    )

    df["level_5"] = np.dot(
        np.logical_and.reduce(
            [
                np.equal(exp[0], lvl5[0]),
                np.equal(exp[1], lvl5[1]),
                np.equal(exp[2], lvl5[2]),
            ]
        ),
        lvl5[3],
    )

    df = df.drop(["REF", "ALT", "POS"], axis=1)
    df = df.replace("", np.nan)

    df = (
        df.groupby(["Sample"])
        .agg(lambda x: ",".join(x.dropna()))
        .reset_index()
        .reindex(columns=df.columns)
    )

    df2 = df.copy()

    df2["level_1"] = df2["level_1"].str.split(",")
    df2["level_2"] = df2["level_2"].str.split(",")
    df2["level_1"] = lineage4_decision(df2["level_1"])
    df2["level_2"] = lineage4_9_decision(df2["level_2"])
    df2["level_1"] = [count_level1_variants(item) for item in df2["level_1"]]
    df2["level_2"] = [count_level2_variants(item) for item in df2["level_2"]]
    df2["level_2"] = lineage2_decision(df2["level_2"])

    df2[["level_1", "level_2"]] = df2[["level_1", "level_2"]].applymap(
        lambda x: ", ".join(map(str, x))
    )

    df2 = df2.sort_values(
        by=["level_1", "level_2", "level_3", "level_4", "level_5"]
    ).reset_index(drop=True)

    return df2


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
            lottie_container("No data was uploaded!", "warning", "⚠️", lottie_warning)

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

            except ValueError:
                info_box()
                lottie_container("Wrong file type!", "warning", "⚠️", lottie_warning)

            except BadGzipFile:
                info_box()
                lottie_container("File is not gzipped!", "error", "❗", lottie_error)

            except StopIteration:
                info_box()
                lottie_container("VCF file is malformed!", "error", "❗", lottie_error)

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
                    info_box()
                    lottie_container(
                        "No genotypes were called", "warning", "⚠️", lottie_warning
                    )

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

                    tsv = convert_df_to_tsv(results)
                    csv = convert_df_to_csv(results)

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
        lottie_container(
            "Press the <Genotype lineage> button!", "info", None, lottie_arrow
        )

    elif len(uploaded_files) == 0:
        lottie_container(
            "Upload input data in the sidebar to start!", "info", None, lottie_arrow
        )


if __name__ == "__main__":
    main()
