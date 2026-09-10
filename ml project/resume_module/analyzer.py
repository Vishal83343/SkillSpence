skills_list = [
    "python", "java", "c++", "c", "sql",
    "excel", "power bi", "tableau",
    "machine learning", "deep learning",
    "artificial intelligence", "data analysis",
    "data science", "statistics",
    "numpy", "pandas", "matplotlib",
    "seaborn", "scikit-learn",
    "html", "css", "javascript",
    "react", "node.js", "express",
    "mongodb", "mysql", "postgresql",
    "git", "github",
    "linux", "aws", "docker",
    "kubernetes", "api", "rest api",
    "oop", "data structures", "algorithms",
    "dbms", "operating system",
    "computer networks", "communication"
]


def extract_skills(text):
    text = text.lower()
    found = []

    for skill in skills_list:
        if skill in text:
            found.append(skill)

    return found


def missing_skills(found):
    return [skill for skill in skills_list if skill not in found]


def calculate_score(text, skills):
    text = text.lower()

    score = 0

    # Skill Score (Max 50)
    score += min(len(skills) * 10, 50)

    # Keyword Score (Max 30)
    keywords = [
        "project",
        "experience",
        "internship",
        "development"
    ]

    for word in keywords:
        if word in text:
            score += 7

    # Resume Length Score (Max 20)
    if len(text) > 1000:
        score += 20
    elif len(text) > 500:
        score += 10

    return min(score, 100)

def recommend_courses(missing_skills):

    course_map = {

        "python": [
            ("🐍 freeCodeCamp Python", "https://www.freecodecamp.org/learn/"),
            ("🎓 Coursera Python", "https://www.coursera.org/search?query=python"),
            ("📺 Python Full Course", "https://www.youtube.com/results?search_query=python+full+course")
        ],

        "java": [
            ("☕ Java Programming", "https://www.udemy.com/course/java-the-complete-java-developer-course/"),
            ("📘 W3Schools Java", "https://www.w3schools.com/java/"),
            ("📺 Java Full Course", "https://www.youtube.com/results?search_query=java+full+course")
        ],

        "c++": [
            ("💻 LearnCpp", "https://www.learncpp.com/"),
            ("📘 GeeksforGeeks C++", "https://www.geeksforgeeks.org/c-plus-plus/"),
            ("📺 C++ Full Course", "https://www.youtube.com/results?search_query=c%2B%2B+full+course")
        ],

        "sql": [
            ("🗄 SQLBolt", "https://sqlbolt.com/"),
            ("🎓 Coursera SQL", "https://www.coursera.org/learn/sql-for-data-science"),
            ("📘 W3Schools SQL", "https://www.w3schools.com/sql/")
        ],

        "excel": [
            ("📊 Microsoft Learn Excel", "https://learn.microsoft.com/"),
            ("🎓 Excel Course", "https://www.udemy.com/course/microsoft-excel-course/"),
            ("📺 Excel Full Course", "https://www.youtube.com/results?search_query=excel+full+course")
        ],

        "power bi": [
            ("📊 Microsoft Learn Power BI", "https://learn.microsoft.com/en-us/training/powerplatform/power-bi/"),
            ("🎓 Coursera Power BI", "https://www.coursera.org/search?query=power+bi"),
            ("📺 Power BI YouTube", "https://www.youtube.com/results?search_query=power+bi+full+course")
        ],

        "machine learning": [
            ("🤖 Andrew Ng ML", "https://www.coursera.org/learn/machine-learning"),
            ("📘 Kaggle Learn", "https://www.kaggle.com/learn"),
            ("📺 ML Full Course", "https://www.youtube.com/results?search_query=machine+learning+full+course")
        ],

        "data analysis": [
            ("📈 Google Data Analytics", "https://www.coursera.org/professional-certificates/google-data-analytics"),
            ("📘 Kaggle Data Analysis", "https://www.kaggle.com/learn"),
            ("📺 Data Analysis Course", "https://www.youtube.com/results?search_query=data+analysis+full+course")
        ],

        "html": [
            ("🌐 freeCodeCamp HTML", "https://www.freecodecamp.org/learn/responsive-web-design/"),
            ("📘 W3Schools HTML", "https://www.w3schools.com/html/"),
            ("📺 HTML Full Course", "https://www.youtube.com/results?search_query=html+full+course")
        ],

        "css": [
            ("🎨 freeCodeCamp CSS", "https://www.freecodecamp.org/learn/responsive-web-design/"),
            ("📘 W3Schools CSS", "https://www.w3schools.com/css/"),
            ("📺 CSS Full Course", "https://www.youtube.com/results?search_query=css+full+course")
        ],

        "javascript": [
            ("⚡ freeCodeCamp JavaScript", "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/"),
            ("📘 JavaScript.info", "https://javascript.info/"),
            ("📺 JavaScript Full Course", "https://www.youtube.com/results?search_query=javascript+full+course")
        ],

        "react": [
            ("⚛ React Docs", "https://react.dev/learn"),
            ("🎓 Coursera React", "https://www.coursera.org/search?query=react"),
            ("📺 React Full Course", "https://www.youtube.com/results?search_query=react+full+course")
        ],

        "git": [
            ("🐙 Git Handbook", "https://guides.github.com/"),
            ("📘 Atlassian Git", "https://www.atlassian.com/git/tutorials"),
            ("📺 Git & GitHub", "https://www.youtube.com/results?search_query=git+github+full+course")
        ]
    }

    recommendations = []

    for skill in missing_skills:

        skill = skill.lower().strip()

        if skill in course_map:

            recommendations.append({
                "skill": skill,
                "courses": course_map[skill]
            })

        else:

            recommendations.append({
                "skill": skill,
                "courses": [
                    (
                        f"🔍 Learn {skill.title()}",
                        f"https://www.google.com/search?q=learn+{skill.replace(' ','+')}"
                    )
                ]
            })

    return recommendations