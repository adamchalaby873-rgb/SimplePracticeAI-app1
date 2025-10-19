import streamlit as st
import json
import time
from Query import QueryAI

st.set_page_config(page_title="PracticeAI", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
        
        /* Animated mesh gradient background */
        @keyframes gradientShift {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        
        .stApp {
            background: linear-gradient(-45deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
        }
        
        .block-container {
            padding-top: 5rem !important;
            padding-bottom: 3rem !important;
            max-width: 800px !important;
        }
        
        /* Glass morphism header */
        .main-header {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 24px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        
        .main-title {
            font-family: 'Inter', sans-serif;
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0;
            text-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            letter-spacing: -1px;
        }
        
        .subtitle {
            color: rgba(255, 255, 255, 0.95);
            font-size: 1.1rem;
            margin-top: 0.5rem;
            font-weight: 500;
        }
        
        /* Input section - transparent */
        .input-container {
            background: transparent;
            padding: 0;
            margin-bottom: 2rem;
        }
        
        /* Question cards with hover effect */
        .question-card {
            background: rgba(255, 255, 255, 0.98);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
            border: 2px solid transparent;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .question-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
            transform: scaleX(0);
            transform-origin: left;
            transition: transform 0.3s ease;
        }
        
        .question-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(102, 126, 234, 0.25);
            border-color: rgba(102, 126, 234, 0.3);
        }
        
        .question-card:hover::before {
            transform: scaleX(1);
        }
        
        /* Question number badge */
        .question-badge {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.5rem 1.2rem;
            border-radius: 50px;
            font-weight: 700;
            font-size: 0.9rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        /* Styled labels */
        label {
            font-weight: 600 !important;
            color: #2d3748 !important;
            font-size: 1rem !important;
        }
        
        /* Radio buttons */
        .stRadio > label {
            display: none !important;
        }
        
        .stRadio > div {
            gap: 0.5rem;
        }
        
        .stRadio > div > label {
            background: white !important;
            padding: 1rem 1.2rem !important;
            border-radius: 12px !important;
            border: 2px solid #e2e8f0 !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
            font-weight: 500 !important;
            color: #2d3748 !important;
        }
        
        .stRadio > div > label:hover {
            border-color: #667eea !important;
            background: rgba(102, 126, 234, 0.05) !important;
            transform: translateX(4px) !important;
        }
        
        .stRadio > div > label > div {
            color: #2d3748 !important;
        }
        
        /* Generate button */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 1rem 2rem !important;
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 30px rgba(102, 126, 234, 0.6) !important;
        }
        
        .stButton > button:active {
            transform: translateY(0) !important;
        }
        
        /* Clear button (second button in columns) */
        div[data-testid="column"]:nth-child(2) .stButton > button {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%) !important;
            box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4) !important;
        }
        
        div[data-testid="column"]:nth-child(2) .stButton > button:hover {
            box-shadow: 0 8px 30px rgba(255, 107, 107, 0.6) !important;
        }
        
        /* Submit answer buttons */
        div[data-testid="column"] .stButton > button {
            width: auto;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
            padding: 0.7rem 1.5rem !important;
            font-size: 0.95rem !important;
            margin-top: 1rem;
        }
        
        div[data-testid="column"] .stButton > button:hover {
            box-shadow: 0 6px 25px rgba(245, 87, 108, 0.5) !important;
        }
        
        /* Success/Error messages */
        .stSuccess, .stError {
            border-radius: 12px !important;
            border: none !important;
            padding: 1rem 1.5rem !important;
            font-weight: 600 !important;
            animation: slideIn 0.3s ease !important;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .stSuccess {
            background: linear-gradient(135deg, #81FBB8 0%, #28C76F 100%) !important;
            color: #155724 !important;
        }
        
        .stError {
            background: linear-gradient(135deg, #FF6B9D 0%, #C9379D 100%) !important;
            color: white !important;
        }
        
        /* Spinner */
        .stSpinner > div {
            border-top-color: #667eea !important;
        }
        
        /* Quiz description */
        .quiz-description {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            padding: 1.5rem;
            border-radius: 16px;
            border-left: 4px solid #667eea;
            margin-bottom: 2rem;
            font-size: 1.05rem;
            line-height: 1.6;
            color: #2d3748;
        }
        
        /* Prevent quiz description styling from applying to empty markdown elements */
        div[data-testid="stMarkdownContainer"]:empty {
            display: none !important;
            background: none !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        
        /* Hide white boxes */
        .stRadio > div:first-child {
            display: none !important;
        }
        
        div[data-testid="stVerticalBlock"] > div:has(.quiz-description) + div {
            display: none !important;
        }
        
        /* Hide empty white boxes above questions */
        .question-card + div[data-testid="stVerticalBlock"] > div:empty,
        div[data-testid="stVerticalBlock"] > div:empty {
            display: none !important;
        }
        
        .element-container:has(> .question-card) + .element-container:empty {
            display: none !important;
        }
        
        /* Dividers */
        hr {
            margin: 2rem 0;
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, #667eea, transparent);
        }
        
        /* Hide blank white boxes between questions */
        hr + div:empty,
        div:has(> hr) + div:empty {
            display: none !important;
        }
        
        .element-container:has(hr) + .element-container:empty {
            display: none !important;
        }
        
        /* Additional targeting for white boxes before question cards */
        div[data-testid="stVerticalBlock"] > div[data-testid="element-container"]:empty {
            display: none !important;
        }
        
        div[data-testid="stHorizontalBlock"] + div:empty {
            display: none !important;
        }
        
        /* Hide any empty divs within the vertical block */
        div[data-testid="stVerticalBlock"] > div:not(:has(*)) {
            display: none !important;
        }
        
        /* Explanation text animation container */
        .explanation-box {
            background: rgba(102, 126, 234, 0.05);
            padding: 1rem 1.5rem;
            border-radius: 12px;
            border-left: 3px solid #667eea;
            margin-top: 1rem;
            font-family: 'Inter', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class='main-header'>
        <div class='main-title'>✨ PracticeAI</div>
        <div class='subtitle'>AI-Powered Practice Quizzes That Adapt to You</div>
    </div>
""", unsafe_allow_html=True)

# Input section
st.markdown("<div class='input-container'>", unsafe_allow_html=True)
topic = st.text_input("📚 Enter a topic to generate a quiz for:", value="AP Hug Unit 2: Population and Migration Patterns and Processes")
num_questions = st.number_input("🔢 Number of questions:", min_value=1, max_value=50, value=10, step=1)

col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Generate Quiz"):
        with st.spinner("✨ Crafting your personalized quiz..."):
            raw_quiz = QueryAI(topic, str(num_questions))
            try:
                st.session_state.quiz = json.loads(raw_quiz)
                st.session_state.submitted = {}
            except Exception:
                st.error("❌ Failed to parse quiz JSON. The API may have returned an error or invalid data.")
                st.text(raw_quiz)
                st.stop()

with col2:
    if st.button("🗑️ Clear Quiz"):
        if "quiz" in st.session_state:
            del st.session_state.quiz
        if "submitted" in st.session_state:
            del st.session_state.submitted
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# Display quiz
if "quiz" in st.session_state:
    quiz = st.session_state.quiz
    
    if quiz.get('quiz_description'):
        st.markdown(f"<div class='quiz-description'>📝 {quiz.get('quiz_description', '')}</div>", unsafe_allow_html=True)
    
    if 'submitted' not in st.session_state:
        st.session_state.submitted = {}
    
    for question in quiz["questions"]:
        st.markdown("<div class='question-card'>", unsafe_allow_html=True)
        
        st.markdown(f"<span class='question-badge'>Question {question['id']}</span>", unsafe_allow_html=True)
        st.markdown(f"**{question['question']}**")
        
        key_radio = f"q_{question['id']}"
        user_answer = st.radio("Choose your answer:", question["choices"], key=key_radio)
        
        key_btn = f"submit_{question['id']}"
        if st.button("Submit Answer ✓", key=key_btn):
            user_letter = user_answer[0]
            st.session_state.submitted[question['id']] = True
            
            if user_letter + "." == question["answer"]:
                st.success("✅ Correct! Excellent work!")
            else:
                st.error(f"❌ Not quite right. The correct answer is **{question['answer']}**")
                
                explanation_placeholder = st.empty()
                explanation_text = f"💡 {question['explanation']}"
                displayed_text = ""
                for char in explanation_text:
                    displayed_text += char
                    explanation_placeholder.markdown(f"<div class='explanation-box'>{displayed_text}</div>", unsafe_allow_html=True)
                    time.sleep(0.02)
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)