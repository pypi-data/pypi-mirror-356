import typer
from .core import random_time

tardy = typer.Typer()


@tardy.command()
def tell(hr24: bool = True, showtimezone: bool = False):
  print(random_time(hr24=hr24, showtimezone=showtimezone))


if __name__ == "__main__":
  tardy()
