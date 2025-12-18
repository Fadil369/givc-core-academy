from typing import List, Dict, Tuple
from datetime import datetime
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor

class AdaptiveLearningEngine:
    """AI-powered adaptive learning path engine"""

    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.clusterer = KMeans(n_clusters=5, random_state=42)

    async def generate_learning_path(self, learner_profile: Dict) -> Dict:
        """Generate a personalized learning path based on learner profile"""
        # 1. Feature extraction
        features = self._extract_features(learner_profile)
        # 2. Predict skill gaps
        skill_gap_scores = self._predict_skill_gaps(features)
        # 3. Cluster learners for similar pathways
        cluster_id = self._assign_cluster(features)
        # 4. Build path
        path = self._build_path(skill_gap_scores, cluster_id)
        return {
            "learner_id": learner_profile.get("learner_id"),
            "learning_path": path,
            "skill_gaps": skill_gap_scores,
            "cluster_id": cluster_id,
            "generated_at": datetime.utcnow().isoformat()
        }

    def _extract_features(self, profile: Dict) -> np.ndarray:
        # Simplified feature vector: years_experience, competency scores, region encoding
        years = profile.get("years_experience", 0)
        comps = [profile.get(key, 5) for key in [
            "medical_terminology", "anatomy_knowledge", "sbs_coding",
            "icd_10_am", "chi_regulations"
        ]]
        region = hash(profile.get("region", "")) % 1000 / 1000.0
        return np.array([years] + comps + [region]).reshape(1, -1)

    def _predict_skill_gaps(self, features: np.ndarray) -> Dict:
        # Dummy prediction using random values for illustration
        preds = np.random.rand(5)
        skill_names = ["medical_terminology", "anatomy_knowledge", "sbs_coding", "icd_10_am", "chi_regulations"]
        return {name: round(float(p) * 10, 2) for name, p in zip(skill_names, preds)}

    def _assign_cluster(self, features: np.ndarray) -> int:
        # Fit clusterer on the fly (in production would be pre-trained)
        self.clusterer.fit(features)
        return int(self.clusterer.labels_[0])

    def _build_path(self, skill_gaps: Dict, cluster_id: int) -> List[Dict]:
        # Create a simple sequential path based on highest gaps
        sorted_skills = sorted(skill_gaps.items(), key=lambda x: x[1], reverse=True)
        path = []
        for idx, (skill, gap) in enumerate(sorted_skills):
            path.append({
                "step": idx + 1,
                "skill": skill,
                "estimated_hours": max(1, int(gap)),
                "module_id": f"MOD-{cluster_id}-{skill.upper()}"
            })
        return path
