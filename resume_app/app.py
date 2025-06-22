import os
from pathlib import Path
import streamlit as st
from PIL import Image
from openai import OpenAI
import os
from dotenv import load_dotenv

# ---- path settings ----
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"
resume_file = current_dir / "assets" / "Resume2025.pdf"
profile_pic = current_dir / "assets" / "profile-pic.png"
capstone_path = current_dir / "assets" / "CAPSTONE_report.pdf"
with open(capstone_path, "rb") as f:
    capstone_data = f.read()


# ---- general settings ----
page_title = "Resume | Albert Shilling"
page_icon = ":wave:"
name = "Albert Shilling"
description = "B.S. Data Science & Analytics, assisting enterprises by supporting data-driven decision making."
email = "albertshilling1225@gmail.com"
social_media = {
    "Github": "https://github.com/chasingbytes",
    "LinkedIn": "https://linkedin.com/in/albertshilling",
}
projects = {
    ":blue car: Rising Tide Car Wash daily customer predictor": "https://risingtide-predictor.streamlit.app/",
}
st.set_page_config(page_title=page_title, page_icon=page_icon, layout="wide")

# ---- load CSS ----
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
with open(resume_file, "rb") as pdf_file:
    PDFbyte = pdf_file.read()
profile_pic = Image.open(profile_pic)

# ---- hero section ----
col1, col2 = st.columns(2, gap="small")
with col1:
    st.image(profile_pic, width=330)

with col2:
    st.title(name)
    st.write(description)
    st.download_button(
        label="Download Resume",
        data=PDFbyte,
        file_name=resume_file.name,
        mime="application/octet-stream",
    )
    st.write(":mailbox:", email)

# ---- social links -----
# Custom columns for buttons and links
col1, col2, col3, col4 = st.columns(4)

# Assign social links manually to the center columns
col2.markdown(f"[Github]({social_media['Github']})")
col3.markdown(f"[LinkedIn]({social_media['LinkedIn']})")

st.write("---")
# ---- Capstone report -----
# Create 3 columns: left spacer, center, right spacer
left_col, center_col, right_col = st.columns([1, 2, 1])

with center_col:
    st.download_button(
        label="Decision Trees vs. Neural Networks:  Which one for predictions?",
        data=capstone_data,
        file_name="CAPSTONE_report.pdf",
        mime="application/pdf"
    )


st.write("---")

# ---- experience & qualifications ----
st.write("#")
st.subheader("Experience & Qualifications")
st.write(
    """
    - ➤ Developed and implemented a predictive model for Rising Tide Car Wash to forecast daily customer traffic using 3 years of historical data, currently being used in operations at the Parkland location. Version 2.0 is currently in production where it will support all three locations. 
    - ➤ Built an automated email response system using a customized GPT model integrated with the Gmail API  
    - ➤ Experience in data mining, neural networks, machine learning classifiers, and predictive statistical programming  
    - ➤ Proficient in Python, C++, SQL, and Excel; strong hands-on learner  
    - ➤ Team-oriented with a strong sense of initiative and independent problem-solving ability
    """
)

# ---- skills ----
st.write("#")
st.subheader("Technical Skills")
st.write(
    """
    - ➤ **Programming**: Python (Scikit-learn, PyTorch, Keras, TensorFlow, Pandas, NumPy), SQL, C++  
    - ➤ **Data Visualization**: Streamlit, Matplotlib, Seaborn, MS Excel  
    - ➤ **Modeling & Machine Learning**: XGBoost, Logistic Regression, Decision Trees, LSTM Neural Networks, Kaplan-Meier Survival Analysis  
    - ➤ Experienced with key tools and frameworks including Streamlit for web app development and XGBoost for model training and optimization  
    """
)


# ---- Work history ----
st.write("---")
st.write("#")
st.subheader("Work History")

# ---- Job 1 ----
st.write("🚙 ", "**Operations Analyst | Rising Tide Car Wash**")
st.write("01/2025 - Present")
st.write(
    """
    - 💼 Currently supporting operations and innovation at Rising Tide Car Wash, where I combine programming skills with hands-on leadership to improve efficiency and decision-making.
    - 🚗 Built predictive web apps to forecast customer traffic and automated customer email responses using GPT — freeing up time for the team to focus on what matters most.
    - 🔍 Always exploring how data and tech can transform operations, especially in small business environments. Open to roles in data science, operations analytics, or cloud-based AI solutions.
    """
)

# ---- job 2 -----
st.write("🚙 ", "**Operations Manager | Rising Tide Car Wash**")
st.write("08/2021 - Present")
st.write(
    """
    - 👥 Working alongside the Site Manager with daily operations including staff scheduling, customer service, and team relations  
    - 🛠️ Ensure mechanical systems are operating efficiently and coordinate routine maintenance  
    - 💻 Troubleshoot technical issues related to point-of-sale systems and automated entry equipment  
    - 🌟 Support a high-functioning, inclusive work environment and uphold service quality standards  
    """
)

# ---- Chat bot assistant -----

# load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

with st.sidebar:
    st.markdown("### 💬 Ask Albert's Resume Assistant")
    st.markdown("*Try asking:*")
    st.markdown("- What are your top skills?\n- What was your capstone?\n- Any experience with Machine Learning?")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_query = st.text_input("Ask something about Albert:")

    if user_query:
        # Your personal summary prompt
        system_prompt = """
        You are a helpful assistant that answers questions about Albert Shilling.

        Albert is a recent graduate from Florida Atlantic University with a B.S. in Data Science & Analytics.
        He specializes in machine learning, Python, XGBoost, LSTMs, and Streamlit.
        He built a car wash predictor using 3 years of weather data and deployed it via Streamlit, with version 1.0 used by the Parkland location at Rising Tide Car Wash. Version 2.0 is being built currently to support operations company wide-across all three stores. A pdf version is also availible to download a full report on this from my resume page titled: "Decision Trees vs Neural Networks: Which one for predictions".
        He's also automated customer support emails using GPT and the Gmail API while working as Rising Tide Car Wash's Operations Analyst.
        """

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4o" if available
            messages=messages
        )
        reply = response.choices[0].message.content
        st.session_state.chat_history.append((user_query, reply))

    # Show chat history in the sidebar
    for q, a in reversed(st.session_state.chat_history):
        st.markdown(f"**You:** {q}")
        st.markdown(f"**Albert's Assistant:** {a}")
