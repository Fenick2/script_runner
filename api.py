import sh
from fastapi import FastAPI
from loguru import logger

from schemas import AddModifyScript, DelScript

logger.add("./logs/api.log", format="{time} {level} {message}",
           level="ERROR", rotation="100 KB",
           colorize=True, compression="zip")
logger.info("App started.")

app = FastAPI()


nginx1 = sh.Command("./management/nginx_tpl_1.sh")
nginx2 = sh.Command("./management/nginx_tpl_2.sh")
nginx3 = sh.Command("./management/nginx_tpl_3.sh")
nginx4 = sh.Command("./management/nginx_tpl_4.sh")
deltpl1 = sh.Command("./management/del_tpl_1.sh")
deltpl2 = sh.Command("./management/del_tpl_2.sh")
getssl = sh.Command("./management/get_ssl_cert.sh")
checkssl = sh.Command("./management/check_ssl_cert.sh")


def add_mod_script(scripter: AddModifyScript) -> None:
    """Запускает скрипт конфига по условию"""

    if scripter.domain and scripter.customjs:
        sh.RunningCommand = nginx1()
    elif scripter.domain and not scripter.customjs:
        sh.RunningCommand = nginx2()
    elif scripter.customjs and not scripter.domain:
        sh.RunningCommand = nginx3()
    else:
        sh.RunningCommand = nginx4()


@logger.catch
@app.post("/add")
def add_scripter(scripter: AddModifyScript) -> None:

    sh.RunningCommand = getssl()
    add_mod_script(scripter)


@logger.catch
@app.post("/modify")
def mod_scripter(scripter: AddModifyScript) -> None:

    sh.RunningCommand = checkssl()
    add_mod_script(scripter)


@logger.catch
@app.delete("/remove")
def del_container(container: DelScript):
    domain = container.domain
    name = container.name

    if domain and name:
        sh.RunningCommand = deltpl1()
    else:
        sh.RunningCommand = deltpl2()
