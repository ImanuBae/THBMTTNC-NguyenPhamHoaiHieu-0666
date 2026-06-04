from cipher.ecc import ECCCipher
from flask import Flask, jsonify, request
from cipher.rsa import RSACipher

app = Flask(__name__)
rsa_cipher = RSACipher()


@app.route('/api/rsa/generate_keys', methods=['GET'])
def rsa_generate_keys():
    rsa_cipher.generate_key()
    return jsonify({'message': 'Keys generated successfully'})


@app.route('/api/rsa/encrypt', methods=['POST'])
def rsa_encrypt():
    data = request.json or {}
    message = data.get('message')
    if message is None:
        return jsonify({'error': 'Missing message'}), 400

    public_key, _ = rsa_cipher.load_key()
    encrypted_message = rsa_cipher.encrypt(message, public_key)
    return jsonify({'encrypted_message': encrypted_message.hex()})


@app.route('/api/rsa/decrypt', methods=['POST'])
def rsa_decrypt():
    data = request.json or {}
    ciphertext_hex = data.get('ciphertext')
    if ciphertext_hex is None:
        return jsonify({'error': 'Missing ciphertext'}), 400

    try:
        ciphertext = bytes.fromhex(ciphertext_hex)
    except ValueError:
        return jsonify({'error': 'ciphertext must be hex string'}), 400

    _, private_key = rsa_cipher.load_key()
    decrypted_message = rsa_cipher.decrypt(ciphertext, private_key)
    return jsonify({'decrypted_message': decrypted_message})


@app.route('/api/rsa/sign', methods=['POST'])
def rsa_sign_message():
    data = request.json or {}
    message = data.get('message')
    if message is None:
        return jsonify({'error': 'Missing message'}), 400

    _, private_key = rsa_cipher.load_key()
    signature = rsa_cipher.sign(message, private_key)
    return jsonify({'signature': signature.hex()})


@app.route('/api/rsa/verify', methods=['POST'])
def rsa_verify_signature():
    data = request.json or {}
    message = data.get('message')
    signature_hex = data.get('signature')
    if message is None or signature_hex is None:
        return jsonify({'error': 'Missing message or signature'}), 400

    try:
        signature = bytes.fromhex(signature_hex)
    except ValueError:
        return jsonify({'error': 'signature must be hex string'}), 400

    public_key, _ = rsa_cipher.load_key()
    is_verified = rsa_cipher.verify(message, signature, public_key)
    return jsonify({'is_verified': is_verified})

# ECC API endpoints can be implemented similarly to RSA endpoints, using ECCCipher class.
ecc_cipher = ECCCipher()
@app.route('/api/ecc/generate_keys', methods=['GET'])
def ecc_generate_keys():
    ecc_cipher.generate_keys()
    return jsonify({'message': 'ECC Keys generated successfully'})  

@app.route('/api/ecc/sign', methods=['POST'])
def ecc_sign_message():
    data = request.json or {}
    message = data.get('message')
    if message is None:
        return jsonify({'error': 'Missing message'}), 400

    private_key, _ = ecc_cipher.load_keys()
    signature = ecc_cipher.sign(message, private_key)
    signature_hex = signature.hex()
    return jsonify({'signature': signature_hex})

@app.route('/api/ecc/verify', methods=['POST'])
def ecc_verify_signature():
    data = request.json
    message = data.get('message')
    signature_hex = data.get('signature')
    if message is None or signature_hex is None:
        return jsonify({'error': 'Missing message or signature'}), 400

    try:
        signature = bytes.fromhex(signature_hex)
    except ValueError:
        return jsonify({'error': 'signature must be hex string'}), 400

    _, public_key = ecc_cipher.load_keys()
    is_verified = ecc_cipher.verify(message, signature, public_key)
    return jsonify({'is_verified': is_verified})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
