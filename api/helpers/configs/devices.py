import yaml


class DevicesConfig:
    def __init__(self):
        self.filename = "devices.yaml"

        self.init_file()

    def init_file(self):
        with open(self.filename, "r") as config_file:
            self.config = yaml.load(config_file.read(), Loader=yaml.FullLoader)

    def get(self, name: str) -> dict:
        return self.config.get(name, None)

    def set_device(self, name: str, data: dict):
        self.config[name] = data

    def save_file(self):
        with open(self.filename, "w") as config_file:
            config_file.write(yaml.dump(self.config))
