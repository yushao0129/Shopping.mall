import streamlit as st
import os
import smtplib
import json
import urllib.request
from datetime import datetime
from email.mime.text import MIMEText
from email.header import Header
from zoneinfo import ZoneInfo

# --- 網頁外觀設定 (日式低奢風格) ---
st.set_page_config(page_title="王子的好物清單", page_icon="👑", layout="centered")

st.markdown("""
    <style>
    /* 導入思源明體以增加高級感 */
    @import url('[https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;600&display=swap](https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;600&display=swap)');
    
    .stApp {
        /* 日式宣紙紋理 + 頂部微光漸層 */
        background-color: #f7f5f0;
        background-image: 
            radial-gradient(circle at 50% 0%, rgba(255, 255, 255, 0.8) 0%, rgba(255, 255, 255, 0) 60%),
            url('[https://www.transparenttextures.com/patterns/rice-paper-2.png](https://www.transparenttextures.com/patterns/rice-paper-2.png)');
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
    .stButton>button, .stFormSubmitButton>button {
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
    .stButton>button:hover, .stFormSubmitButton>button:hover {
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
    
    /* 首頁商品名稱清單（不顯示圖片） */
    div[class*="st-key-list_"] .stButton>button {
        background-color: rgba(255, 255, 255, 0.6);
        color: #3b3a37;
        border: 1px solid #e4e0d6;
        justify-content: flex-start;
        text-align: left;
        padding: 0.7rem 1rem;
        margin-top: 0;
    }
    div[class*="st-key-list_"] .stButton>button:hover {
        background-color: #3b3a37;
        color: #f7f5f0;
    }
    div[class*="st-key-list_"] .stButton>button div,
    div[class*="st-key-list_"] .stButton>button p {
        text-align: left;
        width: 100%;
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


# --- 產品資料庫 ---
PRODUCTS = {
"golden_goose_liver": {
        "name": "🇭🇺匈牙利經典金鵝肝",
        "sub_name": "歐洲餐桌上的奢華美味",
        "image": "goose1.JPG",
        "detail_image": "goose2.JPG",
        "category": "food",
        "is_recommended": True,
        "description": "匈牙利經典伴手禮！細緻滑順、濃郁香醇，傳承歐洲經典工藝。開罐即可享用，是老饕佐餐與品味生活的頂級饗宴。",
        "usage": "- **搭配食用**：開罐即食，塗抹於烤法式麵包、脆餅上風味絕佳。\n- **餐酒搭配**：適合佐以甜白酒、香檳或精選紅酒。"
    },
    "pumpkin_seed_oil": {
        "name": "🇭🇺匈牙利天然南瓜籽油",
        "sub_name": "男女適合，每天一匙日常保養",
        "image": "oil1.JPG",
        "detail_image": "oil2.JPG",
        "category": "food",
        "is_recommended": True,
        "description": "匈牙利純淨天然萃取南瓜籽油。男性保養有助於維持順暢、夜間舒適；女性保養提供夜間少打擾、自在舒適與安穩睡眠。保健食品非藥品，日常保養首選。",
        "usage": "- **日常保養**：每天一匙，直接飲用或隨餐攝取。\n- **輕食料理**：可淋於生菜沙拉、溫熱湯品中增添堅果香氣。"
    },
    "truffle_sauce": {
        "name": "🇭🇺匈牙利精品白黑松露醬",
        "sub_name": "一小匙，讓料理瞬間升級",
        "image": "truffle1.JPG",
        "detail_image": "truffle2.JPG",
        "category": "food",
        "is_recommended": True,
        "description": "嚴選珍稀白黑松露調配，擁有極致濃郁的松露芬芳。冷熱料理皆適合，無需複雜烹煮，直接加入即可為餐點注入頂級靈魂。",
        "usage": "- **拌麵佐醬**：直接拌入義大利麵、燉飯提升層次。\n- **佐餐抹醬**：塗抹於法棍切片、烘烤麵包。\n- **排餐點綴**：搭配香煎牛排、羊排等肉類料理。"
    },
    "china_oel": {
        "name": "🇩🇪德國百靈油",
        "sub_name": "德國經典百年秘方",
        "image": "oel1.jpg",
        "detail_image": "oel2.JPG",
        "category": "health",
        "is_recommended": False,
        "description": "由純薄荷精油提煉而成的德國經典百年秘方，清心醒腦、順暢呼吸，能有效舒緩日常不適，是家庭必備的萬用良品。＊附贈3瓶鼻吸、分裝吸管和隨身滾珠瓶",
        "usage": "- **外用塗抹**：取適量塗抹於額頭、太陽穴或緊繃肩頸。\n- **吸入蒸氣**：滴於溫熱水中吸入清爽薄荷蒸氣。\n- **搭配隨身配件**：可裝入滾珠瓶隨身攜帶，或搭配專用鼻吸入器使用。"
    },
    "norway_selolje": {
        "name": "🇳🇴挪威頂級深海海豹油",
        "sub_name": "來自北大西洋的純淨海洋力量",
        "image": "selolje1.JPG",
        "detail_image": "selolje2.PNG",
        "category": "health",
        "is_recommended": False,
        "description": "萃取自純淨無污染的北大西洋海域，富含 Omega-3（含 EPA、DHA、DPA）及多元脂肪酸與維生素 D3，滋養每一個重要的日常，有助於保持活力、延緩衰老與改善睡眠品質。",
        "usage": "- **日常保健**：每日2粒隨正餐食用，補充純淨天然營養。\n- **保存方式**：請存放於陰涼乾燥處，避免陽光直射與潮濕。"
   
},
"blueberry": {
    "name": "🇳🇴挪威藍莓護眼膠囊",
    "sub_name": "藍莓萃取，花青素，維生素C",
    "image": "blue.PNG",
    "detail_image": "blue2.PNG",
    "category": "health",
    "is_recommended": False,
    "description": "👁️ 守護靈魂之窗：\n花青素具有抗氧化能力，可協助減少自由基造成的氧化壓力。\n\n👁️ 舒緩長時間用眼：\n適合長時間看手機、電腦、開車及閱讀族群。\n\n👁️ 維持視覺健康：\n花青素與維生素C共同提供抗氧化保護，有助維持眼睛健康。\n\n👁️ 日常保養：\n適合作為每天的營養補充，幫助維持正常生理機能。",
    "usage": "- **日常補充**：每日早晚2粒。\n- **隨餐食用**：可搭配日常餐食一起補充。\n- **保存方式**：請置於陰涼乾燥處，避免陽光直射與高溫潮濕。"
},
"lerbolario_serum": {
    "name": "🇮🇹蕾莉歐海藻多元植物精華保濕液 50mL",
    "sub_name": "海藻萃取，清爽保濕",
    "image": "serum1.jpg",
    "detail_image": "serum2.jpg",
    "category": "skincare",
    "is_recommended": False,
    "description": "義大利蕾莉歐（L'ERBOLARIO）抗時光系列多元精華。海藻萃取，清爽保濕，搭配植物水解蛋白與複合維他命，質地輕盈好吸收，給肌膚即時的緊緻與水潤感。",
    "usage": "- **使用時機**：使用調理滋養液後。\n- **使用方式**：取適量均勻塗抹於臉部、眼周及頸部。"
},
"angel_tears_serum": {
    "name": "🇮🇹蕾利歐 天使之淚保濕精華露 30mL",
    "sub_name": "絲絨般的柔滑觸感",
    "image": "angel1.jpg",
    "detail_image": "angel2.jpg",
    "category": "skincare",
    "is_recommended": False,
    "description": "義大利米蘭 INCAROSE 珍貴精華系列。蘋果細胞萃取搭配玻尿酸鈉，質地如絲絨般柔滑，輕盈好吸收，為肌膚帶來細緻水潤的保濕感。",
    "usage": "- **使用方式**：每日潔膚後，取適量塗抹全臉，輕柔按摩至吸收。\n- **後續保養**：等待 1～2 分鐘，再進行後續保養。"
},
"black_rose_oil": {
    "name": "🇮🇹威尼斯秘密花園之黑玫瑰極速抗老精華油 30mL",
    "sub_name": "黑玫瑰香氛，滋養肌膚光澤",
    "image": "rose1.jpg",
    "detail_image": "rose2.jpg",
    "category": "skincare",
    "is_recommended": False,
    "description": "來自義大利威尼斯 SEGRETI DI BELLEZZA 的秘密花園系列（VELVET BLACK ROSE）。珍貴黑玫瑰乾爽精華油，散發迷人黑玫瑰香氛，蘊含 Omega 3、6、9 脂肪酸，滋養肌膚、提升光澤。",
    "usage": "- **使用方式**：早晚取數滴，於掌心輕輕搓暖，再輕抹臉部與頸部。\n- **注意事項**：請避開眼周。"
},
"botanicus_rose_mask": {
    "name": "🇨🇿菠丹妮奧圖玫瑰美白面膜 100g",
    "sub_name": "玫瑰精油 × 乳木果油",
    "image": "mask1.jpg",
    "detail_image": "mask2.jpg",
    "category": "skincare",
    "is_recommended": False,
    "description": "捷克菠丹妮（BOTANICUS）玫瑰系列。蘊含奧圖玫瑰精油與乳木果油，滋潤乾燥肌膚，留下柔嫩觸感。免沖洗設計，簡單完成居家保養。",
    "usage": "- **使用頻率**：每週 2 次。\n- **使用方式**：潔膚後均勻塗抹，避開眼周與唇周。\n- **免沖洗**：靜敷 20 分鐘後，將剩餘面膜輕輕按摩至吸收即可。"
},
"polarvita_omega3": {
    "name": "🇳🇴Polarvita 挪威高濃度深海魚油 90粒",
    "sub_name": "新配方，每2粒含 Omega-3 870mg",
    "image": "omega1.jpg",
    "detail_image": "omega2.jpg",
    "category": "health",
    "is_recommended": False,
    "description": "Polarvita 新配方高濃度深海魚油（DEEP SEA OMEGA-3）。每 2 粒含 Omega-3 870 mg，其中 DHA 480 mg、EPA 360 mg，並搭配 FloraGLO 葉黃素與多種維生素，一次補足日常所需營養。每瓶 90 粒。",
    "usage": "- **日常補充**：每日 2 粒。\n- **食用時間**：建議餐後食用。\n- **保存方式**：請置於陰涼乾燥處，避免陽光直射與高溫潮濕。"
},
"shar_doctor_seabuckthorn": {
    "name": "🇲🇳Shar Doctor 蒙古純沙棘果油 100mL",
    "sub_name": "100% 沙棘果肉油，蒙古製造",
    "image": "seabuck1.jpg",
    "detail_image": "seabuck2.jpg",
    "category": "health",
    "is_recommended": False,
    "description": "來自蒙古草原的 Shar Doctor 純沙棘果油，100% 沙棘果肉油，蒙古製造。含 Omega-7、Omega-6、Omega-3 脂肪酸，是日常保養的天然好選擇。",
    "usage": "- **建議食用**：每次 1 茶匙，每日 2～3 次。\n- **食用時間**：可於餐前或餐後 30 分鐘食用。"
},
"aomori_kougyoku_apple": {
    "name": "🇯🇵日本青森空運紅顏姬蘋果 每箱36粒",
    "sub_name": "果肉爽脆，入口清甜",
    "image": "fuji1.jpg",
    "detail_image": "fuji2.jpg",
    "category": "fruit",
    "is_recommended": False,
    "description": "日本青森產地直送，空運來台的紅顏姬蘋果。果肉爽脆、入口清甜，洗淨切片即可連皮享用。每箱 36 粒。",
    "usage": "- **享用方式**：洗淨切片，可連皮享用。\n- **保存小提醒**：整箱分裝時，逐顆以廚房紙巾包好，再裝袋封口冷藏。"
},
    
}

# --- 密碼驗證區 ---
def check_password():
    SECRET_PIN = "1234"

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("<h1 style='text-align: center; margin-top: 15vh; font-size: 2.5rem;'>👑 王子的好物清單</h1>", unsafe_allow_html=True)
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

def send_order_email(product_name, customer_name, quantity, phone, delivery, address):
    """把訂單寄到 secrets 裡設定的收件信箱（立即寄送）"""
    cfg = st.secrets["email"]
    order_time = datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y-%m-%d %H:%M")

    body = (
        "王子的好物清單：收到一筆新訂單\n"
        "------------------------------\n"
        f"商品：{product_name}\n"
        f"數量：{quantity}\n"
        f"訂購人：{customer_name}\n"
        f"聯絡電話：{phone}\n"
        f"取貨方式：{delivery}\n"
        f"收件地址：{address or '（現場取貨，免填）'}\n"
        f"時間：{order_time}\n"
    )
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = Header(f"【新訂單】{product_name} × {quantity}（{customer_name}）", "utf-8")
    msg["From"] = cfg["sender"]
    msg["To"] = cfg["receiver"]

    server_host = cfg.get("smtp_server", "smtp.gmail.com")
    server_port = int(cfg.get("smtp_port", 465))
    with smtplib.SMTP_SSL(server_host, server_port, timeout=20) as server:
        server.login(cfg["sender"], cfg["app_password"])
        server.send_message(msg)


def save_order_to_sheet(product_name, customer_name, quantity, phone, delivery, address):
    """把訂單存進 Google 試算表（由 Apps Script 每 4 小時彙整寄一封信）"""
    cfg = st.secrets["order_sheet"]
    payload = json.dumps({
        "token": cfg["token"],
        "time": datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y-%m-%d %H:%M"),
        "product": product_name,
        "quantity": quantity,
        "name": customer_name,
        "phone": phone,
        "delivery": delivery,
        "address": address,
    }).encode("utf-8")
    req = urllib.request.Request(cfg["url"], data=payload,
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=20) as resp:
        result = resp.read().decode("utf-8")
    if "OK" not in result:
        raise RuntimeError(f"試算表回應異常：{result[:200]}")


def submit_order(*order):
    """
    有設定 [order_sheet] 時：訂單先存進試算表，每 4 小時彙整成一封信。
    沒設定或試算表失敗時：改成立即寄信，確保訂單不會遺失。
    """
    try:
        save_order_to_sheet(*order)
        return
    except Exception:
        pass  # 沒設定試算表或存檔失敗 → 改走立即寄信
    send_order_email(*order)


def render_order_form(product_key, product_name):
    """商品詳細頁底部的訂購表單"""
    st.divider()
    st.subheader("🛒 訂購表單")

    with st.form(f"order_form_{product_key}", clear_on_submit=True):
        customer_name = st.text_input("訂購人姓名", placeholder="請輸入您的姓名")
        phone = st.text_input("聯絡電話", placeholder="例如 0912-345-678")
        delivery = st.radio("取貨方式", ["現場取貨", "宅配到府"], horizontal=True)
        address = st.text_input("收件地址（選擇宅配到府才需填寫）", placeholder="現場取貨可留空")
        quantity = st.number_input("訂購數量", min_value=1, max_value=99, value=1, step=1)
        submitted = st.form_submit_button("送 出 訂 單", use_container_width=True)

    if submitted:
        customer_name = customer_name.strip()
        phone = phone.strip()
        address = address.strip()
        phone_digits = "".join(ch for ch in phone if ch.isdigit())

        missing = [label for label, value in
                   (("訂購人姓名", customer_name), ("聯絡電話", phone)) if not value]
        if delivery == "宅配到府" and not address:
            missing.append("收件地址（宅配到府需填寫）")
        if missing:
            st.error(f"請填寫：{'、'.join(missing)}。")
            return
        if not (8 <= len(phone_digits) <= 15) or any(ch not in "0123456789-+() " for ch in phone):
            st.error("聯絡電話格式不正確，請重新確認。")
            return
        try:
            submit_order(product_name, customer_name, int(quantity), phone, delivery, address)
        except (KeyError, FileNotFoundError):
            st.error("訂單系統尚未設定寄件信箱，請聯繫管理員。")
        except Exception:
            st.error("訂單送出失敗，請稍後再試。")
        else:
            st.success(f"感謝 {customer_name}！已收到您的訂單：{product_name} × {int(quantity)}（{delivery}）。")


def render_product_grid(filter_condition, filter_name):
    """
    首頁只列出商品名稱，點擊後進入詳細頁看圖片與介紹。
    filter_condition: 用來過濾商品的 lambda 函數
    filter_name: 用來確保 button key 唯一的區塊名稱
    """
    filtered_keys = [k for k, v in PRODUCTS.items() if filter_condition(v)]

    if not filtered_keys:
        st.markdown("*（目前本區尚無商品）*")
        return

    with st.container(key=f"list_{filter_name}"):
        for key in filtered_keys:
            p = PRODUCTS[key]
            if st.button(f"{p['name']}　›", key=f"btn_{filter_name}_{key}", use_container_width=True):
                st.session_state.current_view = key
                st.rerun()

# ==========================================
# 前端介面：商品列表頁 (首頁)
# ==========================================
if st.session_state.current_view == "shop_list":
    st.markdown("<h1 style='text-align: center; font-size: 2.5rem;'>👑 王子的好物清單</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8c8a84; letter-spacing: 2px;'>全球嚴選・品味生活</p>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("<span class='elegant-subtitle'>日常保健</span>", unsafe_allow_html=True)
    st.subheader("💊 保健品區")
    render_product_grid(lambda p: p["category"] == "health", "health")

    st.divider()

    st.markdown("<span class='elegant-subtitle'>餐桌美味</span>", unsafe_allow_html=True)
    st.subheader("🍽️ 食品區")
    render_product_grid(lambda p: p["category"] == "food", "food")

    st.divider()

    st.markdown("<span class='elegant-subtitle'>美肌保養</span>", unsafe_allow_html=True)
    st.subheader("🌸 保養品區")
    render_product_grid(lambda p: p["category"] == "skincare", "skincare")
    
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
        

    st.divider()

    st.subheader("✨ 產品介紹")
    st.write(p["description"])

    # 若商品有設定產品介紹補充圖，且檔案存在時自動顯示
    if "detail_image" in p:
        if os.path.exists(p["detail_image"]):
            st.image(p["detail_image"], use_container_width=True)
        else:
            render_placeholder(height="240px")

    st.subheader("📖 建議用法")
    st.markdown(p["usage"])

    render_order_form(product_key, p["name"])
