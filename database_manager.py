import os
import json

from datetime import datetime

# returns 0 when success else 1
class DbManager:
    def __init__(self, fpgas_file, gunshot_file) -> None:
        self.fpgas_file = fpgas_file
        self.gunshot_file = gunshot_file

        if not os.path.exists(fpgas_file):
            file = open(fpgas_file, "w")
            file.write("{}")
            file.close()

        if not os.path.exists(gunshot_file):
            file = open(gunshot_file, "w")
            file.write("{}")
            file.close()

    def add_fpga(self, id:str, name:str) -> int:
        fpgas_list = self.get_fpgas()
        fpgas_list[id] = {}
        fpgas_list[id]["name"] = name

        with open(self.fpgas_file, "w") as fpgas:
            json.dump(fpgas_list, fpgas)

        return 0

    def add_gunshot(self, fpga_id:str, elevation:int, direction:int) -> int:
        if self.get_fpgas(fpga_id) == {}:
            return 1

        gunshots_list = self.get_gunshot()

        gunshot_id = str(len(gunshots_list) + 1)
        gunshot_info = {"fpga_id":fpga_id,
                        "elevation":elevation,
                        "direction":direction,
                        "date":datetime.today().strftime('%d-%m-%Y'),
                        "time":datetime.today().strftime('%H:%M:%S')
                    }

        gunshots_list[gunshot_id] = gunshot_info

        with open(self.gunshot_file, "w") as gunshots:
            json.dump(gunshots_list, gunshots)
        
        return 0

    def get_fpgas(self, id:str="") -> dict:
        with open(self.fpgas_file, "r") as fpgas:
            fpgas_list = json.load(fpgas)

        if not id:
            return fpgas_list
        else:
            return fpgas_list.get(id, {})

    def get_gunshot(self) -> dict:
        with open(self.gunshot_file, "r") as gunshots:
            gunshot_list = json.load(gunshots)

        return gunshot_list
