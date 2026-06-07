def suggest_fixes(error_msg, source_line=None):
    """Suggest probable fixes based on error message and source line."""
    suggestions = []
    if "end" in error_msg.lower() and "expected" in error_msg.lower():
        suggestions.append("Missing 'end' keyword – add 'end' after the block.")
    if "indent" in error_msg.lower():
        suggestions.append("Indentation error: Use spaces, not tabs. Each level = 4 spaces.")
    if "unexpected token" in error_msg.lower() and source_line:
        if "end" in source_line:
            suggestions.append("Redundant 'end' – remove the extra 'end'.")
        if "else" in source_line:
            suggestions.append("'else' must be at the same indentation level as 'if'.")
    if "NameError" in error_msg or "not defined" in error_msg:
        suggestions.append("Variable/function used before definition. Check spelling and order.")
    if "constructor" in error_msg.lower():
        suggestions.append("'constructor' can only be used inside a 'class' block.")
    if source_line and ".." in source_line:
        suggestions.append("Range '..' works only with numbers: e.g., '1..5'.")
    if not suggestions:
        suggestions.append("Check parentheses, quotes, and block termination ('end').")
    return suggestions
