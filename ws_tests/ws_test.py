import asyncio
from multiprocessing import Process
import ws_gui as wg
import ws_mechanics as wm


def run_sys():
    t1 = Process(target=wm.create_bknd_task)
    # t1 = asyncio.create_task(wm.start_bknd())
    t2 = Process(target=wg.create_gui_app)
    # t2 = asyncio.create_task(wg.create_gui_app())

    t1.start()
    t2.start() 
    # wg.create_gui_app()
    # wm.start_bknd()

    # await asyncio.gather(t1)

if __name__ == "__main__":
    run_sys()
    # wm.create_bknd_task()
    # wg.create_gui_app()
