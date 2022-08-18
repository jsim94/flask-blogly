from distutils.command.build_scripts import first_line_re


def user_input(first_name, last_name):
    '''Returns a message if there is a validation error, otherwise returns false.'''
    if not first_name:
        return "First name required."
    if not last_name:
        return "Last name required."
    return False


def post_input(title):
    '''Returns a message if there is a validation error, otherwise returns false.'''
    if not title:
        return "Title required."
    return False


def tag_input(name):
    '''Returns a message if there is a validation error, otherwise returns false.'''
    if not name:
        return 'Name required.'
    return False
