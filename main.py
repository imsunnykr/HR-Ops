import streamlit as st
from langchain_helper import get_qa_chain
from guardrails import Guard
from guardrails.hub import DetectPII, ProfanityFree
import sys

def handle_input_error(error_message):
    error_messages = error_message[0].split(". ")
    st.header("Please review your Input/question :")
    for error in error_messages:
        st.write(error)
        st.write("Please Note : Personal identifiable Information (PII) includes information such as EMAIL_ADDRESS, PERSON, PHONE_NUMBER, CREDIT_CARD, US_SSN e.t.c")
    sys.exit()

def validate_input(question, guard):
    try:
        guard.validate(question)
    except Exception as e:
        st.write("The input may have PII information or profanity language, please check and try again")
        sys.exit()

def main():
    guard_pii = Guard().use(DetectPII, ["EMAIL_ADDRESS", "PERSON", "PHONE_NUMBER","DOMAIN_NAME", "IP_ADDRESS","CREDIT_CARD",
                                        "MEDICAL_LICENSE","US_BANK_NUMBER","US_PASSPORT", "US_SSN"], "exception")
    guard_profanity = Guard().use(ProfanityFree, on_fail="exception")

    st.title("FirstSource HR Q&A 🌱")
    question = st.text_input("Question: ")

    if question:
        validate_input(question, guard_pii)
        validate_input(question, guard_profanity)
        
        chain = get_qa_chain()
        response = chain(question)

        st.header("Answer")
        st.write(response["result"])

if __name__ == "__main__":
    main()
