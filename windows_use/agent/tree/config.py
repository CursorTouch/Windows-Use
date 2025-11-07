INTERACTIVE_CONTROL_TYPE_NAMES=set([
    'ButtonControl',
    'ListItemControl',
    'MenuItemControl',
    'EditControl',
    'CheckBoxControl',
    'RadioButtonControl',
    'ComboBoxControl',
    'HyperlinkControl',
    'SplitButtonControl',
    'TabItemControl',
    'TreeItemControl',
    'DataItemControl',
    'HeaderItemControl',
    'TextBoxControl',
    'SpinnerControl',
    'ScrollBarControl'
])

DOCUMENT_CONTROL_TYPE_NAMES=set([
    'DocumentControl'
])

STRUCTURAL_CONTROL_TYPE_NAMES = set([
    'PaneControl',
    'GroupControl',
    'CustomControl'
])

INFORMATIVE_CONTROL_TYPE_NAMES=set([
    'TextControl',
    'ImageControl',
    'StatusBarControl',
    # 'ProgressBarControl',
    # 'ToolTipControl',
    # 'TitleBarControl',
    # 'SeparatorControl',
    # 'HeaderControl',
    # 'HeaderItemControl',
])

DEFAULT_ACTIONS=set([
    'Click',
    'Press',
    'Jump',
    'Check',
    'Uncheck',
    'Double Click'
])

THREAD_MAX_RETRIES = 3