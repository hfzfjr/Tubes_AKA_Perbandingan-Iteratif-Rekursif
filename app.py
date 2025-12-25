from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import random
import time
import sys
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Helper function to generate string based on pattern
def generate_string(n, pattern='mixed'):
    """
    Generate a random string of length n based on pattern
    Patterns: 'mixed', 'lower', 'upper'
    """
    if pattern == 'lower':
        chars = 'abcdefghijklmnopqrstuvwxyz'
    elif pattern == 'upper':
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    else:  # mixed
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    
    return ''.join(random.choice(chars) for _ in range(n))

# New conversion function based on pattern and direction
def convert_case(text, pattern, direction=None):
    """
    Convert case based on pattern:
    - 'lower': convert to uppercase
    - 'upper': convert to lowercase
    - 'mixed': convert based on direction ('to_upper' or 'to_lower')
    """
    if pattern == 'lower':
        return text.upper()
    elif pattern == 'upper':
        return text.lower()
    elif pattern == 'mixed':
        if direction == 'to_upper':
            return text.upper()
        elif direction == 'to_lower':
            return text.lower()
        elif direction == 'swap':
            return text.swapcase()
        else:
            return text  # Default: no change if direction invalid
    else:
        return text  # Default: no change

# Measure memory usage (approximate)
def measure_memory_usage(text):
    # Approximate memory usage in bytes
    # In Python, strings are more complex, but this gives a rough estimate
    return (len(text.encode('utf-8')) + 56) / 1024  # Convert to KB

# API Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_string_api():
    try:
        data = request.get_json()
        n = data.get('n', 100)
        pattern = data.get('pattern', 'mixed')
        
        # No size limit
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
        pattern = data.get('pattern', 'mixed')  # New: pattern from frontend
        direction = data.get('direction', None)  # New: direction for mixed
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # Measure execution time
        start_time = time.perf_counter()
        
        if algorithm == 'iterative':
            result = convert_case(text, pattern, direction)
        elif algorithm == 'recursive':
            # For recursive, we can implement a simple recursive version if needed, but since conversion is straightforward, use iterative for now
            # To keep it recursive, we can add a recursive wrapper, but for simplicity, use the same logic
            result = convert_case(text, pattern, direction)  # No recursion needed for simple conversion
        else:
            return jsonify({'error': 'Invalid algorithm'}), 400
        
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        # Measure memory usage
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
            'max_recommended_length': 1000
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
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    app.run(debug=True, port=5000)