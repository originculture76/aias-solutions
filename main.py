from flask import Flask, request, jsonify
import os
from supabase import create_client, Client

app = Flask(__name__)

# جلب بيانات الاتصال بقاعدة بيانات Supabase من متغيرات البيئة في Render
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# تهيئة عميل Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# هذا المسار (Route) هو الذي سيستقبل رسائل الواتساب
@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    if request.method == 'GET':
        # هذا للتحقق من الـ Webhook (Verify Token)
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == 'YOUR_VERIFY_TOKEN':
            return challenge
        return 'Verification failed', 403
    
    elif request.method == 'POST':
        # هنا ستصلك بيانات رسائل الواتساب
        data = request.json
        print("Received Data:", data) # لطباعة البيانات في سجلات Render
        
        try:
            # استخراج البيانات المرسلة من Hoppscotch أو واتساب
            sender_val = data.get("sender", "Unknown")
            message_val = data.get("message", "No message")
            
            # إدخال البيانات مباشرة في جدول messages في Supabase
            response = supabase.table("messages").insert({
                "sender": sender_val,
                "message": message_val
            }).execute()
            
            print("Inserted into Supabase successfully:", response)
            
        except Exception as e:
            print("Error saving to Supabase:", str(e))
            return jsonify({"status": "error", "details": str(e)}), 500
        
        return jsonify({"status": "received and saved"}), 200

@app.route('/')
def home():
    return "AIAS CRM is Running Successfully!"

if __name__ == '__main__':
    # Render يخصص "Port" تلقائياً، لذا يجب أن نستخدم os.environ.get
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
