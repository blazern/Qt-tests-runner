from TestResult import *

class TestingData:
	_before_group_name_str = "Start testing of "

	def __init__(self):
		self.executables_count = 0
		self.entire_output = str()
		self.fails = list()
		self.passes = list()

	@property
	def executables_count(self):
		return self.executables_count

	@property
	def entire_output(self):
		return self.entire_output

	@property
	def fails(self):
		return self.fails

	@property
	def passes(self):
		return self.passes

	@property
	def is_empty(self):
		return len(self.entire_output) == 0
	

	def on_test_executable_finished(self, executable_output):
		self.executables_count += 1
		self.entire_output += executable_output + "\n"

		tests_group_name = self._get_tests_group_name(executable_output)

		while (self._has_tests_results(executable_output)):
			test_result_message = self._get_next_text_result_message(executable_output)

			if "FAIL" in test_result_message:
				self.fails.append(TestResult(tests_group_name, True, test_result_message))
			else:
				self.passes.append(TestResult(tests_group_name, False, test_result_message))
			executable_output = executable_output.replace(test_result_message, "")

	def _get_tests_group_name(self, executable_output):
		before_group_name_index = executable_output.find(TestingData._before_group_name_str)
		name_start_index = before_group_name_index + len(TestingData._before_group_name_str)
		name_end_index = executable_output.find(" ", name_start_index)
		return executable_output[name_start_index:name_end_index]

	def _has_tests_results(self, executable_output):
		return "FAIL" in executable_output or "PASS" in executable_output

	def _get_next_text_result_message(self, executable_output):
		max_index = len(executable_output)
		fail_index = executable_output.find("FAIL")
		pass_index = executable_output.find("PASS")

		if fail_index == -1 and pass_index == -1:
			raise Exception("ERROR: there is no any other test message \
							but _get_next_text_result_message() asked to get one")

		fail_index = fail_index if fail_index != -1 else max_index
		pass_index = pass_index if pass_index != -1 else max_index

		start_index = fail_index if fail_index < pass_index else pass_index

		next_fail_index = executable_output.find("FAIL", start_index + 1)
		next_fail_index = next_fail_index if next_fail_index != -1 else max_index
		next_pass_index = executable_output.find("PASS", start_index + 1)
		next_pass_index = next_pass_index if next_pass_index != -1 else max_index
		totals_index = executable_output.find("Totals")

		if totals_index < next_fail_index and totals_index < next_pass_index:
			end_index = totals_index
		else:
			end_index = next_fail_index if next_fail_index < next_pass_index else next_pass_index

		return executable_output[start_index:end_index]
