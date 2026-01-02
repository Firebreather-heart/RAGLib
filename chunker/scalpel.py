from typing import List, Generator, Tuple
from string import whitespace, punctuation


STOPS = set(whitespace + punctuation )

def chunk_str(input_str:str, chunk_size:int, chunk_overlap:int)->List[str]:
    # Well we can't chunk strings less than the chunk size
    if len(input_str) < chunk_size:
        return [input_str, ]
    
    bucket = []

    while len(input_str) > 0:
        chunk, cut_off = clean_cut(input_str, chunk_size)
        bucket.append(chunk)
        chunk_cutoff = overlap_point(input_str[:cut_off], chunk_overlap)
        input_str = input_str[(len(chunk) - chunk_cutoff):]
    return bucket

def chunk_generator(input_str:str, chunk_size:int, chunk_overlap:int)->Generator[Tuple[str, int], None, None]:
    if len(input_str) < chunk_size:
        yield (input_str, 0)
        return

    while len(input_str) > 0:
        chunk, cut_off = clean_cut(input_str, chunk_size)
        chunk_cutoff = overlap_point(input_str[:cut_off], chunk_overlap)
        # input_str = input_str[(len(chunk) - chunk_cutoff):]
        yield chunk, chunk_cutoff

        step = len(chunk) - chunk_cutoff
        if step <= 0:
            step = 1
        input_str = input_str[step:]
    


def clean_cut(s:str, char_n:int)->tuple[str, int]:
    """Returns a tuple of the cut string and the index of cut-off"""
    if len(s) < char_n:
        return s,0
    buf = s[:char_n]

    idx = 0
    
    #check if the word was cut in half
    if s[char_n] not in STOPS:
        # then we cut it in half
        # move backwards till the next whitespace or punctuation
        idx = 0
        while s[char_n + idx] not in STOPS and (char_n + idx > 0):
            buf = buf[:-1]
            idx -= 1
    if len(buf) == 0: #massive word
        return s[:char_n], char_n
    return buf, char_n + idx


def overlap_point(s:str, char_n:int)->int:
    """Move until the overlap chunk is satisfied and returns the index
    The idx returned should be subtracted from the length of the
    input string"""
    s = s[::-1]
    if len(s) < char_n:
        return 0
    idx = 0
    for _ in range(char_n):
        idx += 1
    
    if s[char_n] not in STOPS:
        while s[idx] not in STOPS:
            idx += 1
    return idx


if __name__ == '__main__':
    TEST_STR = """
Akinrotimi Daniel Feyisola
Forward Deployed Engineer
dtenny95@gmail.com
+2349168700610
linkedin.com/in/daniel-akinrotimi-firebc
Lagos, NIgeria
github.com/firebreather-heart
https://firebdev.vercel.app
PROFILE
Results-oriented Forward Deployed Engineer with 5 years of experience architecting high-
performance backend systems and AI-powered data pipelines. Expert in Python, Data
Engineering, and GenAI, with a proven track record of building RAG architectures and
orchestrating complex integrations (LLMs, Slack, Google). Skilled in bridging the gap
between client data needs and scalable technical solutions using SQL, ETL workflows, and
Machine Learning models.
SKILLS
Programming Languages
Python(Expert), Javascript, Rust
Backend and Infrastructure
FastAPI, Django, PostgreSQL, Docker,
Redis, Kafka, RabbitMQ, Linux, Nginx,
CI/CD.
GenAI & Machine Learning:
GenAI Engineering, Microsoft AutoGen,
Retrieval-Augmented Generation (RAG),
LLM Orchestration, OpenAI API, Vector
Databases, TensorFlow, Scikit-learn.
Data Engineering
ETL Pipelines, Pandas, NumPy, Data
Cleaning & Normalization.
PROFESSIONAL EXPERIENCE
Worksage, Forward Deployed Backend Engineer
October 2025 – Present
I architected the backend infrastructure for a multi-agent orchestration platform,
integrating Microsoft AutoGen to enable autonomous agents.
I engineered real-time API connectors to securely fetch and structure live context from
Slack and Google, enabling agents to act on dynamic user data.
I implemented RAG (Retrieval-Augmented Generation) systems using FastAPI and
Vector Databases to ground LLM responses in user-specific context.
I also led the backend engineering and deployment strategy for the official MVP launch,
ensuring high availability and scalable architecture.
•
•
•
•
Starix, Lead Backend | Data Engineer
September 2025 – December 2025
Built a social media data ingestion pipeline to track creator performance across multiple
platforms (Instagram, Youtube, TikTok).
Implemented a custom scoring algorithm to normalize diverse engagement metrics into
a unified, fair leaderboard ranking.
•
•Architected a secure payout orchestration system, ensuring accurate financial
distribution to winners based on algorithmic results.
•
Glintplus, Backend Engineer
May 2024 – January 2025
Architected and implemented scalable RESTful APIs using Django Rest Framework,
supporting 300+ active users.
Optimized SQL queries and database indexing, reducing response times for data-heavy
research endpoints.
Led DevOps automation for server provisioning, improving deployment reliability using
Linux and Nginx.
•
•
•
Freelance, Software Engineer
2021 – 2023
Delivered full-stack web solutions for diverse clients, managing the entire lifecycle from
requirement gathering to deployment.
•
RELEVANT EXPERIENCE
Team Lead, Nuesa Tech Community, Funaab.
May 2023 – December 2024
Co-founded the NUESA Tech Community at FUNAAB, fostering a collaborative
ecosystem for engineering students.
Led planning and execution of internship and upskilling initiatives, connecting 50+
students to real-world opportunities.
Established an internship forum and curated monthly tech talks, encouraging peer-
driven learning and industry collaboration.
•
•
•
Web Backend Development Instructor,
May 2023 – December 2024
NUTEC funaab
Designed and delivered an intensive web backend curriculum covering Python, Bash
scripting, and Git/version control.
Mentored 30+ students through project-based learning, guiding them from basic
scripting to deploying backend APIs.
Simplified complex backend concepts (e.g., routing, authentication, database models) to
support learners of diverse backgrounds.
Facilitated hands-on sessions, enabling students to build and deploy real-world
backend services.
•
•
•
•
CERTIFICATES
Software Engineering
Alx Africa
PROJECTS
FireAutoML
Automated Machine Learning & ETL Library | Python, Pandas, Scikit-learn, Flask
Engineered a configurable ETL pipeline that automates data cleaning, feature
normalization, and categorical encoding, explicitly handling class imbalance via
SMOTE/ADASYN strategies before model training.
Architected a dual-interface system (CLI & REST API) that exposes the full ML lifecycle
—from data ingestion to model serialization—allowing backend systems to trigger
training jobs programmatically.
•
•Implemented an automated reporting engine (ModelEvaluator) that generates self-
contained HTML reports with embedded ROC curves and confusion matrices, enabling
immediate visual assessment of model performance.
•
Swiftdeploy
Model-to-Web Serving Framework | Python, Flask, Jinja2
Built a dynamic HTML generation engine (MarkupModel) that parses Python
dictionaries to algorithmically construct semantic HTML5 forms, effectively abstracting
the frontend layer for ML engineers.
Developed a generic Flask wrapper that dynamically routes requests to arbitrary model
inference functions, enforcing strict input validation based on the model's defined
schema before execution.
•
•
Shinzoku
High-Performance Rust Backend Tools: Rust, Solana SDK, Next.js
Engineered a low-latency game backend using Rust, optimizing memory safety and
execution speed for a Web3 PvP auto-battler.
Integrated Solana wallet authentication and handled complex state management for
dynamic character systems.
•
•
EDUCATION
Mechatronics Engineering,
Federal university of Agriculture Abeokuta
Software Engineering, ALX Africa
January 2021 – May 2025
January 2023 – March 2024
"""

    chunks = chunk_str(TEST_STR,250, 30)
    for i in chunks:
        print(i, '\n\n\n')