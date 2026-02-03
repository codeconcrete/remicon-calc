import streamlit as st
import math
import pandas as pd

# -----------------------------------------------------------------------------
# 1. 디자인 설정 (모바일 최적화 + 강제 화이트)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="레미콘 적산기", page_icon="🚛", layout="centered")

hide_st_style = """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
            
            /* [모바일 최적화] 좌우 여백 줄이기 */
            .block-container {
                padding-top: 2rem;
                padding-bottom: 5rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }

            /* [색상 강제 통일] 모든 글씨 무조건 흰색 */
            html, body, [class*="css"], div, span, p, label, h1, h2, h3, h4, h5, h6 {
                font-family: 'Noto Sans KR', sans-serif;
                color: #ffffff !important;
            }
            
            /* 메인 배경색 */
            .stApp { background-color: #1a1a1a; }
            
            /* [입력창 스타일] 글씨 흰색 + 배경 진회색 */
            .stTextInput input, .stNumberInput input {
                background-color: #333333 !important;
                color: #ffffff !important; 
                font-weight: bold;
                border: 1px solid #555555;
            }

            /* ★★★ [핵심] 플레이스홀더(입력 전 흐린 글씨)도 흰색으로! ★★★ */
            ::placeholder {
                color: #cccccc !important; /* 약간 연한 흰색 */
                opacity: 1; /* 투명도 제거 */
            }
            
            /* 라디오 버튼 선택 항목 */
            .stRadio div[role='radiogroup'] > label {
                color: #ffffff !important;
                font-weight: bold;
            }
            
            /* [버튼 스타일] 모바일에서 누르기 좋게 큼직하게 */
            div.stButton > button {
                background-color: #0085ff;
                color: white !important;
                border: none;
                border-radius: 12px; /* 둥글게 */
                font-size: 18px;
                font-weight: bold;
                width: 100%;
                padding: 15px 0; /* 위아래 폭 키움 */
                margin-top: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            }
            div.stButton > button:hover {
                background-color: #0066cc;
                border: 1px solid #ffffff;
            }
            
            /* 초기화 버튼 (빨간색) */
            div[data-testid="stButton"] button[kind="secondary"] {
                background-color: #ff4b4b;
            }
            
            /* 결과 박스 디자인 */
            .result-box {
                background-color: #262626;
                padding: 20px;
                border-radius: 12px;
                border: 1px solid #444;
                border-left: 6px solid #0085ff;
                margin-top: 20px;
            }
            
            /* 데이터프레임(표) 스타일 */
            [data-testid="stDataFrame"] { background-color: #262626; }
            
            /* 안내 문구 박스 (Info) 스타일 재정의 */
            .stAlert {
                background-color: #222222 !important;
                color: #ffffff !important;
                border: 1px solid #444;
            }
            
            /* 불필요한 헤더 숨김 */
            #MainMenu, footer, header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 세션 상태 (장바구니)
# -----------------------------------------------------------------------------
if 'calc_list' not in st.session_state:
    st.session_state.calc_list = []

# -----------------------------------------------------------------------------
# 3. 타이틀
# -----------------------------------------------------------------------------
st.markdown("<h3 style='text-align:center;'>🚛 레미콘 물량 적산기</h3>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. 입력 영역 (모바일 레이아웃)
# -----------------------------------------------------------------------------
with st.container():
    # 라디오 버튼 가로 배치
    calc_type = st.radio("구조물 유형", ("슬래브 (바닥/기초)", "옹벽 (벽체)"), label_visibility="collapsed", horizontal=True)
    
    st.write("") # 간격

    # 부위 명칭 입력 (플레이스홀더 회색 문제 해결됨)
    item_name = st.text_input("어디 타설하나요?", placeholder="예: 101동 1층 바닥 (입력 안 해도 됨)")

    st.write("") # 간격

    # 3단 컬럼 (모바일에서는 자동으로 좁아지거나 줄바꿈됨)
    col1, col2, col3 = st.columns(3)
    
    # 유형에 따라 라벨 변경
    if "슬래브" in calc_type:
        l1, l2, l3 = "가로(m)", "세로(m)", "두께(m)"
    else:
        l1, l2, l3 = "벽길이(m)", "벽높이(m)", "벽두께(m)"

    with col1:
        dim1 = st.number_input(l1, value=0.0, step=0.5, format="%.2f", key="d1")
    with col2:
        dim2 = st.number_input(l2, value=0.0, step=0.5, format="%.2f", key="d2")
    with col3:
        dim3 = st.number_input(l3, value=0.0, step=0.1, format="%.2f", key="d3")

    # 추가 버튼 (왕 버튼)
    if st.button("➕ 리스트에 추가하기", use_container_width=True):
        if dim1 > 0 and dim2 > 0 and dim3 > 0:
            vol = dim1 * dim2 * dim3
            
            # 이름 없으면 자동 생성
            if not item_name:
                short_type = "슬래브" if "슬래브" in calc_type else "옹벽"
                item_name = f"{short_type}-{len(st.session_state.calc_list)+1}"
            
            st.session_state.calc_list.append({
                "부위": item_name,
                "물량(m³)": round(vol, 2),
                "규격": f"{dim1}x{dim2}x{dim3}"
            })
            st.toast(f"✅ '{item_name}' 추가됨!")
        else:
            st.error("치수를 입력해주세요!")

# -----------------------------------------------------------------------------
# 5. 결과 리스트 & 총괄표
# -----------------------------------------------------------------------------
st.write("---")

if len(st.session_state.calc_list) > 0:
    st.markdown("##### 📋 계산 내역")
    
    # 데이터프레임 (표)
    df = pd.DataFrame(st.session_state.calc_list)
    st.dataframe(df, use_container_width=True, hide_index=True)

    total_vol_theory = df["물량(m³)"].sum()

    st.write("")
    # 할증률 & 트럭 용량 (2단 배치)
    c_opt1, c_opt2 = st.columns(2)
    with c_opt1:
        loss_rate = st.slider("할증률(%)", 0, 15, 3)
    with c_opt2:
        truck_capa = st.number_input("차량용량(m³)", value=6.0, step=1.0)

    # 최종 계산
    final_vol = total_vol_theory * (1 + loss_rate / 100)
    trucks_needed = math.ceil(final_vol / truck_capa)
    last_truck_vol = final_vol % truck_capa
    if last_truck_vol == 0 and final_vol > 0:
        last_truck_vol = truck_capa

    # 결과 박스 (폰트 크기 조절)
    st.markdown(f"""
    <div class="result-box">
        <div style="font-size: 16px;">총 타설 물량 (Loss {loss_rate}%)</div>
        <div style="font-size: 36px; font-weight:bold; color:#0085ff !important; margin: 10px 0;">
            {final_vol:.2f} m³
        </div>
        <div style="border-top: 1px solid #555; padding-top: 10px;">
            <span style="font-size: 20px;">🚛 필요 대수: </span>
            <span style="font-size: 24px; font-weight:bold; color:#ffffff !important;">{trucks_needed} 대</span>
        </div>
        <div style="font-size: 14px; color: #cccccc !important; margin-top:5px;">
            (막차 {last_truck_vol:.2f}루베 / {truck_capa}루베 차)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.info("💡 새로고침하면 내역이 사라지니 주의하세요.")

else:
    # 데이터 없을 때 안내 문구 (회색 -> 흰색 변경됨)
    st.info("👆 위 칸에 치수를 입력하고 [추가하기] 버튼을 눌러주세요.")

# -----------------------------------------------------------------------------
# 6. 초기화 버튼
# -----------------------------------------------------------------------------
st.write("")
st.write("")
if st.button("🗑️ 초기화 (새로 하기)", type="secondary", use_container_width=True):
    st.session_state.calc_list = []
    st.rerun()
