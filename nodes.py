import requests
import numpy
from PIL import Image
from io import BytesIO


class TelegramImageSaver:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "bot_token": (
                    "STRING",
                    {"default": ""},
                ),
                "chat_id": (
                    "STRING",
                    {"default": ""},
                ),
                "caption": ("STRING", {"default": "", "multiline": True}),
                "timeout": ("INT", {"default": 30}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "send"
    CATEGORY = "_local_nodes"
    OUTPUT_NODE = True

    def send(
        self, images, bot_token: str, chat_id: str, caption: str = "", timeout: int = 30
    ):

        try:
            response = requests.post(
                url=f"https://api.telegram.org/bot{bot_token}/sendPhoto",
                data={"chat_id": chat_id, "caption": caption},
                files={
                    "photo": (
                        "image.jpg",
                        self.image_to_buffer(images[0]),
                        "image/jpeg",
                    )
                },
                timeout=timeout,
            )
            response.raise_for_status()
        except Exception as exception:
            print("[telegram] request error:", exception)

        return (images,)

    def image_to_buffer(self, image):

        image = image.numpy()

        image = numpy.clip(image * 255, 0, 255).astype(numpy.uint8)

        pil_img = Image.fromarray(image)

        buffer = BytesIO()
        pil_img.save(buffer, format="JPEG", quality=90)
        buffer.seek(0)

        return buffer


NODE_CLASS_MAPPINGS = {
    "TelegramImageSaver": TelegramImageSaver,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TelegramImageSaver": "Telegram image saver",
}
