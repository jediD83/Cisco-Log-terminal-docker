import streamlit as st
import pandas as pd
import re
import io

# --- 1. THE PARSING LOGIC ---
def parse_cli_output(file_content: str) -> dict:
    switch_data = {}
    
    # Hostname
    hostname_match = re.search(r'^([\w.-]+)#', file_content, re.MULTILINE)
    switch_data['Hostname'] = hostname_match.group(1) if hostname_match else 'Not-Found'
    
    # Version
    version_match = re.search(r'Cisco.*Software.*, Version ([\w.()]+)', file_content, re.IGNORECASE)
    if not version_match:
        version_match = re.search(r'System image file is .*-(.+)\.bin', file_content)
    switch_data['Version'] = version_match.group(1) if version_match else 'Not Found'
    
    # Memory
    memory_match = re.search(r'Processor Pool Total:.*?Used:\s*(.*?), Free:\s*(.*)', file_content)
    if memory_match:
        switch_data['Used Memory'] = memory_match.group(1).strip()
        switch_data['Free Memory'] = memory_match.group(2).strip()
    else:
        memory_match = re.search(r'Memory usage:.*?Used:\s*(.*?)K.*?Free:\s*(.*?)K', file_content)
        if memory_match:
            switch_data['Used Memory'] = f"{memory_match.group(1)}K"
            switch_data['Free Memory'] = f"{memory_match.group(2)}K"
        else:
            switch_data['Used Memory'] = 'N/A'
            switch_data['Free Memory'] = 'N/A'
            
    # CPU
    cpu_match = re.search(r'five minutes: ([\d.]+)%', file_content)
    switch_data['5min CPU %'] = f"{cpu_match.group(1)}%" if cpu_match else 'N/A'
    
    return switch_data

# --- 2. THE DASHBOARD UI ---
st.set_page_config(page_title="Cisco Log Analyzer", layout="wide")

st.title("🌐 Cisco Network Log Analyzer")
st.markdown("Upload your Cisco `.txt` log files below to extract system information.")

# File Uploader
uploaded_files = st.file_uploader("Choose Cisco Log Files", type="txt", accept_multiple_files=True)

if uploaded_files:
    all_data = []
    
    for uploaded_file in uploaded_files:
        # Read file content
        stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
        content = stringio.read()
        
        # Parse content
        parsed_results = parse_cli_output(content)
        all_data.append(parsed_results)
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    
    # Display the Table
    st.subheader("Analysis Results")
    st.dataframe(df, use_container_width=True)
    
    # --- 3. EXPORT TO EXCEL ---
    # Create an Excel buffer
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Cisco_Inventory')
    
    st.download_button(
        label="📥 Download Results as Excel",
        data=buffer.getvalue(),
        file_name="cisco_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    # --- 4. COPY TO CLIPBOARD (Optional Text Area) ---
    with st.expander("Show Copyable Text (TSV Format)"):
        st.text_area("Copy this into Excel manually if needed:", df.to_csv(sep='\t', index=False), height=200)

else:
    st.info("Waiting for files to be uploaded...")