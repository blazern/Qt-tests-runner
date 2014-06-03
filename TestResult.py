class TestResult:
	def __init__(self, tests_group_name, is_fail, message):
		self.tests_group_name = tests_group_name
		self.is_fail = is_fail
		self.message = message

	@property
	def tests_group_name(self):
		return self.tests_group_name

	@property
	def is_fail(self):
		return self.is_fail

	@property
	def message(self):
		return self.message
