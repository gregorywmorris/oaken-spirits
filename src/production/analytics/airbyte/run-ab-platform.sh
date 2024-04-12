#!/bin/bash

# version=1.0

########## Pointless Banner for street cred ##########
# Make sure the console is huuuge

  # Make it green!
  echo -e "\033[32m"
  echo -e " █████╗ ██╗██████╗ ██████╗ ██╗   ██╗████████╗███████╗"
  echo -e "██╔══██╗██║██╔══██╗██╔══██╗╚██╗ ██╔╝╚══██╔══╝██╔════╝"
  echo -e "███████║██║██████╔╝██████╔╝ ╚████╔╝    ██║   █████╗  "
  echo -e "██╔══██║██║██╔══██╗██╔══██╗  ╚██╔╝     ██║   ██╔══╝  "
  echo -e "██║  ██║██║██║  ██║██████╔╝   ██║      ██║   ███████╗"
  echo -e "╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═════╝    ╚═╝      ╚═╝   ╚══════╝"
  echo -e "                                            Move Data"
  # Make it less green
  echo -e "\033[0m"
  sleep 1

########## Environment Variables

cp env-template .env

########## Docker ##########

docker-compose up -d
