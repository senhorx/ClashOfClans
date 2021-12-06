#Libs Python
import json
import os
import requests
import time
import datetime
import autoit
import pandas as pd


#Lib do Selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchWindowException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

#My Libs
import vars
import lib
import lib_web
from lib_txt import log
from clash_royale import clash_royale