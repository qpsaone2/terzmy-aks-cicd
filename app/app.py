from flask import Flask, request, jsonify
import os
from datetime import datetime
import json

app = Flask(__name__)
DATA_PATH = os.getenv('DATA_PATH', '/data')

@app.route('/')
def home():
    return jsonify({
        "status": "healthy",
        "message": "AKS CI/CD Demo App",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/write', methods=['POST'])
def write_data():
    """Blob Storage에 데이터 쓰기"""
    try:
        data = request.get_json()
        filename = data.get('filename', f'data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        filepath = os.path.join(DATA_PATH, filename)
        
        # 디렉토리 존재 확인
        os.makedirs(DATA_PATH, exist_ok=True)
        
        # 데이터 쓰기
        with open(filepath, 'w') as f:
            json.dump({
                'content': data.get('content', 'test data'),
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
        
        return jsonify({
            "status": "success",
            "message": f"Data written to {filename}",
            "path": filepath
        }), 201
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/read')
def read_data():
    """Blob Storage에서 파일 목록 읽기"""
    try:
        files = os.listdir(DATA_PATH)
        return jsonify({
            "status": "success",
            "files": files,
            "count": len(files)
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
