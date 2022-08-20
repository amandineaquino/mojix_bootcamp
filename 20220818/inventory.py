import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title('Inventory')
st.sidebar.header("Upload your CSV files below:")
inv_soh = st.sidebar.file_uploader('Expected inventory', type="csv")
inv_rfid = st.sidebar.file_uploader('Counted inventory', type="csv")

def compare_headers(from_df, cols_expected):
    col=0
    df_header = from_df.axes[1]
    a = [i for i in cols_expected if i not in df_header]
    return(len(a))

if (inv_soh and inv_rfid):
    df_soh = pd.read_csv(inv_soh, encoding="latin-1", dtype=str)
    df_rfid = pd.read_csv(inv_rfid, encoding="latin-1", dtype=str)
    soh_cols_expected = ["Retail_Product_Color",
    "Retail_Product_Level1Name",
    "Retail_Product_Name",
    "Retail_Product_SKU",
    "Retail_SOHQTY"]
    rfid_cols_expected = ["Retail_Product_SKU", "RFID"]

    if compare_headers(df_soh, soh_cols_expected) == 0 and compare_headers(df_rfid, rfid_cols_expected) == 0:
        df_soh = df_soh[soh_cols_expected]
        df_rfid = df_rfid.drop_duplicates("RFID")
        df_rfid_groupby = df_rfid.groupby("Retail_Product_SKU").count()[["RFID"]].reset_index()[rfid_cols_expected].rename(columns={"RFID":"Retail_CCQTY"})
        df_discrepancies = pd.merge(df_soh, df_rfid_groupby, how="outer", left_on="Retail_Product_SKU", right_on="Retail_Product_SKU")
        df_discrepancies['Retail_CCQTY'] = df_discrepancies['Retail_CCQTY'].fillna(0).astype(int)
        df_discrepancies["Retail_SOHQTY"] = df_discrepancies["Retail_SOHQTY"].fillna(0).astype(int)
        df_discrepancies = df_discrepancies.rename(columns={
            "Retail_Product_Level1Name":"Department",
            "Retail_Product_Name":"Product name",
            "Retail_Product_Color":"Color",
            "Retail_Product_SKU":"SKU"})

        df_discrepancies["Diff"] = df_discrepancies["Retail_CCQTY"] - df_discrepancies["Retail_SOHQTY"]
        
        df_discrepancies.loc[df_discrepancies["Diff"]<0, "Unders"] = df_discrepancies["Diff"] * (-1)
        df_discrepancies["Unders"] = df_discrepancies["Unders"].fillna(0).astype(int)
        
        df_discrepancies.loc[df_discrepancies["Diff"]>0, "Overs"] = df_discrepancies["Diff"]
        df_discrepancies["Overs"] = df_discrepancies["Overs"].fillna(0).astype(int)

        overview, details_dis, rfid_details = st.tabs(["Overview","Details Discrepancies","RFID details"])

        with overview:
            st.table(df_discrepancies.groupby("Department").sum())
        
        with details_dis:
            st.subheader('Filters')
            df_only_discrepancies = df_discrepancies.loc[df_discrepancies['Diff'] != 0]
            department=st.selectbox('Select department', df_only_discrepancies['Department'].dropna().unique())
            df_filtered_department = df_only_discrepancies.loc[df_only_discrepancies['Department']==department]
            
            if(len(df_filtered_department['Color'].dropna().unique())) > 0:
                color=st.selectbox('Select color', df_filtered_department['Color'].dropna().unique())
                new_df = df_filtered_department.loc[(df_only_discrepancies['Color']==color)]
                expected_columns = ["Department","Color","Product name","SKU","Retail_SOHQTY", "Retail_CCQTY", "Unders", "Overs"]
            else:
                new_df = df_filtered_department
                expected_columns = ["Department","Product name","SKU","Retail_SOHQTY", "Retail_CCQTY", "Unders", "Overs"]
            
            final_df = new_df[expected_columns].reset_index()
            st.dataframe(final_df[expected_columns])

        with rfid_details:
            st.subheader("Distribution by zone")
            labels = df_rfid['Retail_ZoneName'].unique().tolist()
            sizes = df_rfid.groupby("Retail_ZoneName").count()["RFID"].astype(float).tolist()
            colors = ['#66b3ff','#99ff99']
            
            fig1, ax1 = plt.subplots()
            patches, texts, autotexts = ax1.pie(
                sizes, colors = colors, labels=labels,
                autopct='%1.1f%%', startangle=45,
                explode=(0, 0.1))
            for text in texts:
                text.set_color('grey')
            for autotext in autotexts:
                autotext.set_color('black')

            # Equal aspect ratio ensures that pie is drawn as a circle
            ax1.axis('equal')  
            plt.tight_layout()
            fig1.patch.set_alpha(0)

            st.pyplot(fig1)

            
    else:
        st.error("Error: at least one file doesn't contains the expected columns", icon="🚨")
else:
        st.info("Please upload expected and counted inventory files", icon="ℹ️")
