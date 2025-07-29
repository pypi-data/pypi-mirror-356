from typing import Any


DEVELOPING = True



def handle_error(
    error: Exception, 
    function: str, 
    default_error: str
) -> None:
    """
    Displays error message and what function the error occurred in.
    Either displays the full error message or just the error text,
    depending on whether the script is being developed or not.

    
    Parameters
    ----------
    error : Exception
        The exception that was raised.

    function : str
        The name of the function that the expection was raised in.

    default_error : str
        The error message to be displayed to the user, non-technical
        such that the user can more obviously know what to do.
    """

    if DEVELOPING:
        print_internal('Error in function: ' + function, True)
        print_internal(type(error), True)
        print_internal(error, True)
    else:
        print_internal(default_error)

    etc()
    return


def etc() -> None:
    """
    Displays prompt to user to press Enter to continue.
    """

    input('Press Enter to continue\n')
    return


def print_internal(
    text: Any, 
    display_error_notice: bool=False
) -> None:
    """
    Prints a message with an indent indicating an internal message,
    a message that appears during setup of the script.

    
    Parameters
    ----------
    text : Any
        The data to display.

    display_error_notice : bool, default=False
        True if "[ERROR]" prefix is desired.
        False if "]" prefix is desired.
    """

    if display_error_notice:
        print(f'[ERROR] {text}')
    else:
        print(f'] {text}')
    return


def print_script_message(text : str) -> None:
    """
    Prints a message with a >, indicating a message from the script.

    
    Parameters
    ----------
    text : str
        The data to display.
    """

    print(f'> {text}')
    return


def save_log(filename: str, data: Any) -> None:
    """
    Appends the given data to the given file.

    
    Parameters
    ----------
    filename : str
        The file path and name of the file to append to.

    data : Any
        The data to append to the file.
    """
    with open(filename, 'a+', encoding="utf-8") as f:
        f.write(str(data))
    
    return


def prompt_for_answer(prompt_text : str) -> str:
    """
    Prompts the user for an input to answer the given prompt.

    
    Parameters
    ----------
    prompt_text : str
        The prompt to give the user.

        
    Returns
    -------
    str
        The answer the user inputted.
    """
    answer = input(f'> {prompt_text}: ').strip()

    while not answer:
        print('Please enter a non-empty string.')
        answer = input(f'> {prompt_text}: ').strip()

    return answer


def select_list_options(options : list[str]) -> int:
    """
    Prints a given list of options for the user to choose from by selecting
    a number option.

    
    Parameters
    ----------
    options : list[str]
        The options for the user to choose from.

        
    Returns
    -------
    int
        The integer indicating the chosen option.
    """

    for i, option in enumerate(options):
        print(f'({i + 1}) {option}')

    try:
        choice = int(input('] '))

        if choice - 1 not in range(len(options)):
            raise IndexError
        
        print()
        return choice

    except ValueError:
        print('Given choice is not a number.\n')
        return select_list_options(options)
    
    except IndexError:
        print('Given choice is not in the range of options.\n')
        return select_list_options(options)
    

# method used
# https://stackoverflow.com/a/7205107
def merge_dicts(dict1: dict, dict2: dict, path=[]) -> None:
    """
    Merges two dictionaries, storing the result in the first `dict` argument.

    
    Paremeters
    ----------
    dict1 : dict
        The first dictionary to merge.

    dict2 : dict
        The second dictionary to merge.


    Raises
    ------
    Exception
        If there is a conflict with keys between the two dictionaries.
        A conflict occurs if both dictionaries have the same key, but the
        types of values, or the values themselves, are different 
        (ex. attempting to merge `{'count' : 1}` with `{'count' : 3}`
        or with `{'count' : 'one'}`)
    """
    
    for key in dict2:
        if key in dict1:
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                merge_dicts(dict1[key], dict2[key], path + [str(key)])
            elif dict1[key] != dict2[key]:
                raise Exception('Conflict at ' + '.'.join(path + [str(key)]))
        else:
            dict1[key] = dict2[key]
    
    return dict1
