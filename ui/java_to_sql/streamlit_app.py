import streamlit as st
import os
import json
from snowflake.snowpark.context import get_active_session
session = get_active_session()
st.title("Java Migration Assistant")
selected_method = None
with st.sidebar:
    current_repo = st.text_input("git repo name:")
    branch     = st.selectbox("branch",["main","master"])
    
    if branch and current_repo:
        try:
            rows=session.sql(f"ls @{current_repo}/branches/{branch}").select('"name"')\
            .collect()
            rows=[r["name"] for r in rows if r["name"].endswith(".java")]
            filename=st.selectbox("selected_file",rows)
            if filename:
                # Copy files from main to Snowflake stage
                session.sql("""CREATE OR REPLACE STAGE git_clone DIRECTORY = (enable=true)""").show()
                session.sql(f"""COPY FILES into @git_clone from @{filename}""").show()
                st.write(session.sql("ls @git_clone"))
                base_filename = os.path.basename(filename)
                st.write(f"Reading '@git_clone/{base_filename}'")
                class_info = session.sql(f"select parse_java_file('@git_clone/{base_filename}')")\
                .first()[0]
                class_info = json.loads(class_info)
                selected_method = st.selectbox("method",class_info,format_func=lambda x:x["name"])                
        except Exception as ex:
            st.write(f"There was an issue getting files from repo: {ex}")

if selected_method:
    st.write(f"Method: {selected_method['name']}")
    code = selected_method["code"]
    code = code.replace('\\n','\n')
    st.code(code,language="java")

    if st.button("Convert"):
        result = session.call("convert_with_cortex",code)
        st.code(result,language="markdown")