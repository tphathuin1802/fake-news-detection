import streamlit as st

# Tiêu đề ứng dụng
st.title("Ứng dụng phát hiện tin giả")

# Trường nhập văn bản cho người dùng
user_input = st.text_area("Nhập nội dung bài báo vào đây:")

# Nút để gửi dự đoán
if st.button("Kiểm tra"):
    if user_input:
        # (Bước tiếp theo: Tải mô hình và thực hiện dự đoán ở đây)
        st.write("Đang xử lý...") # Placeholder
    else:
        st.write("Vui lòng nhập nội dung bài báo.") 