import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from datetime import date

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Define contract types and their associated fields with default values
contract_types = {
    "Employment Contract": {
        "Employee Name": "John Doe",
        "Job Title": "Software Engineer",
        "Start Date": "3 july 2023",
        "Salary": "100,000 USD",
        "Benefits": "Health Insurance, 401(k)"
    },
    "Non-Disclosure Agreement (NDA)": {
        "Parties Involved": "Company A, Company B",
        "Confidential Information": "Product Design",
        "Term": "2 years"
    },
    "Service Agreement": {
        "Client Name": "Jane Smith",
        "Client Address": "123 Main St, Anytown, USA",
        "Service Provider": "XYZ Consulting",
        "Service Provider Address": "456 Elm St, Anytown, USA",
        "Start Date":"4 july 2023",
        "End Date": "5 july 2025",
        "Scope of Work": "Web Development Services",
        "Payment Terms": "50% upfront, 50% upon completion"
    },
    # Add more contract types and their fields as needed
}

# Function to generate content with retries
def generate_contract_text(model, input_text, retries=5):
    for i in range(retries):
        try:
            response = model.generate_content(input_text)
            return response.text
        except Exception as e:
            st.warning(f"Attempt {i+1}/{retries} failed. Retrying...")
    
    st.error("Failed to generate a response after multiple attempts.")
    return None

# Create a Streamlit app
def main():
    st.header("Nu-pie Contract Drafting Tool")
    
   

    # Display contract type dropdown
    selected_contract_type = st.selectbox("Select Contract Type", list(contract_types.keys()))

    # Display fields based on selected contract type
    contract_fields = contract_types[selected_contract_type]
    contract_data = {}
    for field, default_value in contract_fields.items():
        if isinstance(default_value, date):
            contract_data[field] = st.date_input(field, default_value)
        else:
            contract_data[field] = st.text_input(field, default_value)
        
    # Generate contract text using Gemini 1.5 Flash
    if st.button("Generate Contract"):
        prompt = f"Draft a Professional {selected_contract_type} with the following details:\n"
        for field, value in contract_data.items():
            prompt += f"{field}: {value}\n"

        # Use Gemini 1.5 Flash to generate contract text with retries
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
        contract_text = generate_contract_text(model, prompt)
        
        if contract_text:
            st.subheader("Generated Contract")
            st.write(contract_text)
            st.write('Made with ❤️ by [Nu-Pie Data Science Team](https://nu-pie.com/data-team-as-a-service-dtaas/)')


if __name__ == "__main__":
    main()
