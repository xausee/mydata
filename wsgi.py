from app import app as application

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=443, debug=False, ssl_context=("cert/full_chain.pem", "cert/private.key"))
