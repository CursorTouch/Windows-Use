Compress the conversation history into a concise continuation prompt. The agent will NOT have access to prior messages.

IMPORTANT: Structure your response EXACTLY as follows:

## TASK
[State the original user task in 1-2 sentences. What does the user want the agent to accomplish?]

## PROGRESS SUMMARY
[List all completed actions since the task started:
- Windows/applications opened or closed
- UI elements found and interacted with (include element names, control types, coordinates)
- Data entered, extracted, or verified
- Navigation completed (which pages visited, URLs accessed)
- Decisions made and why (e.g., "clicked Search instead of Browse because it's faster")
- Obstacles encountered and how they were resolved
- Actions that FAILED and should NOT be retried with same approach]

## CURRENT SITUATION
[Describe the present state:
- **Active window**: Name and control type of currently visible window
- **Recent action**: What was just executed and its result
- **Current UI state**: What elements are visible on screen (major controls, buttons, text)
- **Last known coordinates**: Important element positions if relevant to next step
- **Data state**: Any extracted information, form fields filled, values entered
- **Failures to avoid**: What approaches didn't work and why]

## INSIGHTS & PATTERNS
[What has the agent learned about this task?
- Which UI elements consistently work vs have issues
- How to efficiently navigate this application
- Edge cases encountered (e.g., popups, delays, element state changes)
- Best sequence of actions discovered
- Application quirks or timing requirements
- Any looping detected that should be avoided
- LLM patterns (which reasoning approaches worked, which ones led to errors)]

## NEXT ACTION
[What should happen immediately next?
- Tool to use (click_tool, type_tool, scroll_tool, etc.)
- Exact target (element name, coordinates, or control type to find)
- Expected outcome
- Fallback if this action fails]

## CRITICAL STATE
[Preserve only essential info for continuation:
- Open window/application names
- Form data already entered (field → value pairs)
- Extracted data that answers the task
- Navigation breadcrumbs (back button locations, URL history)
- Known element identifiers or locations
- Any credentials or sensitive data entered (for reuse if needed)]

Be concise but complete—this replaces all prior conversation history. Include only what's necessary to continue effectively.