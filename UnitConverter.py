import pint
from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler


class UnitConverter(AliceSkill):
	"""
	Author: Lazza
	Description: Converts between two given units of measurement.
	Also deals with gas oven gas mark conversion
	"""


	def __init__(self):
		self._comparing = False
		super().__init__()


	@IntentHandler('convertUnit')
	def convertBetweenUnits(self, session: DialogSession):
		self.processRequest(session=session)


	@IntentHandler('compareUnit')
	def compareBetweenUnits(self, session: DialogSession):
		self._comparing = True
		self.processRequest(session=session)


	def processRequest(self, session):
		"""
		Process the incoming request and convert it to the desired unit
		:param session: The dialog session
		:return:
		"""
		# failsafe just in case this method catches a gasmark request
		if 'GasMark' in session.slots and 'TemperatureType' in session.slots:
			return

		# Check both units are specified for proper conversion
		if self.checkForInvalidInput(session):
			return

		requestedNumber: int = session.slotValue('UnitNumber')
		if not requestedNumber:
			requestedNumber = 1

		firstUnit, secondUnit = self.firstAndSecondUnits(session=session)

		# Get Raw value to dodge the need to convert to plurals from pints naming scheme
		rawFirstUnit: str = session.slotRawValue('FirstUnit')
		rawSecondUnit: str = session.slotRawValue('SecondUnit')

		# If it's a temperature conversion request then use another method
		if self.checkIfTemperatureRequest(session=session, firstUnit=firstUnit, requestedNumber=requestedNumber):
			return

		try:
			convertedValue, dimension1, dimension2 = self.returnCalulationResults(
				requestedNumber=requestedNumber,
				firstUnit=firstUnit,
				secondUnit=secondUnit
			)

			if convertedValue == 'cancel':
				self.endDialog(
					sessionId=session.sessionId,
					text=f'You can\'t convert between a {dimension1} and a {dimension2}. It\'s that whole comparing between apples and pears thing, just doesn\'t work',
					deviceUid=session.deviceUid)
				return

			if self._comparing:
				answer = f"For every {requestedNumber} {rawSecondUnit} there is {convertedValue} {rawFirstUnit} "
			else:
				answer = f"{requestedNumber} {rawFirstUnit} equals {convertedValue} {rawSecondUnit}"

			self.replyWithResults(session=session, answer=answer)

		except:
			self.logError(f"An error occured. Please check my logs")
			self.endDialog(
				sessionId=session.sessionId,
				text=f"An error occured. Please check my logs",
				deviceUid=session.deviceUid
			)


	@IntentHandler('informGasMark')
	def gasMarkIntent(self, session):
		"""
		Get the gas mark level for ovens
		:param session: The dialog session
		:return:
		"""
		if 'Number' not in session.slotsAsObjects:
			self.endDialog(session.sessionId, self.randomTalk(text='respondNoIdea'))
			return

		# Spokeninput is the users requested temperature
		spokenInput = session.slotValue('Number')

		fahrenheitList = ['degF', 'Fahrenheit', 'f', 'F']
		if session.slotValue('TemperatureType') in fahrenheitList:
			spokenInput = self.convertToCelsius(spokenInput)

		if spokenInput < 135:
			self.endDialog(session.sessionId, self.randomTalk(text='respondOutOfRange'))
			return
		elif 135 <= spokenInput <= 148:
			correctGasMark = 1
		elif 149 <= spokenInput <= 162:
			correctGasMark = 2
		elif 163 <= spokenInput <= 176:
			correctGasMark = 3
		elif 177 <= spokenInput <= 190:
			correctGasMark = 4
		elif 191 <= spokenInput <= 203:
			correctGasMark = 5
		elif 204 <= spokenInput <= 217:
			correctGasMark = 6
		elif 218 <= spokenInput <= 231:
			correctGasMark = 7
		elif 232 <= spokenInput <= 245:
			correctGasMark = 8
		elif 246 <= spokenInput <= 269:
			correctGasMark = 9
		elif 270 <= spokenInput <= 290:
			correctGasMark = 10
		else:
			self.endDialog(session.sessionId, self.randomTalk(text='respondAboveRange'))
			return

		self.endDialog(session.sessionId, self.randomTalk(text='respondGasMark', replace=[correctGasMark]))


	def firstAndSecondUnits(self, session):
		"""
		Create the first and second units depepnding if it's a compare or a convert request
		:param session: the dialog Session
		:return:
		"""
		if self._comparing:
			firstUnit: str = self.joinMultpileWords(stringg=session.slotValue('SecondUnit'))
			secondUnit: str = self.joinMultpileWords(stringg=session.slotValue('FirstUnit'))
		else:
			firstUnit: str = self.joinMultpileWords(stringg=session.slotValue('FirstUnit'))
			secondUnit: str = self.joinMultpileWords(stringg=session.slotValue('SecondUnit'))

		return firstUnit, secondUnit


	@staticmethod
	def convertToFahrenheit(temperature: int) -> int:
		return int((9 * temperature) / 5 + 32)


	@staticmethod
	def convertToCelsius(temperature: int) -> int:
		return int((temperature - 32) * 5 / 9)


	@staticmethod
	def joinMultpileWords(stringg: str):
		"""
		Place the underscore back into the slot for re use with pint
		:param stringg: the slot value
		:return: stringg joined with a underscore if required
		"""
		return stringg.replace(" ", "_")


	def checkIfTemperatureRequest(self, session, firstUnit, requestedNumber) -> bool:
		"""
		Processes a temperature request as the procedure is a little different than a normal conversion
		:param session: The dialog session
		:param firstUnit: The first requested temperture Unit IE: celsius
		:param requestedNumber: The second rquested temperature unit IE: Fahrenhiet
		:return: True if user request was a temperature conversion
		"""
		degList = ['degF', 'degC']
		if firstUnit in degList and session.slotValue('SecondUnit') in degList:

			ureg = pint.UnitRegistry()
			converterInstance = ureg.Quantity
			ureg.default_format = '.1f'

			if firstUnit == "degF":
				temperatureUnit = ureg.degF
				outputUnit = "degC"

			else:
				temperatureUnit = ureg.degC
				outputUnit = "degF"

			requestedTemperature = converterInstance(requestedNumber, temperatureUnit)

			answer = f"That would be {str(requestedTemperature.to(outputUnit)).replace('_', ' ')} "

			self.replyWithResults(session=session, answer=answer)
			return True

		return False


	def returnCalulationResults(self, requestedNumber, firstUnit, secondUnit):
		"""
		Do the conversion calculation and return required values
		:param requestedNumber: The number requested from the user
		:param firstUnit: The first unit the user spoke
		:param secondUnit: The unit the user wants converted into
		:return: value, modified unitName, modified RequestedName
		"""
		ureg = pint.UnitRegistry()
		converterInstance = ureg.Quantity
		converterInstance(requestedNumber, firstUnit)
		userInput = f'{requestedNumber} * {firstUnit} to {secondUnit}'
		src, dst = userInput.split(' to ')

		# Capture Error before a exception occurs
		if converterInstance(src).dimensionality != converterInstance(dst).dimensionality:
			return 'cancel', converterInstance(src).dimensionality, converterInstance(dst).dimensionality

		# Check if converted value is a whole number, adjust decimal places as required
		convertedValue = self.isWhole(number=converterInstance(src).to(dst).magnitude)
		return convertedValue, converterInstance(src).dimensionality, converterInstance(dst).dimensionality


	def replyWithResults(self, session, answer):
		""" End dialog with the converted answer"""
		self._comparing = False
		self.endDialog(
			sessionId=session.sessionId,
			text=f"{answer}",
			deviceUid=session.deviceUid
		)


	@staticmethod
	def isWhole(number):
		"""
		Adjust decimal positions based on the converted value
		:param number: The converted number
		:return: Modified value with required decimal place
		"""
		if number % 1 == 0:
			return int(number)
		elif 0.01 <= number % 1 <= 0.09:
			return round(number, 3)
		elif 0.001 <= number % 1 <= 0.009:
			return round(number, 4)
		elif 0.0001 <= number % 1 <= 0.0009:
			return round(number, 5)
		else:
			return round(number, 1)


	def checkForInvalidInput(self, session) -> bool:
		if not session.slotValue('FirstUnit') or not session.slotValue('SecondUnit'):
			self.logWarning(f"Sorry but I require two different units to compare")

			self.endDialog(
				sessionId=session.sessionId,
				text=f"Sorry but I require two different units to compare",
				deviceUid=session.deviceUid
			)
			return True
		else:
			return False
