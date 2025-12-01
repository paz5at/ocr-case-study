import os
import requests

BASE_URL = "http://localhost:8080"
OCR_URL = f"{BASE_URL}/api/v1/ocr_upload"
SAMPLE_IMG = "../assets/sample1.jpg"


def test_server_running():
    r = requests.get(BASE_URL)
    assert r.status_code == 200


def test_ocr_upload():
    assert os.path.exists(SAMPLE_IMG), "Add a sample image to assets/sample1.jpg"
    files = {"file": open(SAMPLE_IMG, "rb")}
    r = requests.post(OCR_URL, files=files)
    data = r.json()

    assert r.status_code == 200
    assert "results" in data
    assert isinstance(data["results"], list)


if __name__ == "__main__":
    print("Running tests...")
    test_server_running()
    test_ocr_upload()
    print("All tests passed!")
