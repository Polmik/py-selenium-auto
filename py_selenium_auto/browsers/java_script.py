import enum
import os.path

from py_selenium_auto_core.utilities.file_reader import FileReader
from py_selenium_auto_core.utilities.root_path_helper import RootPathHelper


class JavaScript(enum.Enum):
    AutoAcceptAlerts = 'auto_accept_alerts.js'
    BorderElement = 'border_element.js'
    ClickElement = 'click_element.js'
    ElementIsOnScreen = 'element_is_on_screen.js'
    ExpandShadowRoot = 'expand_shadow_root.js'
    GetCheckBoxState = 'get_check_box_state.js'
    GetComboBoxSelectedText = 'get_combo_box_selected_text.js'
    GetComboBoxTexts = 'get_combo_box_texts.js'
    GetCurrentUrl = 'get_current_url.js'
    GetElementByXPath = 'get_element_by_x_path.js'
    GetElementText = 'get_element_text.js'
    GetElementXPath = 'get_element_x_path.js'
    GetElementYCoordinate = 'get_element_y_coordinate.js'
    GetMediaType = 'get_media_type.js'
    GetScrollCoordinates = 'get_scroll_coordinates.js'
    GetTextFirstChild = 'get_text_first_child.js'
    GetViewPortCoordinates = 'get_view_port_coordinates.js'
    GetWindowSize = 'get_window_size.js'
    GetXPathFromCss = 'get_x_path_from_css.js'
    IsPageLoaded = 'is_page_loaded.js'
    IsTouchEnabled = 'is_touch_enabled.js'
    MouseHover = 'mouse_hover.js'
    OpenInNewTab = 'open_in_new_tab.js'
    OpenNewTab = 'open_new_tab.js'
    OpenUrlInNewWindow = 'open_url_in_new_window.js'
    ScrollBy = 'scroll_by.js'
    ScrollToBottom = 'scroll_to_bottom.js'
    ScrollToElement = 'scroll_to_element.js'
    ScrollToElementCenter = 'scroll_to_element_center.js'
    ScrollToTop = 'scroll_to_top.js'
    ScrollWindowBy = 'scroll_window_by.js'
    SelectComboBoxValueByText = 'select_combo_box_value_by_text.js'
    SetAttribute = 'set_attribute.js'
    SetFocus = 'set_focus.js'
    SetInnerHTML = 'set_inner_h_t_m_l.js'
    SetValue = 'set_value.js'

    @property
    def script_from_file(self):
        return FileReader.get_resource_file(
            os.path.join('java_scripts', self.value),
            RootPathHelper.current_root_path(__file__),
        )
