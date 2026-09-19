"""
Test Cases for Account Model
"""
import json
from pathlib import Path
import pytest
from models import db
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

@pytest.fixture(scope="module", autouse=True)
def load_account_data():
    """ Load data needed by tests """
    global ACCOUNT_DATA
    with open(Path(__file__).parent / 'fixtures' / 'account_data.json') as json_data:
        ACCOUNT_DATA = json.load(json_data)

    # Set up the database tables
    db.create_all()
    yield
    db.session.close()

@pytest.fixture
def setup_account():
    """Fixture to create a test account"""
    account = Account(name="John businge", email="john.businge@example.com")
    db.session.add(account)
    db.session.commit()
    return account

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    """ Truncate the tables and set up for each test """
    db.session.query(Account).delete()
    db.session.commit()
    yield
    db.session.remove()

######################################################################
#  E X A M P L E   T E S T   C A S E
######################################################################

# ===========================
# Test Group: Role Management
# ===========================

# ===========================
# Test: Account Role Assignment
# Author: John Businge
# Date: 2025-01-30
# Description: Ensure roles can be assigned and checked.
# ===========================

def test_account_role_assignment():
    """Test assigning roles to an account"""
    account = Account(name="John Doe", email="johndoe@example.com", role="user")

    # Assign initial role
    assert account.role == "user"

    # Change role and verify
    account.change_role("admin")
    assert account.role == "admin"

# ===========================
# Test: Invalid Role Assignment
# Author: John Businge
# Date: 2025-01-30
# Description: Ensure invalid roles raise a DataValidationError.
# ===========================

def test_invalid_role_assignment():
    """Test assigning an invalid role"""
    account = Account(role="user")

    # Attempt to assign an invalid role
    with pytest.raises(DataValidationError):
        account.change_role("moderator")  # Invalid role should raise an error


######################################################################
#  T O D O   T E S T S  (To Be Completed by Students)
######################################################################

"""
Each student in the team should implement **one test case** from the list below.
The team should coordinate to **avoid duplicate work**.

Each test should include:
- A descriptive **docstring** explaining what is being tested.
- **Assertions** to verify expected behavior.
- A meaningful **commit message** when submitting their PR.
"""

# Test Assignments

# Student 1: Test account serialization
# - Verify that the account object is correctly serialized to a dictionary.
# - Ensure all expected fields are included in the output.
# Target Method: to_dict()

# Student 2: Test invalid email input
# - Ensure invalid email formats raise a validation error.
# Target Method: validate_email()

# ===========================
# Test: Invalid Email Input
# Author: Kyle Burns
# Date: 2026-09-18
# Description: Ensure invalid emails raise a DataValidationError.
# ===========================

def test_invalid_email():
    """Test making an invalid email"""
    account = Account(name="KB", email="invalid-email")
    with pytest.raises(DataValidationError):
        account.validate_email()

# Student 3: Test missing required fields
# - Ensure a DataValidationError is raised when name or email is missing.
# - Note: SQLAlchemy does not validate on construction, so Account() itself
#   never raises. Call the validation method on the constructed object.
# Target Method: validate_required_fields()

# Student 4: Test positive deposit
# - Verify that depositing a positive amount correctly increases the balance.
# Target Method: deposit()

# ===========================
# Test: Positive Deposit
# Author: Abel Berhe
# Date: 2026-09-18
# Description: Ensures a positive amount deposits correctly increases the balance.
# ===========================
def test_positive_deposit():
    """Test depositing a positive amount into an account"""
    account = Account(name="John Doe", email="johndoe@example.com", balance=100)

    # Deposit a positive amount
    account.deposit(50)

    # Verify the balance increased correctly
    assert account.balance == 150





# Student 5: Test deposit with zero/negative values
# - Ensure zero or negative deposits are rejected.
# Target Method: deposit()

# Student 6: Test valid withdrawal
# - Verify that withdrawing a valid amount correctly decreases the balance.
# Target Method: withdraw()
# ===========================
# Test: Valid Account Withdrawal
# Author: Mingchuan Hu
# Date: 2026-09-18
# Description: Ensure a valid withdrawal correctly decreases the balance
# ===========================
def test_valid_withdrawal():
    """Test withdrawing a valid amount from an account"""
    account = Account(name="Mingchuan Hu", email="ming.hu@example.com", balance = 100.0)

    account.withdraw(35.0)

    assert account.balance == 65.0


# Student 7: Test withdrawal with insufficient funds
# - Ensure withdrawal fails when balance is insufficient.
# Target Method: withdraw()
# ===========================
# Test: Test withdrawal with insufficient funds
# Author: Devin Allen
# Date: 2026-09-18
# Description: Ensure withdrawing more than the available balance raises DataValidationError and does not change the balance. 
# ===========================
def test_withdraw_insufficient_funds():
    "Test withdrawing more than the avilable account balance"
    account = Account(
        name = "Apple Apple",
        email= "Apple@test.com",
        balance = 100
        )

    # Attempt to withdraw greater money than account
    with pytest.raises(DataValidationError, match="Insufficient balance"): 
        account.withdraw(150)

    # Verify failed withdrawal
    assert account.balance == 100


# Student 8: Test password hashing
# - Ensure passwords are properly hashed.
# - Verify that password verification works correctly.
# Target Methods: set_password() / check_password()

# ===========================
# Test: Test password hashing
# Author: David Penrose
# Date: 2026-09-18
# Description: Ensure passwords are properly hashed and can be verified.
# ===========================
def test_password_hashing():
    """Test password hashing and verification"""
    account = Account(name="John Doe", email="johndoe@example.com", balance=100)
    account.set_password("securepassword")
    assert account.check_password("securepassword") is True
    assert account.check_password("wrongpassword") is False

# Student 9: Test account deactivation/reactivation
# - Ensure accounts can be deactivated and reactivated correctly.
# Target Methods: deactivate() / reactivate()
# ===========================
# Test: Account Deactivation and Reactivation
# Author: Omari Rich
# Date: 2026-09-18
# Description: Ensure an account can be deactivated and reactivated.
# ===========================

def test_account_deactivation_reactivation():
    """Test deactivating and reactivating an account"""
    account = Account(
        name="Omari Rich",
        email="omari.rich@example.com",
        disabled=False
    )

    assert account.disabled is False

    account.deactivate()
    assert account.disabled is True

    account.reactivate()
    assert account.disabled is False

# Student 10: Test email uniqueness enforcement
# - Ensure duplicate emails are not allowed.
# Target Method: validate_unique_email()

# Student 11: Test deleting an account
# - Verify that an account can be successfully deleted from the database.
# Target Method: delete()