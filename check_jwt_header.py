import jwt

# Replace this with the complete JWT token
token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VybmFtZSIsImV4cCI6MTczMzU1NjAwOX0.YsyQxgCK1QuObEF8NoHxAbPrPHlZnocYwLkuiLASlyJOxGTmLKC4OBW8TJAp95bvR8U65UnwqjYFgK0CjS_rpFh5FniJI3LfaCsSk-WAWlpa9q1na96zJBzTFOGg7WJ6UyYBCEHQMrmlEZVoed6w_bFRt2ZAEwJaN36JLoPivW5vB-aWbVIKbGzfF3WibUhmHi968GrKUKB5oRIHOU__R-wNtB-3cDNLUzTt_8_Awg-ERhxr_052Yh02Im7mv-oSHuCWXsUnRLavoHVVd2IgNzQIKqwo-NMu7nYCh0iQ2ekDobVtTR6ictWayO2KfC_XbyHm0oIF_DQxawr7tZ0GVA"

try:
    # Decode the JWT token without verifying the signature
    decoded_token = jwt.decode(token, options={"verify_signature": False})
    print("Decoded JWT token:", decoded_token)
except jwt.ExpiredSignatureError:
    print("Token has expired")
except jwt.InvalidTokenError:
    print("Invalid token")
except Exception as e:
    print("An error occurred while decoding the token:", str(e))
