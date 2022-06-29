import logging


class ReportPortalReporter(object):
    def __init__(self):
        self.logger = logging.getLogger("reporter.rportal")
        self.logger.setLevel(logging.DEBUG - 5)

    def warning(self, message):
        self.logger.warning(message)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def trace(self, message):
        self.logger.trace(message)

    def error(self, message):
        self.logger.error(message)

    def image(self, image_name, description=None):
        if description is None:
            description = image_name
        try:
            with open(image_name, "rb") as fh:
                image = fh.read()

            self.logger.info(
                description,
                attachment={
                    "data": image,
                    "mime": "image/png"
                },
            )
        except Exception as e:
            pass
            # print(f"Exception when trying to save image to report portal: {e}")

    def file(self, file_name, description=None):
        if description is None:
            description = file_name
        try:
            with open(file_name, "rb") as fh:
                content = fh.read()

            self.logger.info(
                description,
                attachment={
                    "data": content,
                    "mime": "application/octet-stream"
                },
            )
        except Exception as e:
            pass
            # print(f"Exception when trying to save image to report portal: {e}")
