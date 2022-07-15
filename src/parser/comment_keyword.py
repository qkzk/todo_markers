EOL = "\n"

COMMENT_KEYWORDS = {
    ("md"): (("<!--", "-->"),),
    ("py"): (("#", EOL),),
    ("c", "js"): (("//", EOL), ("/*", "*/")),
    ("rs", "go"): (("//", EOL),),
    ("lua"): (("--", EOL),),
}