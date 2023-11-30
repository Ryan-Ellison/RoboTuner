import adafruit_ssd1306
import board
import busio
from PIL import Image, ImageDraw, ImageFont

class Display:
	def __init__(_, startup_msg="RoboTuner\nbooting up..."):
		_.mode = True
		_.note = "Waiting..."
		_.cents_off = "Waiting..."
		
		_.width = 128
		_.height = 64
		_.i2c = busio.I2C(board.pin.D1, board.pin.D0)
		_.oled = adafruit_ssd1306.SSD1306_I2C(_.width, _.height, _.i2c, addr=0x3c)
		
		_.oled.fill(0)
		_.oled.show()
		_.image = Image.new("1", (_.oled.width, _.oled.height))
		_.draw = ImageDraw.Draw(_.image)
		
		_.data_str = "mode: {0}\nnote:      {1}\ncents off: {2}\n"
		_.homing_str = "homing..."
		_.res_det_str = "RESISTANCE DETECTED\n\nPlease lubricate\nyour tuning slide"
		_.check_complete_str = "Hardware check complete\nRefer to Hardware Assembly tab"
		
		# ~ _.update_display(startup_msg)

	def update_display(_, msg, offsetx=2, offsety=2):
		_.draw.rectangle((0, 0, _.width, _.height), 0)
		font = ImageFont.load_default()
		_.draw.multiline_text((2, 2), msg, font=font, fill=255)
		_.oled.image(_.image)
		_.oled.show()

	def update_data(_, mode=True, note=None, cents_off=None):
		_.mode = "Auto Tuning" if mode else "Reference Pitch"
		if note != None: _.note = note
		if cents_off != None: _.cents_off = cents_off
		
		text = _.data_str.format(_.mode, _.note, _.cents_off)
		_.update_display(text)
		
	def homing(_):
		_.update_display(_.homing_str)
		
	def res_detected(_):
		_.update_display(_.res_det_str)

	def hardware_check(_):
		_.update_display(_.check_complete_str)

# ~ import time
# ~ dis = Display()
# ~ while True:
	# ~ dis.update_data()
	# ~ time.sleep(2)
	# ~ dis.homing()
	# ~ time.sleep(2)
	# ~ dis.res_detected()
	# ~ time.sleep(2)
