import time

from common.constants import (
    PERIOD_SHUTDOWN_BUTTON,
    LOOPS_TO_WAIT_SHUTDOWN_BUTTON)
from common.logger import loggerERROR
from shutdown_button.helpers import (
    setup_GPIO_shutdown_button,
    is_shutdown_button_pressed,
    set_for_shutdown,
    cleanup_GPIO
    )

def main():
    consecutive_press_count = 0
    setup_GPIO_shutdown_button()

    try:
        while True:
            if is_shutdown_button_pressed():
                consecutive_press_count += 1
            else:
                consecutive_press_count = 0

            if consecutive_press_count == LOOPS_TO_WAIT_SHUTDOWN_BUTTON:
                set_for_shutdown()
                break

            time.sleep(PERIOD_SHUTDOWN_BUTTON)  

    except Exception as e:
        loggerERROR(f"exception on shutdown_button loop: {e}")
    finally:
        cleanup_GPIO()

if __name__ == "__main__":
    main()
