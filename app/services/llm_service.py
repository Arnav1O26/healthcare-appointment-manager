import os
import google.generativeai as genai

def setup_ai():
    """Initializes the Gemini API using the key from .env"""
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        genai.configure(api_key=api_key)

def generate_pre_visit_summary(symptoms_text):
    """
    Analyzes patient symptoms before the appointment.
    Gracefully falls back to returning the raw text if the AI fails.
    """
    setup_ai()
    prompt = f"""
    Analyse these symptoms and return: urgency level (Low / Medium / High), 
    chief complaint, and three suggested questions for the doctor. 
    Symptoms: {symptoms_text}
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return {"success": True, "summary": response.text}
    except Exception as e:
        # Fallback: Don't break the system, just pass the raw symptoms to the doctor
        print(f"LLM Pre-visit Error: {e}")
        return {"success": False, "summary": symptoms_text, "error": str(e)}

def generate_post_visit_summary(clinical_notes):
    """
    Translates complex doctor notes into a patient-friendly summary.
    Gracefully falls back to returning raw notes if the AI fails.
    """
    setup_ai()
    prompt = f"""
    Convert these clinical notes into a patient-friendly summary with 
    medication schedule and follow-up steps: 
    {clinical_notes}
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return {"success": True, "summary": response.text}
    except Exception as e:
        # Fallback: Just provide the raw notes so the patient still gets their instructions
        print(f"LLM Post-visit Error: {e}")
        return {"success": False, "summary": clinical_notes, "error": str(e)}