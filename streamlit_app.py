import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
import matplotlib.pyplot as plt

icon = Image.open("icon.png")

st.set_page_config(
    page_title="Data Application",
    page_icon=icon,
    # layout="centered",
    layout='wide',
    initial_sidebar_state="auto",
)

st.image("./EA-Logo.png", width=150)
#adding title
st.title("Data Visualization App")

dif_tabs= ['Plotly', 'Matplotlib', 'Altair']
#add tabs
tab1, tab2, tab3 = st.tabs([dif_tabs[0],
                            dif_tabs[1],
                            dif_tabs[2]])

#add a subheader in the side bar
st.sidebar.subheader("Visualization settings")

# add a file uploader
upload_file= st.sidebar.file_uploader(
    label="Upload your csv or excel file here",
    type=["csv", "xlsx"]
)

#option to visualize or not viaualize the data
display_df= st.sidebar.checkbox(label="Would you like to view the uploaded dataset")
print(upload_file)

global df
global num_cols
global non_num_cols

#accounting for case whre uploaded file is not none
if upload_file is not None:

    try:
        if upload_file.name.endswith(".csv"):
                df = pd.read_csv(upload_file)
        else:
            df = pd.read_excel(upload_file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

    upload_file.seek(0)
    
    if display_df:
        st.write(df)

    #extract numeric columns
    num_cols=list(df.select_dtypes(['float','int']).columns)

    #non numeric columns
    non_num_cols=list(df.select_dtypes(['object']).columns)

    #append None value to non_numeric list
    non_num_cols.append("None")

    

    x_value = st.sidebar.selectbox(label='x-axis', options= num_cols)
    y_value = st.sidebar.selectbox(label='y-axis', options=num_cols)



    with tab1:
        # Create columns for buttons
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Bar Chart", icon=":material/bar_chart:"):
                st.session_state.chart_type = "bar"
        with col2:
            if st.button("Line Chart", icon=":material/show_chart:"):
                st.session_state.chart_type = "line"
        with col3:
            if st.button("Scatter Plot", icon=":material/scatter_plot:"):
                st.session_state.chart_type = "scatter"

        # Display chart based on selection
        if "chart_type" not in st.session_state:
            st.session_state.chart_type = "bar" # Default chart

        st.subheader(f"Displaying: {st.session_state.chart_type.replace('_', ' ').title()} Chart")

        # try:
        if st.session_state.chart_type == "bar":
            fig = px.bar(df, x=x_value, y=y_value, title='Bar Chart Example')
            st.plotly_chart(fig, use_container_width=True)
        elif st.session_state.chart_type == "line":
            fig = px.line(df, x=x_value, y=[y_value], title='Line Chart Example')
            st.plotly_chart(fig, use_container_width=True)
        elif st.session_state.chart_type == "scatter":
            specify_color=st.sidebar.checkbox(
                    label="Would you like to specify the color?")
            if specify_color:
                color_value=st.sidebar.selectbox(label='Color',
                                                    options=non_num_cols)
                
                fig = px.scatter(data_frame=df, x=x_value, y=y_value, color=color_value ,title='Scatter Plot Example')
                st.plotly_chart(fig, use_container_width=True)
            else:
                plot=px.scatter(data_frame=df, x=x_value, y=y_value)
                st.plotly_chart(plot)

        # except Exception as e:
            # print(e)
    with tab2:
        
        import altair as alt

        @st.cache_data
        def load_data():
            df = pd.read_csv(r"data/ted.csv")
            return df


        df = load_data()


        def main():
            page = st.sidebar.selectbox(
                "Select a Page",
                [
                    "Homepage",
                    "Bar Plot",
                    "Horizontal Bar Plot",
                    "Scatter Plot",
                    "Histogram",
                    "Pie Chart",
                    "Two Subplots",
                    "Four Subplots",
                    "Two Axes",
                    "Four Axes",
                ],
            )

            if page == "Homepage":
                # st.header("Data Application")
                """
                # Building apps with Streamlit
                Please select a page on the left
                """
                st.write(df)
            elif page == "Bar Plot":
                bar_chart()

            elif page == "Horizontal Bar Plot":
                horizontal_bar()

            elif page == "Scatter Plot":
                visualize_scatter()

            elif page == "Histogram":
                st.header("Languages Histogram")
                histogram()

            elif page == "Pie Chart":
                st.header("Views and Day Pie Chart")
                pie_chart()

            elif page == "Two Subplots":
                st.header("Two Subplots")
                two_subplots()
            elif page == "Four Subplots":
                st.header("Four Subplots")
                four_subplots()

            elif page == "Two Axes":
                st.header("Two Axes")
                two_axes()

            elif page == "Four Axes":
                st.header("Four Axes")
                four_axes()


        def bar_chart():
            fig = plt.figure(figsize=(12, 5))
            plt.xticks(rotation=80)
            bar_data = df.sort_values(by="views", ascending=False)
            bar_data = bar_data.head(20)
            plt.ticklabel_format(style="plain")
            plt.bar(bar_data["event"], bar_data["views"])
            plt.xlabel("Event")
            plt.ylabel("Views")
            plt.title("Event and Views Plot")
            st.pyplot(fig)


        def horizontal_bar():
            fig = plt.figure(figsize=(12, 5))
            plt.xticks(rotation=80)
            bar_data = df.sort_values(by="views", ascending=False)
            bar_data = bar_data.head(20)
            plt.ticklabel_format(style="plain")
            plt.barh(bar_data["event"], bar_data["views"])
            plt.xlabel("Event")
            plt.ylabel("Views")
            plt.title("Event and Views Plot")
            st.pyplot(fig)


        def visualize_scatter():
            fig = plt.figure(figsize=(10, 8))
            plt.scatter(
                x=df["comments"],
                y=df["views"],
                marker="*",
                s=df["languages"],
                c=df["languages"],
                alpha=0.5,
            )
            st.pyplot(fig)


        def histogram():
            fig = plt.figure(figsize=(12, 5))
            plt.hist(df["languages"], color="y", bins=50)
            st.pyplot(fig)


        def pie_chart():
            days_data = (
                df.groupby("published_day")["views"]
                .sum()
                .sort_values(ascending=False)
                .reset_index()
            )
            fig = plt.figure(figsize=(10, 8))
            explode = (0.1, 0, 0, 0, 0, 0, 0)
            plt.pie(
                days_data["views"],
                labels=days_data["published_day"],
                shadow=True,
                explode=explode,
                autopct="%1.1f%%",
            )
            st.pyplot(fig)


        def two_subplots():
            fig = plt.figure(figsize=(15, 10))
            plt.subplot(1, 2, 1)
            bar_data = df.sort_values(by="views", ascending=False)
            bar_data = bar_data.head(20)
            plt.barh(bar_data["event"], bar_data["views"])

            plt.subplot(1, 2, 2)
            plt.scatter(df["views"], df["comments"], c=df["languages"], marker="*")
            st.pyplot(fig)


        def four_subplots():
            days_data = (
                df.groupby("published_day")["views"]
                .sum()
                .sort_values(ascending=False)
                .reset_index()
            )
            months_data = (
                df.groupby("published_month")["views"]
                .sum()
                .sort_values(ascending=False)
                .reset_index()
            )
            fig = plt.figure(figsize=(12, 10))
            plt.subplot(2, 2, 1)
            plt.title("Views & Published Day")
            plt.pie(
                days_data["views"],
                labels=days_data["published_day"],
                shadow=True,
                autopct="%1.1f%%",
            )
            plt.subplot(2, 2, 2)
            plt.title("Views & Published Month")
            plt.pie(
                months_data["views"],
                labels=months_data["published_month"],
                shadow=True,
                autopct="%1.1f%%",
            )
            plt.subplot(2, 2, 3)
            bar_data = df.sort_values(by="views", ascending=False)
            bar_data = bar_data.head(20)
            plt.xticks(rotation=80)
            plt.bar(bar_data["event"], bar_data["views"])

            plt.subplot(2, 2, 4)
            views = df.groupby("published_year")["views"].sum().reset_index()
            plt.plot(views["published_year"], views["views"])

            st.pyplot(fig)


        def two_axes():
            fig, ax = plt.subplots(1, 2, figsize=(15, 10))
            bar_data = df.sort_values(by="views", ascending=False)
            bar_data = bar_data.head(20)
            ax[0].barh(bar_data["event"], bar_data["views"])
            ax[1].scatter(df["views"], df["comments"], c=df["languages"], marker="*")
            st.pyplot(fig)


        def four_axes():
            days_data = (
                df.groupby("published_day")["views"]
                .sum()
                .sort_values(ascending=False)
                .reset_index()
            )
            months_data = (
                df.groupby("published_month")["views"]
                .sum()
                .sort_values(ascending=False)
                .reset_index()
            )
            fig, ax = plt.subplots(2, 2, figsize=(12, 10))

            ax[0, 0].pie(
                days_data["views"],
                labels=days_data["published_day"],
                shadow=True,
                autopct="%1.1f%%",
            )
            ax[0, 1].pie(
                months_data["views"],
                labels=months_data["published_month"],
                shadow=True,
                autopct="%1.1f%%",
            )

            bar_data = df.sort_values(by="views", ascending=False)
            bar_data = bar_data.head(20)
            ax[1, 0].bar(bar_data["event"], bar_data["views"])

            views = df.groupby("published_year")["views"].sum().reset_index()
            ax[1, 1].plot(views["published_year"], views["views"])

            st.pyplot(fig)


        if __name__ == "__main__":
            main()



    with tab3:
        import altair as alt
        alt.themes.enable("urbaninstitute")

        @st.cache_data
        def load_data():
            df = pd.read_csv(r"data/ted.csv")
            return df


        df = load_data()


        def main():
            page = st.selectbox(
                "Select a Page",
                [
                    "Vega Lite",
                    "Line Plot",
                    "Bar",
                    "Scatter",
                    "Area Chart",
                    "Scatter Matrix",
                    "Link Scatter",
                    "Heatmap",
                    "Horizontal Bar",
                    "Grouped Bar",
                    "Stacked Bar Chart",
                    "Normalized Chart",
                    "Text and Chart",
                    "Box Plot",
                    "Interactive Legend",
                    "Concatenate",
                    "Dual Y Axis",
                    "Horizontal Concatenation",
                    "Vertical Concatenation",
                    "Interactive Chart",
                ],
            )
            if page == "Vega Lite":
                st.balloons()
                st.header("Vega Lite")
                vegalite()
            elif page == "Line Plot":
                st.header("Line Plot")
                visualize_line()
            elif page == "Bar":
                st.header("Bar")
                bar()
            elif page == "Scatter":
                st.header("Scatter")
                scatter()
            elif page == "Area Chart":
                st.header("Area Chart")
                area_chart()
            elif page == "Scatter Matrix":
                st.header("Scatter Matrix")
                scatter_matrix()
            elif page == "Link Scatter":
                st.header("Link Scatter")
                link_scatter()
            elif page == "Heatmap":
                st.header("Heatmap")
                heatmap()
            elif page == "Horizontal Bar":
                st.header("Horizontal Bar")
                horizontal_bar()
            elif page == "Grouped Bar":
                st.header("Grouped Bar")
                grouped_bar()
            elif page == "Stacked Bar Chart":
                st.header("Stacked Bar Chart")
                stacked_bar()

            elif page == "Normalized Chart":
                st.header("Normalized Chart")
                normalized_chart()

            elif page == "Text and Chart":
                st.header("Text and Chart")
                text_chart()
            elif page == "Box Plot":
                st.header("Box Plot")
                boxplot()
            # elif page == "Interactive Legend":
            #     st.header("Interactive Legend")
            #     legend()
            elif page == "Concatenate":
                concatenate()
            elif page == "Dual Y Axis":
                dual_y_axis()
            elif page == "Horizontal Concatenation":
                horizontal_concat()
            elif page == "Vertical Concatenation":
                vertical_concat()
            elif page == "Interactive Chart":
                interactive_chart()


        def vegalite():
            st.vega_lite_chart(
                df,
                {
                    "mark": {"type": "circle", "tooltip": True},
                    "width": 650,
                    "height": 500,
                    "encoding": {
                        "x": {"field": "duration", "type": "quantitative"},
                        "y": {"field": "views", "type": "quantitative"},
                        "size": {"field": "languages", "type": "quantitative"},
                        "color": {"field": "languages", "type": "quantitative"},
                    },
                },
            )


        def visualize_line():
            df_copy = df.copy()
            df_copy = df_copy[
                (df_copy["film_year"] == 1999)
                | (df_copy["film_year"] == 2000)
                | (df_copy["film_year"] == 2001)
            ]
            df_copy["film_date"] = pd.to_datetime(df_copy["film_date"])
            line = (
                alt.Chart(df_copy)
                .mark_line()
                .encode(x="film_date", y="views")
                .properties(width=650, height=500)
                .interactive()
            )
            st.altair_chart(line)


        def bar():
            bar_data = df.sort_values(by="views", ascending=False)
            bar_data = bar_data.head(20)
            sort = st.checkbox("Sort")
            if sort:
                chart = (
                    alt.Chart(bar_data)
                    .mark_bar()
                    .encode(x=alt.X("event:N", sort="-y"), y="sum(views)")
                    .properties(width=650, height=500)
                    .interactive()
                )
            else:
                chart = (
                    alt.Chart(bar_data)
                    .mark_bar()
                    .encode(x="event", y="views")
                    .properties(width=650, height=500)
                    .interactive()
                )

            st.altair_chart(chart)


        def scatter():
            toggle = st.checkbox("Toggle Scatter")
            if toggle:
                chart = (
                    alt.Chart(df, background="maroon")
                    .mark_point()
                    .encode(
                        x="duration",
                        y="views",
                        size="languages",
                        color="languages",
                        tooltip=["duration", "views", "comments", "languages"],
                    )
                    .properties(width=650, height=500)
                )
            else:
                chart = (
                    alt.Chart(df)
                    .mark_point()
                    .encode(
                        x="duration",
                        y="views",
                        size="languages",
                        color="languages",
                        tooltip=["duration", "views", "comments", "languages"],
                    )
                    .properties(width=650, height=500)
                )

            st.altair_chart(chart)


        def area_chart():
            df_copy = df[df["film_year"] == 2012]
            df_copy["film_date"] = pd.to_datetime(df_copy["film_date"])
            radio_button = st.radio("Filled or Not", ("filled", "not_filled"))
            if radio_button == "filled":
                chart = (
                    alt.Chart(df_copy)
                    .mark_area(color="maroon", line=True)
                    .encode(x="film_date", y="views")
                    .properties(width=650, height=500)
                )
            else:
                chart = (
                    alt.Chart(df_copy)
                    .mark_area(color="maroon")
                    .encode(x="film_date", y="views")
                    .properties(width=650, height=500)
                )

            st.altair_chart(chart)


        def scatter_matrix():
            chart = (
                alt.Chart(df)
                .mark_circle()
                .encode(
                    alt.X(alt.repeat("column"), type="quantitative"),
                    alt.Y(alt.repeat("row"), type="quantitative"),
                    color="published_day",
                )
                .properties(width=150, height=150)
                .repeat(
                    row=["duration", "views", "comments"],
                    column=["comments", "views", "duration"],
                )
                .interactive()
            )
            st.altair_chart(chart)


        def link_scatter():
            chart = (
                alt.Chart(df)
                .mark_point()
                .encode(
                    x="duration",
                    y="comments",
                    color="published_month",
                    href="url:N",
                    tooltip=["event", "url:N"],
                )
                .interactive()
                .properties(width=650, height=500)
                .configure_legend(
                    strokeColor="#ea4663",
                    fillColor="#EEEEEE",
                    padding=10,
                    cornerRadius=10,
                    orient="top-right",
                )
            )
            st.altair_chart(chart)


        def heatmap():
            chart = (
                alt.Chart(df)
                .mark_rect()
                .encode(
                    x="published_year:O",
                    y="published_day",
                    color="languages",
                    tooltip=["languages", "published_day"],
                )
                .interactive()
                .properties(width=650, height=500)
            )
            st.altair_chart(chart)


        def horizontal_bar():
            bar_data = df.sort_values(by="views", ascending=False)
            bar_data = bar_data.head(20)
            chart = (
                alt.Chart(bar_data)
                .mark_bar()
                .encode(x="views", y="event")
                .properties(width=650, height=500)
                .interactive()
            )
            st.altair_chart(chart)


        def grouped_bar():
            dff = df[(df["published_day"] == "Monday") | (df["published_day"] == "Tuesday")]
            toggle = st.checkbox("Toggle Horizontal")
            if toggle:
                chart = (
                    alt.Chart(dff)
                    .mark_bar()
                    .encode(
                        y="published_year:O",
                        x=alt.X("sum(views):Q", title="Sum of Views"),
                        color="published_year:N",
                        column="published_day:N",
                    )
                    .properties(height=500, width=500)
                )
            else:
                chart = (
                    alt.Chart(dff)
                    .mark_bar()
                    .encode(
                        x="published_year:O",
                        y=alt.Y("sum(views):Q", title="Sum of Views"),
                        color="published_year:N",
                        column="published_day:N",
                    )
                    .properties(height=500, width=500)
                )

            st.altair_chart(chart)


        def stacked_bar():
            toggle = st.checkbox("Toggle this")
            if toggle:
                chart = (
                    alt.Chart(df)
                    .mark_bar()
                    .encode(
                        y="published_year:O",
                        x="sum(views)",
                        color="published_day",
                        tooltip=["sum(views)"],
                    )
                    .properties(height=500, width=700)
                    .interactive()
                )
            else:
                chart = (
                    alt.Chart(df)
                    .mark_bar()
                    .encode(
                        x="published_year:O",
                        y="sum(views)",
                        color="published_day",
                        tooltip=["sum(views)"],
                    )
                    .properties(height=500, width=700)
                    .interactive()
                )

            st.altair_chart(chart)


        def normalized_chart():
            chart = (
                alt.Chart(df)
                .mark_bar()
                .encode(
                    x=alt.X("mean(views)", stack="normalize"),
                    y="published_year:O",
                    color="published_day",
                    tooltip=["mean(views)", "published_day"],
                )
                .interactive()
                .properties(width=900, height=600)
            )
            st.altair_chart(chart)


        def text_chart():
            text = (
                alt.Chart(df)
                .mark_text(dx=-16, color="white")
                .encode(
                    x=alt.X("sum(num_speaker):Q", stack="normalize"),
                    y="published_year:O",
                    detail="published_day",
                    text=alt.Text("sum(num_speaker):Q", format=".1f"),
                )
            )

            chart = (
                alt.Chart(df)
                .mark_bar()
                .encode(
                    x=alt.X("sum(num_speaker)", stack="normalize"),
                    y="published_year:O",
                    color="published_day",
                    tooltip=["sum(num_speaker)", "published_day"],
                )
                .interactive()
                .properties(height=500, width=700)
            )
            st.altair_chart(chart + text)


        def boxplot():
            chart = (
                alt.Chart(df)
                .mark_boxplot()
                .encode(x="published_year:O", y="duration")
                .interactive()
                .properties(height=500, width=700)
            )
            st.altair_chart(chart)


        def legend():
            text = (
                alt.Chart(df)
                .mark_text(dx=-16, color="white")
                .encode(
                    x=alt.X("sum(num_speaker):Q", stack="normalize"),
                    y="published_year:O",
                    detail="published_day",
                    text=alt.Text("sum(num_speaker):Q", format=".1f"),
                )
            )
            selection = alt.selection_multi(fields=["published_day"], bind="legend")
            chart = (
                alt.Chart(df)
                .mark_bar()
                .encode(
                    x=alt.X("sum(num_speaker)", stack="normalize"),
                    y="published_year:O",
                    opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
                    color="published_day",
                    tooltip=["sum(num_speaker)", "published_day"],
                )
                .interactive()
                .properties(height=500, width=700)
                .add_selection(selection)
            )
            st.altair_chart(chart + text)


        def concatenate():
            scatter = (
                alt.Chart(df)
                .mark_point()
                .encode(x="duration", y="views:Q")
                .properties(width=250, height=250)
            )

            chart = alt.concat(
                scatter.encode(color="published_month"), scatter.encode(color="published_day")
            ).resolve_scale(color="independent")
            st.altair_chart(chart)


        def dual_y_axis():
            base = alt.Chart(df).encode(alt.X("year(published_date):T"))
            line_A = base.mark_line(color="#ea4663").encode(
                alt.Y("average(views):Q", axis=alt.Axis(titleColor="#ea4663"))
            )
            line_B = base.mark_line(color="#1a9988").encode(
                alt.Y("average(comments):Q", axis=alt.Axis(titleColor="#1a9988"))
            )

            chart = (
                alt.layer(line_A, line_B)
                .resolve_scale(y="independent")
                .properties(height=500, width=700)
            )
            st.altair_chart(chart)


        def horizontal_concat():
            chart1 = (
                alt.Chart(df)
                .mark_point()
                .encode(x="duration", y="views")
                .properties(height=300, width=300)
            )
            chart2 = (
                alt.Chart(df)
                .mark_point()
                .encode(x="languages", y="views")
                .properties(height=300, width=300)
            )

            # chart = chart1 | chart2
            chart = alt.hconcat(chart1, chart2)

            st.altair_chart(chart)


        def vertical_concat():
            base = (
                alt.Chart(df)
                .mark_area()
                .encode(x="published_date:T", y="languages:Q")
                .properties(width=600, height=200)
            )
            brush = alt.selection(type="interval", encodings=["x"])
            upper = base.encode(alt.X("published_date:T", scale=alt.Scale(domain=brush)))
            lower = base.properties(height=60).add_selection(brush)

            chart = upper & lower

            # chart = alt.vconcat(upper, lower)
            st.altair_chart(chart)


        def interactive_chart():
            brush = alt.selection_interval()
            chart = (
                alt.Chart(df)
                .mark_point()
                .encode(
                    x="languages:Q",
                    y="views:Q",
                    color=alt.condition(brush, "languages:Q", alt.value("gray")),
                )
                .properties(width=600, height=500)
                .add_selection(brush)
            )
            st.altair_chart(chart)


        if __name__ == "__main__":
            main()
else:
    st.balloons()

    
    st.warning("Please upload a DataSet to Start Visualization")
    st.stop()