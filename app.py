from flask import Flask, request, make_response, jsonify
import random
import socket
import sys

app = Flask(__name__, instance_relative_config=True)

log_file_path = "./op_log.log"

def save_last_op(op, args, res):
    with open(log_file_path, 'w') as file:
        operation = f"{op}({args})={res}"
        file.write(operation)

def read_last_op():
    with open(log_file_path, 'r') as file:
        data = file.read().strip()
        return data

@app.route('/add')
def add():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a and b:
        result = a + b
        
        # Save if success
        save_last_op("add", f"{a},{b}", result)

        return make_response(jsonify(s=result), 200)
    else:
        return make_response('Invalid input\n', 400)

@app.route('/sub')
def sub():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a and b:
        result = a - b
        save_last_op("sub", f"{a},{b}", result)
        return make_response(jsonify(s=result), 200)
    else:
        return make_response('Invalid input\n', 400)

@app.route('/mul')
def mul():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a and b:
        result = a * b
        save_last_op("mul", f"{a},{b}", result)
        return make_response(jsonify(s=result), 200)
    else:
        return make_response('Invalid input\n', 400)

@app.route('/div')
def div():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a is not None and b is not None and b != 0:
        result = a / b
        save_last_op("div", f"{a},{b}", result)
        return make_response(jsonify(s=result), 200)
    else:
        return make_response('Invalid input, b must be different than 0\n', 400)

@app.route('/mod')
def mod():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a is not None and b is not None and b != 0:
        result = a % b
        save_last_op("mod", f"{a},{b}", result)
        return make_response(jsonify(s=result), 200)
    else:
        return make_response('Invalid input\n', 400)

@app.route('/random')
def rand():
    a = request.args.get('a', type=int)
    b = request.args.get('b', type=int)
    if a is not None and b is not None and a <= b:
        result = random.randint(a, b)
        save_last_op("rand", f"{a},{b}", result)
        return make_response(jsonify(s=result), 200)
    else:
        return make_response('Invalid input\n', 400)

@app.route('/upper')
def upper():
    a = request.args.get('a', type=str)
    if a:
        result = a.upper()
        save_last_op("upper", a, result)
        return make_response(jsonify(s=result), 200)
    else:
        return make_response('Invalid input\n', 400)

@app.route('/lower')
def lower():
    a = request.args.get('a', type=str)
    if a:
        result = a.lower()
        save_last_op("lower", a, result)
        return make_response(jsonify(s=result), 200)
    else:
        return make_response('Invalid input\n', 400)

@app.route('/concat')
def concat():
    a = request.args.get('a', type=str)
    b = request.args.get('b', type=str)
    if a and b:
        result = a + b
        save_last_op("concat", f"{a},{b}", result)
        return make_response(jsonify(s=result), 200)
    else:
        return make_response('Invalid input\n', 400)

def add_list(lst):
    return sum(lst)

def sub_list(lst):
    return lst[0] - sum(lst[1:])

def mul_list(lst):
    result = 1

    for num in lst:
        result *= num

    return result

def div_list(lst):
    result = lst[0]

    for num in lst[1:]:
        if num == 0:
            raise ValueError("Division by zero")
        result /= num

    return result

def upper_list(lst):
    return ''.join(s.upper() for s in lst)

def lower_list(lst):
    return ''.join(s.lower() for s in lst)

def concat_list(lst):
    return ''.join(str(s) for s in lst)

@app.route('/reduce', methods=['GET'])
def reduce():
    op = request.args.get('op')
    lst = eval(request.args.get('lst'))

    operations = {
        'add': add_list,
        'sub': sub_list,
        'mul': mul_list,
        'div': div_list,
        'upper': upper_list,
        'lower': lower_list,
        'concat': concat_list
    }

    if op not in operations:
        return jsonify({'error': f'Invalid operation, choose one between: {[key for key in operations.keys()]}'}), 400

    try:
        result = operations[op](lst)
        save_last_op(f"reduce('{op}'", str(lst), result)
        return jsonify({'s': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/crash', methods=['GET'])
def crash():
    host = socket.gethostname()
    port = 5005

    response = jsonify({
        'host': host,
        'port': port
    })
    
    def shutdown():
        sys.exit(0)

    response.call_on_close(shutdown)
    return response

@app.route('/last', methods=['GET'])
def last():
    last_op = read_last_op()
    if last_op is None:
        return make_response('No operation performed yet', 404)
    return make_response(last_op, 200)

if __name__ == '__main__':
    app.run(debug=True, port=5005)