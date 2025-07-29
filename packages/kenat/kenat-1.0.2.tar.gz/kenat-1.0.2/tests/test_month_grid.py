import pytest
from kenat.month_grid import MonthGrid
from kenat.exceptions import InvalidGridConfigError

# A mock version of get_weekday that is predictable for testing
# It returns 0 for day 1, 1 for day 2, etc.
def mock_get_weekday(eth_date):
    return (eth_date['day'] - 1) % 7

@pytest.fixture
def mock_kenat_dependencies(mocker):
    """A pytest fixture to mock all external dependencies for MonthGrid."""
    
    # 1. Create a mock object that will be the return value of Kenat.now()
    mock_now_instance = mocker.MagicMock()
    
    # 2. Set the desired attribute on this mock object
    mock_now_instance._ethiopian = {'year': 2016, 'month': 9, 'day': 10}
    
    # 3. Patch Kenat.now WHERE IT LIVES (in kenat.kenat)
    mocker.patch('kenat.kenat.Kenat.now', return_value=mock_now_instance)

    # Mock the calendar data to return a predictable list of 5 days
    mock_calendar_data = [
        {'ethiopian': {'year': 2016, 'month': 9, 'day': d}, 'gregorian': {}}
        for d in range(8, 13) # Days 8, 9, 10, 11, 12
    ]
    # Also patch get_month_calendar WHERE IT LIVES
    mocker.patch(
        'kenat.kenat.Kenat.get_month_calendar',
        return_value=mock_calendar_data
    )
    
    # These other mocks are correct because they are looked up from within the month_grid module
    mocker.patch('kenat.month_grid.holidays.get_holidays_in_month', return_value=[])
    mocker.patch('kenat.month_grid.get_weekday', side_effect=mock_get_weekday)


class TestMonthGrid:
    """Tests the MonthGrid class."""

    def test_returns_valid_grid_structure(self, mock_kenat_dependencies):
        """Tests that the create method returns a grid with the correct shape."""
        grid = MonthGrid.create(year=2016, month=9)
        assert 'headers' in grid
        assert 'days' in grid
        assert isinstance(grid['headers'], list)
        assert isinstance(grid['days'], list)
        assert len(grid['headers']) == 7

    def test_flags_today_correctly(self, mock_kenat_dependencies):
        """Tests that the correct day is marked with is_today=True."""
        grid = MonthGrid.create(year=2016, month=9)
        
        # Flatten the list of days and find the one marked as "today"
        all_days = [day for week in grid['days'] for day in week if day]
        today_obj = next((d for d in all_days if d.get('is_today')), None)
        
        assert today_obj is not None
        # Our mock "today" is day 10, which is in our mock calendar data
        assert today_obj['ethiopian']['day'] == 10

    def test_accepts_object_input_and_custom_week_start(self, mock_kenat_dependencies):
        """
        Tests custom options like week_start and weekday_lang.
        NOTE: In our library, week starts on Sunday (0). Monday is 1.
        """
        grid = MonthGrid.create(
            year=2016, month=9, week_start=1, weekday_lang='english'
        )
        assert grid['headers'][0] == 'Monday'
        
        # The first day in our mock data is day 8.
        # mock_get_weekday(day=8) returns (8-1)%7 = 0 (Sunday).
        # Since week starts on Monday, the offset is (0 - 1 + 7) % 7 = 6.
        # The first day should be at the end of the first week.
        first_day_obj = grid['days'][0][6] 
        assert first_day_obj['weekday_name'] == 'Sunday'

    def test_pads_days_array_correctly(self, mock_kenat_dependencies):
        """Tests that padding changes based on weekStart."""
        # First day of mock data has weekday 0.
        # With week_start=0 (Sunday), offset is (0 - 0 + 7) % 7 = 0. No padding.
        grid_sun_start = MonthGrid.create(year=2016, month=9, week_start=0)
        offset_sun = next(i for i, d in enumerate(grid_sun_start['days'][0]) if d is not None)
        assert offset_sun == 0

        # With week_start=1 (Monday), offset is (0 - 1 + 7) % 7 = 6. 6 padding days.
        grid_mon_start = MonthGrid.create(year=2016, month=9, week_start=1)
        offset_mon = next(i for i, d in enumerate(grid_mon_start['days'][0]) if d is not None)
        assert offset_mon == 6
    
    def test_throws_error_for_invalid_config(self):
        """
        Tests that the constructor validates its input.
        This replaces the "invalid string" test from JS, as our constructor is stricter.
        """
        # Should fail if only year is provided without month
        with pytest.raises(InvalidGridConfigError):
            # We test the constructor directly, not the create method
            MonthGrid(config={'year': 2016})

        # Should fail if week_start is out of range
        with pytest.raises(InvalidGridConfigError):
            MonthGrid(config={'year': 2016, 'month': 9, 'week_start': 7})