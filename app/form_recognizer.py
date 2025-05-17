from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

FORM_RECOGNIZER_ENDPOINT = "YOUR ENDPOINT HERE"
FORM_RECOGNIZER_KEY = "YOUR KEY HERE"

document_analysis_client = DocumentAnalysisClient(
    endpoint=FORM_RECOGNIZER_ENDPOINT,
    credential=AzureKeyCredential(FORM_RECOGNIZER_KEY)
)

def analyze_claim_form(file_stream):
    poller = document_analysis_client.begin_analyze_document(
        model_id="prebuilt-document",
        document=file_stream
    )
    result = poller.result()
    extracted_data = {}
    for doc in result.documents:
        for field_name, field in doc.fields.items():
            extracted_data[field_name] = field.value if field.value else "N/A"
    return extracted_data
