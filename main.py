#!/usr/bin/python3

from app import app

if __name__ == "__main__":
    # print(app.url_map)
    app.run(debug=True, host="0.0.0.0", port=8005, ssl_context=context)
