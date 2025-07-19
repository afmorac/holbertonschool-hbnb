from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User

# Usamos el mismo diccionario de usuarios
from api.v1.users import users

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Buscar usuario por email
    user = None
    for u in users.values():
        if u.email == data.get('email'):
            user = u
            break

    # Validar usuario y contraseña
    if not user or not user.verify_password(data.get('password')):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Crear JWT con claims (id, is_admin)
    identity = {
        'id': str(user.id),
        'is_admin': getattr(user, 'is_admin', False)
    }

    access_token = create_access_token(identity=identity)
    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """Ruta protegida con JWT"""
    current_user = get_jwt_identity()
    return jsonify({"message": f"Hello, user {current_user['id']}"}), 200
