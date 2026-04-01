[Begin of Agent State]
    Steps: {steps}/{max_steps}
[End of Agent State]
{loop_warning}
[Begin of Desktop]
    Active Desktop: {active_desktop}
    
    Cursor Location: {cursor_location}
    
    [Begin of Window Info]
        Foreground Window: {active_window}
    
        Background Windows:
        {windows}
    [End of Window Info]
    
    [Begin of Screen]
        List of Interactive Elements:
        {interactive_elements}

        List of Scrollable Elements:
        {scrollable_elements}
    [End of Screen]
    
    [Begin of Virtual Desktops]
        Virtual Desktops:
        {desktops}
    [End of Virtual Desktops]
[End of Desktop]

[Begin of User Query]
    {query}
[End of User Query]

REMINDER: You MUST use `done_tool` to deliver any response to the user. Do not produce a text-only reply.
