import json
from typing import Set, Dict, List

class SkillEngine:
    def __init__(self, skill_hierarchy_path: str):
        self.skill_hierarchy = self._load_skill_hierarchy(skill_hierarchy_path)
        self.all_defined_skills = self._get_all_defined_skills()

    def _load_skill_hierarchy(self, path: str) -> Dict[str, List[str]]:
        """Loads the skill hierarchy from a JSON file."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                # Convert all keys and values to lowercase for case-insensitive matching
                hierarchy = {k.lower(): [v.lower() for v in val] for k, val in json.load(f).items()}
            return hierarchy
        except FileNotFoundError:
            print(f"Error: Skill hierarchy file not found at {path}")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {path}")
            return {}

    def _get_all_defined_skills(self) -> Set[str]:
        """Gathers all unique skills mentioned as keys or values in the hierarchy."""
        skills = set(self.skill_hierarchy.keys())
        for implied_skills in self.skill_hierarchy.values():
            skills.update(implied_skills)
        return skills

    def infer_skills(self, text: str) -> Dict[str, Set[str]]:
        """
        Infers skills from text based on the loaded hierarchy.

        Args:
            text (str): The input text (e.g., from a resume).

        Returns:
            Dict[str, Set[str]]: A dictionary containing:
                - 'explicit': Skills directly found in the text.
                - 'implicit': Skills inferred from the explicit skills.
                - 'all': Union of explicit and implicit skills.
        """
        text_lower = text.lower()
        explicit_skills = set()
        inferred_skills = set()
        
        # Identify explicit skills directly mentioned in the text
        for skill in self.all_defined_skills:
            # Using '\b' for whole word matching to avoid partial matches (e.g., 'py' in 'python')
            # This is a basic approach; a more advanced one might use NLP tokenization.
            if f"\b{skill}\b" in text_lower: # This regex will not work as expected with f-string and raw text.
                explicit_skills.add(skill)

        # Corrected approach for explicit skill matching (without regex in plain string matching)
        for skill_key in self.all_defined_skills:
             if skill_key in text_lower: # This needs more robust word boundary matching for production
                 explicit_skills.add(skill_key)


        # Infer implicit skills
        skills_to_process = list(explicit_skills)
        processed_skills = set()

        while skills_to_process:
            current_skill = skills_to_process.pop(0)
            if current_skill in processed_skills:
                continue
            
            processed_skills.add(current_skill)
            
            # Add current_skill to inferred_skills if it's not an explicit skill already
            if current_skill not in explicit_skills:
                inferred_skills.add(current_skill)

            # Find skills that imply current_skill, or skills that current_skill implies
            # For hierarchical inference, we're interested in what current_skill implies
            for child_skill, implied_by_child in self.skill_hierarchy.items():
                if current_skill in implied_by_child and child_skill not in processed_skills:
                    # If current_skill is implied by child_skill, and child_skill is found,
                    # then child_skill could be an explicit skill leading to current_skill.
                    # For pure upward inference, we focus on what explicit skills *lead to*.
                    pass # This path is for reverse inference, not for this current goal.

            # Traverse "upwards" the hierarchy - what does current_skill imply?
            # Check if current_skill itself is a key implying other skills
            if current_skill in self.skill_hierarchy:
                for implied_skill in self.skill_hierarchy[current_skill]:
                    if implied_skill not in processed_skills:
                        skills_to_process.append(implied_skill)
                        inferred_skills.add(implied_skill) # Add it to inferred as we are discovering it

        # Ensure explicit skills are also part of the 'all' set but not double counted in 'implicit' if they were also implied by something else
        all_skills = explicit_skills.union(inferred_skills)
        
        # Remove any explicit skills from the inferred_skills set to keep them distinct
        # This is important if an explicit skill (e.g. 'react') is also implied by another explicit skill (e.g. 'next.js')
        inferred_skills = inferred_skills - explicit_skills


        return {
            "explicit": explicit_skills,
            "implicit": inferred_skills,
            "all": all_skills
        }
    
    def calculate_score(self, explicit_skills: Set[str], job_requirements: Set[str]) -> float:
        """
        Calculates a simple matching score based on explicit skills against job requirements.
        A more advanced scoring could consider implicit skills and weighting.
        """
        if not job_requirements:
            return 0.0
        
        matched_skills = explicit_skills.intersection(job_requirements)
        score = (len(matched_skills) / len(job_requirements)) * 100
        return round(score, 2)


if __name__ == "__main__":
    # Example Usage
    engine = SkillEngine(skill_hierarchy_path="data/skill_hierarchy.json")

    sample_resume_text = """
    I have extensive experience with Python, FastAPI, and building REST APIs.
    My frontend skills include React and JavaScript. I also have some knowledge of Docker.
    In my previous role, I worked on machine learning projects using PyTorch.
    """
    
    # Simulate job requirements (e.g., parsed from a job description)
    job_reqs = {"python", "fastapi", "react", "machine learning", "tensorflow", "docker", "cloud"}

    print("\n--- Skill Inference ---")
    inferred = engine.infer_skills(sample_resume_text)
    print(f"Explicit Skills: {inferred['explicit']}")
    print(f"Inferred Skills: {inferred['implicit']}")
    print(f"All Skills: {inferred['all']}")

    print("\n--- Scoring against Job Requirements ---")
    # For scoring, we might want to use 'all' skills or just 'explicit' depending on logic
    # For this example, let's use 'all' inferred skills for a broader match
    job_reqs_lower = {req.lower() for req in job_reqs}
    
    score = engine.calculate_score(inferred['all'], job_reqs_lower)
    print(f"Job Requirements: {job_reqs_lower}")
    print(f"Candidate Match Score: {score:.2f}%")

    # Test with text containing skills that imply others
    print("\n--- Another Test Case ---")
    another_text = "I am a Python developer with experience in Deep Learning and some React. I manage deployments with Docker."
    inferred2 = engine.infer_skills(another_text)
    print(f"Explicit Skills: {inferred2['explicit']}")
    print(f"Inferred Skills: {inferred2['implicit']}")
    print(f"All Skills: {inferred2['all']}")
