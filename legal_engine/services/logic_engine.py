from datetime import date, timedelta
from typing import Dict, Any, List

class RuleValidator:
    """
    Core Logic Engine for Mudadeq.
    Validates cases against procedural rules.
    """

    def validate_case(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for validation.
        Args:
            case_data: Dictionary containing case details (dates, type, etc.)
        Returns:
            Dict with 'is_valid' (bool) and 'reasons' (list).
        """
        reasons = []
        
        # 1. Validate Statute of Limitations (Example Rule)
        if not self._check_statute_of_limitations(case_data):
            reasons.append({
                "code": "STATUTE_LIMITATION_EXCEEDED",
                "message": "The case was filed after the statute of limitations period (60 days).",
                "severity": "BLOCKER"
            })

        # Add more rules here...

        return {
            "is_valid": len(reasons) == 0,
            "reasons": reasons
        }

    def _check_statute_of_limitations(self, case_data: Dict[str, Any]) -> bool:
        """
        Checks if the case is within the 60-day window from the grievance outcome or incident.
        """
        incident_date = case_data.get('incident_date')
        submission_date = case_data.get('submission_date', date.today())
        
        if not incident_date:
            return True # Cannot validate without date
            
        # Parse if strings (mock logic, assume date objects for now or parse)
        if isinstance(incident_date, str):
            from datetime import datetime
            incident_date = datetime.strptime(incident_date, "%Y-%m-%d").date()
            
        # Example logic: 60 days limit
        limit_days = 60
        delta = (submission_date - incident_date).days
        
        return delta <= limit_days
