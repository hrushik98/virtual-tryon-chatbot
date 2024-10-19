from fastapi import FastAPI, Request, BackgroundTasks
from twilio.rest import Client
import os
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse, Message
from helpers.db_helpers import init_db, retrieve_from_db, store_in_db, reset_user_session
from helpers.github_helpers import upload_to_github
from helpers.openai_helpers import ask_question
from helpers.tryon_api_helpers import send_to_tryon_api


twilio_account_sid = os.getenv("TWILIO_ACC_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")

twilio_client = Client(twilio_account_sid, twilio_auth_token)
# Initialize the database
init_db()

app = FastAPI()


@app.post("/ask")
async def chatgpt(request: Request, background_tasks: BackgroundTasks) -> Response:
    form_data = await request.form()
    incoming_que = form_data.get('Body', '').lower()  
    destination_number = form_data.get('From', None)
    num_media = int(form_data.get('NumMedia', 0))
    destination_number_from_send_to_tryon_api = form_data.get('user_id', None)
    
    bot_resp = MessagingResponse()
    msg = bot_resp.message()

    user_id = destination_number
    send_param = form_data.get('send', None)
    final_url = form_data.get('final_url', None)

    if send_param == "ok" and final_url is not None and destination_number_from_send_to_tryon_api is not None:

        message = twilio_client.messages.create(
            from_=os.getenv("TWILIO_PHONE_NUMBER"),  
            body='Done ✅',
            to=destination_number_from_send_to_tryon_api,  
            media_url=[str(final_url)] 
        )
        return Response(content=str(bot_resp), media_type="application/xml")

    person_url = None
    garment_url = None

    if num_media == 0 and incoming_que == "start":  
        person_url = retrieve_from_db(user_id, "person_url")
        garment_url = retrieve_from_db(user_id, "garment_url")
        
        if person_url and garment_url:
            print("sent this")
            print(person_url, garment_url, user_id)
            background_tasks.add_task(send_to_tryon_api, person_url, garment_url, user_id)
            msg.body("Processing, this will take some time (upto 1 min). Your patience is appreciated.")
            return Response(content=str(bot_resp), media_type="application/xml")
        else:
            msg.body("Please upload both person and garment images first.")
            return Response(content=str(bot_resp), media_type="application/xml")

    if incoming_que == "reset":
        reset_user_session(user_id)
        msg.body("Session reset. You can start over.")
        return Response(content=str(bot_resp), media_type="application/xml")

    if num_media == 0:
        answer = await ask_question(incoming_que)
        msg.body(answer)
    else:
        media_url = form_data.get('MediaUrl0')
        print(f"Media URL: {media_url}")

    if incoming_que == "person":
        person_url = upload_to_github(media_url)
        if person_url:
            store_in_db(user_id, "person_url", person_url)
            garment_url = retrieve_from_db(user_id, "garment_url")
            if garment_url:
                msg.body("Both images received. Type 'START' to process your request or 'RESET' to start over.")
            else:
                msg.body("Person image received ✅. Please send garment image.")
        else:
            msg.body("Failed to process person image. Please try again.")

    elif incoming_que == "garment":
        garment_url = upload_to_github(media_url)
        if garment_url:
            store_in_db(user_id, "garment_url", garment_url)
            person_url = retrieve_from_db(user_id, "person_url")
            if person_url:
                msg.body("Both images received. Type 'START' to process your request or 'RESET' to start over.")
            else:
                msg.body("Garment image received ✅. Please send person image.")
        else:
            msg.body("Failed to process garment image. Please try again.")

    return Response(content=str(bot_resp), media_type="application/xml")
