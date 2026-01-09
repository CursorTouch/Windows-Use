```xml
<output>
    <evaluate>{evaluate}</evaluate>
    <thought>{thought}</thought>
    <action>
        <name>{action_name}</name>
        <input>{action_input}</input>
        <evidence> Provide the minimal observable evidence you expect after this action (e.g., "Dialog 'Save as' open", "Button 'OK' visible").</evidence>
        <post_check>Provide a one-line verification the agent must perform after the action to confirm success.</post_check>
    </action>
</output>
```