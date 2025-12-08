languages_extensions = {
    "c": ".c",
    "c++03": ".cpp",
    "c++14": ".cpp",
    "c++20": ".cpp",
    "go": ".go",
    "java8": ".java",
    "pascal": ".pas",
    "pypy2": ".py",
    "py3": ".py",
    "rust": ".rs",
    "c++themis": ".cpp",
    "c++11": ".cpp",
    "c++17": ".cpp",
    "c11": ".c",
    "java25": ".java",
    "kotlin": ".kt",
    "pasthemis": ".pas",
    "pypy3": ".py",
    "python3": ".py",
    "scratch": ".sb3"
}

def get_extension(language: str) -> str:
    language_lower = language.lower()
    return languages_extensions.get(language_lower, ".txt")