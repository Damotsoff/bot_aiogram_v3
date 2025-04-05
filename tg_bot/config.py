from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin: int
    database_url: str
    money_token: str
    wallet: str

    @classmethod
    def from_env(cls, env: Env) -> "TgBot":
        token = env.str("BOT_TOKEN")
        admin = env.int("ADMIN")
        database_url = env.str("DATABASE_URL")
        money_token = env.str("MONEY_TOKEN")
        wallet = env.str("WALLET")
        return TgBot(
            token=token,
            admin=admin,
            database_url=database_url,
            money_token=money_token,
            wallet=wallet,
        )


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str = "./tg_bot/.env") -> Config:
    env = Env()
    env.read_env(path=path)
    return Config(TgBot.from_env(env))
