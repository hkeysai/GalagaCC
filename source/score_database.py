"""
Persistent score database for Galaga
Stores high scores across game sessions
"""
import json
import os
from datetime import datetime
from typing import List, Dict
from . import constants as c


class ScoreDatabase:
    """Manages persistent high scores"""
    
    def __init__(self, filename="galaga_scores.json"):
        self.filename = filename
        self.scores = []
        self.current_session_high = 0
        self.load_scores()
    
    def load_scores(self):
        """Load scores from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.scores = data.get('scores', [])
                    self.current_session_high = data.get('session_high', 0)
                    # Ensure we have the right number of scores
                    self._ensure_default_scores()
            except (json.JSONDecodeError, IOError):
                # If file is corrupted, start fresh
                self._create_default_scores()
        else:
            self._create_default_scores()
    
    def _create_default_scores(self):
        """Create default high score list"""
        self.scores = [
            {'name': 'AAA', 'score': 30000, 'date': '2024-01-01', 'stage': 5},
            {'name': 'BBB', 'score': 20000, 'date': '2024-01-01', 'stage': 4},
            {'name': 'CCC', 'score': 10000, 'date': '2024-01-01', 'stage': 3},
            {'name': 'DDD', 'score': 9000, 'date': '2024-01-01', 'stage': 2},
            {'name': 'EEE', 'score': 8000, 'date': '2024-01-01', 'stage': 2}
        ]
        self.save_scores()
    
    def _ensure_default_scores(self):
        """Ensure we have at least 5 scores"""
        while len(self.scores) < c.NUM_TRACKED_SCORES:
            self.scores.append({
                'name': 'CPU',
                'score': 1000 * (c.NUM_TRACKED_SCORES - len(self.scores)),
                'date': '2024-01-01',
                'stage': 1
            })
    
    def save_scores(self):
        """Save scores to JSON file"""
        try:
            # Sort scores by score descending
            self.scores.sort(key=lambda x: x['score'], reverse=True)
            # Keep only top scores
            self.scores = self.scores[:c.NUM_TRACKED_SCORES]
            
            data = {
                'scores': self.scores,
                'session_high': self.current_session_high,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Error saving scores: {e}")
    
    def is_high_score(self, score: int) -> bool:
        """Check if score qualifies for high score list"""
        if len(self.scores) < c.NUM_TRACKED_SCORES:
            return True
        return score > self.scores[-1]['score']
    
    def add_score(self, name: str, score: int, stage: int) -> int:
        """
        Add a new high score
        Returns the position in the high score list (1-based), or 0 if not a high score
        """
        if not self.is_high_score(score):
            return 0
        
        # Create new score entry
        new_score = {
            'name': name.upper()[:3],  # Ensure 3 chars, uppercase
            'score': score,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'stage': stage
        }
        
        # Add and sort
        self.scores.append(new_score)
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        self.scores = self.scores[:c.NUM_TRACKED_SCORES]
        
        # Find position
        position = 0
        for i, s in enumerate(self.scores):
            if s == new_score:
                position = i + 1
                break
        
        # Save to disk
        self.save_scores()
        
        return position
    
    def get_high_score(self) -> int:
        """Get the current high score"""
        if self.scores:
            return self.scores[0]['score']
        return 0
    
    def get_scores(self) -> List[Dict]:
        """Get all high scores"""
        return self.scores.copy()
    
    def update_session_high(self, score: int):
        """Update current session high score"""
        if score > self.current_session_high:
            self.current_session_high = score
            self.save_scores()
    
    def reset_session_high(self):
        """Reset session high score"""
        self.current_session_high = 0
        self.save_scores()


# Global instance
score_db = ScoreDatabase()