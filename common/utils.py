import jwt
import time


SECRET_KEY = 'your_secret_key'

async def generate_token(payload):
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

async def verify_token(token):
    try:
        decoded_payload = await jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return False, "Token Expired"
    except jwt.InvalidTokenError:
        # Token is invalid
        return False, "Invalid Token"

def epoch_time_after_minutes(minutes=0):
    seconds_from_now = minutes * 60
    return int(time.time() + seconds_from_now)

# # Generate token
# token = generate_token(payload)
# print("Generated Token:", token)

# # Verify token
# verified_payload = verify_token(token)
# if isinstance(verified_payload, dict):
#     print("Verified Payload:", verified_payload)
# else:
#     print("Token Verification Error:", verified_payload)
