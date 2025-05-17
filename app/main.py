from flask import Flask, request, render_template, jsonify
import openai
import base64
from form_recognizer import analyze_claim_form

app = Flask(__name__)


# Updated for openai>=1.0.0 Azure OpenAI usage
client = openai.AzureOpenAI(
    api_key='2bVpbROWoDFEvnolIIZznXm9lzobbNmNpJAwjQvsYwUcHagwWXyCJQQJ99BEACHYHv6XJ3w3AAAAACOG11EW',
    azure_endpoint='https://itkt-marsk5py-eastus2.openai.azure.com/',
    api_version='2024-12-01-preview'
)
deployment_id = 'gpt-4.1-mini'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['description']
        image = request.files['image']
        image_data = base64.b64encode(image.read()).decode("utf-8")

        form_data = {}
        if request.files.get('form_doc'):
            form_doc = request.files['form_doc']
            form_data = analyze_claim_form(form_doc)

        # Extract estimation from form data if available
        extracted_estimation = None
        for key in form_data:
            if 'estimate' in key.lower() or 'amount' in key.lower() or 'cost' in key.lower():
                extracted_estimation = form_data[key]
                break

        user_prompt = (
            f"User Description: {prompt}. "
            f"Extracted Form Data: {form_data}. "
            f"If the form contains an estimated repair cost, use it as a reference. "
            f"Otherwise, provide your own estimate based on the image and description. "
            f"Always respond with a JSON object with keys: 'assessment', 'suggested_repair_cost_in_inr', and 'extracted_estimation_from_form' (if available)."
        )

        response = client.chat.completions.create(
            model=deployment_id,
            messages=[
                {"role": "system", "content": "You are an expert insurance claims assessor. Along with your response, you also suggest estimated repair costs for the claim in Indian Rupees."},
                {"role": "user", "content": [
                    {"type": "text", "text": user_prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                ]}
            ],
            temperature=0.4
        )
        # Try to parse the response as JSON, fallback to plain text if not possible
        import json
        result_text = response.choices[0].message.content
        try:
            result_json = json.loads(result_text)
        except Exception:
            result_json = {"assessment": result_text, "suggested_repair_cost_in_inr": None, "extracted_estimation_from_form": extracted_estimation}

        # Always include extracted estimation from form if available
        if extracted_estimation and not result_json.get("extracted_estimation_from_form"):
            result_json["extracted_estimation_from_form"] = extracted_estimation

        return render_template('index.html', assessment=result_json.get("assessment"), suggested_repair_cost=result_json.get("suggested_repair_cost_in_inr"), extracted_estimation=result_json.get("extracted_estimation_from_form"))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
