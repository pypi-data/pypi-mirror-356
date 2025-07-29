from fonderlib.config.config_service import ConfigService


def main():
    config = ConfigService()
    value = config.get_open_ai_config()
    print("Value from config value")
    print(value)


if __name__ == "__main__":
    main()
