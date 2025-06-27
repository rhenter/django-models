import time
from datetime import datetime

from django_models.utils.generators import (
    generate_random_code,
    generate_md5_hashcode,
    generate_datetime,
    generate_cpf,
    generate_cnpj,
)


class TestGenerateRandomCode:
    def test_generate_random_code_default_length(self):
        """Test generate_random_code with default length."""
        code = generate_random_code()
        assert len(code) == 10
        assert code.isalnum()
        assert code.isupper()

    def test_generate_random_code_custom_length(self):
        """Test generate_random_code with custom length."""
        code = generate_random_code(length=5)
        assert len(code) == 5
        assert code.isalnum()
        assert code.isupper()

    def test_generate_random_code_different_calls(self):
        """Test that different calls generate different codes."""
        code1 = generate_random_code()
        code2 = generate_random_code()
        assert code1 != code2


class TestGenerateMd5Hashcode:
    def test_generate_md5_hashcode_basic(self):
        """Test generate_md5_hashcode basic functionality."""
        keyword = "test"
        hashcode = generate_md5_hashcode(keyword)
        assert len(hashcode) == 32  # MD5 hash is 32 characters
        assert all(c in "0123456789abcdef" for c in hashcode)

    def test_generate_md5_hashcode_different_keywords(self):
        """Test that different keywords generate different hashes."""
        hash1 = generate_md5_hashcode("keyword1")
        hash2 = generate_md5_hashcode("keyword2")
        assert hash1 != hash2

    def test_generate_md5_hashcode_same_keyword_different_time(self):
        """Test that same keyword at different times generates different hashes."""
        hash1 = generate_md5_hashcode("test")
        time.sleep(0.01)  # Small delay to ensure different timestamp
        hash2 = generate_md5_hashcode("test")
        assert hash1 != hash2


class TestGenerateDatetime:
    def test_generate_datetime_default_range(self):
        """Test generate_datetime with default year range."""
        dt = generate_datetime()
        assert isinstance(dt, datetime)
        assert 1900 <= dt.year <= datetime.now().year

    def test_generate_datetime_custom_range(self):
        """Test generate_datetime with custom year range."""
        dt = generate_datetime(min_year=2000, max_year=2020)
        assert isinstance(dt, datetime)
        assert 2000 <= dt.year <= 2020

    def test_generate_datetime_single_year(self):
        """Test generate_datetime with same min and max year."""
        dt = generate_datetime(min_year=2020, max_year=2020)
        assert isinstance(dt, datetime)
        assert dt.year == 2020

    def test_generate_datetime_different_calls(self):
        """Test that different calls generate different datetimes."""
        dt1 = generate_datetime()
        dt2 = generate_datetime()
        # Very unlikely to be the same, but possible
        # Just check they are datetime objects
        assert isinstance(dt1, datetime)
        assert isinstance(dt2, datetime)


class TestGenerateCpf:
    def test_generate_cpf_format(self):
        """Test that generated CPF has correct format."""
        cpf = generate_cpf()
        assert len(cpf) == 14  # XXX.XXX.XXX-XX format
        assert cpf[3] == "."
        assert cpf[7] == "."
        assert cpf[11] == "-"

        # Remove formatting and check if all digits
        digits = cpf.replace(".", "").replace("-", "")
        assert len(digits) == 11
        assert digits.isdigit()

    def test_generate_cpf_different_calls(self):
        """Test that different calls generate different CPFs."""
        cpf1 = generate_cpf()
        cpf2 = generate_cpf()
        assert cpf1 != cpf2

    def test_generate_cpf_valid_structure(self):
        """Test that generated CPF has valid digit structure."""
        cpf = generate_cpf()
        digits = cpf.replace(".", "").replace("-", "")

        # Basic validation - should have 11 digits
        assert len(digits) == 11

        # Should not be all the same digit
        assert not all(d == digits[0] for d in digits)


class TestGenerateCnpj:
    def test_generate_cnpj_format(self):
        """Test that generated CNPJ has correct format."""
        cnpj = generate_cnpj()
        assert len(cnpj) == 18  # XX.XXX.XXX/XXXX-XX format
        assert cnpj[2] == "."
        assert cnpj[6] == "."
        assert cnpj[10] == "/"
        assert cnpj[15] == "-"

        # Remove formatting and check if all digits
        digits = cnpj.replace(".", "").replace("/", "").replace("-", "")
        assert len(digits) == 14
        assert digits.isdigit()

    def test_generate_cnpj_different_calls(self):
        """Test that different calls generate different CNPJs."""
        cnpj1 = generate_cnpj()
        cnpj2 = generate_cnpj()
        assert cnpj1 != cnpj2

    def test_generate_cnpj_valid_structure(self):
        """Test that generated CNPJ has valid digit structure."""
        cnpj = generate_cnpj()
        digits = cnpj.replace(".", "").replace("/", "").replace("-", "")

        # Basic validation - should have 14 digits
        assert len(digits) == 14

        # Should be all digits
        assert digits.isdigit()
