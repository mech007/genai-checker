# checkerapp/llm_service.py
import openai
import os
import fitz
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY
PDF_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media', 'forms')


def extract_text_from_pdf(customer_name, account_number):
    filename = f"{customer_name.upper()}_{account_number}.pdf"
    filepath = os.path.join(PDF_FOLDER, filename)

    if not os.path.exists(filepath):
        return "No matching PDF found."

    text = ""
    try:
        with fitz.open(filepath) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        text = f"Failed to extract text: {str(e)}"

    return text

def validate_form_with_llm(entry):
    pdf_content = extract_text_from_pdf(entry.customer_name, entry.customer_account_number)
    prompt = f"""Please validate the following form submission using the referenced document content.

        --- Form Data ---
        Customer Name: {entry.customer_name}
        Account Number: {entry.customer_account_number}
        Currency: {entry.currency}
        Beneficiary: {entry.beneficiary_name}
        Beneficiary Account: {entry.beneficiary_account_number}
        Branch Code: {entry.branch_code}

        --- Document Extract ---
        {pdf_content}

        --- Instruction ---
        Cross-verify if form fields match document details. Respond with "APPROVED" or "REJECTED with reason".
        """

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a bank form checker AI."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"AI validation failed: {str(e)}"
