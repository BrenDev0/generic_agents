from dotenv import load_dotenv
load_dotenv()
import pytest
from unittest.mock import Mock
from src.email.application.use_cases.verification_email import VerificationEmail
from src.email.domain.entities import Email

@pytest.fixture
def mock_sender():
    return Mock()

@pytest.fixture
def use_case(mock_sender):
    return VerificationEmail(sender=mock_sender)


def test_verification_email_with_real_template(
    mock_sender,
    use_case: VerificationEmail
):
    to = "test@example.com"
    verification_code = 123456
    
    use_case.execute(to=to, verification_code=verification_code)
    
    email_arg = mock_sender.execute.call_args[1]['email']
    
    assert email_arg.to == to
    assert str(verification_code) in email_arg.html