#!/usr/bin/python3
'''command intepreter'''
import cmd
from models.base_model import BaseModel
from models.state import State
from models.job import Job
from models.city import City
from models import storage
from models.profession import Profession

classes = {
    'BaseModel': BaseModel,
    'Job': Job,
    'State': State,
    'City': City,
    'Profession': Profession
}


class Shell(cmd.Cmd):
    '''simple command intepreter'''
    prompt = '(Shell)$ '

    def do_create(self, line):
        '''
        Creates and saves a class
        ps: line is a string
        '''
        if self.validate(line):
            args = line.split(" ")
            command = args[0]
            new_obj = classes[command]()
            for i in range(1, len(args)):
                try:
                    arg = args[i].split("=")
                    val = eval(arg[1])
                    if type(val) == str:
                        val = val.replace("_", " ")
                    key = arg[0]
                    setattr(new_obj, key, val)
                except Exception:
                    continue
            print(new_obj)
            new_obj.save()
            print(new_obj.id)
        else:
            pass

    def validate(self, line):
        '''validates the input'''
        if line:
            args = line.split(" ")
            command = args[0]
            if command in classes:
                return 1
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing *")
        return 0

    def do_show(self, line):
        '''prints the string representation of an instance
        based on cls name and id'''
        if self.validate(line):
            args = line.split(' ')
            num_args = len(args)

            if num_args == 2:
                cls_req = args[0]
                cls_id = args[1]
            elif num_args == 1:
                print('** instance id missing **')
                return

            obj_array = storage.all(cls_req)
            for obj in obj_array:
                if obj.id == cls_id:
                    print(obj)
                    return
            print("** no instance found **")
        else:
            pass

    def do_destroy(self, line):
        '''deletes an obj from storage'''
        if self.validate(line):
            args = line.split(' ')
            num_args = len(args)

            if num_args == 2:
                cls_req = args[0]
                cls_id = args[1]
            elif num_args == 1:
                print('** instance id missing **')
                return

            obj_array = storage.all(cls_req)
            del_obj_id = f'{cls_req}.{cls_id}'
            if storage.delete(del_obj_id):
                pass
            else:
                print("** no instance found **")
        else:
            pass

    def do_all(self, line):
        '''prints all string representation of all instances
           based or not on the class name'''
        args = line.split(" ")
        s_cls = args[0]
        if self.validate(line):
            print([obj.__str__() for obj in storage.all(s_cls)])

    def do_update(self, line):
        '''Updates an instance based on the class name
        and id by adding or updating attribute
        (save the change into the JSON file)'''
        if self.validate(line):
            args = line.split(' ')
            num_args = len(args)

            if num_args == 4:
                cls_req = args[0]
                cls_id = args[1]
                cls_attr = args[2]
                cls_val = args[3]
            elif num_args == 1:
                print('** instance id missing **')
                return
            elif num_args == 2:
                print('** attribute name missing **')
                return
            else:
                print('** value missing **')
                return

            obj_array = storage.all(cls_req)
            for obj in obj_array:
                if obj.id == cls_id:
                    setattr(obj, cls_attr, cls_val)
                    storage.save()
                    return
            print("** no instance found **")
        else:
            pass

    def do_emptyline(self):
        '''ensures last command is not repeated'''
        pass

    def do_quit(self, line):
        '''Gracefully termination of program'''
        return self.do_EOF(line)

    def do_EOF(self, line):
        '''handle the end of character'''
        return True


if __name__ == "__main__":
    Shell().cmdloop()
