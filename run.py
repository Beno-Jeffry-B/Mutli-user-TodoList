import os
from todo import app
from todo.routes import debug_bp  

app.register_blueprint(debug_bp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
