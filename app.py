import streamlit as st
import pandas as pd

# Function to load CSV files
def load_csv(file_path):
    return pd.read_csv(file_path)

# Function to verify Gherkin steps against templates
def verify_gherkin(gherkin_executable, step_templates_df):
    # Split the Gherkin executable into individual steps
    steps = [line.strip() for line in gherkin_executable.split('\n') if line.strip() and not line.strip().startswith('|') and not line.strip().startswith('Feature') and not line.strip().startswith('Scenario')]

    # Check each step against the templates
    for step in steps:
        if not any(step.startswith(template.split(':')[0]) for template in step_templates_df['Step Function']):
            return False
    return True

# Load CSV files
step_templates_df = load_csv('data/combined_ccp_post_trade_step_functions.csv')
stories_df = load_csv('data/ccp_post_trade_stories.csv')

# Streamlit UI
st.title('CCP Post-Trade Story to Gherkin Executable')

# Dropdown to select a story
story_selection = st.selectbox("Select a Story", stories_df['Story'].unique())

# Display and verify the Gherkin executable for the selected story
if story_selection:
    gherkin_executable = stories_df[stories_df['Story'] == story_selection]['Gherkin Executable'].values[0]
    st.text("Gherkin Executable:")
    st.text(gherkin_executable)

    # Verification
    is_valid = verify_gherkin(gherkin_executable, step_templates_df)
    if is_valid:
        st.success("The Gherkin executable aligns with the predefined step templates.")
    else:
        st.error("The Gherkin executable does not fully align with the predefined step templates.")

# Running the Streamlit app
if __name__ == '__main__':
    st.sidebar.title("Navigation")
    st.sidebar.info("Select a story to view and verify its Gherkin executable.")
