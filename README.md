# Virtual Try-On Chatbot

This project is a **Virtual Try-On Chatbot** built using **FastAPI** that allows users to upload images of a person and a garment via WhatsApp. The bot processes the images and provides a virtual try-on experience by combining the two images and returning the result. The project integrates various services such as **Twilio**, **OpenAI**, **GitHub**, and a **Virtual Try-On API** to achieve its functionality.

## Features

- Users can interact with the chatbot via WhatsApp using Twilio.
- Users can send images with specific captions ("PERSON" or "GARMENT") to simulate a virtual try-on.
- The chatbot can process text-based queries using OpenAI's GPT 4o mini model and the images with https://huggingface.co/spaces/Nymbo/Virtual-Try-On
- Images are stored and managed using a local SQLite database.
- Uploaded images are stored on GitHub for easy access.
- Once both images are received (person and garment), the system integrates with a try-on API and returns a combined image of the person wearing the garment.

### Key Components

- **src/app.py**: The entry point for the FastAPI application. It handles incoming requests, processes them based on user input, and integrates with helper functions.
- **db_helpers.py**: Handles all interactions with the SQLite database for storing and retrieving user images.
- **github_helpers.py**: Contains functions for uploading images to GitHub and retrieving download URLs.
- **openai_helpers.py**: Interacts with OpenAI to handle text-based queries from users.
- **tryon_api_helpers.py**: Integrates with the Virtual Try-On API to combine person and garment images.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- **Python 3.12**
- **SQLite3** (included with Python)
- **pip** (Python package installer)

You will also need:

- A **Twilio** account with a phone number for handling WhatsApp messages.
- An **OpenAI API key**.
- A **GitHub repository** and personal access token for uploading images.
- Access to a **Virtual Try-On API**.
- Check the .env.example for more info 

### Installation

1. **Clone the repository**:

```bash
git clone https://github.com/your_username/virtual_tryon_chatbot.git
cd virtual_tryon_chatbot
```

2. **Create a virtual environment** (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Run the application**:

```bash
uvicorn app:app --reload
```

5. **Setup Twilio Webhook**:
   - Set the webhook URL for your Twilio phone number to point to your running FastAPI application, e.g., `http://your-domain.com/ask`.

### Usage

1. **Starting a session**:
   - Send a message to the WhatsApp number connected to Twilio by scanning the QR code.
     ![image](https://github.com/user-attachments/assets/d23e3957-1bbd-494f-b6cf-14aae3cb2c07)

   - The bot will ask you to upload a person image and a garment image.

2. **Uploading Images**:
   - Send an image with the caption `PERSON` to upload the person image.
   - Send an image with the caption `GARMENT` to upload the garment image.

3. **Processing**:
   - Once both images are uploaded, type `START` again to begin the virtual try-on process.
   - The bot will respond with the combined image of the person wearing the garment.

4. **Reset Session**:
   - To reset the session at any time, send the message `RESET`.

### Project Workflow

1. **User Interaction**: Users interact with the chatbot by sending messages and images through WhatsApp.
2. **Image Uploading**: The chatbot stores images (person or garment) in a local SQLite database, and they are uploaded to a GitHub repository.
3. **Processing Images**: When both images are received, the system sends them to the Virtual Try-On API to generate a combined image.
4. **Response**: The bot replies to the user with the generated image via WhatsApp.

## Example Session

1. User scans the QR code.
2. The bot asks for a person image.
3. The user uploads a person image with the caption "PERSON".
4. The bot confirms and asks for a garment image.
5. The user uploads a garment image with the caption "GARMENT".
6. The bot processes both images and replies with a combined image.

## SCREENSHOTS

1. User uploads person image with caption as 'PERSON'

![image](https://github.com/user-attachments/assets/8b4fbc19-cf60-4405-91b7-23e7344e5399)

2. User uploads garment image with caption as 'GARMENT'

![image](https://github.com/user-attachments/assets/b1f56095-fb70-4abf-ace0-f2b8e2dc7600)

3. User gets the result

![image](https://github.com/user-attachments/assets/b3375e68-8182-42e7-aab7-a71ce8e3604c)




## Acknowledgments

- [OpenAI](https://openai.com/) for GPT model integration.
- [Twilio](https://www.twilio.com/) for WhatsApp messaging services.
- [GitHub API](https://docs.github.com/en/rest) for file storage.
- [Nymbo Virtual Try-On API](https://nymbo.tryonapi.com/) for virtual try-on capabilities.

