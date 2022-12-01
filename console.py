#!/usr/bin/python3
""" HBNB console module"""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """ implements the HBNB console"""

    prompt = '(hbnb) '
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, line):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", line)
        if match is not None:
            argl = [line[:match.span()[0]], line[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(line))
        return False

    def do_quit(self, line):
        """
            Quit command to exit the program
            Usage: quit
        """
        return (True)

    def do_EOF(self, line):
        """
            EOF signal to exit the program
            Usage: EOF
        """
        print("")
        return (True)

    def do_create(self, line):
        """
            creates instance of BaseModel and prints id
            Usage: create <class name>
        """
        arg = parse(line)
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg[0])().id)
            storage.save()

    def do_show(self, line):
        """
            Prints the string representation of an instance
            based on the class name
            Usage: show <class name> <id>
        """
        arg = parse(line)
        obj_dict = storage.all()
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg[0], arg[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(argl[0], argl[1])])

    def do_destroy(self, line):
        """
            Deletes an instance based on the class name and id
            Usage: destroy <class name> <id>
        """
        arg = parse(line)
        obj_dict = storage.all()
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg[0], arg[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(arg[0], arg[1])]
            storage.save()

    def do_all(self, line):
        """
            Prints all string representation of all instances
            based or not on the class name.
            Usage: all [<class name>]
        """
        arg = parse(line)
        if len(arg) > 0 and arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(arg) > 0 and arg[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(arg) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, line):
        """
            Retrieves the number of instance of a class
            Usage: show <class name> <id>
        """
        argl = parse(line)
        count = 0
        for obj in storage.all().values():
            if argl[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, line):
        """
            Usage: update <class> <id> <attribute_name> <attribute_value> or
            <class>.update(<id>, <attribute_name>, <attribute_value>) or
            <class>.update(<id>, <dictionary>)
            Update a class instance of a given id by adding or updating
            a given attribute key/value pair or dictionary.
        """
        argl = parse(line)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
