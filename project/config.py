class BaseConfig:
    TESTING = False


class DevelopmentConfig(BaseConfig):
    pass


class TestConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    pass
