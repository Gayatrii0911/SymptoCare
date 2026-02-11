from app import create_app

app = create_app()

if __name__ == "__main__":
    print("\n╔══════════════════════════════════════════════════════╗")
    print("║   Avalon – AI Health Triage Copilot (Backend)        ║")
    print("╚══════════════════════════════════════════════════════╝")
    print("  → http://127.0.0.1:5000")
    print("  → POST /triage  |  GET /symptoms  |  GET /diseases\n")
    app.run(host="0.0.0.0", port=5000, debug=True)

