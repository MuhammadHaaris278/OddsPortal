import logging

def get_logger(name="scraper"):
    logging.basicConfig(
        format="[*] %(message)s",
        level=logging.INFO
    )
    logger = logging.getLogger(name)

    # Add custom "success" level
    SUCCESS_LEVEL = 25  # Between INFO (20) and WARNING (30)
    logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")

    def success(self, message, *args, **kwargs):
        if self.isEnabledFor(SUCCESS_LEVEL):
            self._log(SUCCESS_LEVEL, message, args, **kwargs)

    logging.Logger.success = success
    return logger
