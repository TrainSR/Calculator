import streamlit as st

st.markdown(
    "<h1 style='text-align: center;'>Progress Calculator</h1>",
    unsafe_allow_html=True
)

# Khởi tạo session state
if 'y' not in st.session_state:
    st.session_state.y = None
if 'logs' not in st.session_state:
    st.session_state.logs = []  # Mỗi log là tuple: (x, y, result_str)
if 'skip_first_x' not in st.session_state:
    st.session_state.skip_first_x = True 
# Sidebar để nhập giá trị y ban đầu và hiển thị y hiện tại
with st.sidebar:
    st.header("Thiết lập ban đầu")
    if st.session_state.y is None:
        y_init = st.number_input("Nhập giá trị ban đầu y", step=1, format="%d", key='y_input')
        if st.button("Xác nhận.", key="Y_INIT"):
            st.session_state.y = y_init
    else:
        st.success(f"y hiện tại: {st.session_state.y}")
if st.session_state.y is not None:
    x = st.number_input("Nhập x", step=1, format="%d", key='x_input')
    try:
        z = st.session_state.y
        result = 1 - x / st.session_state.y
        st.session_state.last_result_sign = result
        value = abs(result * 100)
        formatted_number = f"{value:.3f}".rstrip('0').rstrip('.')
        if result >= 0:
            formatted_result = f"− {formatted_number}%"
        else:
            formatted_result = f"+ {formatted_number}%"
        st.session_state.last_result = formatted_result
    except ZeroDivisionError:
        st.session_state.logs.append((x, st.session_state.y, "Lỗi: chia cho 0."))
        st.session_state.last_result_sign = None
        st.session_state.last_result = "Undefined."
    if st.session_state.skip_first_x and x == 0:
        st.session_state.skip_first_x = False   # bỏ qua đúng 1 lần
    else:
        st.session_state.logs.append((x, z, st.session_state.last_result))
        st.session_state.y = x

    # Hiển thị kết quả mới nhất riêng
    if 'last_result' in st.session_state:
        st.markdown(f"<h1 style='color: blue; text-align: center; font-size: 90px;'>{z} → {x}</h1>", unsafe_allow_html=True)
        st.subheader("Impact:")
        if 'last_result_sign' in st.session_state and st.session_state.last_result_sign is not None:
            color = 'color:lime' if st.session_state.last_result_sign >= 0 else 'color:red'
        else:
            color = 'color:black'
        st.markdown(f"<span style='{color}'>{st.session_state.last_result}</span>", unsafe_allow_html=True)

    # Lịch sử hiển thị theo định dạng x - y = ±xyz%
    if st.session_state.logs:
        with st.expander("History:"):
            logs_to_show = st.session_state.logs[:-1] if 'last_result' in st.session_state else st.session_state.logs
            for entry in reversed(logs_to_show):
                if isinstance(entry, tuple) and len(entry) == 3:
                    x_val, y_val, res = entry
                    st.write(f"{y_val} → {x_val} = {res}")
                else:
                    st.write(entry)  # fallback nếu là string
