1. The Two Types of Stages

Galaga's progression is built around a repeating cycle of two distinct types of stages:
* Standard Combat Stages: These are the primary levels (like Stages 1 and 2) where your goal is to destroy waves of enemies that fly into a formation and then break off to attack you. Your ship can be destroyed in these stages.
* Challenging Stages (Bonus Rounds): These are risk-free bonus rounds (starting with Stage 3) where enemies fly in elaborate, preset patterns without shooting. Your goal is to destroy all 40 enemies for a 10,000-point "PERFECT" bonus. You cannot be destroyed in these stages.


2. The Stage Progression Cycle

The game follows a predictable pattern of combat and bonus rounds. The first Challenging Stage is Level 3, and a new one appears every four stages after that.
The initial cycle looks like this:
Stage Number	Stage Type	Key Characteristics
1	Standard Combat	Introductory formation pattern.
2	Standard Combat	More complex entry formation.
3	Challenging Stage	First Bonus Round.
4	Standard Combat	New entry formation.
5	Standard Combat	New entry formation.
6	Standard Combat	New entry formation.
7	Challenging Stage	Second Bonus Round.
8	Standard Combat	New entry formation.
9	Standard Combat	New entry formation.
10	Standard Combat	New entry formation.
11	Challenging Stage	Third Bonus Round.
...	...	...and so on.

3. Stage Looping and Difficulty Scaling

Galaga does not have an infinite number of unique level designs. Instead, it cycles through a set of pre-designed entry formations and Challenging Stage patterns. However, the game continues to get harder in several key ways:

Stage Pattern Repetition

The entry formations from the early levels begin to repeat in later stages. For example, the pattern you see in Stage 1 will reappear in a later stage, but with a significant increase in difficulty.

How Difficulty Increases

1. Increased Speed: This is the most noticeable change. As you advance, the enemies fly faster during both their entry formations and their attack dives, giving you less time to react and shoot.
2. Increased Firing Rate: Enemies fire their missiles more frequently. In later stages, the screen can quickly fill with enemy projectiles, requiring constant dodging.
3. Elimination of Pauses: In the very early stages, there is a brief moment of calm after all enemies have assembled into the formation before they begin their attack dives. After the first few loops, this pause is completely eliminated. The moment the last alien settles into its spot, another one immediately breaks off to attack. This creates a relentless, non-stop pace of action.


4. The "Kill Screen": Stage 256

Like many classic arcade games of its era, Galaga was not designed to be played forever. The game has a definitive, unbeatable end due to a programming bug.
* What it is: Stage 256 is the final level of the game, commonly referred to as the "kill screen."
* Why it happens: The game's level counter was stored in a single 8-bit byte of memory. An 8-bit byte can only hold values from 0 to 255. When the game tries to advance from Stage 255 to Stage 256, the byte "overflows" and wraps around to 0. The game attempts to load data for "Stage 0," which doesn't exist.
* What you see: The right side of the screen becomes a garbled mess of sprites and random text from the game's memory. The game freezes or crashes, making it impossible to continue. Reaching this screen is the ultimate goal for score-chasing masters of the game, as it signifies the end of a complete run.


###
Galaga - Level 1 Spec

This document outlines the enemy behaviors, formations, attack patterns, and scoring for the first level of the original Galaga arcade game.


1. Level Overview

Level 1, also known as Stage 1, introduces the player to all three standard enemy types and their fundamental behaviors. The level consists of two primary phases: the Formation Entry Phase, where enemies fly onto the screen in choreographed patterns to assemble into a static formation, and the In-Formation Attack Phase, where they break off from the formation to attack the player's ship. Enemies do not fire at the player while in their entry patterns.


2. Enemy Roster

Enemy Type	Image (Sprite)	Formation Position	Behavior & Notes
Bee (Zako)	🐝	Bottom two rows	The most common enemy. Dives straight down or at a slight angle, firing a single missile.
Butterfly (Goei)	🦋	Middle two rows	More agile than the Bee. Dives in a looping or twisting pattern, firing a single missile. Often acts as an escort for a Boss Galaga.
Boss Galaga (Bosconian)	👾	Top row	The most dangerous enemy. Can dive alone or with two Butterfly escorts. On a second dive, it can use a tractor beam to capture the player's fighter.

3. Phase 1: Formation Entry

A total of 40 enemies arrive in 6 distinct groups to form the final 5x8 grid.
* Group 1: Boss & Escorts (Left)
    * Units: 1x Boss Galaga, 2x Butterflies.
    * Path: Enters from the top-left of the screen, performs a wide clockwise loop, and settles into the top-right and second-from-top-right positions in the formation.
* Group 2: Boss & Escorts (Right)
    * Units: 1x Boss Galaga, 2x Butterflies.
    * Path: Mirrors Group 1. Enters from the top-right, performs a counter-clockwise loop, and settles into the top-left and second-from-top-left positions.
* Group 3: Bee Squadron (Left)
    * Units: 8x Bees.
    * Path: Enters from the top-left corner, flies down towards the center, then banks right to fill the two bottom-right rows of the formation.
* Group 4: Bee Squadron (Right)
    * Units: 8x Bees.
    * Path: Mirrors Group 3. Enters from the top-right corner, flies down towards the center, then banks left to fill the two bottom-left rows of the formation.
* Group 5: Butterfly Squadron (Looping)
    * Units: 8x Butterflies.
    * Path: Enters in a single file line from a spawn point off-screen to the left of the player's ship. They fly up and to the right, then loop back left to fill the two middle-left rows of the formation.
* Group 6: Final Bosses
    * Units: 4x Boss Galagas.
    * Path: Enter from the top of the screen in two pairs. They fly straight down to fill the remaining empty spots in the center of the top row.


4. Phase 2: In-Formation Attack

Once all 40 enemies are in formation, they begin to attack.
* Standard Dive: Enemies peel off from the formation one or two at a time, dive towards the player, and fire a single shot.
    * Bees typically dive straight down or at a shallow angle.
    * Butterflies perform more complex, looping dives.
* Boss Galaga Dive:
    * A Boss Galaga can dive alone, firing a standard shot.
    * It can also dive with one or two Butterfly escorts. The escorts will follow its path closely.
* Tractor Beam Attack:
    * A Boss Galaga on a solo dive (without escorts) may stop its descent partway down the screen and emit a blue, conical tractor beam.
    * If the player's fighter is caught in this beam, it is captured and sits beneath the Boss Galaga at the top of the formation. The player loses a life but can continue playing with their next ship.
* Captured Fighter Dynamic:
    * The Boss Galaga holding the captured fighter will eventually dive again, with the captured fighter in tow.
    * During this dive, both the Boss and the captured fighter will shoot at the player.
    * Rescue Opportunity: If the player destroys the diving Boss Galaga without hitting the captured fighter, the fighter is rescued. It will return to the player's position and combine with the current ship, creating a dual fighter with double the firepower.
    * Losing the Fighter: If the player accidentally destroys the captured fighter, it is lost permanently for that level. Destroying the Boss afterwards yields standard points.


5. Scoring Dynamics

Points awarded depend on the enemy's state (in formation or diving).
Action	Enemy	State	Points Awarded	Notes
Destroy	Bee	In Formation	50	
Destroy	Bee	Diving	100	
Destroy	Butterfly	In Formation	80	
Destroy	Butterfly	Diving	160	
Destroy	Boss Galaga	In Formation	150	
Destroy	Boss Galaga	Diving	400	This is for a standard dive.
Destroy	Boss Galaga	Diving with escorts	800 - 1600	Score varies. 800 for the Boss alone, plus 160 for each diving escort.
Destroy	Boss Galaga	Diving with captured fighter	1000	For destroying the Boss Galaga only, which frees the captured fighter.
Bonus	Dual Fighter	Formation	0	No points awarded, but a significant tactical advantage.

##########
Galaga - Level 2 Spec

This document outlines the enemy behaviors, formations, attack patterns, and scoring for the second level of the original Galaga arcade game.


1. Level Overview

Level 2, or Stage 2, uses the same set of enemies as the first level but introduces entirely new, more complex entry patterns. The general difficulty increases, with enemies breaking from the final formation to attack more frequently and aggressively than in Stage 1.


2. Enemy Roster

The enemy types and their base characteristics remain identical to Level 1.
Enemy Type	Image (Sprite)	Formation Position	Behavior & Notes
Bee (Zako)	🐝	Bottom two rows	The most common enemy. Dives straight down or at a slight angle, firing a single missile.
Butterfly (Goei)	🦋	Middle two rows	More agile than the Bee. Dives in a looping or twisting pattern, firing a single missile. Often acts as an escort for a Boss Galaga.
Boss Galaga (Bosconian)	👾	Top row	The most dangerous enemy. Can dive alone or with two Butterfly escorts. On a second dive, it can use a tractor beam to capture the player's fighter.

3. Phase 1: Formation Entry

A total of 40 enemies arrive in 5 distinct groups to form the final 5x8 grid. The entry paths are unique to this stage. Enemies do not fire at the player during this phase.
* Group 1: Bee Squadron (Left)
    * Units: 8x Bees.
    * Path: Enters from the bottom-left corner of the screen, flies up the left edge, performs a tight clockwise turn at the top, and files into the two bottom-left rows of the formation.
* Group 2: Bee Squadron (Right)
    * Units: 8x Bees.
    * Path: Mirrors Group 1. Enters from the bottom-right corner, flies up the right edge, performs a tight counter-clockwise turn, and files into the two bottom-right rows.
* Group 3: Butterfly Squadron (Left)
    * Units: 8x Butterflies.
    * Path: Enters from the top-left, flies down towards the center, then executes a sharp counter-clockwise loop to fill the two middle-left rows of the formation from the outside in.
* Group 4: Butterfly Squadron (Right)
    * Units: 8x Butterflies.
    * Path: Mirrors Group 3. Enters from the top-right, flies down towards the center, then executes a sharp clockwise loop to fill the two middle-right rows.
* Group 5: The Bosses
    * Units: 4x Boss Galagas.
    * Path: All four enter from the top-center in a single file line. They fly about halfway down the screen, then split into two pairs. The left pair loops out to the left and back to the center, while the right pair loops out to the right and back. They then settle into the four centermost positions of the top row.


4. Phase 2: In-Formation Attack

The attack phase mechanics are fundamentally the same as Level 1, but with increased intensity.
* Increased Aggression: Enemies break from formation to attack more quickly and often in larger groups (e.g., trios). The time between attack waves is shorter.
* Standard Dive: Bees and Butterflies peel off to attack the player, firing single shots. Their dive patterns are the same, but the overall pace is faster.
* Boss Galaga Dive: The Boss Galaga's behavior is consistent with Level 1. It can dive alone, with escorts, or perform a tractor beam attack.
* Tractor Beam & Rescue: The tractor beam mechanic and the ability to rescue a captured fighter to form a dual fighter remain unchanged. The increased number of enemies attacking simultaneously can make the rescue attempt more hazardous.


5. Scoring Dynamics

The point values for all enemy interactions are identical to Level 1.
Action	Enemy	State	Points Awarded	Notes
Destroy	Bee	In Formation	50	
Destroy	Bee	Diving	100	
Destroy	Butterfly	In Formation	80	
Destroy	Butterfly	Diving	160	
Destroy	Boss Galaga	In Formation	150	
Destroy	Boss Galaga	Diving	400	This is for a standard dive.
Destroy	Boss Galaga	Diving with escorts	800 - 1600	Score varies. 800 for the Boss alone, plus 160 for each diving escort.
Destroy	Boss Galaga	Diving with captured fighter	1000	For destroying the Boss Galaga only, which frees the captured fighter.
Bonus	Dual Fighter	Formation	0	No points awarded, but a significant tactical advantage.

####
Stage 3 - Challenge

Challenging stage 1 (level 3)

——————————

Of course. Here are the detailed instructions for Galaga's Level 3, the first Challenging Stage.


Galaga - Level 3 Spec (Challenging Stage 1)

This document outlines the enemy behaviors, flight patterns, and scoring for the third level of Galaga. This stage is a special bonus round with unique rules.


1. Level Overview

Level 3 is the first Challenging Stage. The gameplay changes significantly:
* No Player Risk: The enemies fly across the screen in fixed patterns but do not shoot at the player's ship, nor can they collide with it. The player cannot be destroyed.
* No Tractor Beams: The Boss Galaga's tractor beam ability is disabled during this stage.
* Objective: The goal is to destroy all 40 incoming enemies before they fly off-screen.
* Bonus Reward: Destroying all 40 enemies awards a large point bonus.


2. Enemy Roster

While the same enemy sprites are used, their roles are reduced to targets in pre-determined flight paths.
Enemy Type	Image (Sprite)	Role in this Stage
Bee (Zako)	🐝	Appears in various waves as a standard target.
Butterfly (Goei)	🦋	Appears in various waves as a standard target.
Boss Galaga (Bosconian)	👾	Appears as a high-value target in the final wave.

3. Gameplay: Flight Patterns

The 40 enemies arrive in 5 distinct waves of 8. The player must anticipate these patterns to achieve a perfect clear.
* Wave 1: Left-Side Weave
    * Units: 8 enemies (mix of Bees/Butterflies).
    * Path: Enters from the top-left corner, flies down the left side of the screen, crosses over to the right at the bottom, and flies up the right side before exiting off the top-right.
* Wave 2: Right-Side Weave
    * Units: 8 enemies (mix of Bees/Butterflies).
    * Path: Mirrors Wave 1. Enters from the top-right, flies down the right side, crosses left at the bottom, and exits off the top-left.
* Wave 3: Center Loop (Left Group)
    * Units: 8 enemies (mix of Bees/Butterflies). This wave is complex and arrives in two sub-groups.
    * Path (Sub-group 1): Four enemies enter from the top-center, peel off to the left, and perform a large, counter-clockwise loop in the upper-left quadrant of the screen before exiting off the top.
* Wave 4: Center Loop (Right Group)
    * Units: This is the second half of the previous group of 8 enemies.
    * Path (Sub-group 2): The other four enemies from the center entry peel off to the right, mirroring the previous group. They perform a large, clockwise loop in the upper-right quadrant and exit off the top.
* Wave 5: Boss Galaga Escort
    * Units: 8 enemies (2x Boss Galagas, 6x Butterflies).
    * Path: Arrives in two columns of four from the top-left and top-right. They fly downwards, converging slightly towards the center before flying off the bottom of the screen. The Boss Galagas are the trailing enemies in each column, making them the last targets to appear.


4. Scoring Dynamics

Scoring in a Challenging Stage is simplified and focuses on the completion bonus. The "diving" multiplier does not apply.
Action	Enemy	Points Awarded	Notes
Destroy	Bee or Butterfly	100	The point value is static for these enemies.
Destroy	Boss Galaga	200	
Destroy	All 40 Enemies	10,000	A "PERFECT" bonus awarded at the end of the stage.
	•	No Partial Bonus: There is no bonus for destroying a high percentage of enemies; the 10,000 points are only awarded for a perfect 40/40 clear.
* End-of-Stage Stats: After the stage, the game displays the number of hits and shots fired, along with the player's hit percentage. This does not affect scoring but provides performance feedback.
