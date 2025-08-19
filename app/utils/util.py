from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify, current_app
from jose import jwt, exceptions as jose_exceptions

def encode_token(customer_id: int) -> str: 
    payload = {
        "exp": datetime.now(timezone.utc) + timedelta( hours = 1),
        "iat": datetime.now(timezone.utc),
        "sub": str(customer_id)
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm= current_app.config["ALG"])

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        token = auth.split(" ")[1] if auth.startswith("Bearer ") and " " in auth else None
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=[current_app.config["ALG"]])
            customer_id = int(data["sub"])
        except jose_exceptions.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jose_exceptions.JWTError:
            return jsonify({"message": "Invalid token"}), 401
        return f(customer_id, *args, **kwargs)
    return decorated