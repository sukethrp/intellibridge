from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict, Tuple
import pandas as pd
import json
import os


class ExpertMatcher:
    def __init__(self):
        """Initialize the matcher with Sentence-BERT model."""
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.feedback_file = 'match_feedback.json'
        self.load_feedback()

    def load_feedback(self):
        """Load historical feedback data."""
        if os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'r') as f:
                self.feedback_data = json.load(f)
        else:
            self.feedback_data = {
                'positive_matches': [],
                'negative_matches': [],
                'skill_weights': {}
            }

    def save_feedback(self):
        """Save feedback data to file."""
        with open(self.feedback_file, 'w') as f:
            json.dump(self.feedback_data, f, indent=2)

    def add_feedback(self, human: str, ai: str, is_positive: bool, reason: str = None):
        """Add feedback for a match."""
        feedback = {
            'human': human,
            'ai': ai,
            'timestamp': pd.Timestamp.now().isoformat(),
            'reason': reason
        }

        if is_positive:
            self.feedback_data['positive_matches'].append(feedback)
        else:
            self.feedback_data['negative_matches'].append(feedback)

        self.save_feedback()
        self.update_skill_weights()

    def update_skill_weights(self):
        """Update skill weights based on feedback."""
        # Count skill occurrences in positive matches
        positive_skills = {}
        for match in self.feedback_data['positive_matches']:
            human_profile = next(
                (p for p in self.human_profiles if p['name'] == match['human']), None)
            if human_profile:
                for skill in human_profile['skills']:
                    positive_skills[skill] = positive_skills.get(skill, 0) + 1

        # Update weights based on positive feedback
        total_positive = sum(positive_skills.values())
        if total_positive > 0:
            for skill, count in positive_skills.items():
                self.feedback_data['skill_weights'][skill] = count / \
                    total_positive

    def _get_embedding(self, text: str) -> np.ndarray:
        """Convert text to embedding vector."""
        return self.model.encode(text)

    def _calculate_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        return cosine_similarity([vec1], [vec2])[0][0]

    def _calculate_complementarity(self, human_skills, ai_capabilities) -> float:
        # Accepts either a list or a dict of lists
        def flatten(sk):
            if isinstance(sk, dict):
                result = set()
                for v in sk.values():
                    result.update(v)
                return result
            elif isinstance(sk, list):
                return set(sk)
            else:
                return set()
        human_skill_set = flatten(human_skills)
        ai_capability_set = flatten(ai_capabilities)
        intersection = len(human_skill_set.intersection(ai_capability_set))
        union = len(human_skill_set.union(ai_capability_set))
        if union == 0:
            return 0.0
        jaccard_similarity = intersection / union
        complementarity = 1 - jaccard_similarity
        return complementarity

    def match_experts(self,
                      human_profiles: List[Dict],
                      ai_profiles: List[Dict],
                      weights: Dict[str, float] = None) -> List[Dict]:
        """
        Match human experts with AI agents based on skills and capabilities.

        Args:
            human_profiles: List of human expert profiles
            ai_profiles: List of AI agent profiles
            weights: Dictionary of weights for different matching criteria

        Returns:
            List of matches with scores and explanations
        """
        self.human_profiles = human_profiles  # Store for feedback processing

        if weights is None:
            weights = {
                'skill_similarity': 0.4,
                'complementarity': 0.4,
                'domain_alignment': 0.2
            }

        matches = []

        for human in human_profiles:
            human_matches = []

            # Get human profile embedding
            human_text = f"{human['bio']} {' '.join(human['skills'])}"
            human_embedding = self._get_embedding(human_text)

            for ai in ai_profiles:
                # Get AI profile embedding
                ai_text = f"{ai['description']} {' '.join(ai['capabilities'])}"
                ai_embedding = self._get_embedding(ai_text)

                # Calculate different similarity scores
                skill_similarity = self._calculate_similarity(
                    human_embedding, ai_embedding)
                complementarity = self._calculate_complementarity(
                    human['skills'], ai['capabilities'])

                # Calculate domain alignment
                human_domains = set(human['skills']) if isinstance(
                    human['skills'], list) else set(human['skills'].get('domains', []))
                ai_domains = set(ai['capabilities']) if isinstance(
                    ai['capabilities'], list) else set(ai['capabilities'].get('domains', []))
                domain_alignment = len(human_domains.intersection(
                    ai_domains)) / max(len(human_domains.union(ai_domains)), 1)

                # Apply feedback-based adjustments
                feedback_adjustment = self._calculate_feedback_adjustment(
                    human, ai)

                # Calculate weighted score
                total_score = (
                    weights['skill_similarity'] * skill_similarity +
                    weights['complementarity'] * complementarity +
                    weights['domain_alignment'] * domain_alignment
                ) * (1 + feedback_adjustment)

                match = {
                    'human': human['name'],
                    'ai': ai['name'],
                    'total_score': total_score,
                    'skill_similarity': skill_similarity,
                    'complementarity': complementarity,
                    'domain_alignment': domain_alignment,
                    'feedback_adjustment': feedback_adjustment,
                    'explanation': self._generate_explanation(
                        skill_similarity, complementarity, domain_alignment, feedback_adjustment
                    )
                }

                human_matches.append(match)

            # Sort matches by total score
            human_matches.sort(key=lambda x: x['total_score'], reverse=True)
            matches.extend(human_matches)

        return matches

    def _calculate_feedback_adjustment(self, human: Dict, ai: Dict) -> float:
        """Calculate score adjustment based on historical feedback."""
        adjustment = 0.0

        # Check for direct feedback on this pair
        for match in self.feedback_data['positive_matches']:
            if match['human'] == human['name'] and match['ai'] == ai['name']:
                adjustment += 0.1  # Boost score for positive feedback

        for match in self.feedback_data['negative_matches']:
            if match['human'] == human['name'] and match['ai'] == ai['name']:
                adjustment -= 0.1  # Reduce score for negative feedback

        # Apply skill-based adjustments
        for skill in human['skills']:
            if skill in self.feedback_data['skill_weights']:
                adjustment += self.feedback_data['skill_weights'][skill] * 0.05

        return adjustment

    def _generate_explanation(self,
                              skill_similarity: float,
                              complementarity: float,
                              domain_alignment: float,
                              feedback_adjustment: float) -> str:
        """Generate human-readable explanation for the match."""
        explanation = []

        if skill_similarity > 0.7:
            explanation.append("High skill similarity")
        elif skill_similarity > 0.4:
            explanation.append("Moderate skill similarity")
        else:
            explanation.append("Low skill similarity")

        if complementarity > 0.7:
            explanation.append("Highly complementary skills")
        elif complementarity > 0.4:
            explanation.append("Moderately complementary skills")
        else:
            explanation.append("Low skill complementarity")

        if domain_alignment > 0.7:
            explanation.append("Strong domain alignment")
        elif domain_alignment > 0.4:
            explanation.append("Moderate domain alignment")
        else:
            explanation.append("Low domain alignment")

        if feedback_adjustment > 0:
            explanation.append("Positive historical feedback")
        elif feedback_adjustment < 0:
            explanation.append("Negative historical feedback")

        return ". ".join(explanation)
