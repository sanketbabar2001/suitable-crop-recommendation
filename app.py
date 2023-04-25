from website import create_app
import pickle

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)