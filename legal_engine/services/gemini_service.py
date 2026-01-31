import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class GeminiService:
    """
    Wrapper for Google Gemini API for Legal Analysis.
    """
    
    def __init__(self):
        # Configure the API
        if GEMINI_API_KEY and GEMINI_API_KEY != "ضع_المفتاح_هنا":
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
            self.is_active = True
        else:
            self.is_active = False

    def analyze_text(self, text: str) -> str:
        """
        Analyzes the plaintiff's text using Gemini.
        """
        if not self.is_active:
             return "Gemini API غير مفعل. (الوضع التجريبي)"

        try:
            prompt = f"""
            أنت خبير قانوني في ديوان المظالم السعودي.
            قم بتحليل نص الدعوى التالي واستخرج النقاط الجوهرية فقط:
            "{text}"
            """
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"خطأ في الاتصال بـ Gemini: {str(e)}"

    def generate_reasoning(self, case_data: dict, validation_result: dict) -> str:
        """
        Generates eloquent legal reasoning for the judge.
        """
        if not self.is_active:
            # Mock Response if no key
            status = "Accepted" if validation_result.get('is_valid') else "Rejected"
            return f"التسبيب الافتراضي (تجريبي): بناءً على المعطيات، فإن التوصية هي {status}."

        try:
            # Prepare Context
            status = "قبول الدعوى شكلاً" if validation_result.get('is_valid') else "عدم قبول الدعوى شكلاً"
            reasons = validation_result.get('reasons', [])
            reasons_text = "\n".join([r['message'] for r in reasons]) if reasons else "لا يوجد موانع إجرائية."
            
            prompt = f"""
            بصفتك مستشاراً أول في المحكمة الإدارية (ديوان المظالم)، قم بصياغة "منطوق حكم وتسبيب" مبدئي يوجه للقاضي ناظر القضية.

            البيانات الأساسية:
            - موضوع الدعوى: {case_data.get('description', '')}
            - تاريخ القرار الإداري: {case_data.get('decision_date', 'غير محدد')}
            - تاريخ العلم بالقرار: {case_data.get('incident_date', 'غير محدد')} (الأساس لحساب المدة)
            - هل يوجد تظلم سابق؟: {'نعم' if case_data.get('grievance_date') else 'لا'}
            
            نتيجة التدقيق النظامي (الآلي):
            - التوصية: {status}ذ
            - الملاحظات الإجرائية: {reasons_text}

            المطلوب منك:
            كتابة فقرة قانونية رصينة جداً (لا تتجاوز 5 أسطر) تبدأ بعبارة "بناءً على ما تقدم...".
            
            يجب أن توضح النص النظامي المستند عليه (مثل المادة 8 أو 16 من نظام المرافعات) وتشرح لماذا تم قبول الدعوى أو رفضها بناءً على التواريخ والوقائع أعلاه.
            اجعل الأسلوب قضائياً بحتاً ومقنعاً.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"تعذر توليد التسبيب: {str(e)}"
