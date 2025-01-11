import argparse
import logging
import asyncio
from aiopath import AsyncPath
from aioshutil import copyfile
from typing import List, Any
from time import time

class Sorter:

    def __init__(self, read_folder, copy_folder, log_level):
        self.read_folder = read_folder
        self.copy_folder = copy_folder
        self.logger = self.build_logger(self.get_log_level(log_level))

    def get_log_level(self, log_level):
        match log_level:
            case "DEBUG":
                return logging.DEBUG
            case "INFO":
                return logging.INFO
            case "WARNING":
                return logging.WARNING
            case "ERROR":
                return logging.ERROR
            case "CRITICAL":
                return logging.CRITICAL
            case _:
                raise ValueError(f"Invalid log level {log_level}")

    def build_logger(self, log_level):
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger = logging.getLogger('Sorter')
        logger.setLevel(log_level)
        logger.addHandler(ch)
        return logger
    
    def get_extention(self, file_name):
        return file_name.split(".")[-1]
    
    async def create_subfolder(self, parent_dir, subfolder_name):
        subfolder_path = AsyncPath(parent_dir) / subfolder_name
        if await subfolder_path.exists():
            self.logger.debug(f"Subfolder '{subfolder_name}' in '{subfolder_path}' already exists")
            return
        else:
            await subfolder_path.mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"Subfolder '{subfolder_name}' in '{parent_dir}' created successfully!")

    async def copy_file(self, target: AsyncPath, file: AsyncPath):
        self.logger.debug(f"Start processing file '{file.name}'")
                    
        extention = self.get_extention(file.name)
        self.logger.debug(f"Extention defined ='{extention}'")
                    
        await self.create_subfolder(target, extention)

        self.logger.debug(f"Copying {file.name} to {target}{extention}")
        await copyfile(file, target / extention / file.name)
        
        self.logger.debug(f"Copied file '{file.name}'")

    async def handle_dir(self,apath: AsyncPath, target: AsyncPath) -> List[Any]:
        self.logger.debug(f"Folder '{apath}' exists")
        result = []
        async for object in apath.iterdir():
            if await object.is_file():
                result.append(await self.copy_file(target, object))
            elif await object.is_dir():
                result.extend(await self.handle_dir(apath / object.name, target))
        return result

    async def copy_files(self):
        apath = AsyncPath(self.read_folder)
        target = AsyncPath(self.copy_folder)

        if await apath.exists():
            asyncs = await self.handle_dir(apath, target)
            self.logger.info(f"found files {len(asyncs)}")
            asyncio.gather(*(asyncio.create_task(task) for task in asyncs if task is not None))
        else:
            self.logger.error(f"Folder '{self.read_folder}' does not exist")

    def process(self):
        self.logger.info("Starting")
        self.logger.debug(f"read_folder='{self.read_folder}'")
        self.logger.debug(f"copy_file='{self.copy_folder}'")
        start = time()
        asyncio.run(self.copy_files())
        self.logger.info(f"Finished in {time() - start} seconds")

def get_parameter_value(parameter):
    return parameter.split("=")[1]

def copy_file():
    parser = argparse.ArgumentParser(description="Application for sorting files by extension")
    parser.add_argument("read_folder", type=str, help="directory to read files from")
    parser.add_argument("copy_folder", type=str, help="directory to copy files to")
    parser.add_argument("--log_level", type=str, choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="INFO", help="log level", required=False)
    args = parser.parse_args()
    Sorter(get_parameter_value(args.read_folder), get_parameter_value(args.copy_folder), args.log_level).process()

if __name__ == '__main__':
    copy_file()