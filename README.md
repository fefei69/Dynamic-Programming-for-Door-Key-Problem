# ECE276B SP24 Project 1

## Overview
This project focuses on autonomous navigation in a
Door & Key environment. The objective is to get our agent to the
goal location. The environment may contain a door which blocks
the way to the goal. If the door is closed, the agent needs to
pick up a key to unlock the door. 

In the first part of the project, we will perform
Dynamic Programming algorithm 7 times for 7 different
known environments that the position of key, door and goal
are known. We will have 7 different optimal policy for 7
different environments. 

In the second part of the project, we
will perform a single Dynamic Programming algorithm for 36
random environments that have several possible key, door and
goal position, etc. By expanding the state space, the algorithm
can encompass all possible variations or configurations within
the environments, ensuring that it captures every potential
scenario or possibility.
[Report of the project](https://drive.google.com/file/d/1gGTy6aJvMT_aJA7Lo34wo0f0j_Yyy1Jp/view?usp=sharing)
<p align="center">
<img src="results/partA/doorkey-5x5-normal.gif" alt="Door-key Problem" width="200"/></br>
</p>

There are 7 test scenes you have to test and include in the report.

|           doorkey-5x5-normal            |
| :-------------------------------------: |
| <img src="results/partA/doorkey-5x5-normal.gif"> |

|           doorkey-6x6-normal            |            doorkey-6x6-direct            |            doorkey-6x6-shortcut            |
| :-------------------------------------: | :--------------------------------------: | :----------------------------------------: |
| <img src="results/partA/doorkey-6x6-normal.gif"> | <img src="results/partA/doorkey-6x6-direct.gif" > | <img src="results/partA/doorkey-6x6-shortcut.gif" > |

|           doorkey-8x8-normal            |            doorkey-8x8-direct            |            doorkey-8x8-shortcut            |
| :-------------------------------------: | :--------------------------------------: | :----------------------------------------: |
| <img src="results/partA/doorkey-8x8-normal.gif"> | <img src="results/partA/doorkey-8x8-direct.gif" > | <img src="results/partA/doorkey-8x8-shortcut.gif" > |

# How to use
## Known Environments (Part A)
```
python doorkey_parta.py
```

## Random Environments (Part B)
```
python doorkey_partb.py
```



