import re
from typing import List, Dict

class SkillExtractor:
    def __init__(self):
        # Common technical skills and domains
        self.technical_skills = {
            'programming': ['python', 'java', 'javascript', 'c++', 'ruby', 'go', 'rust'],
            'ai_ml': ['machine learning', 'deep learning', 'neural networks', 'nlp', 'computer vision'],
            'data': ['data analysis', 'data science', 'big data', 'sql', 'nosql'],
            'cloud': ['aws', 'azure', 'gcp', 'cloud computing', 'devops'],
            'web': ['web development', 'frontend', 'backend', 'full stack'],
        }

    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        text_lower = text.lower()
        extracted_skills = {
            'technical': [],
            'soft_skills': [],
            'domains': [],
            'tools': []
        }
        # Extract technical skills
        for category, skills in self.technical_skills.items():
            for skill in skills:
                if skill in text_lower:
                    extracted_skills['technical'].append(skill)
        # Extract soft skills using common patterns
        soft_skills_pattern = r'leadership|communication|teamwork|problem-solving|creativity|adaptability|time management|collaboration'
        soft_skills = re.findall(soft_skills_pattern, text_lower)
        extracted_skills['soft_skills'].extend(soft_skills)
        # Simple domain/tool extraction (look for keywords)
        domain_keywords = ['healthcare', 'finance', 'education', 'retail', 'manufacturing', 'cloud', 'web', 'ai', 'ml']
        for word in domain_keywords:
            if word in text_lower:
                extracted_skills['domains'].append(word)
        tool_keywords = ['tensorflow', 'pytorch', 'docker', 'kubernetes', 'figma', 'adobe xd']
        for word in tool_keywords:
            if word in text_lower:
                extracted_skills['tools'].append(word)
        return extracted_skills

    def extract_ai_capabilities(self, text: str) -> Dict[str, List[str]]:
        text_lower = text.lower()
        capabilities = {
            'tasks': [],
            'domains': [],
            'techniques': [],
            'limitations': []
        }
        # Extract task capabilities
        task_patterns = [
            r'can ([a-z ]+)',
            r'able to ([a-z ]+)',
            r'capable of ([a-z ]+)'
        ]
        for pattern in task_patterns:
            matches = re.findall(pattern, text_lower)
            capabilities['tasks'].extend(matches)
        # Simple domain/technique extraction
        domain_keywords = ['healthcare', 'finance', 'education', 'retail', 'manufacturing', 'cloud', 'web', 'ai', 'ml']
        for word in domain_keywords:
            if word in text_lower:
                capabilities['domains'].append(word)
        technique_keywords = ['regression', 'classification', 'clustering', 'simulation', 'optimization']
        for word in technique_keywords:
            if word in text_lower:
                capabilities['techniques'].append(word)
        # Extract limitations
        limitation_patterns = [
            r'cannot ([a-z ]+)',
            r'unable to ([a-z ]+)',
            r'limited in ([a-z ]+)'
        ]
        for pattern in limitation_patterns:
            matches = re.findall(pattern, text_lower)
            capabilities['limitations'].extend(matches)
        return capabilities 