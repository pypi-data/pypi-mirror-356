"""
Evaluation framework for LLM responses.
"""

import re
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

from metricllm.utils.logging import get_logger


class EvaluationFramework:
    """Framework for evaluating LLM responses across multiple dimensions."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.evaluators = {
            "basic_quality": self._evaluate_basic_quality,
            "coherence": self._evaluate_coherence,
            "relevance": self._evaluate_relevance,
            "completeness": self._evaluate_completeness,
            "factual_consistency": self._evaluate_factual_consistency,
            "linguistic_quality": self._evaluate_linguistic_quality
        }
    
    def evaluate(self, 
                 prompt: str, 
                 response: str, 
                 provider: str, 
                 model: str,
                 custom_evaluators: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Evaluate an LLM response across multiple dimensions.
        
        Args:
            prompt: Input prompt
            response: Model response
            provider: LLM provider
            model: Model name
            custom_evaluators: List of specific evaluators to run
        
        Returns:
            Dictionary containing evaluation results
        """
        evaluation_results = {
            "timestamp": datetime.now().isoformat(),
            "evaluator_version": "1.0",
            "prompt_length": len(prompt),
            "response_length": len(response),
            "evaluations": {},
            "overall_score": 0.0,
            "summary": {}
        }
        
        # Determine which evaluators to run
        evaluators_to_run = custom_evaluators or list(self.evaluators.keys())
        
        scores = []
        for evaluator_name in evaluators_to_run:
            if evaluator_name in self.evaluators:
                try:
                    evaluation = self.evaluators[evaluator_name](prompt, response)
                    evaluation_results["evaluations"][evaluator_name] = evaluation
                    scores.append(evaluation["score"])
                except Exception as e:
                    self.logger.warning(f"Evaluator {evaluator_name} failed: {str(e)}")
                    evaluation_results["evaluations"][evaluator_name] = {
                        "score": 0.0,
                        "error": str(e)
                    }
        
        # Calculate overall score
        if scores:
            evaluation_results["overall_score"] = round(sum(scores) / len(scores), 2)
        
        # Generate summary
        evaluation_results["summary"] = self._generate_evaluation_summary(evaluation_results)
        
        return evaluation_results
    
    def _evaluate_basic_quality(self, prompt: str, response: str) -> Dict[str, Any]:
        """Evaluate basic response quality."""
        score = 0.0
        details = {}
        
        # Check if response is not empty
        if response.strip():
            score += 2.0
            details["has_content"] = True
        else:
            details["has_content"] = False
        
        # Check response length appropriateness
        response_length = len(response)
        if 10 <= response_length <= 5000:
            score += 2.0
            details["appropriate_length"] = True
        else:
            details["appropriate_length"] = False
        
        # Check for basic structure (sentences, punctuation)
        if '.' in response or '!' in response or '?' in response:
            score += 1.0
            details["has_punctuation"] = True
        else:
            details["has_punctuation"] = False
        
        return {
            "score": min(score, 5.0),
            "max_score": 5.0,
            "details": details,
            "description": "Basic quality checks including content presence, length, and structure"
        }
    
    def _evaluate_coherence(self, prompt: str, response: str) -> Dict[str, Any]:
        """Evaluate response coherence and logical flow."""
        score = 0.0
        details = {}
        
        sentences = [s.strip() for s in re.split(r'[.!?]+', response) if s.strip()]
        
        # Check sentence count
        if 1 <= len(sentences) <= 50:
            score += 1.0
            details["appropriate_sentence_count"] = True
        else:
            details["appropriate_sentence_count"] = False
        
        # Check for repetition
        if len(set(sentences)) / max(len(sentences), 1) > 0.8:
            score += 1.0
            details["low_repetition"] = True
        else:
            details["low_repetition"] = False
        
        # Check for logical connectors
        connectors = ["however", "therefore", "furthermore", "moreover", "additionally", "consequently"]
        if any(connector in response.lower() for connector in connectors):
            score += 1.0
            details["has_logical_connectors"] = True
        else:
            details["has_logical_connectors"] = False
        
        # Check paragraph structure
        paragraphs = [p.strip() for p in response.split('\n\n') if p.strip()]
        if len(paragraphs) > 1:
            score += 1.0
            details["has_paragraph_structure"] = True
        else:
            details["has_paragraph_structure"] = False
        
        # Check for contradictions (simple check)
        contradiction_patterns = [
            (r'\bnot\b.*\byes\b', r'\byes\b.*\bnot\b'),
            (r'\bno\b.*\byes\b', r'\byes\b.*\bno\b'),
            (r'\bfalse\b.*\btrue\b', r'\btrue\b.*\bfalse\b')
        ]
        
        has_contradictions = False
        for pattern1, pattern2 in contradiction_patterns:
            if re.search(pattern1, response.lower()) or re.search(pattern2, response.lower()):
                has_contradictions = True
                break
        
        if not has_contradictions:
            score += 1.0
            details["no_obvious_contradictions"] = True
        else:
            details["no_obvious_contradictions"] = False
        
        return {
            "score": score,
            "max_score": 5.0,
            "details": details,
            "description": "Coherence evaluation including logical flow, structure, and consistency"
        }
    
    def _evaluate_relevance(self, prompt: str, response: str) -> Dict[str, Any]:
        """Evaluate how relevant the response is to the prompt."""
        score = 0.0
        details = {}
        
        # Extract key terms from prompt
        prompt_words = set(re.findall(r'\b\w+\b', prompt.lower()))
        response_words = set(re.findall(r'\b\w+\b', response.lower()))
        
        # Remove common stop words
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "can", "must"}
        
        prompt_keywords = prompt_words - stop_words
        response_keywords = response_words - stop_words
        
        # Calculate keyword overlap
        if prompt_keywords:
            keyword_overlap = len(prompt_keywords & response_keywords) / len(prompt_keywords)
            score += keyword_overlap * 3.0
            details["keyword_overlap_ratio"] = round(keyword_overlap, 2)
        
        # Check if response addresses the prompt type
        question_types = {
            "what": ["what", "definition", "explanation"],
            "how": ["how", "method", "process", "way"],
            "why": ["why", "reason", "because", "cause"],
            "when": ["when", "time", "date", "period"],
            "where": ["where", "location", "place"]
        }
        
        prompt_lower = prompt.lower()
        response_lower = response.lower()
        
        for q_type, indicators in question_types.items():
            if q_type in prompt_lower:
                if any(indicator in response_lower for indicator in indicators):
                    score += 1.0
                    details[f"addresses_{q_type}_question"] = True
                    break
                else:
                    details[f"addresses_{q_type}_question"] = False
        
        # Check response length appropriateness relative to prompt
        prompt_length = len(prompt)
        response_length = len(response)
        
        if prompt_length > 0:
            length_ratio = response_length / prompt_length
            if 0.5 <= length_ratio <= 10:
                score += 1.0
                details["appropriate_length_ratio"] = True
            else:
                details["appropriate_length_ratio"] = False
        
        return {
            "score": min(score, 5.0),
            "max_score": 5.0,
            "details": details,
            "description": "Relevance evaluation based on keyword overlap and prompt addressing"
        }
    
    def _evaluate_completeness(self, prompt: str, response: str) -> Dict[str, Any]:
        """Evaluate completeness of the response."""
        score = 0.0
        details = {}
        
        # Check if response seems complete (ends with proper punctuation)
        if response.rstrip().endswith(('.', '!', '?', ':', ';')):
            score += 1.0
            details["proper_ending"] = True
        else:
            details["proper_ending"] = False
        
        # Check for cut-off indicators
        cutoff_indicators = ["...", "continue", "more", "etc.", "and so on", "[truncated]"]
        has_cutoff = any(indicator in response.lower() for indicator in cutoff_indicators)
        
        if not has_cutoff:
            score += 1.0
            details["no_cutoff_indicators"] = True
        else:
            details["no_cutoff_indicators"] = False
        
        # Check if response addresses multiple aspects (for complex prompts)
        if len(prompt.split('?')) > 1 or len(prompt.split('.')) > 2:
            # Complex prompt - check for structured response
            if any(marker in response for marker in ['1.', '2.', '-', '*', 'First', 'Second', 'Additionally']):
                score += 1.5
                details["structured_multi_part_response"] = True
            else:
                details["structured_multi_part_response"] = False
        
        # Check response depth
        if len(response) > 200:
            score += 1.0
            details["sufficient_depth"] = True
        else:
            details["sufficient_depth"] = False
        
        # Check for examples or elaboration
        example_indicators = ["for example", "such as", "like", "including", "specifically", "namely"]
        if any(indicator in response.lower() for indicator in example_indicators):
            score += 0.5
            details["includes_examples"] = True
        else:
            details["includes_examples"] = False
        
        return {
            "score": min(score, 5.0),
            "max_score": 5.0,
            "details": details,
            "description": "Completeness evaluation including proper endings, depth, and structure"
        }
    
    def _evaluate_factual_consistency(self, prompt: str, response: str) -> Dict[str, Any]:
        """Evaluate factual consistency (basic checks)."""
        score = 3.0  # Start with neutral score
        details = {}
        
        # Check for contradictory statements
        contradictory_patterns = [
            (r'\balways\b.*\bnever\b', r'\bnever\b.*\balways\b'),
            (r'\ball\b.*\bnone\b', r'\bnone\b.*\ball\b'),
            (r'\bimpossible\b.*\bpossible\b', r'\bpossible\b.*\bimpossible\b')
        ]
        
        contradiction_found = False
        for pattern1, pattern2 in contradictory_patterns:
            if re.search(pattern1, response.lower(), re.IGNORECASE) or re.search(pattern2, response.lower(), re.IGNORECASE):
                contradiction_found = True
                break
        
        if not contradiction_found:
            score += 1.0
            details["no_internal_contradictions"] = True
        else:
            score -= 1.0
            details["no_internal_contradictions"] = False
        
        # Check for hedging language (indicates uncertainty, which is good for factual accuracy)
        hedging_words = ["might", "could", "possibly", "perhaps", "likely", "probably", "seems", "appears", "suggests"]
        if any(word in response.lower() for word in hedging_words):
            score += 0.5
            details["uses_hedging_language"] = True
        else:
            details["uses_hedging_language"] = False
        
        # Check for absolute statements (which are often problematic)
        absolute_words = ["always", "never", "all", "none", "every", "completely", "totally", "absolutely"]
        absolute_count = sum(1 for word in absolute_words if word in response.lower())
        
        if absolute_count <= 2:
            score += 0.5
            details["appropriate_absolute_statements"] = True
        else:
            score -= 0.5
            details["appropriate_absolute_statements"] = False
        
        return {
            "score": max(0, min(score, 5.0)),
            "max_score": 5.0,
            "details": details,
            "description": "Basic factual consistency checks including contradictions and certainty language"
        }
    
    def _evaluate_linguistic_quality(self, prompt: str, response: str) -> Dict[str, Any]:
        """Evaluate linguistic quality of the response."""
        score = 0.0
        details = {}
        
        # Check for proper capitalization
        sentences = [s.strip() for s in re.split(r'[.!?]+', response) if s.strip()]
        properly_capitalized = sum(1 for s in sentences if s and s[0].isupper())
        
        if sentences and properly_capitalized / len(sentences) > 0.8:
            score += 1.0
            details["proper_capitalization"] = True
        else:
            details["proper_capitalization"] = False
        
        # Check for varied sentence length
        if sentences:
            sentence_lengths = [len(s.split()) for s in sentences]
            if len(set(sentence_lengths)) > 1:
                score += 1.0
                details["varied_sentence_length"] = True
            else:
                details["varied_sentence_length"] = False
        
        # Check for spelling errors (basic check)
        # Look for common patterns that might indicate spelling errors
        potential_errors = re.findall(r'\b\w*[aeiou]{3,}\w*\b|\b\w*[bcdfghjklmnpqrstvwxyz]{4,}\w*\b', response.lower())
        
        if len(potential_errors) <= 2:
            score += 1.0
            details["few_spelling_errors"] = True
        else:
            details["few_spelling_errors"] = False
        
        # Check for appropriate punctuation
        punctuation_count = len(re.findall(r'[.!?,;:]', response))
        word_count = len(response.split())
        
        if word_count > 0 and 0.05 <= punctuation_count / word_count <= 0.3:
            score += 1.0
            details["appropriate_punctuation"] = True
        else:
            details["appropriate_punctuation"] = False
        
        # Check for vocabulary diversity
        words = re.findall(r'\b\w+\b', response.lower())
        if words:
            unique_words = len(set(words))
            diversity_ratio = unique_words / len(words)
            
            if diversity_ratio > 0.6:
                score += 1.0
                details["good_vocabulary_diversity"] = True
            else:
                details["good_vocabulary_diversity"] = False
        
        return {
            "score": score,
            "max_score": 5.0,
            "details": details,
            "description": "Linguistic quality including capitalization, sentence variety, and vocabulary"
        }
    
    def _generate_evaluation_summary(self, evaluation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of the evaluation results."""
        evaluations = evaluation_results.get("evaluations", {})
        
        # Find best and worst performing areas
        scores = {name: eval_data.get("score", 0) for name, eval_data in evaluations.items()}
        
        best_area = max(scores, key=scores.get) if scores else None
        worst_area = min(scores, key=scores.get) if scores else None
        
        # Categorize overall performance
        overall_score = evaluation_results.get("overall_score", 0)
        if overall_score >= 4.0:
            performance_category = "excellent"
        elif overall_score >= 3.0:
            performance_category = "good"
        elif overall_score >= 2.0:
            performance_category = "fair"
        else:
            performance_category = "poor"
        
        return {
            "overall_score": overall_score,
            "performance_category": performance_category,
            "best_performing_area": best_area,
            "worst_performing_area": worst_area,
            "total_evaluations": len(evaluations),
            "areas_above_average": sum(1 for score in scores.values() if score >= 2.5),
            "areas_below_average": sum(1 for score in scores.values() if score < 2.5)
        }
