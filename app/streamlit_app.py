# import python packages
import streamlit as st
import pandas as pd
import altair as alt

from common.data_utils import get_active_session
import logging

logger = logging.getLogger("todo_app")

st.markdown("#TODOS")
st.divider()
st.markdown(
    """ A simple TODO application to demonstrate how we can use Streamlit to build a CRUD application. This application gives a quick overview of Streamlit features,
* A graphical representation of the TODOS grouped by Category, Status

* Using DataFrame to show list of TODO 

The script to create Database and its data is available at https://github.com/Snowflake-Labs/snow-cli-demo.git.
"""
)

st.divider()

session = get_active_session()
db_name = "TODO_APP_DB"
schema = "DATA"
table = "TODOS"

table_fqn = f"{db_name}.{schema}.{table}"
todo_df = session.table(table_fqn)
todo_category_count_df = (
    todo_df.select(["category", "status"]).groupBy(["category", "status"]).count()
)

# execute the query and convert it into a Pandas dataframe
queried_data = todo_category_count_df.to_pandas()
# set all True to "Done" abd all false to "WIP"
queried_data.loc[queried_data["STATUS"] == True, "STATUS"]= "Done"
queried_data.loc[queried_data["STATUS"] == False, "STATUS"] = "WIP" 

# create a simple bar chart
st.subheader("Tasks by category")
st.bar_chart(
    data = queried_data,
    x = "CATEGORY",
    y = "COUNT",
    color = "STATUS",
)

df2 = todo_df.select(["title", "category", "status"])
st.subheader("Underlying data")
# list to show all todos
event = st.dataframe(
    df2,
    hide_index = True,
    selection_mode = ["single-row"],
    on_select="rerun",
    key = "todos",
    column_config={
        "TITLE": st.column_config.TextColumn(
            label = "Title",
            help = "Title of the Task",
            width = "medium",
        ),
        "CATEGORY": st.column_config.TextColumn(
            label = "Category",
            help = "Category of the Task",
            width = "small",
        ),
        "STATUS": st.column_config.CheckboxColumn(
            label = "Status",
            help = "Status of the Task",
            width = "small",
        ),
    },
)
