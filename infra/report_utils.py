import logging

log = logging.getLogger('report')


def add_file(message: str, file_name: str, data: str, mime: str = 'application/octet-stream'):
    log.debug(
        message,
        attachment={
            "name": file_name,
            "data": data,
            "mime": mime,
        },
    )


def add_image(message: str, image_name):
    try:
        with open(image_name, "rb") as fh:
            image = fh.read()

        log.info(
            message,
            attachment={
                "data": image,
                "mime": "image/png"
            },
        )
    except Exception as e:
        pass
