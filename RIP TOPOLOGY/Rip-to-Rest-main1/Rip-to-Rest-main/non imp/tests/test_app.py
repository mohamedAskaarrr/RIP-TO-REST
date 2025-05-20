from app import create_app

def test_app_creation():
    app = create_app()
    assert app is not None
    print("Application created successfully!")

if __name__ == '__main__':
    test_app_creation()