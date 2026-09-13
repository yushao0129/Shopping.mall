import streamlit as st
import os

# --- 網頁外觀設定 (日式低奢風格) ---
st.set_page_config(page_title="王子的旅行代購", page_icon="👑", layout="centered")

st.markdown("""
    
""", unsafe_allow_html=True)


# --- 產品資料庫 ---
PRODUCTS = {
    "golden_goose_liver": {
        "name": "匈牙利經典金鵝肝",
        "sub_name": "歐洲餐桌上的奢華美味",
        "image": "goose1.JPG",
        "detail_image": "goose2.JPG",
        "category": "europe",
        "is_recommended": True,
        "description": "匈牙利經典伴手禮！細緻滑順、濃郁香醇，傳承歐洲經典工藝。開罐即可享用，是老饕佐餐與品味生活的頂級饗宴。",
        "usage": "- **搭配食用**：開罐即食，塗抹於烤法式麵包、脆餅上風味絕佳。\n- **餐酒搭配**：適合佐以甜白酒、香檳或精選紅酒。"
    },
    "pumpkin_seed_oil": {
        "name": "匈牙利天然南瓜籽油",
        "sub_name": "男女都適合・每天一匙日常保養",
        "image": "oil1.JPG",
        "detail_image": "oil2.JPG",
        "category": "europe",
        "is_recommended": True,
        "description": "匈牙利純淨天然萃取南瓜籽油。男性保養有助於維持順暢、夜間舒適；女性保養提供夜間少打擾、自在舒適與安穩睡眠。保健食品非藥品，日常保養首選。",
        "usage": "- **日常保養**：每天一匙，直接飲用或隨餐攝取。\n- **輕食料理**：可淋於生菜沙拉、溫熱湯品中增添堅果香氣。"
    },
    "truffle_sauce": {
        "name": "匈牙利精品白黑松露醬",
        "sub_name": "一小匙・讓料理瞬間升級",
        "image": "truffle1.JPG",
        "detail_image": "truffle2.JPG",
        "category": "europe",
        "is_recommended": True,
        "description": "嚴選珍稀白黑松露調配，擁有極致濃郁的松露芬芳。冷熱料理皆適合，無需複雜烹煮，直接加入即可為餐點注入頂級靈魂。",
        "usage": "- **拌麵佐醬**：直接拌入義大利麵、燉飯提升層次。\n- **佐餐抹醬**：塗抹於法棍切片、烘烤麵包。\n- **排餐點綴**：搭配香煎牛排、羊排等肉類料理。"
    },
    "china_oel": {
        "name": "德國百靈油",
        "sub_name": "德國經典百年秘方",
        "image": "oel1.JPG",
        "category": "europe",
        "is_recommended": False,
        "description": "由純薄荷精油提煉而成的德國經典百年秘方，清心醒腦、順暢呼吸，能有效舒緩日常不適，是家庭必備的萬用良品。＊附贈3瓶鼻吸、分裝吸管和隨身滾珠瓶",
        "usage": "- **外用塗抹**：取適量塗抹於額頭、太陽穴或緊繃肩頸。\n- **吸入蒸氣**：滴於溫熱水中吸入清爽薄荷蒸氣。\n- **搭配隨身配件**：可裝入滾珠瓶隨身攜帶，或搭配專用鼻吸入器使用。"
    },
    "norway_selolje": {
        "name": "挪威頂級深海海豹油",
        "sub_name": "來自北大西洋的純淨海洋力量",
        "image": "selolje1.JPG",
        "category": "europe",
        "is_recommended": False,
        "description": "萃取自純淨無污染的北大西洋海域，富含 Omega-3（含 EPA、DHA、DPA）及多元脂肪酸與維生素 D3，滋養每一個重要的日常，有助於保持活力、延緩衰老與改善睡眠品質。",
        "usage": "- **日常保健**：每日定時隨餐食用，補充純淨天然營養。\n- **保存方式**：請存放於陰涼乾燥處，避免陽光直射與潮濕。"
    }
}

# --- 密碼驗證區 ---
def check_password():
    SECRET_PIN = "1234"

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("
