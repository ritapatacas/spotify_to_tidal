class Text:
    term_colors = {
        "red": "\033[91m",
        "red bright": "\033[38;5;132m",
        "white": "\033[0m",
        "green": "\033[38;5;70m",
        "yellow": "\033[38;5;186m",
        "blue": "\033[38;5;75m",
        "purple": "\033[95m",
        "cyan": "\033[96m",
        "grey bright": "\033[38;5;249m",
        "grey mid": "\033[38;5;102m",
        "grey dark": "\033[38;5;238m",
        "black": "\033[30m",
        "bg_red": "\033[41m",
        "bg_green": "\033[42m",
        "bg_yellow": "\033[43m",
        "bg_blue": "\033[44m",
        "bg_purple": "\033[45m",
    }

    @staticmethod
    def color(text, color):
        return Text.term_colors[color] + text + Text.term_colors["white"]

    @staticmethod
    def u(text):
        return "\033[4m" + text + Text.term_colors["white"]

    @staticmethod
    def b(text):
        return "\033[1m" + text + Text.term_colors["white"]

    @staticmethod
    def log(text):
        return Text.term_colors["green"] + "> " + Text.term_colors["white"] + text

    @staticmethod
    def error(text):
        return (
            Text.term_colors["red"]
            + " ! "
            + Text.term_colors["red bright"]
            + text
            + Text.term_colors["white"]
        )

    @staticmethod
    def display_selection(selection):
        txt = (
            Text.term_colors["green"]
            + "> "
            + Text.term_colors["white"]
            + "current selection [ "
            + Text.term_colors["purple"]
        )
        selection = ", ".join(selection)
        end = Text.term_colors["white"] + " ]"
        return txt + selection + end

    @staticmethod
    def busy(text):
        return Text.term_colors["grey mid"] + ".." + text + Text.term_colors["white"]
