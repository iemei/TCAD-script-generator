
def validate(script):
    errors = []

    if "Physics {" not in script:
        errors.append("Missing Physics block")

    if "Solve {" not in script:
        errors.append("Missing Solve block")

    if "contact" not in script.lower():
        errors.append("Missing contacts")

    return errors
