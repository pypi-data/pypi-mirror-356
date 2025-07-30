"""
Responsible AI checks for LLM monitoring.
"""

import re
from typing import Dict, Any, List, Set
from datetime import datetime

from metricllm.utils.logging import get_logger


class ResponsibleAI:
    """Responsible AI checks including content filtering and bias detection."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        
        # Content filtering keywords
        self.harmful_keywords = {
            "violence": [
                "kill", "murder", "assault", "attack", "violence", "harm", "hurt", "damage",
                "destroy", "weapon", "gun", "knife", "bomb", "explosive", "fight", "beat"
            ],
            "hate_speech": [
                "hate", "racism", "sexism", "discrimination", "bigotry", "prejudice",
                "slur", "offensive", "derogatory", "insulting"
            ],
            "adult_content": [
                "explicit", "sexual", "pornographic", "adult", "inappropriate", "nsfw"
            ],
            "harassment": [
                "bully", "harass", "threaten", "intimidate", "stalk", "abuse", "torment"
            ]
        }
        
        # Bias detection patterns
        self.bias_patterns = {
            "gender_bias": [
                r"\b(he|she|his|her|him|her)\b.*\b(should|must|always|never)\b",
                r"\b(men|women|male|female|boys|girls)\b.*\b(are|aren't|can't|cannot)\b"
            ],
            "racial_bias": [
                r"\b(people|person|individual|group)\b.*\b(race|ethnicity|color|origin)\b",
                r"\b(they|them|those)\b.*\b(culture|background|heritage)\b"
            ],
            "age_bias": [
                r"\b(young|old|elderly|senior|teen|adult)\b.*\b(should|must|always|never)\b",
                r"\b(generation|age|years)\b.*\b(are|aren't|can't|cannot)\b"
            ]
        }
    
    def check(self, prompt: str, response: str) -> Dict[str, Any]:
        """
        Perform comprehensive responsible AI checks.
        
        Args:
            prompt: Input prompt
            response: Model response
        
        Returns:
            Dictionary containing responsible AI check results
        """
        check_results = {
            "timestamp": datetime.now().isoformat(),
            "responsible_ai_version": "1.0",
            "content_filter": self._content_filter_check(prompt, response),
            "bias_detection": self._bias_detection_check(prompt, response),
            "toxicity_analysis": self._toxicity_analysis(prompt, response),
            "privacy_check": self._privacy_check(prompt, response),
            "fairness_assessment": self._fairness_assessment(prompt, response),
            "overall_safety_score": 0.0,
            "safety_level": "unknown",
            "recommendations": []
        }
        
        # Calculate overall safety score
        check_results["overall_safety_score"] = self._calculate_safety_score(check_results)
        
        # Determine safety level
        check_results["safety_level"] = self._determine_safety_level(check_results["overall_safety_score"])
        
        # Generate recommendations
        check_results["recommendations"] = self._generate_recommendations(check_results)
        
        return check_results
    
    def _content_filter_check(self, prompt: str, response: str) -> Dict[str, Any]:
        """Check for harmful content using keyword filtering."""
        results = {
            "prompt_flags": {},
            "response_flags": {},
            "total_flags": 0,
            "severity": "low"
        }
        
        # Check prompt
        for category, keywords in self.harmful_keywords.items():
            flags = []
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', prompt.lower()):
                    flags.append(keyword)
            
            if flags:
                results["prompt_flags"][category] = flags
                results["total_flags"] += len(flags)
        
        # Check response
        for category, keywords in self.harmful_keywords.items():
            flags = []
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', response.lower()):
                    flags.append(keyword)
            
            if flags:
                results["response_flags"][category] = flags
                results["total_flags"] += len(flags)
        
        # Determine severity
        if results["total_flags"] >= 5:
            results["severity"] = "high"
        elif results["total_flags"] >= 2:
            results["severity"] = "medium"
        else:
            results["severity"] = "low"
        
        return results
    
    def _bias_detection_check(self, prompt: str, response: str) -> Dict[str, Any]:
        """Detect potential bias in the content."""
        results = {
            "prompt_bias": {},
            "response_bias": {},
            "total_bias_indicators": 0,
            "bias_risk": "low"
        }
        
        # Check prompt for bias patterns
        for bias_type, patterns in self.bias_patterns.items():
            matches = []
            for pattern in patterns:
                found = re.findall(pattern, prompt.lower(), re.IGNORECASE)
                matches.extend(found)
            
            if matches:
                results["prompt_bias"][bias_type] = len(matches)
                results["total_bias_indicators"] += len(matches)
        
        # Check response for bias patterns
        for bias_type, patterns in self.bias_patterns.items():
            matches = []
            for pattern in patterns:
                found = re.findall(pattern, response.lower(), re.IGNORECASE)
                matches.extend(found)
            
            if matches:
                results["response_bias"][bias_type] = len(matches)
                results["total_bias_indicators"] += len(matches)
        
        # Determine bias risk
        if results["total_bias_indicators"] >= 3:
            results["bias_risk"] = "high"
        elif results["total_bias_indicators"] >= 1:
            results["bias_risk"] = "medium"
        else:
            results["bias_risk"] = "low"
        
        return results
    
    def _toxicity_analysis(self, prompt: str, response: str) -> Dict[str, Any]:
        """Analyze toxicity levels in the content."""
        results = {
            "prompt_toxicity": {
                "score": 0.0,
                "indicators": []
            },
            "response_toxicity": {
                "score": 0.0,
                "indicators": []
            },
            "overall_toxicity": "low"
        }
        
        # Toxicity indicators
        toxicity_indicators = [
            "stupid", "idiot", "moron", "fool", "dumb", "pathetic", "worthless",
            "disgusting", "horrible", "terrible", "awful", "hate", "despise"
        ]
        
        # Check prompt toxicity
        prompt_indicators = [word for word in toxicity_indicators if word in prompt.lower()]
        results["prompt_toxicity"]["indicators"] = prompt_indicators
        results["prompt_toxicity"]["score"] = min(len(prompt_indicators) * 0.2, 1.0)
        
        # Check response toxicity
        response_indicators = [word for word in toxicity_indicators if word in response.lower()]
        results["response_toxicity"]["indicators"] = response_indicators
        results["response_toxicity"]["score"] = min(len(response_indicators) * 0.2, 1.0)
        
        # Overall toxicity assessment
        max_toxicity = max(results["prompt_toxicity"]["score"], results["response_toxicity"]["score"])
        if max_toxicity >= 0.6:
            results["overall_toxicity"] = "high"
        elif max_toxicity >= 0.3:
            results["overall_toxicity"] = "medium"
        else:
            results["overall_toxicity"] = "low"
        
        return results
    
    def _privacy_check(self, prompt: str, response: str) -> Dict[str, Any]:
        """Check for potential privacy issues."""
        results = {
            "prompt_privacy_risks": [],
            "response_privacy_risks": [],
            "privacy_score": 1.0,
            "privacy_level": "safe"
        }
        
        # Privacy patterns
        privacy_patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
            "credit_card": r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
            "ip_address": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        }
        
        # Check prompt
        for privacy_type, pattern in privacy_patterns.items():
            if re.search(pattern, prompt):
                results["prompt_privacy_risks"].append(privacy_type)
        
        # Check response
        for privacy_type, pattern in privacy_patterns.items():
            if re.search(pattern, response):
                results["response_privacy_risks"].append(privacy_type)
        
        # Calculate privacy score
        total_risks = len(results["prompt_privacy_risks"]) + len(results["response_privacy_risks"])
        results["privacy_score"] = max(0.0, 1.0 - (total_risks * 0.2))
        
        # Determine privacy level
        if results["privacy_score"] >= 0.8:
            results["privacy_level"] = "safe"
        elif results["privacy_score"] >= 0.6:
            results["privacy_level"] = "moderate_risk"
        else:
            results["privacy_level"] = "high_risk"
        
        return results
    
    def _fairness_assessment(self, prompt: str, response: str) -> Dict[str, Any]:
        """Assess fairness and inclusivity of the content."""
        results = {
            "inclusive_language_score": 0.0,
            "representation_balance": "unknown",
            "fairness_indicators": [],
            "overall_fairness": "neutral"
        }
        
        # Positive inclusive language indicators
        inclusive_indicators = [
            "diverse", "inclusive", "equal", "fair", "respectful", "balanced",
            "various", "different", "multiple", "range", "variety", "spectrum"
        ]
        
        # Check for inclusive language
        inclusive_count = sum(1 for word in inclusive_indicators if word in response.lower())
        results["inclusive_language_score"] = min(inclusive_count * 0.2, 1.0)
        
        # Check for balanced representation
        representation_words = {
            "gender": ["he", "she", "his", "her", "him", "men", "women", "male", "female"],
            "perspective": ["i think", "in my opinion", "some believe", "others argue", "various views"]
        }
        
        gender_balance = 0
        for word in representation_words["gender"]:
            if word in response.lower():
                gender_balance += 1
        
        if gender_balance >= 2:
            results["representation_balance"] = "balanced"
        elif gender_balance == 1:
            results["representation_balance"] = "potentially_biased"
        else:
            results["representation_balance"] = "neutral"
        
        # Overall fairness assessment
        if results["inclusive_language_score"] >= 0.6 and results["representation_balance"] == "balanced":
            results["overall_fairness"] = "high"
        elif results["inclusive_language_score"] >= 0.3:
            results["overall_fairness"] = "moderate"
        else:
            results["overall_fairness"] = "low"
        
        return results
    
    def _calculate_safety_score(self, check_results: Dict[str, Any]) -> float:
        """Calculate an overall safety score."""
        scores = []
        
        # Content filter score (inverted - fewer flags = higher score)
        content_flags = check_results["content_filter"]["total_flags"]
        content_score = max(0.0, 1.0 - (content_flags * 0.1))
        scores.append(content_score)
        
        # Bias detection score (inverted)
        bias_indicators = check_results["bias_detection"]["total_bias_indicators"]
        bias_score = max(0.0, 1.0 - (bias_indicators * 0.2))
        scores.append(bias_score)
        
        # Toxicity score (inverted)
        max_toxicity = max(
            check_results["toxicity_analysis"]["prompt_toxicity"]["score"],
            check_results["toxicity_analysis"]["response_toxicity"]["score"]
        )
        toxicity_score = 1.0 - max_toxicity
        scores.append(toxicity_score)
        
        # Privacy score
        privacy_score = check_results["privacy_check"]["privacy_score"]
        scores.append(privacy_score)
        
        # Fairness score
        fairness_mapping = {"high": 1.0, "moderate": 0.6, "low": 0.3, "neutral": 0.5}
        fairness_score = fairness_mapping.get(check_results["fairness_assessment"]["overall_fairness"], 0.5)
        scores.append(fairness_score)
        
        return round(sum(scores) / len(scores), 2)
    
    def _determine_safety_level(self, safety_score: float) -> str:
        """Determine safety level based on score."""
        if safety_score >= 0.8:
            return "safe"
        elif safety_score >= 0.6:
            return "moderate_risk"
        elif safety_score >= 0.4:
            return "high_risk"
        else:
            return "critical_risk"
    
    def _generate_recommendations(self, check_results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on the checks."""
        recommendations = []
        
        # Content filter recommendations
        if check_results["content_filter"]["total_flags"] > 0:
            recommendations.append("Review content for potentially harmful keywords and consider content moderation.")
        
        # Bias detection recommendations
        if check_results["bias_detection"]["bias_risk"] in ["medium", "high"]:
            recommendations.append("Consider reviewing content for potential bias and ensure inclusive language.")
        
        # Toxicity recommendations
        if check_results["toxicity_analysis"]["overall_toxicity"] in ["medium", "high"]:
            recommendations.append("Review content for toxic language and consider implementing toxicity filtering.")
        
        # Privacy recommendations
        if check_results["privacy_check"]["privacy_level"] in ["moderate_risk", "high_risk"]:
            recommendations.append("Review content for personal information and implement privacy protection measures.")
        
        # Fairness recommendations
        if check_results["fairness_assessment"]["overall_fairness"] == "low":
            recommendations.append("Consider improving inclusivity and representation in the content.")
        
        # Overall safety recommendations
        if check_results["overall_safety_score"] < 0.6:
            recommendations.append("Implement comprehensive content review and safety measures.")
        
        return recommendations
