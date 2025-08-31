# === Imports and Setup ===
import streamlit as st
import pandas as pd
import seaborn as sns
from st_aggrid import AgGrid, GridUpdateMode, GridOptionsBuilder
from io import BytesIO

st.set_page_config(page_title="📁 Excel Manager", layout="wide")
st.title("📁 Record Manager ")
st.sidebar.header("🔧 Upload or Download")

# === Block: Upload and File Selection ===
uploaded_files = st.sidebar.file_uploader("Upload one or more Excel/CSV files", type=["xlsx", "csv"], accept_multiple_files=True)

if uploaded_files:
    file_names = [f.name for f in uploaded_files]
    selected_file_name = st.sidebar.selectbox("Select a file to view/edit", file_names)
    selected_file = next(f for f in uploaded_files if f.name == selected_file_name)

    try:
        file_ext = selected_file.name.split('.')[-1].lower()
        if file_ext == 'csv':
            df = pd.read_csv(selected_file)
        elif file_ext == 'xlsx':
            sheet_names = pd.ExcelFile(selected_file).sheet_names
            selected_sheet = st.sidebar.selectbox("Select sheet", sheet_names)
            df = pd.read_excel(selected_file, sheet_name=selected_sheet, engine='openpyxl')
        else:
            st.error("❌ Unsupported file type.")
            st.stop()
    except Exception as e:
        st.error(f"❌ Failed to read file: {e}")
        st.stop()

    df.columns = [col.strip().upper() for col in df.columns]
    updated_df = df.copy()

    # === Block: Styled Table View ===
    st.subheader("📄 View Table")
    st.dataframe(updated_df.style.background_gradient(cmap='cubehelix'), use_container_width=True)

    # === Block: AG-Grid Inline Editor ===
    st.subheader("✏️ Edit Data Inline ")
    gb = GridOptionsBuilder.from_dataframe(updated_df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=100)
    gb.configure_default_column(editable=True, groupable=True)
    gb.configure_selection(selection_mode="single", use_checkbox=True)
    gridOptions = gb.build()

    grid_response = AgGrid(
        updated_df,
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
        height=600,
        theme="balham"
    )
    updated_df = grid_response["data"]

    # === Block: Add New Column ===
    with st.expander("➕ Add New Column to Table"):
        new_col_name = st.text_input("Column Name")
        default_val = st.text_input("Default Value (optional)", "")
        if st.button("Add Column"):
            if new_col_name and new_col_name.upper() not in updated_df.columns:
                updated_df[new_col_name.upper()] = default_val
                st.success(f"Column '{new_col_name.upper()}' added.")
            else:
                st.warning("Column already exists or name is empty.")

    # === Block: Add New Record ===
    with st.expander("➕ Add New Record"):
        with st.form("add_record_form", clear_on_submit=True):
            st.markdown("Add values matching existing columns:")
            new_row = {}
            cols = st.columns(3)

            for i, col in enumerate(updated_df.columns):
                col_upper = col.upper()
                if "DATE" in col_upper or "D.O.B" in col_upper:
                    new_row[col] = cols[i % 3].date_input(
                        col,
                        value=pd.to_datetime("2000-01-01"),
                        min_value=pd.to_datetime("1950-01-01")
                    )
                elif "STAKING" in col_upper:
                    new_row[col] = cols[i % 3].number_input(col, min_value=0)
                elif "PLAN" in col_upper:
                    new_row[col] = cols[i % 3].selectbox(col, ["FIXED", "VARIABLE"])
                elif "WITHDRAWN" in col_upper:
                    new_row[col] = cols[i % 3].selectbox(col, ["Yes", "No"])
                else:
                    new_row[col] = cols[i % 3].text_input(col)

            submitted = st.form_submit_button("Add Record")
            if submitted:
                for k, v in new_row.items():
                    if isinstance(v, pd.Timestamp):
                        new_row[k] = v.strftime("%d/%m/%Y")
                updated_df = pd.concat([updated_df, pd.DataFrame([new_row])], ignore_index=True)
                st.success("✅ Record added!")

    # === Tool 1: Global Search Across All Text Columns ===
    st.subheader("🔍 Search Tool ")

    global_query = st.text_input("Search ", "")

    filtered_df = updated_df.copy()

    if global_query:
        string_columns = updated_df.select_dtypes(include=["object", "string"]).columns
        mask = pd.Series([False] * len(updated_df))
        for col in string_columns:
            mask |= updated_df[col].astype(str).str.contains(global_query, case=False, na=False)
        filtered_df = updated_df[mask]

    st.write(f"📄 Results found: **{len(filtered_df)}**")
    st.dataframe(filtered_df, use_container_width=True)
    # === Tool 2: Column-Wise Attribute Filter ===
    with st.expander("🎯 Filter Tool", expanded=False):
        attr_search = st.text_input("Search for column name")
        matching_cols = [col for col in updated_df.columns if attr_search.upper() in col.upper()] if attr_search else updated_df.columns.tolist()
        selected_col = st.selectbox("Choose column to filter", matching_cols)

        if selected_col:
            col_data = updated_df[selected_col]
            filtered_df = updated_df.copy()

            if pd.api.types.is_string_dtype(col_data):
                keyword = st.text_input(f"🔤 Search in '{selected_col}'", "")
                if keyword:
                    filtered_df = filtered_df[filtered_df[selected_col].str.contains(keyword, case=False, na=False)]

            elif pd.api.types.is_object_dtype(col_data) or col_data.nunique() < 15:
                options = updated_df[selected_col].dropna().unique().tolist()
                selected_vals = st.multiselect(f"🧩 Choose values for '{selected_col}'", options, default=options)
                filtered_df = filtered_df[updated_df[selected_col].isin(selected_vals)]

            elif pd.api.types.is_numeric_dtype(col_data):
                min_val = float(col_data.min())
                max_val = float(col_data.max())
                range_vals = st.slider(f"🔢 Range for '{selected_col}'", min_val, max_val, (min_val, max_val))
                filtered_df = updated_df[(updated_df[selected_col] >= range_vals[0]) & (updated_df[selected_col] <= range_vals[1])]

            elif pd.api.types.is_datetime64_any_dtype(col_data) or "DATE" in selected_col.upper():
                try:
                    parsed_dates = pd.to_datetime(col_data, errors="coerce")
                    min_date, max_date = parsed_dates.min(), parsed_dates.max()
                    date_range = st.date_input(f"📅 Date range for '{selected_col}'", [min_date, max_date])
                    if len(date_range) == 2:
                        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
                        filtered_df = updated_df[(parsed_dates >= start_date) & (parsed_dates <= end_date)]
                except Exception as e:
                    st.warning(f"⚠️ Date parsing error: {e}")

            else:
                st.info("⚠️ Unsupported column type for filtering.")

            st.write(f"📄 Filtered results: **{len(filtered_df)}**")
            st.dataframe(filtered_df, use_container_width=True)
    # === Tool 3: Advanced Column Sorting Tool ===
    with st.expander("↕ Sort Tool", expanded=False):
        st.markdown("### 📊 Sort the Table")

        # Step 1: Get sortable columns (exclude unstructured types)
        sortable_columns = updated_df.select_dtypes(include=["number", "object", "datetime", "float", "int"]).columns.tolist()

        if not sortable_columns:
            st.warning("No sortable columns available.")
        else:
            # Step 2: Choose column and order
            sort_col = st.selectbox("🔽 Select column to sort by", sortable_columns)
            sort_order = st.radio("⬆️ Sort Order", options=["Ascending", "Descending"], horizontal=True)

            # Step 3: Perform sorting
            ascending = sort_order == "Ascending"

            try:
                sorted_df = updated_df.sort_values(by=sort_col, ascending=ascending, na_position="last").reset_index(drop=True)
                st.success(f"✅ Sorted by '{sort_col}' in {'ascending' if ascending else 'descending'} order.")
                st.dataframe(sorted_df, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Error while sorting: {e}")


    # === Block: Save Updated Excel ===
    st.sidebar.markdown("---")
    st.sidebar.subheader("📅 Save Changes")
    file_name_input = st.sidebar.text_input("Enter file name for download", value="updated_excel")

    def convert_df_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="StakeData")
        return output.getvalue()

    edited_file = convert_df_to_excel(updated_df)
    st.sidebar.download_button(
        label="📥 Download Edited Excel",
        data=edited_file,
        file_name=f"{file_name_input}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("⬅️ Upload one or more Excel or CSV files to get started.")
