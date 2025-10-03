# CS50’s Introduction to AI with Python

This project was completed as part of the course assignments.  
The following description is adapted from the original project specification.  

## Project 2: PageRank (Lecture 2 – Uncertainty)  

This project uses the PageRank’s algorithm to rank web pages by importance. 

To approximate this ranking, two approaches are implemented:

The first is the **Random Surfer Model**, which simulates a user navigating the web by randomly following links or occasionally jumping to a random page, controlled by a damping factor. Over many iterations, the frequency of visits to each page provides an estimate of its rank.

The second approach uses the **Iterative algorithm**, applying a mathematical formula to repeatedly update PageRank values until they converge. 


**Notes**
- The description above is adapted from the official project specification.
- Implemented using the course’s starter code, with modifications made to fulfill the project requirements.
- Completed as part of the CS50’s Introduction to AI with Python (2024 edition) coursework.


### How to Run

1. Run the program using the command `python pagerank.py [corpus]`, where `[corpus]` is the name of the directory containing the web pages to analyze and compute PageRanks for.
