# non-default packages
import colorama
from colorama import init, Fore

import math
import random
import os
import sys
import json
import time
import threading

# custom exceptions
from assets.exceptions import InfoDisplayException, DataNotFoundError

# constants, multipliers
from assets.constants import (ADDITION, SUBTRACTION, MULTIPLICATION, DIVISION,
                              CLEAR_CONSOLE, CURSOR_UP_ONE, ERASE_LINE, COLOR_RESET, erase_line)



class MainMenu():

    # load config info
    def __init__(self, first_time=False):

        self.main_path = os.path.dirname(__file__)

        if not first_time:
            print(CLEAR_CONSOLE)

        # load configuration file
        try:
            with open(os.path.join(self.main_path, "assets/config.json"), "r", encoding="utf-8") as f:
                self.config = json.load(f)

        except FileNotFoundError:
            print(
                "Erorr! config.json file not found, please consider reinstalling the program.")
            time.sleep(4)
            sys.exit("Exiting the program.")

        if first_time:
            # init colorama package
            colorama.init(autoreset=True)

            # print introduction information
            for line in self.config["main"]["title"]:
                print(Fore.CYAN + line)

    def run(self):

        # new alternative in python 3.x
        print(*self.config["main"]["intro"], sep="\n")

        modules = {1: lambda: ModuleArithmetic(
            self.config), 2: lambda: ModuleAlgebra(self.config)}

        instructions = "type 'e' to exit the program, q: Quick-play, 'i' to display additional information\n1: Aritmetic, 2: Algebra\n"

        # branch selection
        print(instructions)

        while True:
            try:
                branch = input()

                if branch == "e":
                    sys.exit("Exiting the program.")
                elif branch == "i":
                    print(CLEAR_CONSOLE)
                    print(*self.config["main"]["info"], sep="\n")
                    print("\n"+instructions)

                    raise InfoDisplayException
                elif branch == "q":
                    return QuickPlay(self.config).preset_selection()

                branch = int(branch)

                selected = modules.get(branch)

                assert selected != None

            except AssertionError:
                print("Please select only from branches mentioned above. Try again.")
                time.sleep(2)
                erase_line(2)

            except ValueError:
                print("Invalid selection. Try again.")
                time.sleep(2)
                erase_line(2)

            except InfoDisplayException:
                pass

            else:
                break

        # execute function from modules dict which initializes a new class for each math branch/module separately
        selected()


# mathematical branches
class ModuleArithmetic():
    def __init__(self, config, preset_run=False):

        self.config = config


        if not preset_run:

            print(CLEAR_CONSOLE)

            # introduction
            for line in self.config["modules"]["arithmetic"]["description"]:
                print(line)

            settings = self.select_mode()

            print(CLEAR_CONSOLE)

            self.run_practice(*settings)

    def select_mode(self):

        default_operations = {1: "+", 2: "-", 3: "*", 4: "/"}
        selected_operations = []

        print("\nPlease select arithmetic operations which you would like to practice:")
        print("-------------------------------------------------------------------------")
        print(default_operations)
        print("Type 'c' to continue, 'e' to return to main menu")

        print(f"selected: {selected_operations}\n")

        while True:
            try:
                op = input()

                erase_line()

                if op == "c" and selected_operations:
                    break

                elif op == "e":
                    MainMenu().run()

                else:
                    op = int(op)

                    selected = default_operations.get(op)

                    assert selected != None

                    selected_operations.append(
                        selected) if selected not in selected_operations else selected_operations.remove(selected)

                    # ANSI escape codes:
                    # "\033[F" – move cursor to the beginning of the previous line
                    # "\033[A" – move cursor up one line

                    # \r character is used to return cursor back to the start of the line, for the purpose of rewriting the same line with different values

                    # move up one line to rewrite selected operations
                    erase_line(2)
                    print(f"selected: {selected_operations}\n")

            except (ValueError, AssertionError):
                pass

        print(CLEAR_CONSOLE)

        # number of digits selection
        while True:
            try:
                digits = input("Max digit length: ")

                if digits == "e":
                    MainMenu().run()

                digits = int(digits)

                assert 1 <= digits <= 9

            except ValueError:
                print("The number of digits needs to be integer. Try again.\n")

            except AssertionError as e:
                print("The number of digits needs to be in range 1-9. Try again.\n")

            else:
                break

        print(CLEAR_CONSOLE)

        # timer selection
        while True:
            try:
                time_limit = input("Select timer (in minutes): ")

                if time_limit == "e":
                    MainMenu().run()

                time_limit = float(time_limit)*60

                assert 0 < time_limit, "Timer length must be greater than 0. Try again.\n"
                assert time_limit <= 60, "Timer length can be max 60 minutes. Try again.\n"

            except ValueError:
                print("The number of digits needs to be integer. Try again.\n")

            except AssertionError as e:
                print(e)

            else:
                break

        # record = True if input(
        #     "Do you want to record your performance? (y/n) ") == "y" else False

        return selected_operations, digits, time_limit

    # def timer(time_limit):

    #     start = time.time()

    #     while time.time() - start < timer:
    #         print(f"time left: {round(timer-(time.time() - start))})")

    def gen_problem(self, operations, digits):

        # system of digit length = 1st digit will be exactly of equal length, 2nd's length will be chosen at random(1, digits)

        digit1 = "".join([str(random.randint(0, 9))
                         for _ in range(digits)])

        digit2 = "".join([str(random.randint(0, 9))
                         for _ in range(random.randint(1, digits))])

        operation = random.choice(operations)

        problem = f"{int(digit1)} {operation} {int(digit2)}"

        try:
            result = int(eval(problem))

            if operation == "/":
                assert int(digit1) % int(digit2) == 0

            return problem, result

        # in order to preserve the same quantity of divisions, generate new, valid division problem
        except (ZeroDivisionError, AssertionError):
            return self.gen_problem(["/"], digits)

    def run_practice(self, operations, digits, time_limit):

        # generate first problem without starting the timer
        problem = self.gen_problem(operations, digits)

        # statistics saving (format: [count, correct])
        statistics = [0, 0]

        ans = input(problem[0]+"\n")

        if ans == "e":
            return MainMenu().run()

        statistics[0] += 1

        try:
            if int(ans) == problem[1]:
                erase_line()
                print(Fore.GREEN + f"{ans}")
                statistics[1] += 1

            else:
                raise ValueError

        except ValueError:
            erase_line()
            print(Fore.RED + f"{ans} ({problem[1]})")

        finally:
            print("Starting the timer. (Type 'e' anytime to exit to main menu, however your performance won't be recorded)\n")

        # initiate the timer (time.time() returns float of time in secons since the epoch -> Jan 1 1970)
        start = time.time()

        while time.time() - start < time_limit:

            problem = self.gen_problem(operations, digits)

            ans = input(problem[0]+"\n")

            if ans == "e":
                MainMenu().run()
                break

            statistics[0] += 1

            try:
                if int(ans) == problem[1]:
                    erase_line()
                    print(Fore.GREEN + f"{ans}")
                    statistics[1] += 1

                else:
                    raise ValueError

            except ValueError:
                erase_line()
                print(Fore.RED + f"{ans} ({problem[1]})")

            finally:
                if time.time() - start < time_limit:
                    print(
                        f"time: {int(time_limit-(time.time() - start))} seconds\n")

        else:
            # save statistics
            self.cleanup(statistics, operations, digits, time_limit)

            print("\nType 'r' to go again or 'е' to exit to main menu.")

            while True:
                choice = input()

                if choice == "r":
                    print(CLEAR_CONSOLE)
                    return self.run_practice(operations, digits, time_limit)

                elif choice == "e":
                    return MainMenu().run()

                else:
                    erase_line()

    # called after finishing the practice, saves performance record to folder with statistics
    def cleanup(self, statistics, operations, digits, time_limit):

        current_total = statistics[0]
        current_correct = statistics[1]

        operations_multiplier = 0

        if "+" in operations:
            operations_multiplier += ADDITION
        if "-" in operations:
            operations_multiplier += SUBTRACTION
        if "*" in operations:
            operations_multiplier += MULTIPLICATION
        if "/" in operations:
            operations_multiplier += DIVISION

        # calculate performance rates

        # absolute perf = correct / total * 100% (rounding 2 decimals)
        current_absolute = round(current_correct / current_total * 100, 2)

        # relative perf = absolute perf * ([correct*digits*operations multiplier] / seconds) (rounding 2 decimals)
        current_relative = round(
            current_absolute * ((current_correct*(digits**2)*(operations_multiplier*0.5)) / time_limit), 2)

        try:
            with open(os.path.join(os.path.dirname(__file__), "statistics.txt"), "r+", encoding="utf-8") as f:
                # READING

                # find past average relative performances (located on the last line)
                # the last line can be efficiently accessed only through opening file for reading in binary mode
                with open(os.path.join(os.path.dirname(__file__), "statistics.txt"), "rb") as f_b:
                    try:
                        f_b.seek(-2, os.SEEK_END)

                        while f_b.read(1) != b'\n':
                            f_b.seek(-2, os.SEEK_CUR)

                        f_last_line = f_b.tell()

                        stats = f_b.readline().decode().rstrip().split()

                    except (OSError):
                        f_b.seek(0)

                try:
                    try:
                        # bring pointer back to the start of the last line so that old avg stats will be overridden
                        f.seek(f_last_line)
                    except:
                        raise DataNotFoundError

                    if stats[0] == "AVERAGE-RELATIVE-PERFORMANCE:" and stats[3] == "TOTAL-PRACTICE-SESSIONS:":
                        avg_relative = float(stats[1])
                        total_practices = int(stats[4])
                    else:
                        raise DataNotFoundError

                except (DataNotFoundError):
                    print(Fore.YELLOW + f"\nWarning! 'AVERAGE-RELATIVE-PERFORMANCE:' and/or 'TOTAL-PRACTICE-SESSIONS:' not found in 'statistics.txt' file (created new)")
                    avg_relative = current_relative
                    total_practices = 1

                # APPENDING

                # date, time
                f.write(time.strftime("%m/%d/%Y %H:%M:%S"))

                # settings
                # time rounded to 1 decimal (nearest even number rounding is defaultly used - bank rounding)
                f.write(
                    f"\n{time_limit/60:0.1f} min    {digits} digits    {operations}")

                # statistics
                f.write(
                    f"\ntotal: {current_total}    correct: {current_correct}")

                # update this session's performance rates
                f.write(
                    f"\nabsolute perf: {current_absolute} %   relative perf: {current_relative} %")

                # lastly, calc and new total avg relative and add total count of practice sessions (rounding 2 decimals)
                new_avg_relative = round(
                    (total_practices * avg_relative + current_relative) / (total_practices + 1), 2)

                f.write(
                    f"\n\nAVERAGE-RELATIVE-PERFORMANCE: {new_avg_relative} %   TOTAL-PRACTICE-SESSIONS: {total_practices + 1}")

        # in case 'statistics.txt' file was not found, create new
        except FileNotFoundError:
            with open(os.path.join(os.path.dirname(__file__), "statistics.txt"), "w", encoding="utf-8") as f:
                # load default introduction for 'statistics.txt' file from config.json
                for line in self.config["main"]["file_intros"]["statistics"]:
                    f.write(line+"\n")

                # WRITE LAST SESSION DETAILS

                # date, time
                f.write(time.strftime("\n%m/%d/%Y %H:%M:%S"))

                # settings
                # time rounded to 1 decimal (nearest even number rounding is defaultly used - bank rounding)
                f.write(
                    f"\n{time_limit/60:0.1f} min    {digits} digits    {operations}")

                # statistics
                f.write(
                    f"\ntotal: {current_total}    correct: {current_correct}")

                # update this session's performance rates
                f.write(
                    f"\nabsolute perf: {current_absolute} %  relative perf: {current_relative} %")

                f.write(
                    f"\n\nAVERAGE-RELATIVE-PERFORMANCE: {current_relative} %    TOTAL-PRACTICE-SESSIONS: {1}")

                avg_relative = current_relative

        # CONSOLE OUTPUT
        print("\nTime is up! Some quick stats:")
        print(f"total: {current_total}   correct: {current_correct}")
        print(
            f"absolute: {Fore.MAGENTA}{current_absolute} % {COLOR_RESET}   relative: {current_relative} %")
        print(f"average relative: {avg_relative} %")
        print(f"You scored {abs(current_relative-avg_relative):0.2f} % {(Fore.GREEN + 'better') if current_relative >= avg_relative else (Fore.RED + 'worse')}{COLOR_RESET} than your past average performance.")


class ModuleAlgebra():
    def __init__(self, config):
        erase_line()
        print("This feature is in the process of development, returning to main menu.")
        time.sleep(2)

        # clear console and return to main menu
        print(CLEAR_CONSOLE)

        return MainMenu().run()


class QuickPlay():
    def __init__(self, config):
        self.config = config

        print(CLEAR_CONSOLE)

    def preset_selection(self):
        print("\nWelcome to preset selection.")
        print("List of your presets:")

        presets = self.load_presets()

        print(
            "\ntype #id (without #) of a preset to select it or 'е' to go back to main menu")

        while True:
            choice = input()

            erase_line()

            if choice == "e":
                return MainMenu().run()
            else:
                for preset in presets:
                    if choice == preset.id_num:
                        return preset.run_preset()

    def load_presets(self):

        presets = []
        presets_obj = []

        try:
            with open(os.path.join(os.path.dirname(__file__), "presets.txt"), "r", encoding="utf-8") as f:

                preset_pos = False

                for line in f:

                    line = line.rstrip()

                    if preset_pos:
                        print(line)

                        presets.append(line)

                        preset_pos -= 1

                    if line and line[0] == "#":
                        print("\n"+line)

                        presets.append(line[1:])

                        preset_pos = 4

            for i in range(int(len(presets)/5)):
                id_num = presets[i*5+0]
                name = presets[i*5+1]
                operations = presets[i*5+2]
                digits = presets[i*5+3]
                time_limit = presets[i*5+4]

                presets_obj.append(
                    Preset(self.config, id_num, name, operations, digits, time_limit))

            return presets_obj

        # if no 'presets.txt' file found, create one and load again
        except FileNotFoundError:

            with open(os.path.join(os.path.dirname(__file__), "presets.txt"), "w", encoding="utf-8") as f:

                for line in self.config["main"]["file_intros"]["presets"]:
                    f.write(line+"\n")

            return self.load_presets()


class Preset():
    def __init__(self, config, id_num, name, operations, digits, time_limit):
        self.config = config

        self.id_num = id_num
        self.name = name
        self.operations = operations.strip().strip("[]").replace(",", "").split()
        self.digits = int(digits)
        self.time_limit = float(time_limit)*60

    def run_preset(self):
        print(CLEAR_CONSOLE)
        print(f"\nLaunching quick-run template with the name '{self.name}'")
        return ModuleArithmetic(self.config, preset_run=True).run_practice(self.operations, self.digits, self.time_limit)


if __name__ == "__main__":
    MainMenu(first_time=True).run()
