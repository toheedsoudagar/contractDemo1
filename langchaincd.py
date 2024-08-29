import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Set your Google API Key
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Streamlit page configuration
st.set_page_config(page_title="Contract Drafting Application")
st.header("Contract Drafting Application")

# Sidebar for contract category selection with styling
with st.sidebar:
    st.markdown("""
    <style>
    /* Increase sidebar width */
    [data-testid="stSidebar"] {
        width: 350px;
    }
    /* Adjust the width of the main content area accordingly */
    [data-testid="stSidebar"] .css-ng1t4o {
        width: 350px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🤗💬 Nu-Pie LLM Personalized Contract Drafting Application")
    contract_type = st.selectbox(
        "Select Contract Type",
        [
            "Service Provider and Vendor",
            "Employee and Company",
            "Licensing Agreement",
        ],
    )

    st.markdown("<br><br>", unsafe_allow_html=True)  # Adds extra space
    st.markdown("<br><br>", unsafe_allow_html=True)  # Adds extra space

    st.markdown(
        """
        ## About
        This app is an LLM-powered chatbot built using:
        - [Streamlit](https://streamlit.io/)
        - [LangChain](https://python.langchain.com/)
        """,
        unsafe_allow_html=True,
    )

    st.write(
        'Made with ❤️ by [Nu-Pie Data Science Team](https://nu-pie.com/data-team-as-a-service-dtaas/)'
    )

# Define contract templates
service_provider_vendor_template = """
generate the professional contract based on the template below
This Agreement ("Agreement") is made between {vendor} ("Vendor") and {service_provider} ("Service Provider"). The parties agree to the following terms:
1. **Tenure Period**: This Agreement shall commence on {start_date} and continue for a period of {tenure_period} months, ending on {end_date}.
2. **Services Provided**: The Service Provider agrees to provide the following services: {service}.
3. **Purpose**: The purpose of this Agreement is to {purpose}.
4. **Payment Terms**: The Vendor agrees to pay the Service Provider according to the following schedule: {payment_details}.
5. **Confidentiality**: {confidentiality}
6. **Termination**: {termination}
7. **Miscellaneous**: Any amendments or modifications to this Agreement must be in writing and signed by both parties.
IN WITNESS WHEREOF, the parties have executed this Agreement on the date first written above. 
"""

employee_company_template = """
generate the professional contract based on the template below
This Employment Agreement ("Agreement") is made between {company} ("Company") and {employee} ("Employee"). The parties agree to the following terms:
1. **Position**: The Employee is hired as a {position}.
2. **Start Date**: The Employee's employment will commence on {start_date}.
3. **Salary**: The Employee will be compensated at a rate of {salary} per year, paid on a {payment_schedule} basis.
4. **Benefits**: The Employee is entitled to the following benefits: {benefits}.
5. **Confidentiality**: {confidentiality}
6. **Termination**: {termination}
7. **Miscellaneous**: Any amendments or modifications to this Agreement must be in writing and signed by both parties.
IN WITNESS WHEREOF, the parties have executed this Agreement on the date first written above. 
"""



licensing_agreement_template = """
This Licensing Agreement ("Agreement") is made as of by and between:
**Licensor:**
Name: {licensor_name}
Address: {licensor_address}
**Licensee:**
Name: {licensee_name}
Address: {licensee_address}
1. **Intellectual Property**: The Licensor grants the Licensee a license to use the following intellectual property: {intellectual_property_description}.
2. **License Grant**: The license is {exclusive_or_nonexclusive}, {territory} and for a period of {license_duration}.
3. **License Fee**: The Licensee agrees to pay the Licensor {license_fee} as follows: {payment_terms}.
4. **Purpose**: The purpose of this license is {license_purpose}.
5. **Confidentiality**: {confidentiality_clause}
6. **Term and Termination**: The Agreement will commence on {start_date} and continue until {end_date} or until terminated by either party as per the terms: {termination_conditions}.
7. **Governing Law**: This Agreement will be governed by the laws of {governing_law}.
8. **Miscellaneous**: Any amendments or modifications to this Agreement must be in writing and signed by both parties.
IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first above written. 
"""

# Function to get a response from Google GenAI
def get_gemini_response(input_text):
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    retries = 5
    for i in range(retries):
        try:
            response = model.generate_content(input_text)
            return response.text
        except Exception as e:
            st.warning(f"Attempt {i+1}/{retries} failed due to: {str(e)}. Retrying...")
            
    st.error("Failed to generate a response after multiple attempts.")
    return None
    response = model.generate_content(input_text)
    return response.text

# Inputs based on the selected contract type
if contract_type == "Service Provider and Vendor":
    vendor = st.text_input("Vendor")
    service_provider = st.text_input("Service Provider")
    tenure_period = st.number_input(
        "Tenure Period in months", min_value=1, max_value=100, value=5, step=1
    )
    service = st.text_input("Service")
    purpose = st.text_input("Purpose")
    payment_details = st.text_area(
        "Payment Details",
        (
            "Upon 50% completion of the project, an amount of 60% from the agreed amount "
            "will be paid, and on 100% completion of the project, the remaining amount will be paid."
        ),
    )
    start_date = st.date_input("Project Start Date")
    end_date = st.date_input("Project End Date")
    confidentiality = st.text_area(
        "Confidentiality Clause",
        "Both parties agree to keep all sensitive information confidential and not to disclose it to third parties without prior written consent.",
    )
    termination = st.text_area(
        "Termination Clause",
        "Either party may terminate this Agreement by providing 30 days' written notice. Upon termination, all outstanding payments for services rendered will be due immediately.",
    )
    

    # Generate contract button
    if st.button("Generate Contract"):
        # Format the template with the details
        contract_text = service_provider_vendor_template.format(
            vendor=vendor,
            service_provider=service_provider,
            tenure_period=tenure_period,
            service=service,
            purpose=purpose,
            payment_details=payment_details,
            start_date=start_date,
            end_date=end_date,
            confidentiality=confidentiality,
            termination=termination,
           
        )

        # Generate the contract using Google GenAI
        response = get_gemini_response(contract_text)

        # Display the generated contract
        st.subheader("Generated Contract")
        st.write(response)

elif contract_type == "Employee and Company":
    company = st.text_input("Company")
    employee = st.text_input("Employee")
    position = st.text_input("Position")
    start_date = st.date_input("Start Date")
    salary = st.text_input("Salary")
    payment_schedule = st.selectbox("Payment Schedule", ["Monthly", "Bi-Weekly", "Weekly"])
    benefits = st.text_area("Benefits", "List of benefits provided by the company.")
    confidentiality = st.text_area(
        "Confidentiality Clause",
        "The Employee agrees to keep all sensitive information confidential and not to disclose it to third parties without prior written consent.",
    )
    termination = st.text_area(
        "Termination Clause", "Either party may terminate this Agreement by providing 30 days' written notice."
    )
   

    # Generate contract button
    if st.button("Generate Contract"):
        # Format the template with the details
        contract_text = employee_company_template.format(
            company=company,
            employee=employee,
            position=position,
            start_date=start_date,
            salary=salary,
            payment_schedule=payment_schedule,
            benefits=benefits,
            confidentiality=confidentiality,
            termination=termination,
          
        )

        # Generate the contract using Google GenAI
        response = get_gemini_response(contract_text)

        # Display the generated contract
        st.subheader("Generated Contract")
        st.write(response)


elif contract_type == "Licensing Agreement":
    licensor_name = st.text_input("Licensor's Name")
    licensor_address = st.text_input("Licensor's Address")
    licensee_name = st.text_input("Licensee's Name")
    licensee_address = st.text_input("Licensee's Address")
    intellectual_property_description = st.text_area("Description of Intellectual Property")
    exclusive_or_nonexclusive = st.text_input("Exclusive or Non-exclusive License")
    territory = st.text_input("Territory")
    license_duration = st.text_input("License Duration")
    license_fee = st.text_input("License Fee")
    payment_terms = st.text_area("Payment Terms")
    license_purpose = st.text_input("Purpose of License")
    confidentiality_clause = st.text_area("Confidentiality Clause")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    termination_conditions = st.text_area("Termination Conditions")
  

    if st.button("Generate Contract"):
        # Format the template with the details
        contract_text = licensing_agreement_template.format(
            licensor_name=licensor_name,
            licensor_address=licensor_address,
            licensee_name=licensee_name,
            licensee_address=licensee_address,
            intellectual_property_description=intellectual_property_description,
            exclusive_or_nonexclusive=exclusive_or_nonexclusive,
            territory=territory,
            license_duration=license_duration,
            license_fee=license_fee,
            payment_terms=payment_terms,
            license_purpose=license_purpose,
            confidentiality_clause=confidentiality_clause,
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            termination_conditions=termination_conditions,
            
        )

        st.subheader("Generated Licensing Agreement")
        st.write(contract_text)
