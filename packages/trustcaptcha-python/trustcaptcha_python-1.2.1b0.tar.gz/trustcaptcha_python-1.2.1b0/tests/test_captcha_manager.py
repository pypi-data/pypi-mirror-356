import unittest
from uuid import UUID

from src.trustcaptcha.captcha_manager import CaptchaManager, VerificationTokenInvalidException, \
    VerificationNotFoundException, SecretKeyInvalidException, VerificationNotFinishedException

# Vordefinierte Base64-Tokens
VERIFICATION_VALID = "eyJhcGlFbmRwb2ludCI6Imh0dHBzOi8vYXBpLmNhcHRjaGEudHJ1c3RjYXB0Y2hhLmNvbSIsInZlcmlmaWNhdGlvbklkIjoiMDAwMDAwMDAtMDAwMC0wMDAwLTAwMDAtMDAwMDAwMDAwMDAwIiwiZW5jcnlwdGVkQWNjZXNzVG9rZW4iOiJ0b2tlbiJ9"
VERIFICATION_NOT_FOUND = "eyJhcGlFbmRwb2ludCI6Imh0dHBzOi8vYXBpLmNhcHRjaGEudHJ1c3RjYXB0Y2hhLmNvbSIsInZlcmlmaWNhdGlvbklkIjoiMDAwMDAwMDAtMDAwMC0wMDAwLTAwMDAtMDAwMDAwMDAwMDAxIiwiZW5jcnlwdGVkQWNjZXNzVG9rZW4iOiJ0b2tlbiJ9"
VERIFICATION_LOCKED = "eyJhcGlFbmRwb2ludCI6Imh0dHBzOi8vYXBpLmNhcHRjaGEudHJ1c3RjYXB0Y2hhLmNvbSIsInZlcmlmaWNhdGlvbklkIjoiMDAwMDAwMDAtMDAwMC0wMDAwLTAwMDAtMDAwMDAwMDAwMDAyIiwiZW5jcnlwdGVkQWNjZXNzVG9rZW4iOiJ0b2tlbiJ9"

class TestCaptchaManager(unittest.TestCase):

    def test_run_get_verification_result(self):
        result = CaptchaManager.get_verification_result("secret-key", VERIFICATION_VALID)
        self.assertEqual(result.verificationId, UUID('00000000-0000-0000-0000-000000000000'))

    def test_throw_verification_token_invalid_exception(self):
        with self.assertRaises(VerificationTokenInvalidException):
            CaptchaManager.get_verification_result("", "")

    def test_throw_verification_not_found_exception(self):
        with self.assertRaises(VerificationNotFoundException):
            CaptchaManager.get_verification_result("secret-key", VERIFICATION_NOT_FOUND)

    def test_throw_secret_key_invalid_exception(self):
        with self.assertRaises(SecretKeyInvalidException):
            CaptchaManager.get_verification_result("invalid-key", VERIFICATION_VALID)

    def test_throw_verification_not_finished_exception(self):
        with self.assertRaises(VerificationNotFinishedException):
            CaptchaManager.get_verification_result("secret-key", VERIFICATION_LOCKED)


if __name__ == "__main__":
    unittest.main()
