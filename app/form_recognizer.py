from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

FORM_RECOGNIZER_ENDPOINT = "https://aiagentic-documentintelligence.cognitiveservices.azure.com/"
FORM_RECOGNIZER_KEY = "72jGtDDTI4tix8Mv1jamBez45sWJFRF6OO5hwcJmdiGCl0ChM0a9JQQJ99BEACYeBjFXJ3w3AAALACOGl1oQ"

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
