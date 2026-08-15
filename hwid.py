from flask import Flask, request, jsonify

app = Flask(__name__)

# Cơ sở dữ liệu Key mô phỏng
DATABASE_KEYS = {
    "CUCTAY-EX-V20-VIP": {
        "hwid": None,  # Chưa kích hoạt
        "expire_date": "2026-12-31",
        "active": True
    }
}

# Màn hình trang chủ Web khi vào http://127.0.0.1:5000
@app.route('/')
def home():
    return "<h1>Server Key & HWID Validator - Status: ONLINE 🟢</h1>"

# API nhận Request xác thực từ App Client
@app.route('/verify', methods=['POST'])
def verify_key():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "Dữ liệu gửi lên không hợp lệ!"}), 400

    user_key = data.get("key")
    user_hwid = data.get("hwid")

    # 1. Kiểm tra Key có tồn tại không
    if user_key not in DATABASE_KEYS:
        return jsonify({"status": "error", "message": "Key không tồn tại!"}), 400

    key_info = DATABASE_KEYS[user_key]

    # 2. Kiểm tra Key có bị khóa không
    if not key_info["active"]:
        return jsonify({"status": "error", "message": "Key đã bị khóa!"}), 400

    # 3. Lần đầu sử dụng -> Lưu HWID máy người dùng vào Key
    if key_info["hwid"] is None:
        key_info["hwid"] = user_hwid
        return jsonify({"status": "success", "message": "Kích hoạt HWID thành công!"}), 200

    # 4. Các lần sau -> Kiểm tra HWID có trùng khớp không
    if key_info["hwid"] == user_hwid:
        return jsonify({"status": "success", "message": "Xác thực thành công!"}), 200
    else:
        return jsonify({"status": "error", "message": "Key này đã được dùng trên máy khác!"}), 403

if __name__ == '__main__':
    # Đã chỉnh về 127.0.0.1 và tắt debug để chống lỗi CONNECTION_RESET
    app.run(host='127.0.0.1', port=5000, debug=False)