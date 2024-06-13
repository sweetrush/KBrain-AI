import streamlit as st
import os
from streamlit_extras.file_selection import file_selector

def main():
    st.title("File Editor")

    # --- Directory Selection ---
    selected_directory = file_selector(
        label="Select a directory",
        folder_mode=True,  # Set to True to select directories
        start_directory="."  # Start in the current directory
    )

    if selected_directory:
        st.write(f"Selected directory: {selected_directory}")

        # --- File Listing and Selection ---
        files = [f for f in os.listdir(selected_directory) if os.path.isfile(os.path.join(selected_directory, f))]
        selected_file = st.selectbox("Select a file to edit:", files)

        if selected_file:
            file_path = os.path.join(selected_directory, selected_file)
            st.write(f"Editing: {file_path}")

            # --- File Reading and Editing ---
            with open(file_path, "r") as f:
                file_content = f.read()

            edited_content = st.text_area("Edit the file:", file_content)

            # --- Saving Changes ---
            if st.button("Save Changes"):
                try:
                    with open(file_path, "w") as f:
                        f.write(edited_content)
                    st.success("File saved successfully!")
                except Exception as e:
                    st.error(f"Error saving file: {e}")

if __name__ == "__main__":
    main()