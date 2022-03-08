
import Bonten
from Bonten import Bonten, scheduler



def set_client(new_client):
    Bonten.client = new_client


def add_job(function, seconds=3):
    scheduler.add_job(function, "interval", seconds=seconds, args=[Bonten.client])

