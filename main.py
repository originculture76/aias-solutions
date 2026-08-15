from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# هذا المسار (Route) هو الذي سيستقبل رسائل الواتساب
@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    if request.method == 'GET':
        # هذا للتحقق من الـ Webhook (Verify Token)
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        # استبدل 'YOUR_VERIFY_TOKEN' بكلمة السر التي وضعتها في فيسبوك/واتساب
        if mode == 'subscribe' and token == 'YOUR_VERIFY_TOKEN':
            return challenge
        return 'Verification failed', 403
    
    elif request.method == 'POST':
        # هنا ستصلك بيانات رسائل الواتساب
        data = request.json
        print(data) # لطباعة البيانات في سجلات Render
        return jsonify({"status": "received"}), 200

@app.route('/')
def home():
    return "AIAS CRM is Running Successfully!"

if __name__ == '__main__':
    # Render يخصص "Port" تلقائياً، لذا يجب أن نستخدم os.environ.get
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
