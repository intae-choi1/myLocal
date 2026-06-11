from managers.automation_manager import AutomationManager

# from managers.pri_input_manager import InputManager
from managers.boma_input_manager import InputManager


def main():
    automation_manager = AutomationManager()

    input_manager = InputManager(automation_manager)

    input_manager.start()


if __name__ == "__main__":
    main()