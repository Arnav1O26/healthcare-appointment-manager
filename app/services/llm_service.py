import os
import google.generativeai as genai

def setup_ai():
    """Initializes the Gemini API natively"""
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        genai.configure(api_key=api_key)

def generate_pre_visit_summary(symptoms_text):
    setup_ai()
    prompt = f"""
    Analyse these symptoms and return: urgency level (Low / Medium / High), 
    chief complaint, and three suggested questions for the doctor. 
    Symptoms: {symptoms_text}
    """
    
    try:
        model = genai.GenerativeModel('gemini-3.6-flash')
        response = model.generate_content(prompt)
        return {"success": True, "summary": response.text}
    except Exception as e:
        print(f"\n❌ LLM Pre-visit CRITICAL Error: {e}\n")
        return {"success": False, "summary": None, "error": str(e)}

def generate_post_visit_summary(clinical_notes):
    setup_ai()
    prompt = f"""
    Convert these clinical notes into a patient-friendly summary with 
    medication schedule and follow-up steps: 
    {clinical_notes}
    """
    
    try:
        model = genai.GenerativeModel('gemini-3.6-flash')
        response = model.generate_content(prompt)
        return {"success": True, "summary": response.text}
    except Exception as e:
        print(f"\n❌ LLM Post-visit CRITICAL Error: {e}\n")
        return {"success": False, "summary": None, "error": str(e)}