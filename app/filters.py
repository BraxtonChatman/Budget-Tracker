# --- TEMPLATE FILTERS ---
def format_currency(value, show_sign=False):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return "$0.00"

    formatted = "${:,.2f}".format(abs(value))

    if show_sign:
        if value < 0:
            return f"-{formatted}"
        else:
            return formatted
    return formatted