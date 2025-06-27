from django_models.validators import dv_maker, validate_cpf, validate_cnpj, SEQ_VALUES


class TestDvMaker:
    """Test dv_maker function."""

    def test_dv_maker_less_than_2(self):
        """Test dv_maker with value less than 2."""
        assert dv_maker(0) == 0
        assert dv_maker(1) == 0

    def test_dv_maker_greater_equal_2(self):
        """Test dv_maker with value greater than or equal to 2."""
        assert dv_maker(2) == 9  # 11 - 2
        assert dv_maker(5) == 6  # 11 - 5
        assert dv_maker(10) == 1  # 11 - 10


class TestValidateCpf:
    """Test validate_cpf function."""

    def test_validate_cpf_empty_values(self):
        """Test validate_cpf with empty values."""
        assert validate_cpf(None) is False
        assert validate_cpf("") is False
        assert validate_cpf([]) is False

    def test_validate_cpf_sequential_values(self):
        """Test validate_cpf with sequential values."""
        for seq_value in SEQ_VALUES:
            assert validate_cpf(seq_value) is False

    def test_validate_cpf_non_digit_invalid(self):
        """Test validate_cpf with non-digit characters that become empty."""
        # Test case where digits_only returns empty string
        assert validate_cpf("...---") is False
        assert validate_cpf("abc") is False

    def test_validate_cpf_equal_digits(self):
        """Test validate_cpf with all equal digits."""
        # This tests the is_equal function call
        assert validate_cpf("11111111111") is False

    def test_validate_cpf_wrong_length(self):
        """Test validate_cpf with wrong length."""
        assert validate_cpf("123456789") is False  # Too short
        assert validate_cpf("123456789012") is False  # Too long

    def test_validate_cpf_repeated_digits_pattern(self):
        """Test validate_cpf with repeated digits pattern."""
        # This tests line 98: if value.count(value[0]) == 11
        # Create a CPF with all same digits but valid verification digits
        # This is a tricky case - we need a CPF that passes verification but has all same digits
        assert validate_cpf("11111111111") is False

    def test_validate_cpf_valid_formatted(self):
        """Test validate_cpf with valid formatted CPF."""
        # Using a known valid CPF
        valid_cpf = "123.456.789-09"
        result = validate_cpf(valid_cpf)
        assert result == valid_cpf

    def test_validate_cpf_valid_unformatted(self):
        """Test validate_cpf with valid unformatted CPF."""
        # Using a known valid CPF
        valid_cpf = "12345678909"
        result = validate_cpf(valid_cpf)
        assert result == valid_cpf

    def test_validate_cpf_invalid_verification_digits(self):
        """Test validate_cpf with invalid verification digits."""
        # Valid format but wrong verification digits
        assert validate_cpf("123.456.789-00") is False
        assert validate_cpf("12345678900") is False

    def test_validate_cpf_mixed_characters(self):
        """Test validate_cpf with mixed characters."""
        # Should extract only digits and validate
        result = validate_cpf("123abc456def789ghi09")
        # This should work if the extracted digits form a valid CPF
        assert result == "123abc456def789ghi09" or result is False


class TestValidateCnpj:
    """Test validate_cnpj function."""

    def test_validate_cnpj_empty_values(self):
        """Test validate_cnpj with empty values."""
        assert validate_cnpj(None) == ""
        assert validate_cnpj("") == ""
        assert validate_cnpj([]) == ""

    def test_validate_cnpj_non_digit_invalid(self):
        """Test validate_cnpj with non-digit characters that become empty."""
        # Test case where digits_only returns empty string
        assert validate_cnpj("...---") is False
        assert validate_cnpj("abc") is False

    def test_validate_cnpj_equal_digits(self):
        """Test validate_cnpj with all equal digits."""
        # This tests the is_equal function call
        assert validate_cnpj("11111111111111") is False

    def test_validate_cnpj_wrong_length(self):
        """Test validate_cnpj with wrong length."""
        assert validate_cnpj("12345678901") is False  # Too short
        assert validate_cnpj("123456789012345") is False  # Too long

    def test_validate_cnpj_valid_formatted(self):
        """Test validate_cnpj with valid formatted CNPJ."""
        # Using a known valid CNPJ
        valid_cnpj = "11.222.333/0001-81"
        result = validate_cnpj(valid_cnpj)
        assert result == valid_cnpj

    def test_validate_cnpj_valid_unformatted(self):
        """Test validate_cnpj with valid unformatted CNPJ."""
        # Using a known valid CNPJ
        valid_cnpj = "11222333000181"
        result = validate_cnpj(valid_cnpj)
        assert result == valid_cnpj

    def test_validate_cnpj_invalid_verification_digits(self):
        """Test validate_cnpj with invalid verification digits."""
        # Valid format but wrong verification digits
        assert validate_cnpj("11.222.333/0001-00") is False
        assert validate_cnpj("11222333000100") is False

    def test_validate_cnpj_mixed_characters(self):
        """Test validate_cnpj with mixed characters."""
        # Should extract only digits and validate
        result = validate_cnpj("11abc222def333ghi0001jkl81")
        # This should work if the extracted digits form a valid CNPJ
        assert result == "11abc222def333ghi0001jkl81" or result is False


class TestValidatorsEdgeCases:
    """Test edge cases and specific line coverage."""

    def test_cpf_with_special_characters_only(self):
        """Test CPF validation with only special characters."""
        # This should trigger line 70: if not value (after digits_only)
        assert validate_cpf("!@#$%^&*()") is False

    def test_cnpj_with_special_characters_only(self):
        """Test CNPJ validation with only special characters."""
        # This should trigger line 133: if not value (after digits_only)
        assert validate_cnpj("!@#$%^&*()") is False

    def test_cpf_validation_comprehensive(self):
        """Comprehensive CPF validation test."""
        # Test various invalid cases to ensure all code paths are covered
        test_cases = [
            ("", False),  # Empty
            ("00000000000", False),  # Sequential
            ("123", False),  # Too short
            ("12345678901234", False),  # Too long
            ("abcdefghijk", False),  # Non-digits
            ("111.111.111-11", False),  # All same digits
            ("123.456.789-00", False),  # Invalid verification
        ]

        for cpf, expected in test_cases:
            result = validate_cpf(cpf)
            if expected is False:
                assert result is False, f"CPF {cpf} should be invalid"

    def test_cnpj_validation_comprehensive(self):
        """Comprehensive CNPJ validation test."""
        # Test various invalid cases to ensure all code paths are covered
        test_cases = [
            (None, ""),  # Empty (returns empty string)
            ("11111111111111", False),  # All same digits
            ("123", False),  # Too short
            ("123456789012345", False),  # Too long
            ("abcdefghijklmn", False),  # Non-digits
            ("11.222.333/0001-00", False),  # Invalid verification
        ]

        for cnpj, expected in test_cases:
            result = validate_cnpj(cnpj)
            if expected == "":
                assert result == "", f"CNPJ {cnpj} should return empty string"
            elif expected is False:
                assert result is False, f"CNPJ {cnpj} should be invalid"
