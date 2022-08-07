import docker
import sh
import logs
from pathlib import Path
from fastapi import FastAPI

from schemas import AddModifyScript, DelScript

app = FastAPI()
client = docker.from_env()

getssl = sh.Command("/home/managment/get_ssl_cert.sh")
nginx1 = sh.Command("/home/managment/nginx_tpl_1.sh")
nginx2 = sh.Command("/home/managment/nginx_tpl_2.sh")
nginx3 = sh.Command("/home/managment/nginx_tpl_3.sh")
nginx4 = sh.Command("/home/managment/nginx_tpl_4.sh")


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


def rm_container(name: str) -> str:
    """ Удаление контейнера 'name' """
    cont = client.containers.get(name)
    cont.remove()
    return f"Container {name} removed"


@app.get("/containers")
def get_container_list() -> list:
    """ Возвращает список контейнеров (аналог docker ps -a)"""
    lst = [{c.name: c.id} for c in client.containers.list(all=True)]
    return lst


@app.post("/add")
def add_scripter(scripter: AddModifyScript) -> None:
    if Path('/home/managment/ssl_cert.sh').exists():
        sh.RunningCommand = getssl()

    add_mod_script(scripter)
    rm_container(scripter.name)
    rm_container(f"{scripter.name}_1")


@app.post("/modify")
def mod_scripter(scripter: AddModifyScript) -> None:

    add_mod_script(scripter)

    name = scripter.name
    name_1 = f"{name}_1"
    rm_container(name)
    rm_container(name_1)


@app.delete("/remove")
def del_container(container: DelScript):
    name = container.name
    name_1 = f"{name}_1"
    cont = client.containers.get(name)
    if not cont:
        return "Container not exists"
    else:
        rm_container(name)
        rm_container(name_1)
