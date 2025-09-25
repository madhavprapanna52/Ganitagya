# Ganitagya
An tool for student to learn math in whole different way, Exploring topic asking intuative questions thinking beyond horizon making them crtitical thinkers not just rote learners

Features 
    1. Making source grounded LLM for being context aware and accurate by using multiple pipelines and references using RAG model for effective LLM orchistration
    2. Manimation abstraction layer 
        ~ Featuring a tool that LLM / custom NLP pipeline would use for making Animation out of texts and equation
    3. State of art next gen Quiz generation and validation platform that makes quiz which tests user on pain points and thinking behaviour making them good thinker not rote learner , evaluation enigne would be different from treditional for scoring


## Main challenges in project

+ Making sources contexting and validation pipeline for LLM anchor to the topic user is learning,
+ Making generalised Manim abstraction layer for LLM to make video and be creative with along with being less depended on LLM for generating the output of animation such that fallback logic can also work with

+ their are many to note ..


## Project structure : Ganitagya

.
├── app.py
├── CORE-Engine
│   └── Animation  # Making animation abstraction layer
│       ├── animation.py  
│       └── __pycache__
│           └── animation.cpython-311.pyc
├── launching_bash.sh # Bash automation scripts 
├── README.md  # main core planning
├── requirements.txt  # listing dependencies
├── static  # The base loading resources
│   ├── css
│   │   ├── style2.css
│   │   └── style.css
│   ├── js
│   │   └── script.js
│   └── MathVideoScene.mp4
└── templates # Front end structure
    ├── base.html
    ├── home.html
    ├── index.html
    ├── login.html
    ├── playground.html
    └── register.html
