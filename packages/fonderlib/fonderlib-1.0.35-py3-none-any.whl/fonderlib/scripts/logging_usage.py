from fonderlib.common.logger import get_logger

logger = get_logger("TestTask", level="DEBUG")


def main():
    logger.info("Resumen de resultados:")
    logger.error("error")
    logger.critical("critical")
    return 0


if __name__ == "__main__":
    main()
