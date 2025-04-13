from settings_manager import SettingsManager, Theme

class ColorManager:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    LIGHT_BLUE = (248, 255, 145)
    DARK_BLUE = (0, 140, 10)
    LIGHT_GRAY = (200, 200, 200)

    @staticmethod
    def get_font_color():
        theme = SettingsManager.get_theme()
        if theme == Theme.LIGHT:
            return ColorManager.BLACK
        elif theme == Theme.DARK:
            return ColorManager.WHITE
        else:
            raise ValueError(f"Unknown theme: {theme}")
        
    @staticmethod
    def get_nice_color():
        theme = SettingsManager.get_theme()
        if theme == Theme.LIGHT:
            return ColorManager.LIGHT_BLUE
        elif theme == Theme.DARK:
            return ColorManager.DARK_BLUE
        else:
            raise ValueError(f"Unknown theme: {theme}")
    
    @staticmethod
    def get_neutral_color():
        theme = SettingsManager.get_theme()
        if theme == Theme.LIGHT:
            return ColorManager.WHITE
        elif theme == Theme.DARK:
            return ColorManager.BLACK
        else:
            raise ValueError(f"Unknown theme: {theme}")