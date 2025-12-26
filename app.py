from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import random
import time
import os
import sys
from datetime import datetime

app = Flask(__name__)
CORS(app)

sys.setrecursionlimit(1000000000)

def generate_string(n, pattern='mixed'):
    if pattern == 'lower':
        chars = 'abcdefghijklmnopqrstuvwxyz'
    elif pattern == 'upper':
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    else:
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(chars) for _ in range(n))

def convert_case_iterative(text, pattern, direction=None):
    result_chars = []
    
    for char in text:
        if pattern == 'lower':
            result_chars.append(char.upper())
        elif pattern == 'upper':
            result_chars.append(char.lower())
        elif pattern == 'mixed':
            if direction == 'to_upper':
                result_chars.append(char.upper())
            elif direction == 'to_lower':
                result_chars.append(char.lower())
            elif direction == 'swap':
                result_chars.append(char.swapcase())
            else:
                result_chars.append(char)
        else:
            result_chars.append(char)
    
    return ''.join(result_chars)

def convert_case_recursive(text, pattern, direction=None, index=0):
    if index >= len(text):
        return ""
    
    char = text[index]
    
    if pattern == 'lower':
        converted_char = char.upper()
    elif pattern == 'upper':
        converted_char = char.lower()
    elif pattern == 'mixed':
        if direction == 'to_upper':
            converted_char = char.upper()
        elif direction == 'to_lower':
            converted_char = char.lower()
        elif direction == 'swap':
            converted_char = char.swapcase()
        else:
            converted_char = char
    
    return converted_char + convert_case_recursive(text, pattern, direction, index + 1)

def measure_memory_usage(text):
    return (len(text.encode('utf-8')) + 56) / 1024

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_string_api():
    try:
        data = request.get_json()
        n = data.get('n', 100)
        pattern = data.get('pattern', 'mixed')
   
        if n < 1:
            return jsonify({'error': 'n must be greater than 0'}), 400
        
        generated_string = generate_string(n, pattern)
        
        return jsonify({
            'success': True,
            'string': generated_string,
            'length': len(generated_string),
            'pattern': pattern,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        text = data.get('text', '')
        algorithm = data.get('algorithm', 'iterative')
        pattern = data.get('pattern', 'mixed')
        direction = data.get('direction', None)
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400

        start_time = time.perf_counter()
        
        if algorithm == 'iterative':
            result = convert_case_iterative(text, pattern, direction)
        elif algorithm == 'recursive':
            result = convert_case_recursive(text, pattern, direction)
        else:
            return jsonify({'error': 'Invalid algorithm'}), 400
        
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000
        
        memory_usage = measure_memory_usage(result)
        
        return jsonify({
            'success': True,
            'input': text,
            'output': result,
            'algorithm': algorithm,
            'execution_time_ms': round(execution_time, 4),
            'memory_usage_kb': round(memory_usage, 2),
            'input_length': len(text),
            'output_length': len(result),
            'timestamp': datetime.now().isoformat()
        })
    
    except RecursionError:
        return jsonify({
            'error': 'Recursion depth exceeded. Try iterative algorithm.',
        }), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'ok',
        'message': 'API is working',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')

    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)