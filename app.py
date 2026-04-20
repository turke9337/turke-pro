import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. إعدادات المنصة الأساسية (نظام مدرستي)
# ==========================================
st.set_page_config(
    page_title="منصة تركي سفياني الذكية",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- تعديل الربط مع الذكاء الاصطناعي ---
try:
    # سيقوم الموقع الآن بقراءة المفتاح من "Secrets" في إعدادات Streamlit Cloud بأمان
    API_KEY = st.secrets["AIzaSyAb5fX0M-Jj1cNDWFX-qnxicHm4q2cnpKI"]
    genai.configure(api_key=API_KEY)
    # استخدام الإصدار المستقر والأقوى حالياً لضمان عدم تعليق السيرفر
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("⚠️ فشل الاتصال بمحرك الذكاء الاصطناعي. تأكد من إعداد Secrets بشكل صحيح.")

# ==========================================
# 2. بوابة الأمان الصارمة
# ==========================================
if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False

# كود CSS لتصميم منصة مدرستي وإصلاح مشاكل العرض
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    
    .profile-card {
        background: linear-gradient(135deg, #0d9488 0%, #0d9488 100%);
        color: white; padding: 25px; border-radius: 20px; text-align: center;
        margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        direction: rtl;
    }
    .stMarkdown, .stText, .stChatMessage { text-align: right; direction: rtl; }
    
    div.stButton > button {
        background-color: white; color: #1e293b; width: 100%; height: 140px;
        border-radius: 20px; border: 2px solid #e2e8f0; font-size: 20px; font-weight: bold;
        transition: all 0.3s ease; box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    }
    div.stButton > button:hover { border-color: #0d9488; color: #0d9488; transform: translateY(-3px); }
    
    .block-container { padding-top: 2rem; }
    [data-testid="stSidebarNav"] { display: none; }
    </style>
""", unsafe_allow_html=True)

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #0f766e;'>🔒 بوابة دخول تركي سفياني</h1>", unsafe_allow_html=True)
    u = st.text_input("اسم المستخدم:")
    p = st.text_input("كلمة المرور:", type="password")
    if st.button("دخول"):
        if u.strip() == "350" and p == "officer":
            st.session_state.logged_in = True
            st.rerun()
        else: 
            st.error("❌ بيانات فاشلة. ركز جيداً.")
    st.stop() 

# إدارة الصفحات
if 'page' not in st.session_state: 
    st.session_state.page = "الرئيسية"
if 'chat_logs' not in st.session_state: 
    st.session_state.chat_logs = []

# ==========================================
# 3. بنك الكلمات المطور
# ==========================================
vocabulary_bank = {
    "A1": [{"word": "go", "type": "verb", "meaning": "move", "example": "I go home"}],
    "A2": [{"word": "officer", "type": "noun", "meaning": "military leader", "example": "He is a brave officer"}],
    "B1": [{"word": "checkmate", "type": "chess", "meaning": "game over", "example": "The final checkmate"}],
    "B2": [{"word": "strategy", "type": "noun", "meaning": "plan", "example": "A winning strategy"}],
    "C1": [{"word": "ambitious", "type": "adj", "meaning": "determined", "example": "Turki is ambitious"}],
    "C2": [{"word": "mastery", "type": "noun", "meaning": "total control", "example": "Mastery of English"}]
}

# ==========================================
# 4. التنقل والمحتوى
# ==========================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/ar/thumb/c/cf/Madrasati_Logo.png/800px-Madrasati_Logo.png", width=120)
    if st.button("🏠 الرئيسية"): 
        st.session_state.page = "الرئيسية"
        st.rerun()
    if st.button("🚪 خروج"): 
        st.session_state.logged_in = False
        st.rerun()

if st.session_state.page == "الرئيسية":
    st.markdown("""
        <div class="profile-card">
            <h1 style='margin:0; font-size:26px;'>مرحباً بك تركي سفياني 🎖️</h1>
            <p style='margin:5px 0; opacity:0.9;'>ثانوية الإمام الشافعي | تم تأكيد هويتك كـ "350".</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🤖\nالذكاء الاصطناعي"): 
            st.session_state.page = "البوت"
            st.rerun()
        if st.button("📚\nالمكتبة"): 
            st.session_state.page = "المكتبة"
            st.rerun()
    with col2:
        if st.button("🔤\nمعسكر الكلمات"): 
            st.session_state.page = "الكلمات"
            st.rerun()
        if st.button("📺\nالمرئيات"): 
            st.session_state.page = "الفيديوهات"
            st.rerun()

elif st.session_state.page == "البوت":
    st.title("🤖 مساعدك الشخصي (جيس)")
    for msg in st.session_state.chat_logs:
        with st.chat_message(msg["role"]): 
            st.markdown(msg["content"])
            
    if prompt := st.chat_input("تحدث معي هنا يا مطيعي..."):
        st.session_state.chat_logs.append({"role": "user", "content": prompt})
        with st.chat_message("user"): 
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            try:
                sys_instruction = "أنت جيس (Jace). حازم، مسيطر، وتلقب تركي بـ 'صغيري'. وجهه بصرامة لتعلم اللغات والشطرنج والتخطيط العسكري."
                full_prompt = f"{sys_instruction}\nالآن رد على هذا الطلب: {prompt}"
                resp = model.generate_content(full_prompt)
                st.markdown(resp.text)
                st.session_state.chat_logs.append({"role": "assistant", "content": resp.text})
            except:
                st.error("السيرفر مشغول الحين... بس أنا هنا معك جرب بعد شوي")

elif st.session_state.page == "الكلمات":
    st.title("🔤 معسكر الكلمات الشامل")
    tabs = st.tabs(["A1", "A2", "B1", "B2", "C1", "C2"])
    for i, level in enumerate(vocabulary_bank.keys()):
        with tabs[i]:
            for item in vocabulary_bank[level]:
                st.markdown(f"""
                    <div style='background:white; padding:20px; border-radius:15px; border:2px solid #e2e8f0; margin-bottom:10px; color:black;'>
                        <h2 style='color:#0d9488; margin:0;'>{item['word']}</h2>
                        <p><b>النوع:</b> {item['type']} | <b>المعنى:</b> {item['meaning']}</p>
                        <p style='color:gray;'><i>مثال: {item['example']}</i></p>
                    </div>
                """, unsafe_allow_html=True)

elif st.session_state.page == "المكتبة":
    st.title("📚 المكتبة التعليمية")
    st.link_button("📖 قراءة كتاب (A1) - قصة الأميرة الصغيرة", "https://english-e-reader.net/book/a-little-princess-frances-hodgson-burnett")

elif st.session_state.page == "الفيديوهات":
    st.title("📺 دروس مرئية")
    st.video("https://www.youtube.com/watch?v=juKd26qkywQ")
