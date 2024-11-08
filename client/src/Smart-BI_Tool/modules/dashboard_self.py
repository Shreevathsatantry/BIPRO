import streamlit as st
import pandas as pd
import plotly.express as px

def show_page():
    # Title of the app
    st.title("Interactive Data Visualization Dashboard")
    
    # Sidebar for CSV/Excel Input
    st.sidebar.header("Upload your CSV or Excel file")
    file = st.sidebar.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])
    
    # Caching the data loading to optimize performance
    @st.cache_data
    def load_data(uploaded_file):
        if uploaded_file is not None:
            file_extension = uploaded_file.name.split('.')[-1]
            if file_extension == "csv":
                return pd.read_csv(uploaded_file, encoding='ISO-8859-1')
            elif file_extension == "xlsx":
                return pd.read_excel(uploaded_file)
        return pd.DataFrame()
    
    # Check if the file is uploaded and load the dataset
    if file:
        try:
            # Load dataset using cache
            df = load_data(file)
            st.sidebar.subheader("Preview Data")

            # Show a checkbox for data preview (sampled to optimize performance)
            if st.sidebar.checkbox("Preview the dataset"):
                st.write(df.head(100))  # Show only first 100 rows for preview

            # Show a checkbox for summary statistics (optional)
            if st.sidebar.checkbox("Show Summary Statistics"):
                st.write(df.describe())
            
            # Filter Option
            st.sidebar.subheader("Filter Data")
            filterable_columns = df.select_dtypes(include=['object', 'category']).columns
            if len(filterable_columns) > 0:
                filter_column = st.sidebar.selectbox("Select a column to filter by", ['None'] + filterable_columns.tolist())
            else:
                filter_column = 'None'
                st.sidebar.write("No categorical columns available for filtering.")
    
            # Apply filter based on user selection
            if filter_column != 'None':
                unique_values = ['None'] + df[filter_column].unique().tolist()
                selected_value = st.sidebar.selectbox(f"Select a value from {filter_column}", unique_values)

                # If a specific value is selected, filter the dataset
                if selected_value != 'None':
                    df = df[df[filter_column] == selected_value]
    
            # Graph Selection
            st.sidebar.subheader("Select Graphs")
            graph_options = []
            if st.sidebar.checkbox("Bar Plot"):
                graph_options.append("Bar Plot")
            if st.sidebar.checkbox("Pie Chart"):
                graph_options.append("Pie Chart")
            if st.sidebar.checkbox("Scatter Plot"):
                graph_options.append("Scatter Plot")
            if st.sidebar.checkbox("Histogram"):
                graph_options.append("Histogram")
            if st.sidebar.checkbox("Box Plot"):
                graph_options.append("Box Plot")
            if st.sidebar.checkbox("Bubble Chart"):
                graph_options.append("Bubble Chart")
            if st.sidebar.checkbox("Treemap"):
                graph_options.append("Treemap")
    
            # Color Pickers for Graphs
            st.sidebar.subheader("Graph Colors")
            bar_color = st.sidebar.color_picker('Select Bar Plot Color', '#00f900')
            pie_color = st.sidebar.color_picker('Select Pie Chart Color', '#ff5733')
            scatter_color = st.sidebar.color_picker('Select Scatter Plot Color', '#17becf')
            histogram_color = st.sidebar.color_picker('Select Histogram Color', '#ffbf00')
            box_color = st.sidebar.color_picker('Select Box Plot Color', '#ff6347')
            bubble_color = st.sidebar.color_picker('Select Bubble Chart Color', '#ff8c00')
            treemap_color = st.sidebar.color_picker('Select Treemap Color', '#ff6600')
    
            # Arrange graphs in two columns
            col1, col2 = st.columns(2)
            graph_counter = 0  # Initialize the counter
    
            def assign_column(graph_component):
                """Assigns the current graph to col1 or col2 based on the counter."""
                nonlocal graph_counter  # Declare graph_counter as nonlocal
                if graph_counter % 2 == 0:
                    with col1:
                        graph_component()
                else:
                    with col2:
                        graph_component()
                graph_counter += 1  # Increment the counter
    
            # Generating graphs
            if "Bar Plot" in graph_options:
                def bar_plot():
                    st.subheader("Interactive Bar Plot")
                    x_axis = st.selectbox('Select X-axis:', df.columns)
                    y_axis = st.selectbox('Select Y-axis:', df.select_dtypes(include=['number']).columns)
                    fig = px.bar(df, x=x_axis, y=y_axis, title="Bar Plot", color_discrete_sequence=[bar_color])
                    st.plotly_chart(fig)
    
                assign_column(bar_plot)
    
            if "Pie Chart" in graph_options:
                def pie_chart():
                    st.subheader("Interactive Pie Chart")
                    category_column = st.selectbox('Select Categorical Column for Pie Chart', df.select_dtypes(['object']).columns)
                    fig = px.pie(df, names=category_column, title="Pie Chart", color_discrete_sequence=[pie_color])
                    st.plotly_chart(fig)
    
                assign_column(pie_chart)
    
            if "Scatter Plot" in graph_options:
                def scatter_plot():
                    st.subheader("Interactive Scatter Plot")
                    x_axis = st.selectbox('Select X-axis for Scatter Plot:', df.select_dtypes(['number']).columns)
                    y_axis = st.selectbox('Select Y-axis for Scatter Plot:', df.select_dtypes(['number']).columns)
                    fig = px.scatter(df, x=x_axis, y=y_axis, title="Scatter Plot", color_discrete_sequence=[scatter_color])
                    st.plotly_chart(fig)
    
                assign_column(scatter_plot)
    
            if "Histogram" in graph_options:
                def histogram():
                    st.subheader("Interactive Histogram")
                    hist_column = st.selectbox("Select Column for Histogram", df.select_dtypes(['number']).columns)
                    fig = px.histogram(df, x=hist_column, title="Histogram", color_discrete_sequence=[histogram_color])
                    st.plotly_chart(fig)
    
                assign_column(histogram)
    
            if "Box Plot" in graph_options:
                def box_plot():
                    st.subheader("Interactive Box Plot")
                    y_axis = st.selectbox("Select Y-axis for Box Plot", df.select_dtypes(['number']).columns)
                    fig = px.box(df, y=y_axis, title="Box Plot", color_discrete_sequence=[box_color])
                    st.plotly_chart(fig)
    
                assign_column(box_plot)
    
            if "Bubble Chart" in graph_options:
                def bubble_chart():
                    st.subheader("Interactive Bubble Chart")
                    x_axis = st.selectbox('Select X-axis for Bubble Chart:', df.select_dtypes(['number']).columns)
                    y_axis = st.selectbox('Select Y-axis for Bubble Chart:', df.select_dtypes(['number']).columns)
                    size = st.selectbox("Select Size for Bubble Chart", df.select_dtypes(['number']).columns)
                    fig = px.scatter(df, x=x_axis, y=y_axis, size=size, color_discrete_sequence=[bubble_color], title="Bubble Chart")
                    st.plotly_chart(fig)

                assign_column(bubble_chart)

            if "Treemap" in graph_options:
                def treemap():
                    st.subheader("Interactive Treemap")
                    path_column = st.selectbox("Select Path for Treemap", df.select_dtypes(['object']).columns)
                    value_column = st.selectbox("Select Value for Treemap", df.select_dtypes(['number']).columns)
                    fig = px.treemap(df, path=[path_column], values=value_column, title="Treemap", color_discrete_sequence=[treemap_color])
                    st.plotly_chart(fig)

                assign_column(treemap)
    
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.write("Please upload a valid CSV or Excel file to start.")


# Run the Streamlit app
if __name__ == "__main__":
    show_page()
