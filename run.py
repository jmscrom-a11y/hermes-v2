from app.utils.logger import info, error
from app.telegram_bot import run_bot


def main():
    info("Hermes V2 Starting")

    try:
        run_bot()

    except KeyboardInterrupt:
        info("Hermes V2 Stopped")

    except Exception as e:
        error(str(e))
        raise


if __name__ == "__main__":
    main()