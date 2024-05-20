from argparse import ArgumentParser
import re
import sys


LETTER_TO_NUMBER = {
    'A': '2',
    'B': '2',
    'C': '2',
    'D': '3',
    'E': '3',
    'F': '3',
    'G': '4',
    'H': '4',
    'I': '4',
    'J': '5',
    'K': '5',
    'L': '5',
    'M': '6',
    'N': '6',
    'O': '6',
    'P': '7',
    'Q': '7',
    'R': '7',
    'S': '7',
    'T': '8',
    'U': '8',
    'V': '8',
    'W': '9',
    'X': '9',
    'Y': '9',
    'Z': '9'
}

class PhoneNumber:
    """Gets and normalizes a phone number
    
    Attributes:
        full_number (str): full phone number
        country_code (str): country code of phone number
        area_code (str): area code of phone number
        exchange_code (str): exchange code of phone number
        line_number (str): line number of phone number
    """
    def __init__(self, number):
        """figures out validiity of the number and cleans the number format.

        Args:
            number (str or int): phone number in string or integer format

        Raises:
            TypeError: raises typerror if number not a str or int
            ValueError: raises valueerror if number not correct length
            
        Side effects:
            can raise errors and create new str of name and phone number
        """
        if isinstance(number, int):
            number = str(number)
        elif isinstance(number, str):
            pass
        else:
            raise TypeError("Phone number must be a string or an integer.")
        
        clean_num = re.sub(r"\W+", "", number)
        
        correct_num = re.sub(r"[A-Za-z]", lambda char: 
            LETTER_TO_NUMBER.get(char.group(0).upper()), clean_num)
        
        if len(correct_num) < 10:
            raise ValueError("Phone number length is invalid")
        elif len(correct_num) > 11:
            raise ValueError("Phone number length is invalid")
        elif len(correct_num) == 11:
            if correct_num[0] == '1':
                pass
            else:
                raise ValueError("Country Code is not for Americas")
        elif len(correct_num) == 10:
            pass
        
        pattern = r"^1?(\d{10,11})"
        phone_groups = re.search(pattern, correct_num)
        if phone_groups:
            matched_digits = phone_groups.group()
            if len(matched_digits) == 11:
                self.full_number = matched_digits[1:]
                self.area_code = matched_digits[1:4]
                self.exchange_code = matched_digits[4:7]
                self.line_number = matched_digits[7:]
            elif len(matched_digits) == 10:
                self.full_number = matched_digits[:]
                self.area_code = matched_digits[:3]
                self.exchange_code = matched_digits[3:6]
                self.line_number = matched_digits[6:]
        elif phone_groups is None:
            raise ValueError("Phone groups are none")
        
        if self.area_code[0] == '0' or self.area_code[0] == '1':
            raise ValueError("Invalid phone number: Starts with 0")
        elif self.exchange_code[0] == '0' or self.exchange_code[0] == '1':
            raise ValueError("Invalid phone number: Starts with 0")
        elif '11' in self.area_code or '11' in self.exchange_code:
            raise ValueError("Invalid phone number: Contains '11' sequence")
        
    def __int__(self):
        "Turns number into an integer"
        return int(self.full_number)
    
    
    def __repr__(self):
        "Turns number into an informal string representation"
        return f"PhoneNumber('{self.full_number}')"
    
    
    def __str__(self):
        "Turns number into a formal string format"
        return f"({self.area_code}) {self.exchange_code}-{self.line_number}"
    
    
    def __lt__(self, other):
        "Checks if one number is smaller than another number"
        return int(self) < int(other)
        
def read_numbers(filepath):
    """read_numbers reads the file of names and numbers in so that we can parse.

    Args:
        filepath (str): filepath to our sample phone numbers file
    
    Returns:
        phone_nums (list): a list of names and their respective phone numbers
        
    Side effects:
        adds phone numbers to empty list, returns list of phone numbers
    """
    phone_nums = []
    with open(filepath, "r", encoding = "UTF-8") as fp:
        for line in fp:
            name, number = line.strip().split("\t")
            try:
                phone_nums.append((name, PhoneNumber(number)))
            except ValueError:
                pass
        sorted_numbers = sorted(phone_nums, key=lambda num: num[1])
        
    return sorted_numbers


def main(path):
    """Read data from path and print results.
    
    Args:
        path (str): path to a text file. Each line in the file should consist of
            a name, a tab character, and a phone number.
    
    Side effects:
        Writes to stdout.
    """
    for name, number in read_numbers(path):
        print(f"{number}\t{name}")


def parse_args(arglist):
    """Parse command-line arguments.
    
    Expects one mandatory command-line argument: a path to a text file where
    each line consists of a name, a tab character, and a phone number.
    
    Args:
        arglist (list of str): a list of command-line arguments to parse.
        
    Returns:
        argparse.Namespace: a namespace object with a file attribute whose value
        is a path to a text file as described above.
    """
    parser = ArgumentParser()
    parser.add_argument("file", help="file of names and numbers")
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.file)

