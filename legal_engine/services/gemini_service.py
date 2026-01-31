import os
import google.generativeai as genai

# ==========================================
# منطقة إعداد المفتاح (ضع السطر الخاص بك هنا)
# ==========================================
GEMINI_API_KEY = "ضع المفتاح هنا"  # <--- انسخ مفتاحك هنا بدلاً من النص الموجود
# ==========================================

class GeminiService:
    """
    Wrapper for Google Gemini API for Legal Analysis.
    """
    
    def __init__(self):
        # Configure the API
        if GEMINI_API_KEY and GEMINI_API_KEY != "ضع المفتاح هنا":
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
            بصفتك مستشاراً في المحكمة الإدارية، صغ "تسبيباً قانونياً" بليغاً وموجزاً يوجه للقاضي.
            
            معلومات الدعوى:
            - الموضوع: {case_data.get('description', '')}
            - تاريخ القرار: {case_data.get('decision_date', 'غير محدد')}
            - تاريخ العلم: {case_data.get('incident_date', 'غير محدد')}
            - هل يوجد تظلم سابق؟: {case_data.get('grievance_date', 'لا') or 'لا'}
            
            نتيجة التدقيق الآلي: {status}
            الأسباب الإجرائية: {reasons_text}
            
            المطلوب:
            اكتب فقرة قانونية رصينة (3-4 أسطر) تبدأ بـ "بناءً على ما تقدم..." تشرح سبب التوصية (القبول أو الرفض) استناداً لنظام المرافعات أمام ديوان المظالم.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"تعذر توليد التسبيب: {str(e)}"
