import streamlit as st
import math

# -----------------------------------------------------------------------------
# 1. 디자인 설정 (BuildTech 테마 - 강제 화이트 텍스트 적용)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="레미콘 물량 계산기", page_icon="🚛")

hide_st_style = """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
            
            /* 글로벌 폰트 & 색상 강제 통일 */
            html, body, [class*="css"]  {
                font-family: 'Noto Sans KR', sans-serif;
                color: #ffffff !important;
            }
            
            /* 메인 배경 */
            .stApp {
                background-color: #1a1a1a;
            }
            
            /* 입력창 스타일 */
            .stNumberInput input {
                background-color: #333333 !important;
                color: #ffffff !important;
                font-weight: bold;
                border: 1px solid #555555;
            }
            
            /* 라벨 & 텍스트 */
            .stNumberInput label, .stSlider label {
                color: #ffffff !important;
                font-weight: bold;
                font-size: 16px;
            }
            
            /* 슬라이더 스타일 */
            div.stSlider > div[data-baseweb="slider"] > div > div {
                background-color: #0085ff !important;
            }
            
            /* 결과 박스 내부 글씨 */
            .result-box p, .result-box span, .result-box div {
                color: #ffffff !important;
            }
            .highlight-text {
                color: #0085ff !important;
                font-weight: bold;
            }
            
            /* 버튼 스타일 */
            div.stButton > button {
                background-color: #0085ff;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
                width: 100%;
                padding: 12px;
                margin-top: 10px;
            }
            div.stButton > button:hover {
                background-color: #0066cc;
                border: 2px solid #ffffff;
            }
            
            /* 결과 박스 디자인 */
            .result-box {
                background-color: #262626;
                padding: 25px;
                border-radius: 12px;
                border-left: 6px solid #0085ff;
                margin-top: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            }
            
            /* 불필요 요소 숨김 */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 타이틀
# -----------------------------------------------------------------------------
st.markdown("<h2 style='text-align: center; color: #ffffff;'>🚛 레미콘 물량 계산기</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaaaaa;'>타설 면적을 입력하면 필요한 루베와 트럭 대수를 알려드립니다.</p>", unsafe_allow_html=True)
st.write("---")

# -----------------------------------------------------------------------------
# 3. 입력 영역 (UI)
# -----------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    length = st.number_input("가로 길이 (m)", value=10.0, step=0.5, format="%.2f")
    depth = st.number_input("타설 두께 (m)", value=0.5, step=0.1, format="%.2f")

with col2:
    width = st.number_input("세로 길이 (m)", value=10.0, step=0.5, format="%.2f")
    # 레미콘 규격 (보통 6루베)
    truck_capa = st.number_input("트럭 1대 용량 (m³)", value=6.0, step=1.0, format="%.1f")

# 할증률 슬라이더
loss_rate = st.slider("할증률 (Loss) 설정 (%)", min_value=0, max_value=10, value=3, step=1)
st.caption(f"💡 보통 슬래브는 3~5%, 기초는 5~7% 할증을 권장합니다.")

# -----------------------------------------------------------------------------
# 4. 계산 로직
# -----------------------------------------------------------------------------
if st.button("물량 계산하기 🧮"):
    # 이론 물량
    vol_theory = length * width * depth
    
    # 할증 포함 필요 물량
    vol_req = vol_theory * (1 + loss_rate / 100)
    
    # 필요한 트럭 대수 (올림 처리)
    trucks_needed = math.ceil(vol_req / truck_capa)
    
    # 막차 물량 (나머지)
    last_truck_vol = vol_req % truck_capa
    if last_truck_vol == 0:
        last_truck_vol = truck_capa # 딱 떨어지면 막차도 꽉 채워서
    
    # -----------------------------------------------------------------------------
    # 5. 결과 출력
    # -----------------------------------------------------------------------------
    st.markdown(f"""
    <div class="result-box">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <span style="font-size: 18px;">총 필요 물량 (할증 {loss_rate}%)</span>
            <span class="highlight-text" style="font-size: 28px;">{vol_req:.2f} m³</span>
        </div>
        <div style="width: 100%; height: 1px; background-color: #444; margin: 10px 0;"></div>
        <div style="font-size: 20px; margin-top: 15px;">
            🚛 레미콘 트럭: <span class="highlight-text" style="font-size: 24px;">총 {trucks_needed} 대</span>
        </div>
        <div style="font-size: 16px; color: #cccccc !important; margin-top: 5px;">
            (6m³ 기준 {trucks_needed-1}대 + <span style="color: #ff4b4b !important; font-weight:bold;">막차 {last_truck_vol:.2f} m³</span>)
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 주문 멘트 생성 (복사하기 좋게)
    st.write("")
    st.info(f"📞 **주문 예시:** \"여기 현장인데요, {truck_capa}루베 차로 총 {trucks_needed}대 보내주시고, 막차는 {last_truck_vol:.1f}루베로 맞춰주세요.\"")
