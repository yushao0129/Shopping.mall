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


# --- 產品資料庫 (全數更新為最新推薦產品) ---
PRODUCTS = {
    "golden_goose_liver": {
        "name": "匈牙利經典金鵝肝",
        "sub_name": "歐洲餐桌上的奢華美味",
        "image": "goose.png",
        "category": "europe",
        "is_recommended": True,
        "spec": "容量：100公克／罐 | 團員限定價：€ 25",
        "description": "匈牙利經典伴手禮！細緻滑順、濃郁香醇，傳承歐洲經典工藝。開罐即可享用，是老饕佐餐與品味生活的頂級饗宴。",
        "usage": "- **搭配食用**：開罐即食，塗抹於烤法式麵包、脆餅上風味絕佳。\n- **餐酒搭配**：適合佐以甜白酒、香檳或精選紅酒。"
    },
    "pumpkin_seed_oil": {
        "name": "匈牙利天然南瓜籽油",
        "sub_name": "男女都適合・每天一匙日常保養",
        "image": "oil.png",
        "category": "europe",
        "is_recommended": True,
        "spec": "容量：100毫升／罐 | 團員限定價：€ 22",
        "description": "匈牙利純淨天然萃取南瓜籽油。男性保養有助於維持順暢、夜間舒適；女性保養提供夜間少打擾、自在舒適與安穩睡眠。保健食品非藥品，日常保養首選。",
        "usage": "- **日常保養**：每天一匙，直接飲用或隨餐攝取。\n- **輕食料理**：可淋於生菜沙拉、溫熱湯品中增添堅果香氣。"
    },
    "truffle_sauce": {
        "name": "匈牙利精品白黑松露醬",
        "sub_name": "一小匙・讓料理瞬間升級",
        "image": "truffle.png",
        "category": "europe",
        "is_recommended": True,
        "spec": "容量：90公克／罐 | 團員限定價：€ 18",
        "description": "嚴選珍稀白黑松露調配，擁有極致濃郁的松露芬芳。冷熱料理皆適合，無需複雜烹煮，直接加入即可為餐點注入頂級靈魂。",
        "usage": "- **拌麵佐醬**：直接拌入義大利麵、燉飯提升層次。\n- **佐餐抹醬**：塗抹於法棍切片、烘烤麵包。\n- **排餐點綴**：搭配香煎牛排、羊排等肉類料理。"
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

    # 增加 apples.jpeg 於產品介紹中
    if os.path.exists("apples.jpeg"):
        st.image("apples.jpeg", use_container_width=True)
    else:
        render_placeholder(height="240px")

    st.subheader("📖 建議用法")
    st.markdown(p["usage"])
