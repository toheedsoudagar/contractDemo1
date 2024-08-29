import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Replace with your Gemini 1.5 Flash API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Define contract types and their associated fields
contract_types = {
    "Employment Contract": ["Employee Name", "Job Title", "Start Date", "Salary", "Benefits"],
    "Non-Disclosure Agreement (NDA)": ["Parties Involved", "Confidential Information", "Term"],
    "Service Agreement": ["Client Name","Client Address", "Service Provider","Service Provider Address","Start Date","End Date", "Scope of Work", "Payment Terms"],
    # Add more contract types and their fields as needed
}

# Create a Streamlit app
def main():
    st.title("Contract Drafting Tool")

    # Display contract type dropdown
    selected_contract_type = st.selectbox("Select Contract Type", list(contract_types.keys()))

    # Display fields based on selected contract type
    contract_fields = contract_types[selected_contract_type]
    contract_data = {}
    for field in contract_fields:
        contract_data[field] = st.text_input(field)
        if contract_data[field]=="Start Date" or "End Date":
            contract_data[field] = st.date_input(field)

    # Generate contract text using Gemini 1.5 Flash
    if st.button("Generate Contract"):
        prompt = f"Draft a Professional {selected_contract_type} with the following details:\n"
        for field, value in contract_data.items():
            prompt += f"{field}: {value}\n"

        # Use Gemini 1.5 Flash to generate contract text
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        st.subheader("Generated Response")
        st.write(response.text)

if __name__ == "__main__":
    main()


#The Service Provider shall develop a custom website for the Client, incorporating the following elements:  
# Homepage: A visually appealing and informative homepage, including a clear call-to-action. About Us Page: A detailed description of the Client's company, mission, and values. Services Page: A comprehensive overview of the Client's offerings, with detailed descriptions and pricing information. Contact Page: A contact form and relevant contact information. Blog: A blog section for publishing articles and updates. The website shall be designed to be responsive and compatible with all major
#  browsers and devices. The Service Provider shall also provide ongoing technical support and maintenance for a period of 24 months.

#Payment Details Upon 50% completion of the project, an amount of 60% from the agreed amount  
# will be paid, and on 100% completion of the project, the remaining amount will be paid
