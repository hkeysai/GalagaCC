Project requirements document (PRD) for a Galaga clone in Python
1. Introduction
This document outlines the requirements for developing a Galaga clone in Python, utilizing the Pygame library. The project aims to recreate the classic arcade game experience with faithful mechanics, visuals, and audio.
1.1 Purpose
The primary purpose of this project is to provide a fun and engaging retro gaming experience for players while serving as a practical exercise in game development using Python and Pygame.
1.2 Scope
This project will focus on recreating the core gameplay loop of Galaga, including the player's spaceship, alien enemies, projectiles, scoring, and the iconic "Challenge Stage". Key features include:
Player spaceship movement and shooting.
Waves of enemies with distinct movement patterns.
Collision detection and scoring.
Recapture mechanic and dual-fighter mode.
Bonus stages (Challenging Stages).
High score tracking.
Basic sound effects from the original game.
Windowed and optional fullscreen mode.
1.3 Target audience
Players who enjoy classic arcade games and are familiar with the original Galaga.
2. Gameplay
2.1 Player control
Movement: Left and right arrow keys control the player's spaceship movement along the bottom of the screen.
Shooting: The spacebar fires projectiles from the player's ship.
2.2 Enemy behavior
Enemies will spawn in waves and fly in predefined patterns towards the player.
Individual enemies will break formation and dive-bomb the player, firing projectiles.
Boss Galaga enemies can capture the player's ship with a tractor beam, resulting in a lost life.
Destroying a Boss Galaga holding a captured ship will rescue the ship and activate dual-fighter mode, doubling the player's firepower.
Destroying a Boss Galaga with a captured ship while in formation will cause the captured ship to turn against the player.
2.3 Levels and stages
The game will progress through multiple stages with increasing difficulty.
Challenging Stages will appear periodically, offering bonus points for destroying all enemies.
3. Graphics and visuals
All game elements, including the player's ship, enemies, and projectiles, will be represented by animated sprites.
Visual effects such as explosions and the tractor beam will be included.
4. Audio
The game will feature sound effects resembling the original Galaga, including firing, explosions, and the signature Challenge Stage music.
5. Scoring and high scores
Points will be awarded for destroying enemies.
Bonus points will be awarded for completing Challenging Stages.
The game will track and display the highest score achieved.
6. Technical requirements
Programming Language: Python
Game Development Library: Pygame
Operating System: Cross-platform compatibility (Windows, macOS, Linux)
Version Control: Git & GitHub
7. Future considerations (potential enhancements)
Different enemy types with unique attack patterns.
Power-ups for the player's ship.
Multiple boss encounters.
Online leaderboards to compete with other players.
Improved sound and visual effects.
This PRD provides a comprehensive overview of the requirements for developing a Galaga clone in Python. It serves as a guide for the development process, ensuring all key features and functionalities are included, and sets the stage for a fun and engaging retro gaming experience.
Implementation of enemy AI and movement patterns in Pygame
1. Core concepts
Pattern Movement: Galaga enemies do not exhibit complex artificial intelligence, but instead rely on pre-defined "pattern movement algorithms" that create the illusion of intelligent behavior.
Sprite Groups: Pygame's SpriteGroup class offers a convenient way to manage groups of enemies, making tasks like drawing and collision detection more efficient.
Modular Design: Breaking down the enemy AI into separate functions or classes (e.g., enemy class, bullet class) improves code organization and readability. 
2. Enemy movement patterns
Arrival in formation:
Enemies enter the screen following "incoming trajectories" (likely pre-computed paths stored as lists of x, y coordinates or mathematical functions).
Each enemy has a designated "terminal position" within the formation.
Enemies follow their trajectory until a designated endpoint, then move towards their final formation position.
Dive-bombing attacks:
Some enemies will break formation and dive toward the player, employing patterns that involve loops and turns while firing projectiles.
These patterns could be implemented using pre-defined sequences of movements or calculations based on the player's position, potentially using techniques like stitching together elliptical arcs to create smooth curves.
Boss Galaga behavior:
Boss Galagas can utilize a tractor beam to capture the player's ship.
Their movement patterns involve looping maneuvers before diving toward the player.
Boss Galagas might exhibit additional behaviors depending on whether a player's ship is captured or if the formation has been broken up.
Challenging Stages:
During Challenging Stages, enemies follow complex, elaborate patterns but do not fire, offering a bonus opportunity for players who manage to shoot them down. 
3. Enemy AI implementation
Enemy Class: Create a class to represent individual enemies, managing properties like position, movement speed, and health.
State Machine: Consider implementing a simple state machine to manage enemy behavior (e.g., 'Formation', 'Diving', 'Captured'), switching between states based on game conditions.
Projectile Handling:
Enemies fire projectiles that move towards the player.
Use a Pygame timer to control the firing rate.
Calculate the projectile's trajectory to ensure it travels in a straight line toward the player's position. 
4. Collision detection and interactions
Pygame's SpriteGroup.groupcollide: This function simplifies collision detection between enemies and projectiles.
Player-enemy collisions: Handle interactions when enemies collide with the player's ship, possibly reducing player health or triggering a game-over state.
Enemy-environment collisions: Ensure enemies do not move outside the screen boundaries, either by bouncing back or disappearing and reappearing from the other side, depending on the desired behavior. 
5. Techniques for implementing movement
Pre-computed Paths: For complex maneuvers, especially formation-based ones, pre-computing and storing enemy movement paths as lists of coordinates can be a viable approach, especially for the original Galaga's era.
Mathematical Functions: Utilizing mathematical functions like Bézier curves can offer smoother, more flexible movement compared to pre-computed paths alone, according to a resource from Better Programming.
Acceleration and Speed Modification: Adjusting enemy movement speed and acceleration (horizontally and vertically) can create a variety of attack profiles, allowing for more dynamic movement patterns. 
By employing these techniques, you can effectively implement engaging enemy AI and recreate the iconic movement patterns of Galaga within your Pygame project.
Detailed breakdown of Galaga levels and challenges
Galaga features a progression of stages that cycle endlessly, with increasing difficulty and unique elements introduced at various points. The game effectively uses a repeating set of "levels" with dynamic adjustments and distinct bonus stages.
1. Enemy types and behavior
Zako (Blue & Yellow Bee-like):
Most common enemy type.
Formation Movement: Fly into formation from the sides of the screen.
Attack Patterns: Dive-bomb the player, sometimes looping from the bottom of the screen to attempt attacks from below.
Scoring: 50 points in formation, 100 points while attacking.
Goei (Red & White Butterfly-like):
Escort units for Boss Galaga.
Formation Movement: Also enter in formation, similar to Zakos.
Attack Patterns: They may make feints during attack runs, creating a challenge in differentiating between real and fake attacks.
Scoring: 80 points in formation, 160 points while attacking.
Boss Galaga (Large, Green to Purple):
Take two hits to destroy; change color to purple on the first hit.
Can use a "tractor beam" to capture the player's ship.
Capture Mechanic: If the player's ship is captured, the Boss Galaga carries it to the top of the screen. The player can then free the captured ship by destroying the Boss Galaga holding it, leading to a dual-fighter mode.
Dual-Fighter Mode: Offers double firepower but increases the player's ship size, making it harder to dodge enemy attacks.
Escorts: Boss Galaga may be accompanied by one or two Goei escorts.
Scoring: 150 points in formation, 400 points in flight (no escorts), 800 points with one escort, 1,600 points with two escorts.
2. Challenging stages
Frequency: Occur every fourth stage, starting with the third stage (stages 3, 7, 11, etc.).
Gameplay: Enemies do not attack or form a formation; instead, they fly across the screen in various pre-determined patterns, functioning like a shooting gallery.
Bonus Points:
100 points for each enemy destroyed.
10,000 points bonus for destroying all 40 enemies in a Challenging Stage.
Enemy Variety: Each challenging stage features a specific enemy type (e.g., Zakos in the first, Goeis in the second) along with four Boss Galaga. There are eight distinct Challenging Stages in total.
Looping: After Stage 31, the challenging stages repeat in the same order.
3. Difficulty progression
Enemy Firing Rate: Increases as the player progresses through the stages, leading to more intense enemy attacks.
Enemy Movement Speed: Enemies might become faster and execute more erratic maneuvers in later stages.
Special Attacks: In later stages, some enemies might exhibit new or more complex attack patterns, and some may split into multiple foes, creating additional challenges.
Game Looping: The game can theoretically continue indefinitely with increasingly difficult levels, repeating a set of stages with variations in enemy behavior and difficulty.
4. Key details for reproduction
Precise Enemy Movement Trajectories: The exact movement patterns of enemies, especially their entrance and attack dives, are crucial. These patterns are not random but deterministic, following a set of rules that players can learn to predict.
Boss Galaga Capture Mechanic: The timing and conditions for the tractor beam's activation, the trajectory of the Boss Galaga during the capture sequence, and the behavior of the captured ship are important elements to recreate accurately.
Dual-Fighter Mode: The implementation of the dual-fighter's mechanics, including its increased firepower, larger size, and how it responds to hits, should be replicated carefully.
Challenging Stage Patterns: Each of the eight challenging stages has unique enemy patterns that need to be reproduced precisely for an authentic experience.
Enemy Spawn Points and Timers: The timing and locations where enemies appear and transition from formation to attack are integral to the game's flow and difficulty.
By meticulously recreating these elements, a full stack developer can successfully capture the essence and precision of the original Galaga, providing a true classic arcade gaming experience.