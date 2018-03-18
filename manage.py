#!/usr/bin/env python
import os
import sys
import dotenv

if __name__ == "__main__":

    dotenv.read_dotenv()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vk_bot_prj.settings")
    os.environ.setdefault('DJANGO_CONFIGURATION', 'Hosting')

    from configurations.management import execute_from_command_line
    
    execute_from_command_line(sys.argv)
