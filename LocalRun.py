from config import config_tool
config_tool.deploy_local_configurations()
from main_controller import meloentjoer_app
if __name__ == "__main__":

    meloentjoer_app.run()
