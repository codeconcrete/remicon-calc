import streamlit as st
import math
import pandas as pd

# -----------------------------------------------------------------------------
# 1. 디자인 설정 (BuildTech 테마 - 강제 화이트 텍스트)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="레미콘 물량 적산기", page_icon="🚛")

hide_st_style = """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
            
            html, body, [class*="css"]  {
                font-family: 'Noto Sans KR', sans-serif;
                color: #ffffff !important;
            }
            .stApp { background-color: #1a1a1a; }
            
            /* 입력창 & 버튼 스타일 */
            .stNumberInput input, .stTextInput input {
                background-color: #333333 !important;
                color: #ffffff !important;
                font-weight: bold;
                border: 1px solid #555555;
            }
            .stNumberInput label, .stTextInput label, .stRadio label, .stSlider label {
                color: #ffffff !important;
                font-weight: bold;
            }
            .stRadio p { color: #ffffff !important; }
            
            /* 메인 버튼 (추가하기) */
            .stButton > button {
                background-color: #0085ff;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                width: 100%;
                padding: 10px;
            }
            .stButton > button:hover { background-color: #0066cc; border: 1px solid white; }
            
            /* 초기화 버튼 (빨간색 커스텀) */
            div[data-testid="stButton"] button[kind="secondary"] {
                background-color: #ff4b4b;
                color: white;
                border: none;
            }
            
            /* 결과 박스 */
            .result-box {
                background-color: #262626;
                padding: 20px;
                border-radius: 12px;
                border-left: 6px solid #0085ff;
                margin-top: 20px;
            }
            .highlight-text { color: #0085ff !important; font-weight: bold; }
            
            /* 테이블 헤더 */
            [data-testid="stDataFrame"] { background-color: #262626; }
            
            #MainMenu, footer, header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 세션 상태 초기화 (장바구니 만들기)
# -----------------------------------------------------------------------------
if 'calc_list' not in st.session_state:
    st.session_state.calc_list = []

# -----------------------------------------------------------------------------
# 3. 타이틀
# -----------------------------------------------------------------------------
st.markdown("<h3 style='color: #ffffff;'>🚛 레미콘 물량 적산기 (합산 기능)</h3>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. 입력 영역
# -----------------------------------------------------------------------------
with st.container():
    st.markdown("#### 1️⃣ 부위별 물량 입력")
    
    # 타입 선택
    col_type, col_name = st.columns([1, 2])
    with col_type:
        calc_type = st.radio("유형", ("슬래브", "옹벽"), label_visibility="collapsed")
    with col_name:
        item_name = st.text_input("부위 명칭 (예: 1층 바닥, 계단실 벽체)", placeholder="부위 이름 입력")

    col1, col2, col3 = st.columns(3)
    
    # 입력 라벨 동적 변경
    if calc_type == "슬래브":
        lbl1, lbl2, lbl3 = "가로 (m)", "세로 (m)", "두께 (m)"
    else:
        lbl1, lbl2, lbl3 = "벽 길이 (m)", "벽 높이 (m)", "벽 두께 (m)"

    with col1:
        dim1 = st.number_input(lbl1, value=0.0, step=0.5, format="%.2f", key="d1")
    with col2:
        dim2 = st.number_input(lbl2, value=0.0, step=0.5, format="%.2f", key="d2")
    with col3:
        dim3 = st.number_input(lbl3, value=0.0, step=0.1, format="%.2f", key="d3")

    # [추가하기] 버튼
    if st.button("➕ 리스트에 추가 (Add)"):
        if dim1 > 0 and dim2 > 0 and dim3 > 0:
            vol = dim1 * dim2 * dim3
            # 명칭이 없으면 자동 생성
            if not item_name:
                item_name = f"{calc_type} ({len(st.session_state.calc_list)+1})"
            
            # 장바구니에 담기
            st.session_state.calc_list.append({
                "부위명": item_name,
                "유형": calc_type,
                "물량(m³)": round(vol, 2),
                "규격": f"{dim1}x{dim2}x{dim3}"
            })
            st.toast(f"✅ '{item_name}' 추가 완료!")
        else:
            st.error("치수를 모두 입력해주세요.")

# -----------------------------------------------------------------------------
# 5. 리스트 확인 및 결과 출력
# -----------------------------------------------------------------------------
st.write("---")
st.markdown("#### 2️⃣ 계산 내역 및 총괄표")

# 리스트가 있을 때만 표시
if len(st.session_state.calc_list) > 0:
    # 데이터프레임으로 변환하여 보여주기
    df = pd.DataFrame(st.session_state.calc_list)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # 총 합계 계산
    total_vol_theory = df["물량(m³)"].sum()

    # 옵션 설정 (할증 & 트럭)
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        loss_rate = st.slider("할증률 (Loss) %", 0, 15, 3)
    with col_opt2:
        truck_capa = st.number_input("트럭 용량 (m³)", value=6.0, step=1.0)

    # 최종 계산
    final_vol = total_vol_theory * (1 + loss_rate / 100)
    trucks_needed = math.ceil(final_vol / truck_capa)
    last_truck_vol = final_vol % truck_capa
    if last_truck_vol == 0 and final_vol > 0:
        last_truck_vol = truck_capa

    # 결과 박스
    st.markdown(f"""
    <div class="result-box">
        <div style="font-size: 18px; margin-bottom:5px;">총 타설 물량 (할증 {loss_rate}%)</div>
        <div class="highlight-text" style="font-size: 32px; margin-bottom: 15px;">{final_vol:.2f} m³</div>
        <div style="border-top: 1px solid #555; padding-top: 15px; font-size: 20px;">
            🚛 필요 대수: <span style="color:#ffffff; font-weight:bold;">{trucks_needed} 대</span>
        </div>
        <div style="font-size: 14px; color: #cccccc !important;">
            (막차 {last_truck_vol:.2f} m³ / {truck_capa}루베 기준)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 위 계산 내역은 새로고침하면 사라질 수 있습니다.")

else:
    st.info("👆 위에서 치수를 입력하고 [추가] 버튼을 눌러주세요.")

# -----------------------------------------------------------------------------
# 6. 초기화 버튼
# -----------------------------------------------------------------------------
st.write("")
if st.button("🗑️ 모두 지우기 (초기화)", type="secondary"):
    st.session_state.calc_list = []
    st.rerun()
