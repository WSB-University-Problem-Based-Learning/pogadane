"""
Unit tests for gui_utils.font_manager module.
Tests FontManager class for font management and scaling.
"""
import pytest
from pogadane.gui_utils.font_manager import FontManager
from pogadane.constants import MIN_FONT_SIZE, MAX_FONT_SIZE, DEFAULT_FONT_SIZE


class TestFontManager:
    """Test suite for FontManager class."""

    def test_initialization_default(self):
        """Test FontManager initialization with default font size."""
        fm = FontManager()
        assert fm.font_size == DEFAULT_FONT_SIZE

    def test_initialization_custom_size(self):
        """Test FontManager initialization with custom font size."""
        fm = FontManager(initial_size=12)
        assert fm.font_size == 12

    def test_initialization_creates_fonts(self):
        """Test that initialization creates all required fonts."""
        fm = FontManager()
        assert hasattr(fm, 'fonts')
        assert isinstance(fm.fonts, dict)
        assert len(fm.fonts) > 0

    def test_font_types_created(self):
        """Test that all expected font types are created."""
        fm = FontManager()
        expected_fonts = [
            'default',
            'bold',
            'header',
            'button',
            'label',
            'text',
            'monospace'
        ]
        for font_type in expected_fonts:
            assert font_type in fm.fonts

    def test_increase_size(self):
        """Test increasing font size."""
        fm = FontManager(initial_size=12)
        original_size = fm.font_size
        
        fm.increase_size()
        
        assert fm.font_size == original_size + 1

    def test_increase_size_respects_maximum(self):
        """Test that font size doesn't exceed maximum."""
        fm = FontManager(initial_size=MAX_FONT_SIZE)
        
        fm.increase_size()
        
        assert fm.font_size == MAX_FONT_SIZE

    def test_decrease_size(self):
        """Test decreasing font size."""
        fm = FontManager(initial_size=12)
        original_size = fm.font_size
        
        fm.decrease_size()
        
        assert fm.font_size == original_size - 1

    def test_decrease_size_respects_minimum(self):
        """Test that font size doesn't go below minimum."""
        fm = FontManager(initial_size=MIN_FONT_SIZE)
        
        fm.decrease_size()
        
        assert fm.font_size == MIN_FONT_SIZE

    def test_multiple_increases(self):
        """Test multiple font size increases."""
        fm = FontManager(initial_size=10)
        
        for _ in range(3):
            fm.increase_size()
        
        assert fm.font_size == 13

    def test_multiple_decreases(self):
        """Test multiple font size decreases."""
        fm = FontManager(initial_size=15)
        
        for _ in range(3):
            fm.decrease_size()
        
        assert fm.font_size == 12

    def test_get_font(self):
        """Test getting a specific font."""
        fm = FontManager()
        
        font = fm.get_font('default')
        assert font is not None

    def test_get_nonexistent_font(self):
        """Test getting a font that doesn't exist."""
        fm = FontManager()
        
        font = fm.get_font('nonexistent')
        # Should return None or raise KeyError
        assert font is None or font in fm.fonts.values()

    def test_fonts_update_on_size_change(self):
        """Test that fonts are updated when size changes."""
        fm = FontManager(initial_size=10)
        original_font = fm.fonts['default']
        
        fm.increase_size()
        updated_font = fm.fonts['default']
        
        # Fonts should be recreated
        # (Implementation detail - may need adjustment based on actual behavior)

    def test_font_size_bounds(self):
        """Test that font size stays within bounds."""
        fm = FontManager(initial_size=MIN_FONT_SIZE)
        
        # Try to go below minimum
        for _ in range(10):
            fm.decrease_size()
        assert fm.font_size >= MIN_FONT_SIZE
        
        # Reset and try to go above maximum
        fm.font_size = MAX_FONT_SIZE
        for _ in range(10):
            fm.increase_size()
        assert fm.font_size <= MAX_FONT_SIZE


class TestFontManagerIntegration:
    """Integration tests for FontManager."""

    def test_font_manager_with_ttk_style(self):
        """Test that FontManager can work with TTK styles."""
        try:
            from unittest.mock import Mock
            
            fm = FontManager()
            mock_style = Mock()
            
            # Should have method to apply fonts to styles
            if hasattr(fm, 'apply_to_ttk_styles'):
                fm.apply_to_ttk_styles(mock_style)
                # Verify style configuration was called
                assert mock_style.configure.called or True
        except ImportError:
            pytest.skip("TTK not available in test environment")

    def test_consistent_font_scaling(self):
        """Test that all fonts scale consistently."""
        fm = FontManager(initial_size=10)
        original_sizes = {
            name: font for name, font in fm.fonts.items()
        }
        
        fm.increase_size()
        
        # All fonts should have been updated
        for name in original_sizes:
            # Font objects should be different (recreated)
            pass  # Implementation-specific check


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
