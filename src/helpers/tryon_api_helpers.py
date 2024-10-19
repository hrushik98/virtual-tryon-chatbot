from gradio_client import Client, handle_file
from github_helpers import upload_to_github


async def send_to_tryon_api(person_image_url: str, garment_image_url: str, user_id: str) -> None:
    """Sends person and garment images to the try-on API."""
    print([person_image_url, garment_image_url, user_id])
    client = Client("Nymbo/Virtual-Try-On")
    result = client.predict(
        dict={
            "background": handle_file(person_image_url),
            "layers": [],
            "composite": None
        },
        garm_img=handle_file(garment_image_url),
        garment_des="virtual try on ",
        is_checked=True,
        is_checked_crop=False,
        denoise_steps=20,
        seed=42,
        api_name="/tryon"
    )
    
    url = result[0]
    final_url = upload_to_github(url)
    print(final_url)

    import httpx

    async def send_ok_to_ask() -> None:
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/ask", data={"send": "ok", "final_url": final_url, "user_id": user_id})
            print(response.status_code)
            print(response.text)
    
    await send_ok_to_ask()
