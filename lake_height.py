#!/usr/bin/python
# Display lake height from NOAA data
#lcd up arrow -> lcd.create_char(1, [0,15,3,5,9,16,0,0])
#lcd down arrow -> lcd.create_char(2, [0,16,9,5,3,15,0,0])
import math
import time
import xml.etree.ElementTree as ET
import urllib2
from bs4 import BeautifulSoup
import Adafruit_CharLCD as LCD

def lcd_output( str ):
	"""Displays str on LCD display"""
	lcd.clear()
	lcd.message( str )
	return

def get_lake_height(heights):
	"""Get xml array from NOAA"""
	tempHeights = []
	try:
		response = urllib2.urlopen( 'http://water.weather.gov/ahps2/hydrograph_to_xml.php?gage=nvlw3&output=xml' )
		html = response.read()
		root = ET.fromstring( html )
		for child in root.iterfind( 'observed/datum/primary' ):
			tempHeights.append( child.text )

		return tempHeights
	except:
		return heights

def get_wind(prev_wind):
	"""Gets speed of wind from html page"""
	try:
		url = 'http://www.windfinder.com/forecast/Edgerton_lake_koshkonong'
		soup = BeautifulSoup(urllib2.urlopen( url ).read())
		speed = soup.find("span", {"class": "current__wind__speed"})
		direction = soup.find("span", {"class": "current__wind__dir"})
		return {"Speed": speed.get_text(), "Direction": direction.get_text().strip().replace("\n", "")}
	except:
		return prev_wind

def print_display( height, wind ):
	"""Prints lastest height and wind to LCD"""
	depth_length = 16 - (len("Depth: ") + len(height) + len(" ft"))
	depth_space = ' ' * depth_length

	wind_length = 16 - (len("Wind: ") + len(wind['Speed']) + len(wind['Direction']) + 1)
	wind_space = ' ' * wind_length

	lcd_output( "Depth: " + depth_space + height + " ft\nWind: " + wind_space + wind['Speed'] + " " + wind['Direction'])

# Initialize LCD
lcd = LCD.Adafruit_CharLCDPlate()

# Initialize variables
heights = get_lake_height([0, 0])
last_save = time.time()
wind = get_wind({"Speed": "0", "Direction": ""})
print_display( heights[0], wind )

while True:
	if time.time() - last_save > 250:
		wind = get_wind(wind)
	if time.time() - last_save > 900:
		heights = get_lake_height(heights)

		# Print to LCD
		print_display( heights[0], wind )

		# Updates last lave
		last_save = time.time()
