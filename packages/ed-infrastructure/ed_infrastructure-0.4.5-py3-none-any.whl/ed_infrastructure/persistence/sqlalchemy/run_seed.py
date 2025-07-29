from ed_infrastructure.persistence.sqlalchemy.demo import get_config
from ed_infrastructure.persistence.sqlalchemy.seed_consumers import \
    seed_consumers
from ed_infrastructure.persistence.sqlalchemy.unit_of_work import UnitOfWork


async def main():
    config = get_config()
    uow = UnitOfWork(config)

    await uow.create_tables()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
