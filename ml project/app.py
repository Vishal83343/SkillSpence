import streamlit as st
import matplotlib.pyplot as plt

import pandas as pd
import streamlit as st
import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(total, week_total, waste, learning, score):
    doc = SimpleDocTemplate("expense_report.pdf")
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("Smart Expense Report", styles["Title"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"Total Spending: ₹{total}", styles["Normal"]))
    content.append(Paragraph(f"Weekly Spending: ₹{week_total}", styles["Normal"]))
    content.append(Paragraph(f"Waste: ₹{waste}", styles["Normal"]))
    content.append(Paragraph(f"Learning: ₹{learning}", styles["Normal"]))
    content.append(Paragraph(f"Financial Score: {score}", styles["Normal"]))

    doc.build(content)

def auto_category(reason):
    reason = reason.lower()

    category_keywords = {
        "food": ["pizza","burger","food","lunch","dinner","snack","restaurant","zomato","swiggy","chai","coffee"],
        "travel": ["uber","ola","auto","bus","train","flight","petrol","cab","metro"],
        "course": ["course","udemy","coursera","book","learning","class","training","python","sql"],
        "shopping": ["shopping","shirt","jeans","clothes","amazon","flipkart","buy","shoes"],
        "entertainment": ["movie","netflix","game","party","music"],
        "health": ["doctor","medicine","gym","health","protein"],
        "bills": ["electricity","bill","wifi","recharge","rent","fees"],
    }

    for category, keywords in category_keywords.items():
        for word in keywords:
            if word in reason:
                return category

    return "others"

from resume_module.parser import extract_text
from resume_module.analyzer import extract_skills, missing_skills
from expense_module.tracker import add_expense, get_expenses
from resume_module.analyzer import calculate_score
from resume_module.analyzer import recommend_courses
from expense_module.tracker import predict_expense

st.set_page_config(page_title="AI Career & Finance Assistant")

st.title("AI Career & Finance Assistant")
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
h1 {
    color: #4CAF50;
    text-align: center;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["Resume", "Expense", "Insights"])


# ---------------- RESUME ----------------
with tab1:
    st.header("📄 Resume Analyzer")

    st.info("📤 Upload your resume and get skill insights")

    file = st.file_uploader("Upload Resume", type=["pdf"])

    if file:

        # 🔥 Check if new resume uploaded
        if "last_resume" not in st.session_state:
            st.session_state["last_resume"] = ""

        if st.session_state["last_resume"] != file.name:
            
            # 🔄 NEW RESUME DETECTED → RESET EXPENSE DATA
            import pandas as pd
            df = pd.DataFrame(columns=["amount", "category"])
            df.to_csv("data/expenses.csv", index=False)

            st.warning("🔄 New Resume Detected → Expense Data Reset!")

            # update last resume
            st.session_state["last_resume"] = file.name

        st.success(f"✅ Resume Uploaded: {file.name}")

        # 🔍 Extract data
        text = extract_text(file)
        skills = extract_skills(text)
        missing = missing_skills(skills)

        # 🔥 Store missing skills globally
        st.session_state["missing"] = missing

        # 📊 Skills display
        st.markdown("### 🧠 Detected Skills")
        st.success(skills)

        st.markdown("### ⚠️ Missing Skills")
        st.error(missing)

        # 🎯 Score
        score = calculate_score(text, skills)

        # 📚 Courses
        courses = recommend_courses(missing)

        st.markdown("### 🎓 Recommended Courses")
        if courses:
            for course in courses:
                st.info(course)
        else:
            st.success("✅ Your skills are good! No major course needed")

        # 📊 Score display
        st.markdown("### 📊 Resume Score")
        st.progress(score / 100)
        st.success(f"Your Resume Score: {score}/100")



# ---------------- EXPENSE ----------------
with tab2:
    st.header("💸 Smart Expense Tracker")

    st.markdown("### ➕ Add Expense")

    col1, col2 = st.columns(2)

    with col1:
        amount = st.number_input("💰 Amount", min_value=0)
        date = st.date_input("📅 Date", datetime.date.today())

    with col2:
        reason = st.text_input("🧠 Reason (e.g. pizza with friends)")

        # 🤖 Auto detect
        auto_cat = auto_category(reason) if reason else "others"

        category = st.selectbox(
            "🏷️ Category",
            ["auto", "food", "travel", "course", "shopping", "entertainment", "health", "bills", "others"]
        )

        final_category = auto_cat if category == "auto" else category

        st.write(f"🤖 Detected Category: **{final_category}**")

    regret = st.selectbox("😬 Was this worth it?", ["Yes", "No"])

    # ➕ Add Expense
    if st.button("➕ Add Expense"):

        new_data = {
            "date": date,
            "amount": amount,
            "category": final_category,
            "reason": reason,
            "regret": regret
        }

        df = get_expenses()
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv("data/expenses.csv", index=False)

        st.success("✅ Expense Added Successfully!")

    # 📋 Show data
    st.markdown("### 📋 Expense History")

    data = get_expenses()

    if not data.empty:
        st.dataframe(data)
    else:
        st.info("No data available yet 🚫")

# ---------------- INSIGHTS (🔥 CORRECT PLACE) ----------------
with tab3:
    st.header("📊 Smart Insights Dashboard")

    import pandas as pd
    import matplotlib.pyplot as plt
    import pyttsx3

    data = get_expenses()

    # 🔥 Resume missing skills
    missing = st.session_state.get("missing", [])

    if not data.empty:

        # 🔊 Voice function
        def speak(text):
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()

        # 📅 Weekly system
        data["date"] = pd.to_datetime(data["date"])
        data["week"] = data["date"].dt.isocalendar().week

        current_week = pd.Timestamp.today().week
        week_data = data[data["week"] == current_week]

        week_total = week_data["amount"].sum()

        total = data["amount"].sum()
        category_sum = data.groupby("category")["amount"].sum()

        # 📊 Metrics
        col1, col2 = st.columns(2)

        with col1:
            st.metric("💰 Total Spending", f"₹{total}")

        with col2:
            top_category = category_sum.idxmax()
            st.metric("🔥 Top Category", top_category)

        st.metric("📆 This Week Spending", f"₹{week_total}")

        # 🔮 Prediction
        predicted = predict_expense(data)

        st.markdown("### 🔮 Future Prediction")
        if predicted:
            st.success(f"📈 Expected Next Expense: ₹{predicted}")
        else:
            st.info("Not enough data for prediction")

        # 📊 Charts
        st.markdown("### 📊 Spending Analysis")

        col3, col4 = st.columns(2)

        with col3:
            fig1, ax1 = plt.subplots()
            ax1.bar(category_sum.index, category_sum.values)
            st.pyplot(fig1)

        with col4:
            fig2, ax2 = plt.subplots()
            ax2.pie(category_sum.values, labels=category_sum.index, autopct='%1.1f%%')
            ax2.axis('equal')
            st.pyplot(fig2)

        # 🎯 Skill vs Waste
        learning = week_data[week_data["category"] == "course"]["amount"].sum()
        waste = week_total - learning

        st.markdown("### 🎯 Skill vs Waste")
        st.write(f"📚 Learning: ₹{learning}")
        st.write(f"💸 Waste: ₹{waste}")

        if waste > learning:
            st.error("🚨 You are wasting more than investing in yourself!")

        # 😬 Regret
        regret_data = week_data[week_data["regret"] == "No"]
        regret_amount = regret_data["amount"].sum()

        st.markdown("### 😬 Regret Spending")
        st.write(f"₹{regret_amount} spent on regret purchases")

        # 🔮 Future Warning
        future = week_total * 4
        st.markdown("### 🔮 Monthly Projection")
        st.warning(f"If you continue like this → ₹{future} per month")

        # 🏆 Score
        score = 100
        if week_total > 2000:
            score -= 30
        if regret_amount > 500:
            score -= 20
        if learning > 0:
            score += 20

        st.metric("🏆 Financial Score", score)

        # 🕳 Hidden Leak
        small = week_data[week_data["amount"] < 100]
        leak = small["amount"].sum()

        st.markdown("### 🕳 Hidden Leak")
        st.write(f"₹{leak} spent on small expenses")

        if leak > 500:
            st.error("🚨 Small expenses are draining your money!")

        # 🚨 Alerts
        st.markdown("### 🚨 Smart Alerts")

        for category, amount in category_sum.items():
            percent = (amount / total) * 100

            if percent >= 50:
                st.error(f"🚨 {category.upper()} is your major expense ({percent:.1f}%)")
            elif percent >= 30:
                st.warning(f"⚠️ High spending on {category} ({percent:.1f}%)")

        # ===========================
        # 🔥 NEW FEATURES START HERE
        # ===========================

        # 🎯 Goal Planner
        st.markdown("### 🎯 Goal Planner")
        goal_amount = st.number_input("Enter your goal (₹)", value=5000)

        if waste > 0:
            months = goal_amount / waste
            st.info(f"💡 You can achieve this goal in {months:.1f} months by saving waste money")

        # 💰 Saving Suggestion
        st.markdown("### 💰 Saving Suggestion")
        saving = waste * 0.5
        st.warning(f"You can save approx ₹{saving} by reducing waste spending")

        # 🔍 Expense Filter
        st.markdown("### 🔍 Filter Expenses")
        selected_cat = st.selectbox("Select Category", data["category"].unique())
        filtered = data[data["category"] == selected_cat]
        st.dataframe(filtered)

        # 🧠 Smart Insight
        st.markdown("### 🧠 Smart Insight")

        if waste > learning:
            st.error("🚨 You are spending more on lifestyle than self-growth")
        elif learning > waste:
            st.success("🔥 Great! You are investing in your future")
        else:
            st.info("⚖️ Balanced spending")

        # 📄 PDF Download
        st.markdown("### 📄 Download Report")

        if st.button("Generate PDF Report"):
            generate_pdf(total, week_total, waste, learning, score)

            with open("expense_report.pdf", "rb") as file:
                st.download_button(
                    label="📥 Download PDF",
                    data=file,
                    file_name="expense_report.pdf",
                    mime="application/pdf"
                )

        # ===========================
        # 🧠 AI Advice (UNCHANGED)
        # ===========================

        st.markdown("### 🧠 AI Financial + Career Advice")

        course_links = {
            "python": ("Python for Beginners", "https://www.freecodecamp.org/learn/"),
            "sql": ("SQL for Data Analysis", "https://www.coursera.org/learn/sql-for-data-science"),
            "machine learning": ("Machine Learning - Andrew Ng", "https://www.coursera.org/learn/machine-learning"),
            "data analysis": ("Google Data Analytics", "https://www.coursera.org/professional-certificates/google-data-analytics"),
            "excel": ("Excel Course", "https://www.udemy.com/course/microsoft-excel-course/"),
            "communication": ("Communication Skills", "https://www.udemy.com/course/communication-skills/"),
            "java": ("Java Course", "https://www.udemy.com/course/java-the-complete-java-developer-course/"),
            "c++": ("C++ Course", "https://www.learncpp.com/"),
            "data structures": ("DSA Course", "https://www.geeksforgeeks.org/data-structures/"),
            "algorithms": ("Algorithms Course", "https://www.coursera.org/specializations/algorithms"),
            "dbms": ("DBMS Course", "https://www.geeksforgeeks.org/dbms/"),
            "html": ("HTML Course", "https://www.freecodecamp.org/learn/responsive-web-design/"),
            "css": ("CSS Course", "https://www.freecodecamp.org/learn/responsive-web-design/"),
            "javascript": ("JavaScript Course", "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/")
        }

        top_amount = category_sum.max()

        if top_amount > 1000:

            st.error(f"🚨 You are spending too much on '{top_category}'")

            if not st.session_state.get("spoken", False):
                speak(f"You are spending too much on {top_category}")
                st.session_state["spoken"] = True

            if missing:
                st.warning("⚠️ Invest in skills instead 👇")

                for skill in missing[:3]:
                    skill_lower = skill.lower().strip()

                    course_name, link = course_links.get(
                        skill_lower,
                        ("Search this skill", f"https://www.google.com/search?q=learn+{skill_lower}")
                    )

                    st.info(f"🎯 Learn {skill}")
                    st.markdown(f"👉 📚 [**{course_name}**]({link})", unsafe_allow_html=True)

            else:
                st.success("🔥 Strong skill set. Focus on saving!")

        else:
            st.success("✅ Spending under control")

    else:
        st.info("No data available yet 🚫")