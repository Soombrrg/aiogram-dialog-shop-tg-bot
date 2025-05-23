from dataclasses import dataclass

from environs import Env
from sqlalchemy.testing.config import db_url


@dataclass
class DbConfig:
    # host: str
    # password: str
    # user: str
    # database: str
    db_url: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(db_url=env.str("DB_URL")),
        misc=Miscellaneous(),
    )
