```xml
<input>
    <agent_state>
        Steps: {steps}/{max_steps}

        Action Response: {observation}
    <agent_state>
    <desktop_state>
        Cursor Location: {cursor_location}
        [Begin of App Info]
        Foreground App: {active_app}

        Background Apps:
        {apps}
        [End of App Info]
        
        [Begin of Screen]
        List of Interactive Elements:
        {interactive_elements}

        List of Scrollable Elements:
        {scrollable_elements}
        [End of Screen]
    <desktop_state>
    <user_query>
        {query}
    </user_query>

Note: Use the `Done Tool` if the task is completely over else continue solving with full potential.
</input>
```