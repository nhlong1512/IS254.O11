import pickle
import streamlit as st
from selenium import webdriver
from ctypes.wintypes import SERVICE_STATUS_HANDLE
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os


driver = webdriver.Firefox()
url_item = 'http://www.google.com'
driver.get(url_item)