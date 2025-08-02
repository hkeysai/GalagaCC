#!/usr/bin/env python3
"""
Galaga QA Checker - Automated testing and issue detection
"""

import os
import sys
import importlib.util
import ast
import json
from pathlib import Path
from typing import List, Dict, Tuple, Any

class GalagaQAChecker:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.issues = []
        self.warnings = []
        self.fixes_applied = []
        
    def add_issue(self, category: str, description: str, file: str = None, line: int = None):
        """Add an issue to the report"""
        issue = {
            "category": category,
            "description": description,
            "file": file,
            "line": line,
            "severity": "error"
        }
        self.issues.append(issue)
        
    def add_warning(self, category: str, description: str, file: str = None):
        """Add a warning to the report"""
        warning = {
            "category": category,
            "description": description,
            "file": file,
            "severity": "warning"
        }
        self.warnings.append(warning)
        
    def check_file_structure(self):
        """Check if all required files and directories exist"""
        print("Checking file structure...")
        
        required_files = [
            "galaga.py",
            "source/__init__.py",
            "source/main.py",
            "source/constants.py",
            "source/sprites.py",
            "source/formation.py",
            "source/patterns.py",
            "source/play.py",
            "source/states.py",
            "source/setup.py",
            "source/tools.py",
            "source/hud.py",
            "source/scoring.py",
            "source/stars.py",
            "resources/graphics/sheet.png",
            "resources/audio/enemy_fire.ogg",
            "README.md",
            "LICENSE.txt"
        ]
        
        for file_path in required_files:
            full_path = self.root_path / file_path
            if not full_path.exists():
                self.add_issue("FILE_STRUCTURE", f"Missing required file: {file_path}")
                
    def check_imports(self):
        """Check for import errors and circular dependencies"""
        print("Checking imports...")
        
        python_files = list(self.root_path.glob("**/*.py"))
        
        for py_file in python_files:
            if "__pycache__" in str(py_file):
                continue
                
            try:
                with open(py_file, 'r') as f:
                    tree = ast.parse(f.read(), filename=str(py_file))
                    
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if alias.name == "pygame":
                                # Check pygame availability separately
                                pass
                    elif isinstance(node, ast.ImportFrom):
                        if node.module and node.module.startswith('.'):
                            # Relative import - check if target exists
                            self._check_relative_import(py_file, node.module)
                            
            except SyntaxError as e:
                self.add_issue("SYNTAX", f"Syntax error: {e}", str(py_file), e.lineno)
            except Exception as e:
                self.add_issue("IMPORT", f"Failed to parse file: {e}", str(py_file))
                
    def _check_relative_import(self, file_path: Path, module: str):
        """Check if relative import target exists"""
        # Convert relative import to path
        parent_dir = file_path.parent
        module_path = module.replace('.', '/')
        
        # Remove leading dots and navigate up
        while module_path.startswith('/'):
            module_path = module_path[1:]
            parent_dir = parent_dir.parent
            
        target_file = parent_dir / f"{module_path}.py"
        target_dir = parent_dir / module_path / "__init__.py"
        
        if not (target_file.exists() or target_dir.exists()):
            self.add_warning("IMPORT", f"Relative import target not found: {module}", str(file_path))
            
    def check_sprite_coordinates(self):
        """Verify sprite sheet coordinates are valid"""
        print("Checking sprite coordinates...")
        
        sprites_file = self.root_path / "source" / "sprites.py"
        if not sprites_file.exists():
            return
            
        with open(sprites_file, 'r') as f:
            content = f.read()
            
        # Check for sprite coordinates
        sprite_coords = [
            ("BLUE_FRAMES", [(80, 80, 16, 16), (96, 80, 16, 16)]),
            ("YELLOW_FRAMES", [(112, 80, 16, 16), (128, 80, 16, 16)]),
            ("RED_FRAMES", [(80, 96, 16, 16), (96, 96, 16, 16)]),
            ("GREEN_FRAMES", [(112, 96, 16, 16), (128, 96, 16, 16)]),
            ("ENEMY_MISSILE", (246, 51, 3, 8)),
            ("PLAYER_MISSILE", (246, 67, 3, 8))
        ]
        
        # Just verify these are defined, actual validation would need sprite sheet
        for coord_name, coords in sprite_coords:
            if coord_name not in content:
                self.add_warning("SPRITES", f"Missing sprite coordinate definition: {coord_name}")
                
    def check_game_constants(self):
        """Verify game constants are properly defined"""
        print("Checking game constants...")
        
        constants_file = self.root_path / "source" / "constants.py"
        if not constants_file.exists():
            return
            
        required_constants = [
            "FPS",
            "GAME_SIZE",
            "PLAYER_SPEED",
            "FORMATION_MIN_SPREAD",
            "FORMATION_MAX_SPREAD",
            "FORMATION_CYCLE_TIME",
            "TITLE_STATE",
            "PLAY_STATE",
            "GAME_OVER_STATE"
        ]
        
        with open(constants_file, 'r') as f:
            content = f.read()
            
        for const in required_constants:
            if f"{const} =" not in content:
                self.add_issue("CONSTANTS", f"Missing required constant: {const}")
                
    def check_collision_logic(self):
        """Check collision detection implementation"""
        print("Checking collision logic...")
        
        play_file = self.root_path / "source" / "play.py"
        if not play_file.exists():
            return
            
        with open(play_file, 'r') as f:
            content = f.read()
            
        # Check for collision methods
        required_collisions = [
            "colliderect",  # Pygame collision
            "enemy.rect.colliderect(a_missile.rect)",  # Enemy-missile
            "missile.rect.colliderect(self.player.rect)"  # Missile-player
        ]
        
        for collision in required_collisions:
            if collision not in content:
                self.add_warning("COLLISION", f"Missing collision check: {collision}")
                
    def check_state_transitions(self):
        """Verify state machine transitions"""
        print("Checking state transitions...")
        
        states = ["TITLE_STATE", "PLAY_STATE", "GAME_OVER_STATE", "SCORE_ENTRY_STATE", "DEMO_STATE"]
        transitions = {
            "TITLE_STATE": ["PLAY_STATE"],
            "PLAY_STATE": ["GAME_OVER_STATE", "SCORE_ENTRY_STATE"],
            "GAME_OVER_STATE": ["TITLE_STATE"],
            "SCORE_ENTRY_STATE": ["GAME_OVER_STATE"]
        }
        
        # Check main.py for state dictionary
        main_file = self.root_path / "source" / "main.py"
        if main_file.exists():
            with open(main_file, 'r') as f:
                content = f.read()
                
            for state in states:
                if state not in content:
                    self.add_warning("STATES", f"State not found in main.py: {state}")
                    
    def check_enemy_behavior(self):
        """Check enemy AI implementation"""
        print("Checking enemy behavior...")
        
        required_methods = [
            "set_entrance_path",
            "start_attack", 
            "_follow_entrance_path",
            "_follow_attack_path",
            "should_fire",
            "trigger_attack_wave"
        ]
        
        # Check sprites.py for enemy methods
        sprites_file = self.root_path / "source" / "sprites.py"
        formation_file = self.root_path / "source" / "formation.py"
        
        for file_path in [sprites_file, formation_file]:
            if file_path.exists():
                with open(file_path, 'r') as f:
                    content = f.read()
                    
                for method in required_methods:
                    if f"def {method}" in content:
                        break
                else:
                    if method not in content:
                        self.add_warning("ENEMY_AI", f"Missing enemy method: {method}")
                        
    def check_resource_references(self):
        """Check that all referenced resources exist"""
        print("Checking resource references...")
        
        # Check audio references
        audio_dir = self.root_path / "resources" / "audio"
        if audio_dir.exists():
            audio_files = set(f.name for f in audio_dir.glob("*.ogg"))
            
            # Find all play_sound calls
            for py_file in self.root_path.glob("source/*.py"):
                with open(py_file, 'r') as f:
                    content = f.read()
                    
                import re
                sound_calls = re.findall(r'play_sound\("([^"]+)"\)', content)
                
                for sound in sound_calls:
                    if f"{sound}.ogg" not in audio_files:
                        self.add_warning("RESOURCES", f"Missing audio file: {sound}.ogg", str(py_file))
                        
    def auto_fix_issues(self):
        """Attempt to auto-fix common issues"""
        print("\nAttempting auto-fixes...")
        
        # Fix missing __init__.py files
        for dir_path in [self.root_path / "source", self.root_path / "resources"]:
            init_file = dir_path / "__init__.py"
            if dir_path.exists() and not init_file.exists():
                init_file.write_text("")
                self.fixes_applied.append(f"Created missing {init_file}")
                
        # Fix missing imports
        for py_file in self.root_path.glob("source/*.py"):
            if py_file.name == "__init__.py":
                continue
                
            with open(py_file, 'r') as f:
                content = f.read()
                
            # Add missing pygame import
            if "pygame" in content and "import pygame" not in content:
                lines = content.split('\n')
                # Find first import line
                for i, line in enumerate(lines):
                    if line.startswith('import') or line.startswith('from'):
                        lines.insert(i, 'import pygame')
                        break
                else:
                    lines.insert(0, 'import pygame')
                    
                with open(py_file, 'w') as f:
                    f.write('\n'.join(lines))
                self.fixes_applied.append(f"Added missing pygame import to {py_file.name}")
                
    def generate_report(self):
        """Generate QA report"""
        print("\n" + "="*60)
        print("GALAGA QA REPORT")
        print("="*60)
        
        # Summary
        print(f"\nTotal Issues: {len(self.issues)}")
        print(f"Total Warnings: {len(self.warnings)}")
        print(f"Fixes Applied: {len(self.fixes_applied)}")
        
        # Issues by category
        if self.issues:
            print("\n### ISSUES ###")
            categories = {}
            for issue in self.issues:
                cat = issue['category']
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(issue)
                
            for cat, issues in categories.items():
                print(f"\n{cat} ({len(issues)} issues):")
                for issue in issues:
                    location = f" [{issue['file']}:{issue['line']}]" if issue['file'] else ""
                    print(f"  - {issue['description']}{location}")
                    
        # Warnings
        if self.warnings:
            print("\n### WARNINGS ###")
            for warning in self.warnings:
                location = f" [{warning['file']}]" if warning['file'] else ""
                print(f"  - {warning['description']}{location}")
                
        # Fixes
        if self.fixes_applied:
            print("\n### AUTO-FIXES APPLIED ###")
            for fix in self.fixes_applied:
                print(f"  ✓ {fix}")
                
        # Recommendations
        print("\n### RECOMMENDATIONS ###")
        print("  1. Install pygame: pip install pygame==1.9.6")
        print("  2. Run the game to test: python galaga.py")
        print("  3. Check sprite sheet exists: resources/graphics/sheet.png")
        print("  4. Verify all audio files in resources/audio/")
        print("  5. Test state transitions and enemy behaviors")
        
        print("\n" + "="*60)
        
        # Save report to file
        report_path = self.root_path / "qa_report.json"
        report_data = {
            "issues": self.issues,
            "warnings": self.warnings,
            "fixes_applied": self.fixes_applied,
            "summary": {
                "total_issues": len(self.issues),
                "total_warnings": len(self.warnings),
                "total_fixes": len(self.fixes_applied)
            }
        }
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
        print(f"\nDetailed report saved to: {report_path}")
        
    def run_all_checks(self):
        """Run all QA checks"""
        print("Starting Galaga QA Check...\n")
        
        self.check_file_structure()
        self.check_imports()
        self.check_sprite_coordinates()
        self.check_game_constants()
        self.check_collision_logic()
        self.check_state_transitions()
        self.check_enemy_behavior()
        self.check_resource_references()
        
        # Apply auto-fixes
        self.auto_fix_issues()
        
        # Generate report
        self.generate_report()
        
        # Return status code
        return 0 if len(self.issues) == 0 else 1


if __name__ == "__main__":
    checker = GalagaQAChecker()
    sys.exit(checker.run_all_checks())