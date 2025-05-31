import streamlit as st

st.title("Progress Calculator")

# Khởi tạo session state
if 'y' not in st.session_state:
    st.session_state.y = None
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'stopped' not in st.session_state:
    st.session_state.stopped = False

if st.session_state.y is None:
    y_init = st.number_input("Nhập giá trị ban đầu y", step=1, format="%d", key='y_input')
    if st.button("Bắt đầu"):
        if y_init == 0:
            st.write("Dừng chương trình: y = 0.")
            st.session_state.stopped = True
        else:
            st.session_state.y = y_init
else:
    if not st.session_state.stopped:
        x = st.number_input("Nhập x", step=1, format="%d", key='x_input')
    if st.button("Tiếp tục"):
        if st.session_state.y == 0:
            st.write("Dừng chương trình: y = 0.")
            st.session_state.stopped = True
        else:
            try:
                result = 1 - x / st.session_state.y
                st.session_state.last_result_sign = result  # Lưu dấu result
                value = abs(result * 100)
                formatted_number = f"{value:.3f}".rstrip('0').rstrip('.')
                if result >= 0:
                    formatted_result = f"− {formatted_number}%"
                else:
                    formatted_result = f"+ {formatted_number}%"
                st.session_state.logs.append(formatted_result)
                st.session_state.last_result = formatted_result
            except ZeroDivisionError:
                st.session_state.logs.append("Lỗi: chia cho 0.")
                st.session_state.last_result_sign = None
            st.session_state.y = x
            if x == 0:
                st.session_state.stopped = True
                st.session_state.logs.append("Dừng vòng lặp vì x = 0.")

# Hiển thị kết quả mới nhất riêng
if 'last_result' in st.session_state:
    st.markdown(f"<h1 style='color: blue; text-align: center; font-size: 90px;'>{x}</h1>", unsafe_allow_html=True)
    st.subheader("Impact:")
    if 'last_result_sign' in st.session_state and st.session_state.last_result_sign is not None:
        color = 'color:lime' if st.session_state.last_result_sign >= 0 else 'color:red'
    else:
        color = 'color:black'
    st.markdown(f"<span style='{color}'>{st.session_state.last_result}</span>", unsafe_allow_html=True)

# Lịch sử có thể ẩn/hiện và đảo thứ tự (cũ nhất ở dưới)
if 'logs' in st.session_state and st.session_state.logs:
    with st.expander("History:"):
        # Lấy lịch sử bỏ kết quả mới nhất (nếu có)
        history_logs = st.session_state.logs[:-1] if 'last_result' in st.session_state else st.session_state.logs
        # Đảo ngược thứ tự để cũ nhất ở dưới cùng
        for line in reversed(history_logs):
            st.write(line)

# Nút reset
if st.button("Reset chương trình"):
    st.session_state.y = None
    st.session_state.logs = []
    st.session_state.stopped = False
    if 'last_result' in st.session_state:
        del st.session_state.last_result
    if 'last_result_sign' in st.session_state:
        del st.session_state.last_result_sign
