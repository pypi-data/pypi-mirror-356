import pytest
from kenat.bahire_hasab import get_bahire_hasab, get_movable_holiday
from kenat.exceptions import InvalidInputTypeError

# By using a class, we can group all related tests, similar to `describe` in Jest.
class TestBahireHasab:
    """
    Test suite for Bahire Hasab calculations.
    """

    # A nested class for tests related to a specific year.
    class TestGetBahireHasabFor2016:
        """
        Tests get_bahire_hasab for the year 2016 E.C.
        """
        # A fixture runs once before the tests in this class that request it.
        # This is more efficient than calling get_bahire_hasab in every test.
        @pytest.fixture(scope="class")
        def bahire_hasab_2016(self):
            return get_bahire_hasab(2016)

        def test_should_calculate_amete_alem_and_metene_rabiet_correctly(self, bahire_hasab_2016):
            assert bahire_hasab_2016['ameteAlem'] == 7516
            assert bahire_hasab_2016['meteneRabiet'] == 1879

        def test_should_identify_the_correct_evangelist(self, bahire_hasab_2016):
            assert bahire_hasab_2016['evangelist']['name'] == 'ዮሐንስ' # Amharic (default)
            assert bahire_hasab_2016['evangelist']['remainder'] == 0

        def test_should_determine_the_correct_new_year_day(self, bahire_hasab_2016):
            assert bahire_hasab_2016['newYear']['dayName'] == 'ማክሰኞ' # Amharic (default)

        def test_should_calculate_medeb_wenber_abektie_and_metqi_correctly(self, bahire_hasab_2016):
            assert bahire_hasab_2016['medeb'] == 11
            assert bahire_hasab_2016['wenber'] == 10
            assert bahire_hasab_2016['abektie'] == 20
            assert bahire_hasab_2016['metqi'] == 10

        def test_should_calculate_the_correct_date_for_nineveh(self, bahire_hasab_2016):
            assert bahire_hasab_2016['nineveh'] == {'year': 2016, 'month': 6, 'day': 18}

    # A nested class for internationalization tests.
    class TestInternationalization:
        """
        Tests the language option.
        """
        def test_should_return_names_in_english_when_specified(self):
            bahire_hasab_english = get_bahire_hasab(2016, lang='english')
            assert bahire_hasab_english['evangelist']['name'] == 'John'
            assert bahire_hasab_english['newYear']['dayName'] == 'Tuesday'

    # A nested class for movable feast calculations.
    class TestMovableFeasts:
        """
        Tests the calculation of movable feasts.
        """
        @pytest.fixture(scope="class")
        def movable_feasts(self):
            return get_bahire_hasab(2016, lang='english')['movableFeasts']

        def test_should_return_a_complete_movable_feasts_object(self, movable_feasts):
            assert movable_feasts is not None
            assert len(movable_feasts.keys()) > 5

        def test_should_correctly_calculate_the_date_for_fasika(self, movable_feasts):
            fasika = movable_feasts['fasika']
            assert fasika is not None
            assert fasika['ethiopian'] == {'year': 2016, 'month': 8, 'day': 27}
            assert fasika['name'] == 'Ethiopian Easter'
            assert 'public' in fasika['tags']

        def test_should_correctly_calculate_the_date_for_abiy_tsome(self, movable_feasts):
            abiy_tsome = movable_feasts['abiyTsome']
            assert abiy_tsome is not None
            assert abiy_tsome['ethiopian'] == {'year': 2016, 'month': 7, 'day': 2}
            assert abiy_tsome['name'] == 'Great Lent'

    # A final nested class for error handling.
    class TestErrorHandling:
        """
        Tests the input validation and error handling.
        """
        def test_should_throw_invalid_input_type_error_for_non_numeric_input(self):
            # pytest.raises serves the same purpose as expect().toThrow()
            with pytest.raises(InvalidInputTypeError):
                get_bahire_hasab('2016')

            with pytest.raises(InvalidInputTypeError):
                get_movable_holiday('TINSAYE', '2016')