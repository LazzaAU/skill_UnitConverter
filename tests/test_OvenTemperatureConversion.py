import unittest

from typing import Any
from unittest import TestCase, mock
from unittest.mock import MagicMock, PropertyMock


try:
	from PublishedSkills.OvenTemperatureConversion.OvenTemperatureConversion import OvenTemperatureConversion
except:
	# noinspection PyUnresolvedReferences
	from OvenTemperatureConversion import OvenTemperatureConversion


class TestOvenTemperatureConversion(TestCase):


	@mock.patch('core.base.SuperManager.SuperManager')
	def test_converting_to_celcius_intent(self, mock_superManager):
		class DialogSession:

			def __init__(self, slotsAsObjects: dict):
				self.slotsAsObjects = slotsAsObjects


			@property
			def sessionId(self) -> str:
				return 'unittest'


			def slotValue(self, slotName: str, index: int = 0, defaultValue: Any = None) -> Any:
				try:
					return self.slotsAsObjects[slotName]
				except (KeyError, IndexError):
					return defaultValue


		class LanguageManager:

			@property
			def activeLanguage(self) -> str:
				return 'en'


			@property
			def supportedLanguages(self) -> list:
				return ['en']


		# mock SuperManager
		mock_superManagerInstance = MagicMock()
		mock_superManager.getInstance.return_value = mock_superManagerInstance
		mock_superManagerInstance.talkManager.randomTalk.return_value = 'unittest'

		mock_languageManager = PropertyMock(return_value=LanguageManager())
		type(mock_superManagerInstance).languageManager = mock_languageManager

		skill = OvenTemperatureConversion()

		# If slot is missing
		session = DialogSession({})
		skill.convertingToCelciusIntent(session)
		mock_superManagerInstance.talkManager.randomTalk.assert_called_once_with(talk='respondNoIdea', skill='UnitConverter')
		mock_superManagerInstance.reset_mock()

		# If slot is wrong case
		session = DialogSession({'number': 10})
		skill.convertingToCelciusIntent(session)
		mock_superManagerInstance.talkManager.randomTalk.assert_called_once_with(talk='respondNoIdea', skill='UnitConverter')
		mock_superManagerInstance.reset_mock()

		# If slot is correct
		session = DialogSession({'Number': 0})
		skill.convertingToCelciusIntent(session)
		mock_superManagerInstance.talkManager.randomTalk.assert_called_once_with(talk='respondTemperature', skill='UnitConverter')
		mock_superManagerInstance.reset_mock()

		# Check if slot value is a int
		session = DialogSession({'Number': 0})
		result = skill.convertingToCelciusIntent(session)

		self.assertTrue(type(result) == int)


	@mock.patch('core.base.SuperManager.SuperManager')
	def test_converting_to_fahrenheit_intent(self, mock_superManager):
		class DialogSession:

			def __init__(self, slotsAsObjects: dict):
				self.slotsAsObjects = slotsAsObjects


			@property
			def sessionId(self) -> str:
				return 'unittest'


			def slotValue(self, slotName: str, index: int = 0, defaultValue: Any = None) -> Any:
				try:
					return self.slotsAsObjects[slotName]
				except (KeyError, IndexError):
					return defaultValue


		class LanguageManager:

			@property
			def activeLanguage(self) -> str:
				return 'en'


			@property
			def supportedLanguages(self) -> list:
				return ['en']


		# mock SuperManager
		mock_superManagerInstance = MagicMock()
		mock_superManager.getInstance.return_value = mock_superManagerInstance
		mock_superManagerInstance.talkManager.randomTalk.return_value = 'unittest'

		mock_languageManager = PropertyMock(return_value=LanguageManager())
		type(mock_superManagerInstance).languageManager = mock_languageManager

		skill = OvenTemperatureConversion()

		# If slot is missing
		session = DialogSession({})
		skill.convertingToFahrenheitIntent(session)
		mock_superManagerInstance.talkManager.randomTalk.assert_called_once_with(talk='respondNoIdea', skill='UnitConverter')
		mock_superManagerInstance.reset_mock()

		# If slot is wrong case
		session = DialogSession({'number': 10})
		skill.convertingToFahrenheitIntent(session)
		mock_superManagerInstance.talkManager.randomTalk.assert_called_once_with(talk='respondNoIdea', skill='UnitConverter')
		mock_superManagerInstance.reset_mock()

		# If slot is correct
		session = DialogSession({'Number': 0})
		skill.convertingToFahrenheitIntent(session)
		mock_superManagerInstance.talkManager.randomTalk.assert_called_once_with(talk='respondTemperature', skill='UnitConverter')
		mock_superManagerInstance.reset_mock()

		# Check if slot value is a int
		session = DialogSession({'Number': 0})
		result = skill.convertingToFahrenheitIntent(session)

		self.assertTrue(type(result) == int)


	def test_ready_to_convert(self):
		pass  # nothing to test


	def test_ask_to_repeat_with_number(self):
		pass  # Nothing to test


	@mock.patch('core.base.SuperManager.SuperManager')
	def test_gas_mark_intent(self, mock_superManager):
		class DialogSession:

			def __init__(self, slotsAsObjects: dict):
				self.slotsAsObjects = slotsAsObjects


			@property
			def sessionId(self) -> str:
				return 'unittest'


			def slotValue(self, slotName: str, index: int = 0, defaultValue: Any = None) -> Any:
				try:
					return self.slotsAsObjects[slotName]
				except (KeyError, IndexError):
					return defaultValue


		class LanguageManager:

			@property
			def activeLanguage(self) -> str:
				return 'en'


			@property
			def supportedLanguages(self) -> list:
				return ['en']


		# mock SuperManager
		mock_superManagerInstance = MagicMock()
		mock_superManager.getInstance.return_value = mock_superManagerInstance
		mock_superManagerInstance.talkManager.randomTalk.return_value = 'unittest'
		mock_languageManager = PropertyMock(return_value=LanguageManager())
		type(mock_superManagerInstance).languageManager = mock_languageManager

		skill = OvenTemperatureConversion()

		# If slot is missing
		session = DialogSession({})
		# send a blank session to the method
		skill.gasMarkIntent(session)
		mock_superManagerInstance.talkManager.randomTalk.assert_called_once_with(skill='UnitConverter', talk='respondNoIdea')
		mock_superManagerInstance.reset_mock()

		# If slot is not uppercase on first char
		session = DialogSession({'number': 10})
		skill.gasMarkIntent(session)
		mock_superManagerInstance.talkManager.randomTalk.assert_called_once_with(skill='UnitConverter', talk='respondNoIdea')
		mock_superManagerInstance.reset_mock()

		# if the Number is under range for a gasmark reading
		session = DialogSession({'Number': 75})
		skill.gasMarkIntent(session)
		mock_superManagerInstance.talkManager.randomTalk.assert_called_once_with(skill='UnitConverter', talk='respondOutOfRange')
		mock_superManagerInstance.reset_mock()

		# if the number is over range for a gasmark reading
		session = DialogSession({'Number': 300})
		skill.gasMarkIntent(session)
		mock_superManagerInstance.talkManager.randomTalk.assert_called_once_with(skill='UnitConverter', talk='respondAboveRange')
		mock_superManagerInstance.reset_mock()

		# This one should be if all is working as expected
		session = DialogSession({'Number': 155})
		skill.gasMarkIntent(session)
		# if session is correct and respondGasMark talk file is called only once then this line passes test
		mock_superManagerInstance.talkManager.randomTalk.assert_called_once_with(skill='UnitConverter', talk='respondGasMark')
		mock_superManagerInstance.reset_mock()

		# Now to test the temperature values fall within the correct gas mark range
		counter = 135
		while counter <= 290:
			if 135 <= counter <= 148:
				session = DialogSession({'Number': counter})
				result = skill.gasMarkIntent(session)
				self.assertEqual(first=1, second=result)
			elif 149 <= counter <= 162:
				session = DialogSession({'Number': counter})
				result = skill.gasMarkIntent(session)
				self.assertEqual(first=2, second=result)
			elif 163 <= counter <= 176:
				session = DialogSession({'Number': counter})
				result = skill.gasMarkIntent(session)
				self.assertEqual(first=3, second=result)
			elif 177 <= counter <= 190:
				session = DialogSession({'Number': counter})
				result = skill.gasMarkIntent(session)
				self.assertEqual(first=4, second=result)
			elif 191 <= counter <= 203:
				session = DialogSession({'Number': counter})
				result = skill.gasMarkIntent(session)
				self.assertEqual(first=5, second=result)
			elif 204 <= counter <= 217:
				session = DialogSession({'Number': counter})
				result = skill.gasMarkIntent(session)
				self.assertEqual(first=6, second=result)
			elif 218 <= counter <= 231:
				session = DialogSession({'Number': counter})
				result = skill.gasMarkIntent(session)
				self.assertEqual(first=7, second=result)
			elif 232 <= counter <= 245:
				session = DialogSession({'Number': counter})
				result = skill.gasMarkIntent(session)
				self.assertEqual(first=8, second=result)
			elif 246 <= counter <= 269:
				session = DialogSession({'Number': counter})
				result = skill.gasMarkIntent(session)
				self.assertEqual(first=9, second=result)
			elif 270 <= counter <= 290:
				session = DialogSession({'Number': counter})
				result = skill.gasMarkIntent(session)
				self.assertEqual(first=10, second=result)

			counter += 1


	# Check that the conversion between Celsius to Fahrenheit is returning correct result
	def test_convertToFahrenheit(self):
		result = OvenTemperatureConversion.convertToFahrenheit(temperature=0)
		self.assertEqual(first=result, second=32)


	# Check that the conversion between Fahrenheit to Celsius is returning correct result
	def test_convertToCelsius(self):
		result = OvenTemperatureConversion.convertToCelsius(temperature=32)
		self.assertEqual(first=result, second=0)


if __name__ == '__main__':
	unittest.main()
