import streamlit as st
import os

# --- 網頁外觀設定 (日式低奢風格) ---
st.set_page_config(page_title="王子的旅行代購", page_icon="👑", layout="centered")

st.markdown("""
    <style>
    /* 導入思源明體以增加高級感 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;600&display=swap');
    
    .stApp {
        /* 日式宣紙紋理 + 頂部微光漸層 */
        background-color: #f7f5f0;
        background-image: 
            radial-gradient(circle at 50% 0%, rgba(255, 255, 255, 0.8) 0%, rgba(255, 255, 255, 0) 60%),
            url('https://www.transparenttextures.com/patterns/rice-paper-2.png');
        background-attachment: fixed;
        font-family: 'Noto Serif TC', serif;
        color: #3b3a37;
    }
    
    /* 標題與內文顏色調整 */
    h1, h2, h3, h4 {
        color: #2c2b29;
        font-weight: 600;
        letter-spacing: 2px;
    }
    
    /* 隱藏 Streamlit 預設元素 */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 優化按鈕外觀 */
    .stButton>button {
        background-color: #3b3a37;
        color: #f7f5f0;
        border: none;
        border-radius: 2px; /* 極簡微圓角 */
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        letter-spacing: 1px;
        width: 100%;
        margin-top: auto; /* 讓按鈕自動推到底部對齊 */
    }
    .stButton>button:hover {
        background-color: #5c5a56;
        color: #ffffff;
    }
    
    /* 讓每一行欄位（column）高度一致並改為 Flex 垂直排列 */
    div[data-testid="column"] {
        background-color: rgba(255, 255, 255, 0.4);
        padding: 1.5rem 1rem;
        border-radius: 4px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
        margin-bottom: 1rem;
        text-align: center;
        display: flex !important;
        flex-direction: column !important;
        height: 100% !important;
    }
    
    /* 讓 Streamlit 欄位內部的容器自動撐開高度 */
    div[data-testid="column"] > div {
        display: flex !important;
        flex-direction: column !important;
        flex-grow: 1 !important;
    }
    
    /* 固定圖片顯示高度與縮放模式 */
    div[data-testid="column"] img {
        height: 160px !important;
        object-fit: contain !important;
        width: 100% !important;
        margin-bottom: 0.5rem;
    }
    
    /* 優雅的中文小副標題 */
    .elegant-subtitle {
        font-size: 0.85rem;
        color: #8c8a84;
        letter-spacing: 3px;
        margin-bottom: 2px;
        display: block;
    }
    </style>
""", unsafe_allow_html=True)


# --- 產品資料庫 (對應您上傳的真實圖片檔名) ---
PRODUCTS = {
    # 歐洲區
    "china_oel": {
        "name": "德國百靈油",
        "sub_name": "萬用薄荷精油",
        "image": "china.oil.jpeg",
        "category": "europe",
        "is_recommended": True, 
        "spec": "容量：100ml | 德國原裝進口",
        "description": "德國原裝進口，由 100% 純薄荷精油提煉而成。主要效用包含緩解頭痛、改善感冒引起的鼻塞與咳嗽、緩解肌肉痠痛、舒緩腸胃不適，是家庭常備的萬用精油。",
        "usage": "- **外用**：取適量塗抹於肌肉痠痛處。\n- **內服**：滴 1~2 滴於溫開水中飲用。\n- **吸入**：滴於熱水中吸入蒸氣。"
    },
    "whisky_21yr": {
        "name": "蘇格蘭 21 年威士忌",
        "sub_name": "桶陳歲月・珍稀醇厚",
        "image": "whisky.21yr.jpeg",
        "category": "europe",
        "is_recommended": True, 
        "spec": "容量：700ml | 酒精濃度：40% | 蘇格蘭原裝進口",
        "description": "嚴選蘇格蘭頂級橡木桶陳釀 21 年以上，經過歲月淬鍊展現出深邃的琥珀色澤。入口帶有濃郁的蜂蜜、成熟果香與淡淡的橡木芬芳，口感絲滑醇厚、尾韻悠長，是品味人士不可錯過的珍稀佳釀。",
        "usage": "- **純飲**：建議常溫飲用，或靜置幾分鐘讓香氣完全釋放。\n- **冰飲**：加入一顆大冰球，感受層次隨溫度變化的迷人風味。"
    },
    "seal_oil": {
        "name": "挪威頂級深海海豹油",
        "sub_name": "北歐頂級保養",
        "image": "seel.oil.png",
        "category": "europe",
        "is_recommended": False,
        "spec": "容量：120 粒膠囊裝",
        "description": "來自純淨挪威海域，富含高純度 Omega-3 (EPA/DHA/DPA)。比一般魚油更容易被人體吸收，是守護全家人心血管與關節健康的北歐秘方。",
        "usage": "- **日常保養**：每日早晚各 1 粒，隨餐食用。\n- **加強保養**：每日 4 粒。"
    },
    "krill_oil": {
        "name": "挪威頂級南極磷蝦油",
        "sub_name": "海洋極境純淨萃取",
        "image": "shrimp.jpeg",
        "category": "europe",
        "is_recommended": True,
        "spec": "容量：60 粒軟膠囊裝",
        "description": "捕撈自純淨無汙染的南極海域，磷蝦油富含磷脂質結合型的 Omega-3 (EPA/DHA) 以及強效抗氧化劑「蝦青素」。其吸收率極高且無腥味，能全面照顧日常思緒、循環與晶亮健康。",
        "usage": "- **日常保健**：每日 1~2 粒，隨餐或餐後食用最佳。\n- **注意事項**：對蝦、蟹等甲殼類過敏者請避免食用。"
    },
    "foie_gras": {
        "name": "匈牙利傳統手工鵝肝醬",
        "sub_name": "經典佐餐名品",
        "image": "goose.liver.jpeg",
        "category": "europe",
        "is_recommended": False,
        "spec": "重量：180g (罐裝)",
        "description": "歐洲老饕的頂級享受！採百年傳統工藝製作，口感如絲綢般滑順，香氣濃郁迷人。適合搭配薄脆餅乾或無花果醬，作為紅酒佐餐的絕佳選擇。",
        "usage": "- **食用建議**：冷藏後取出直接塗抹於烤過的法式麵包或蘇打餅乾上。"
    },
    # 水果區
    "aus_cherry": {
        "name": "澳洲塔斯馬尼亞櫻桃",
        "sub_name": "空運特大果",
        "image": "cherry.jpeg",
        "category": "fruit",
        "is_recommended": True, 
        "spec": "規格：頂級禮盒裝 (優選大果)",
        "description": "冬季限定的紅寶石！空運直送來台，果肉飽滿多汁，甜度極高且帶有迷人脆度。年節送禮最有面子的選擇。",
        "usage": "- **保存方式**：收到後請立即冷藏，建議於 5-7 天內食用完畢以保新鮮。"
    },
    "envy_apple": {
        "name": "紐西蘭 Envy 頂級蘋果",
        "sub_name": "香甜脆口果王",
        "image": "apple.jpeg",
        "category": "fruit",
        "is_recommended": False,
        "spec": "規格：精美禮盒裝",
        "description": "來自紐西蘭的頂級 Envy 蘋果，擁有極佳的清脆口感與濃郁香甜風味。果肉細緻且不易變色，是品味生活的優質之選。",
        "usage": "- **保存方式**：冷藏保存，冰涼後切片食用風味更佳。"
    }
}

# --- 密碼驗證區 ---
def check_password():
    SECRET_PIN = "1234"

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("<h1 style='text-align: center; margin-top: 15vh; font-size: 2.5rem;'>👑 王子的旅行代購</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; letter-spacing: 2px; color: #8c8a84;'>「將世界的美好，帶回您身邊。」</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; margin-bottom: 2rem;'>請輸入專屬密碼以進入會員賣場</p>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1.2, 1])
        with col2:
            password_input = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="••••")
            if st.button("登 入", use_container_width=True):
                if password_input == SECRET_PIN:
                    st.session_state.authenticated = True
                    st.rerun() 
                else:
                    st.error("密碼錯誤，請重新輸入。")
        st.stop()

check_password()

# --- 畫面路由控制 ---
if "current_view" not in st.session_state:
    st.session_state.current_view = "shop_list"

# --- 輔助函式：自動產生商品網格與優雅的文字佔位圖 ---
def render_placeholder(height="160px"):
    """渲染優雅的無圖片文字佔位區塊"""
    st.markdown(f"""
        <div style='height: {height}; display: flex; align-items: center; justify-content: center; 
                    background-color: rgba(255,255,255,0.2); border: 1px dashed #c4c1b8; 
                    border-radius: 4px; margin-bottom: 0.5rem;'>
            <span style='color: #a6a49c; letter-spacing: 4px; font-size: 0.9rem;'>【 影像準備中 】</span>
        </div>
    """, unsafe_allow_html=True)

def render_product_grid(filter_condition, filter_name):
    """
    filter_condition: 用來過濾商品的 lambda 函數
    filter_name: 用來確保 button key 唯一的區塊名稱
    """
    filtered_keys = [k for k, v in PRODUCTS.items() if filter_condition(v)]
    
    if not filtered_keys:
        st.markdown("*（目前本區尚無商品）*")
        return

    cols = st.columns(3)
    for idx, key in enumerate(filtered_keys):
        p = PRODUCTS[key]
        with cols[idx % 3]:
            # 若無圖片，顯示優雅的文字留白
            if os.path.exists(p["image"]):
                st.image(p["image"], use_container_width=True)
            else:
                render_placeholder()
            
            st.markdown(f"<span class='elegant-subtitle'>{p.get('sub_name', '')}</span>", unsafe_allow_html=True)
            st.markdown(f"**{p['name']}**")
            
            if st.button("賞 物", key=f"btn_{filter_name}_{key}", use_container_width=True):
                st.session_state.current_view = key
                st.rerun()

# ==========================================
# 前端介面：商品列表頁 (首頁)
# ==========================================
if st.session_state.current_view == "shop_list":
    st.markdown("<h1 style='text-align: center; font-size: 2.5rem;'>👑 王子的旅行代購</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8c8a84; letter-spacing: 2px;'>全球嚴選・品味生活</p>", unsafe_allow_html=True)
    st.divider()

    st.markdown("<span class='elegant-subtitle'>特別企劃</span>", unsafe_allow_html=True)
    st.subheader("⭐ 本月推薦")
    render_product_grid(lambda p: p.get("is_recommended", False) == True, "rec")
    
    st.divider()
    
    st.markdown("<span class='elegant-subtitle'>歐洲生活</span>", unsafe_allow_html=True)
    st.subheader("🌍 歐洲代購區")
    render_product_grid(lambda p: p["category"] == "europe", "euro")
    
    st.divider()
    
    st.markdown("<span class='elegant-subtitle'>產地直送</span>", unsafe_allow_html=True)
    st.subheader("🍎 異國水果區")
    render_product_grid(lambda p: p["category"] == "fruit", "fruit")


# ==========================================
# 前端介面：商品詳細頁
# ==========================================
elif st.session_state.current_view in PRODUCTS:
    product_key = st.session_state.current_view
    p = PRODUCTS[product_key]

    if st.button("⬅️ 返回賣場"):
        st.session_state.current_view = "shop_list"
        st.rerun()

    st.markdown(f"<span class='elegant-subtitle'>{p.get('sub_name', '')}</span>", unsafe_allow_html=True)
    st.title(p["name"])
    
    img_col, info_col = st.columns([1, 1.5])
    
    with img_col:
        if os.path.exists(p["image"]):
            st.image(p["image"], use_container_width=True)
        else:
            render_placeholder(height="300px")
        
    with info_col:
        st.markdown(f"**📝 規格：** {p['spec']}")
        st.markdown("---")
        st.markdown("💡 *歡迎私訊王子了解更多詳情與最新動態。*")

    st.divider()

    st.subheader("✨ 產品介紹")
    st.write(p["description"])

    st.subheader("📖 建議用法")
    st.markdown(p["usage"])
