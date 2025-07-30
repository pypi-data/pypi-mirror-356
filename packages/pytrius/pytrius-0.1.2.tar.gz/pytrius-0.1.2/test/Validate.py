import os
import math
import struct


class Validate:
    RESULTS_OF_THE_TESTS_CONDUCTED_IN = "=====Results of the tests conducted in "
    TEST_FAILED = " : test failed"
    TERM = "======"
    LOG = ".log"
    SGN_MASK = 0x8000000000000000

    # Directory as a basis for output
    OUTPUT_DIR = "validationLog"  # You may need to replace this with a valid temporary directory path.

    def __init__(self, test_class):
        """Constructor of the Validate object."""
        self.test_class = test_class
        self.deviation_log_non_reg = []
        self.deviation_log_external_ref = []

    def assert_equals(self, actual, non_reg_expected, non_reg_eps, external_ref_expected, external_ref_eps, deviation_description):
        """Works as a replacement to assertEquals, with deviation logging."""
        deviation_value = abs(actual - external_ref_expected)

        try:
            self.assert_equals_internal(actual, external_ref_expected, external_ref_eps)
        except AssertionError as e:
            self.deviation_log_external_ref.append(Deviation(deviation_description + self.TEST_FAILED, deviation_value, external_ref_eps))
            deviation_value = abs(actual - non_reg_expected)
            self.deviation_log_non_reg.append(Deviation(deviation_description + self.TEST_FAILED, deviation_value, non_reg_eps))
            raise e
        self.deviation_log_external_ref.append(Deviation(deviation_description, deviation_value, external_ref_eps))

        deviation_value = abs(actual - non_reg_expected)
        try:
            self.assert_equals_internal(actual, non_reg_expected, non_reg_eps)
        except AssertionError as e:
            self.deviation_log_non_reg.append(Deviation(deviation_description + self.TEST_FAILED, deviation_value, non_reg_eps))
            raise e
        self.deviation_log_non_reg.append(Deviation(deviation_description, deviation_value, non_reg_eps))

    def assert_equals_internal(self, actual, expected, eps):
        """Helper function to assert equality within epsilon."""
        assert self.equals_with_relative_tolerance(actual, expected, eps)

    def assert_equals_array(self, actual, non_reg_expected, non_reg_eps, external_ref_expected, external_ref_eps, deviation_description):
        """Compute the deviation of each table value and store it in the logs."""
        if len(actual) == len(non_reg_expected) and len(actual) == len(external_ref_expected):
            for i in range(len(actual)):
                self.assert_equals(actual[i], non_reg_expected[i], non_reg_eps, external_ref_expected[i], external_ref_eps, deviation_description)

    def assert_equals_with_relative_tolerance(self, actual, non_reg_expected, non_reg_eps, external_ref_expected, external_ref_eps, deviation_description):
        """Works as a replacement to assertEquals for a relative comparison."""
        deviation_value_ref = 0.0
        max_ref = max(abs(actual), abs(external_ref_expected))
        if max_ref != 0.0:
            deviation_value_ref = abs(actual - external_ref_expected) / max_ref

        deviation_value_reg = 0.0
        max_reg = max(abs(actual), abs(non_reg_expected))
        if max_reg != 0.0:
            deviation_value_reg = abs(actual - non_reg_expected) / max_reg

        try:
            self.assert_equals_with_relative_tolerance_internal(actual, external_ref_expected, external_ref_eps)
        except AssertionError as e:
            self.deviation_log_external_ref.append(Deviation(deviation_description + self.TEST_FAILED, deviation_value_ref, external_ref_eps))
            self.deviation_log_non_reg.append(Deviation(deviation_description + self.TEST_FAILED, deviation_value_reg, non_reg_eps))
            raise e
        self.deviation_log_external_ref.append(Deviation(deviation_description, deviation_value_ref, external_ref_eps))

        try:
            self.assert_equals_with_relative_tolerance_internal(actual, non_reg_expected, non_reg_eps)
        except AssertionError as e:
            self.deviation_log_non_reg.append(Deviation(deviation_description + self.TEST_FAILED, deviation_value_reg, non_reg_eps))
            raise e
        self.deviation_log_non_reg.append(Deviation(deviation_description, deviation_value_reg, non_reg_eps))

    def assert_equals_with_relative_tolerance_internal(self, actual, expected, eps):
        """Helper function for relative tolerance assertions."""
        assert self.equals_with_relative_tolerance(actual, expected, eps)

    def produce_log(self, log_dir=None):
        """Print the log in the console and in files."""
        print(self.RESULTS_OF_THE_TESTS_CONDUCTED_IN + self.test_class.__name__ + self.TERM)

        directory = self.OUTPUT_DIR
        if log_dir:
            directory = os.path.join(self.OUTPUT_DIR, log_dir)
        else:
            directory = os.path.join(self.OUTPUT_DIR, self.test_class.__module__)

        os.makedirs(directory, exist_ok=True)

        # Writing non-regression log
        self._write_log(directory, "NonReg", self.deviation_log_non_reg)

        # Writing external reference log
        self._write_log(directory, "ExternalRef", self.deviation_log_external_ref)

    def _write_log(self, directory, log_type, deviation_log):
        """Helper method to write deviation log into a file."""
        file_path = os.path.join(directory, f"{self.test_class.__name__}{log_type}{self.LOG}")
        print(file_path)

        with open(file_path, 'w') as writer:
            writer.write(self.RESULTS_OF_THE_TESTS_CONDUCTED_IN + self.test_class.__name__ + self.TERM + '\n')
            for deviation in deviation_log:
                print(deviation)
                writer.write(str(deviation) + '\n')

    @staticmethod
    def equals(x, y, eps):
        """Return true if x and y are within the allowed epsilon range."""
        gap = abs(y - x) if not (math.isnan(x) or math.isnan(y)) else float('nan')
        return Validate.equals_internal(x, y, 1) or gap <= eps

    @staticmethod
    def equals_internal(x, y, max_ulps):
        """Check if the difference between x and y is within the allowed range of ulps."""
        x_int = struct.unpack('>q', struct.pack('>d', x))[0]
        y_int = struct.unpack('>q', struct.pack('>d', y))[0]

        # Adjust for sign bit
        if x_int < 0:
            x_int = Validate.SGN_MASK - x_int
        if y_int < 0:
            y_int = Validate.SGN_MASK - y_int

        return abs(x_int - y_int) <= max_ulps and not (math.isnan(x) or math.isnan(y))

    @staticmethod
    def equals_with_relative_tolerance(x, y, eps):
        """Check if x and y are within the allowed relative tolerance."""
        if Validate.equals(x, y, 1):
            return True

        absolute_max = max(abs(x), abs(y)) if not (math.isnan(x) or math.isnan(y)) else float('nan')
        if absolute_max == 0.0:
            return False
        relative_difference = abs((x - y) / absolute_max)
        return relative_difference <= eps


class Deviation:
    """Class to represent a deviation's value and description."""

    def __init__(self, description, deviation, epsilon):
        self.description = description
        self.deviation = deviation
        self.epsilon = epsilon

    def __str__(self):
        return f"{self.deviation}\t{self.epsilon}\t{self.description}"

