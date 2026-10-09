USE_DATABASE = False

if USE_DATABASE:
    from app_db import app
    print("MODE BASE DE DONNEES")
else:
    from app_memory import app
    print("MODE MEMOIRE")


if __name__ == "__main__":
    app.run(debug=True)