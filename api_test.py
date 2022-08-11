import sh
from loguru import logger
from pathlib import Path
from fastapi import FastAPI

from schemas import AddModifyScript, DelScript

logger.add("./logs/api_test.log", format="{time} {level} {message}",
           level="INFO", rotation="100 KB", compression="zip")
logger.info("Message (Info)")

app = FastAPI()

getssl = sh.Command("./test/get_ssl.sh")
ps = sh.Command("./test/ps.sh")
gc = sh.Command("./test/gc.sh")
t1 = sh.Command("./test/test1.sh")
t2 = sh.Command("./test/test2.sh")
t3 = sh.Command("./test/test3.sh")
t4 = sh.Command("./test/test4.sh")


def add_script(scripter: AddModifyScript) -> None:
    """Запускает скрипт конфига по условию"""

    if scripter.domain and scripter.customjs:
        sh.RunningCommand = t1()
    elif scripter.domain and not scripter.customjs:
        sh.RunningCommand = t2()
    elif scripter.customjs and not scripter.domain:
        sh.RunningCommand = t3()
    else:
        sh.RunningCommand = t4()


@logger.catch
@app.get("/containers")
def get_container_list() -> None:
    """ Возвращает список контейнеров (аналог docker ps -a)"""

    sh.RunningCommand = gc()


@app.post("/add")
@logger.catch
def add_scripter(scripter: AddModifyScript) -> None:
    p = Path('./test/get_ssl.sh')
    if p.exists():
        sh.RunningCommand = getssl()
    else:
        sh.RunningCommand = ps()

    add_script(scripter)


@app.post("/modify")
@logger.catch
def mod_scripter(scripter: AddModifyScript) -> None:

    add_script(scripter)


@app.delete("/remove")
@logger.catch
def del_container(container: DelScript):
    domain = container.domain
    name = container.name

    if domain and name:
        sh.RunningCommand = t1()
    else:
        sh.RunningCommand = t2()
