from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from payment.service import SandBoxPayment


class SandBoxPaymentTests(SimpleTestCase):

    def setUp(self):
        self.urls = {
            "send_infor": "https://example.com/request",
            "redirect_to_zarinpal": "https://example.com/StartPay/",
            "verify_url": "https://example.com/verify",
        }

        self.payment = SandBoxPayment(self.urls)

    @patch("payment.service.requests.post")
    def test_send_information_success(self, mock_post):
        """
        وقتی زرین پال status_code=200 برگرداند،
        send_information باید True و response json را برگرداند.
        """

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 100,
            "data": {
                "authority": "A000000000000000000000000001"
            }
        }

        mock_post.return_value = mock_response

        status, data = self.payment.send_information(
            merchat_id="test-merchant",
            amount=100000,
            descriptoin="test payment",
            callback_url="http://testserver/payment/verify/",
            metadata={"email": "test@example.com"},
        )

        self.assertTrue(status)
        self.assertEqual(
            data["data"]["authority"],
            "A000000000000000000000000001",
        )

        mock_post.assert_called_once()

    @patch("payment.service.requests.post")
    def test_send_information_failure(self, mock_post):
        """
        وقتی درخواست به زرین پال با status غیر 200 برگردد،
        باید False و None برگردد.
        """

        mock_response = Mock()
        mock_response.status_code = 400

        mock_post.return_value = mock_response

        status, data = self.payment.send_information(
            merchat_id="test-merchant",
            amount=100000,
            descriptoin="test payment",
            callback_url="http://testserver/payment/verify/",
            metadata={"email": "test@example.com"},
        )

        self.assertFalse(status)
        self.assertIsNone(data)

    def test_redirect_to_zarinpal(self):
        """
        باید authority را به URL پرداخت اضافه کند.
        """

        data = {
            "data": {
                "authority": "A123456"
            }
        }

        result = self.payment.redirect_to_zarinpal(data)

        self.assertEqual(
            result,
            "https://example.com/StartPay/A123456",
        )

    @patch("payment.service.requests.post")
    def test_verify_success(self, mock_post):
        """
        وقتی verify با status_code=200 پاسخ دهد،
        باید True و response json برگردد.
        """

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 100,
            "data": {
                "code": 100,
                "card_pan": "603799******1234",
                "fee": 1000,
            },
        }

        mock_post.return_value = mock_response

        request_data = {
            "merchant_id": "test-merchant",
            "amount": 100000,
            "authority": "A123456",
        }

        status, data = self.payment.verify(request_data)

        self.assertTrue(status)
        self.assertEqual(data["data"]["code"], 100)

        mock_post.assert_called_once()

    @patch("payment.service.requests.post")
    def test_verify_failure(self, mock_post):
        """
        وقتی verify با status غیر 200 پاسخ دهد،
        باید False و None برگردد.
        """

        mock_response = Mock()
        mock_response.status_code = 400

        mock_post.return_value = mock_response

        status, data = self.payment.verify({
            "merchant_id": "test-merchant",
            "amount": 100000,
            "authority": "A123456",
        })

        self.assertFalse(status)
        self.assertIsNone(data)
