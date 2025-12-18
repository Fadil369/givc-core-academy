import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class ModuleState:
    """Represents a learning module state in Q-learning"""
    module_id: str
    skills_covered: List[str]
    time_spent: float
    score_achieved: float
    difficulty: str

class QLearningPathOptimizer:
    """
    Q-Learning algorithm for optimizing learning paths
    """
    
    def __init__(
        self,
        modules: List[Dict],
        skill_gaps: Dict,
        learner_profile: LearnerProfile,
        dependency_graph: Dict
    ):
        self.modules = modules
        self.skill_gaps = skill_gaps
        self.learner_profile = learner_profile
        self.dependency_graph = dependency_graph
        
        # Q-learning parameters
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.exploration_rate = 0.3
        
        # Initialize Q-table
        self.q_table = defaultdict(lambda: defaultdict(float))
        
        # State representation
        self.state_space = self._create_state_space()
        self.action_space = self._create_action_space()
    
    def find_optimal_path(
        self, 
        max_steps: int = 20,
        exploration_rate: float = 0.3
    ) -> List[str]:
        """
        Find optimal learning path using Q-learning
        """
        self.exploration_rate = exploration_rate
        
        # Training episodes
        for episode in range(1000):
            state = self._get_initial_state()
            total_reward = 0
            
            for step in range(max_steps):
                # Choose action (ε-greedy)
                if np.random.random() < self.exploration_rate:
                    action = self._choose_random_action(state)
                else:
                    action = self._choose_best_action(state)
                
                # Take action and get reward
                next_state, reward = self._take_action(state, action)
                
                # Update Q-value
                best_next_action = self._choose_best_action(next_state)
                td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
                td_error = td_target - self.q_table[state][action]
                self.q_table[state][action] += self.learning_rate * td_error
                
                state = next_state
                total_reward += reward
                
                # Check termination conditions
                if self._should_terminate(state, step):
                    break
        
        # Extract optimal path
        optimal_path = []
        state = self._get_initial_state()
        
        for _ in range(max_steps):
            if not self.q_table[state]:
                break
            
            action = self._choose_best_action(state)
            optimal_path.append(action)
            
            # Move to next state
            next_state, _ = self._take_action(state, action)
            state = next_state
            
            if self._should_terminate(state, len(optimal_path)):
                break
        
        return optimal_path
    
    def _take_action(
        self, 
        state: Tuple, 
        action: str
    ) -> Tuple[Tuple, float]:
        """
        Take an action and calculate reward
        """
        # Get module details
        module = next(m for m in self.modules if m["id"] == action)
        
        # Calculate reward based on multiple factors
        reward = 0
        
        # 1. Skill gap coverage reward
        skill_coverage_reward = self._calculate_skill_coverage_reward(
            state, module
        )
        reward += skill_coverage_reward * 2.0
        
        # 2. Time efficiency reward (shorter modules preferred)
        time_efficiency_reward = self._calculate_time_efficiency_reward(module)
        reward += time_efficiency_reward
        
        # 3. Difficulty appropriateness reward
        difficulty_reward = self._calculate_difficulty_reward(
            module, self.learner_profile
        )
        reward += difficulty_reward * 1.5
        
        # 4. Prerequisite satisfaction reward
        prerequisite_reward = self._calculate_prerequisite_reward(state, module)
        reward += prerequisite_reward * 3.0  # Higher weight for prerequisites
        
        # 5. Saudi content relevance reward
        saudi_relevance_reward = self._calculate_saudi_relevance_reward(
            module, self.learner_profile.region
        )
        reward += saudi_relevance_reward
        
        # Update state
        new_state = self._update_state(state, action, module)
        
        return new_state, reward
    
    def _calculate_skill_coverage_reward(
        self, 
        state: Tuple, 
        module: Dict
    ) -> float:
        """
        Calculate reward based on how well module covers skill gaps
        """
        reward = 0
        
        # Get skills covered by module
        module_skills = set(module.get("skills_targeted", []))
        
        # Get remaining skill gaps from state
        remaining_gaps = state[1]  # Assuming state[1] contains remaining gaps
        
        # Calculate coverage
        covered_gaps = module_skills.intersection(remaining_gaps)
        
        if covered_gaps:
            # Higher reward for covering larger gaps
            for skill in covered_gaps:
                gap_size = self.skill_gaps.get(skill, {}).get("gap", 0)
                reward += gap_size * 0.5
            
            # Bonus for covering multiple skills
            if len(covered_gaps) > 1:
                reward *= 1.2
        
        return reward
2.3 Performance Tracking & Adaptive Adjustment
python
