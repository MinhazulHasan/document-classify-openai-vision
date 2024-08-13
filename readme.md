# Image Description API

This project provides a FastAPI-based web service that generates descriptions for uploaded images based on specified categories.

## Features

- Image upload support (JPEG and PNG)
- Category-based image description generation
- CORS middleware for cross-origin requests
- Modular project structure for easy maintenance and scalability

## Prerequisites

- Python 3.10
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/image-description-api.git
   cd image-description-api
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate (On MAC)
   venv\Scripts\activate (On Windows)
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the root directory and add the following variables:
   ```
   ALLOWED_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
   ```

2. Adjust other settings in `app/core/config.py` as needed.

## Usage

1. Start the server:
   ```
   python run.py
   ```

2. The API will be available at `http://localhost:8000`.

3. Use the `/image_description/` endpoint to upload an image and get its description:
   ```
   POST /image_description/
   Parameters:
   - category: string
   - file: image file (JPEG or PNG)
   ```

## Project Structure

```
image-description-api/
│
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   │   └── config.py
|   |   └── prompts.py
│   ├── services/
│   │   └── image_service.py
│   ├── utils/
│   │   └── helpers.py
│   └── main.py
│
├── venv/
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```