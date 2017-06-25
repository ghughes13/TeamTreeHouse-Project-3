import datetime
import re


class WorkLog:

    def menu(self):
        """Displays the start menu"""
        do_this = input("Please enter the number of what you would like to do:  "
                        "\n1) Add an entry"
                        "\n2) Search for an entry"
                        "\n3) Exit the program "
                        "\n>> ")
        if do_this == '1':
            self.add_entry()
        elif do_this == '2':
            self.search_entry()
        elif do_this == '3':
            print("Thanks for using Ghughes' worklog!")
            print("Exiting program...")
            exit()
        else:
            print("It doesn't look like that was a valid choice.\n")
            self.menu()

    def add_entry(self):
        """Gathers user input and writes to csv"""
        date_of_task = self.date_error_check(input("When was the task completed? dd/mm/yyyy: "))
        name = input("What's the name of the person who worked on the task? ")
        task_name = input("What's the task's name ")
        task_notes = input("Any notes about the task you would like to include? ")
        time = self.minute_error_check(input("How long did the task take? (Use minutes in whole numbers): "))
        with open('work_log.csv', 'a') as file:
            file.write(date_of_task + ', ' + name + ', ' + task_name + ', ' + task_notes + ', ' + time + '\n')
        print("Info has been added to the work-log. \n Returning to main menu. \n")
        self.menu()

    def search_entry(self):
        """Displays search options and gets user choice"""
        choice = input("What would you like to search by:"
                       "\n1) Exact Date"
                       "\n2) Range of Dates"
                       "\n3) Exact Search"
                       "\n4) Regex Pattern"
                       "\n5) Search by minutes"
                       "\n6) Return to Menu"
                       "\n>> ")
        if choice == '1':
            search_date = self.date_error_check(input("When was the task completed? dd/mm/yyyy: "))
            self.search_file(search_date)
        elif choice == '2':
            start_date = self.date_error_check(input("Please enter a start date. dd/mm/yyyy: "))
            end_date = self.date_error_check(input("Please enter an end date. dd/mm/yyyy: "))
            self.date_range_search(start_date, end_date)
        elif choice == '3':
            look_for = input("Please enter an exact match to find: ")
            self.search_file(look_for)
        elif choice == '4':
            self.regex_search()
        elif choice == '5':
            time_taken = input("How long did the task take? ")
            self.search_file(time_taken)
        elif choice == '6':
            print("Returning to main menu...")
            self.menu()
        else:
            print("Doesn't look like that was a valid choice. Use the numbers next to the choice you want. ")
            self.search_entry()

    def search_file(self, search_arg):
        """Searches csv file for search criteria"""
        query_results_list = []
        with open("work_log.csv") as file:
            for line in file:
                if str(search_arg) in line:
                    query_results_list.append(line)
            self.query_results(query_results_list)

    def regex_search(self):
        """Searches csv file for regex pattern"""
        query_results_list = []
        pattern = input(r"Please input the pattern you want to search with in regex format: ")
        with open("work_log.csv") as file:
            for line in file:
                if re.search(pattern, line):
                    query_results_list.append(line)
            self.query_results(query_results_list)

    def date_range_search(self, start_date, end_date):
        """Searches csv file for lines containing a date between two given dates"""
        start = datetime.datetime.strptime(start_date, '%d/%m/%Y')
        end = datetime.datetime.strptime(end_date, '%d/%m/%Y')
        query_results_list = []
        with open("work_log.csv") as file:
            for line in file:
                split = line.split(',')
                date_in_line = split[0]
                converter = datetime.datetime.strptime(date_in_line, '%d/%m/%Y')
                if start <= converter <= end:
                    query_results_list.append(line)
        self.query_results(query_results_list)

    def what_to_do_next(self, query_results):
        """Asks the user what they want to do next and executes it"""
        quere_index = 0
        with open("work_log.csv") as file:
            while True:
                what_to_do = input("What would you like to do? (Enter: Previous, Next, Delete, Edit"
                                   " or Menu) ").lower()
                if what_to_do == "previous":
                    quere_index -= 1
                    try:
                        print(self.display_entry(query_results[quere_index]))
                    except IndexError:
                        print("No further query results to display. ")
                        quere_index += 1
                elif what_to_do == "next":
                    quere_index += 1
                    try:
                        print(self.display_entry(query_results[quere_index]))
                    except IndexError:
                        print("No further query results to display. ")
                        quere_index -= 1
                elif what_to_do == "menu":
                    self.menu()
                elif what_to_do == "delete":
                    are_you_sure = input("This will delete this line. Are you sure? y/N ").lower()
                    if 'y':
                        self.delete_this(query_results[quere_index])
                    elif 'n':
                        continue
                    else:
                        print("Looks like that wasn't a valid input. ")
                elif what_to_do == "edit":
                    self.edit_line(query_results[quere_index])
                else:
                    print("Whoops, Looks like that wasn't a valid input. Check spelling and try gain. ")

    def delete_this(self, delete_this):
        """Deletes the line the user is on"""
        file = open("work_log.csv", "r")
        lines = file.readlines()
        file.close()
        with open("work_log.csv", 'w') as file:
            for line in lines:
                if delete_this not in line:
                    file.write(line)
        print("That change has been made. Returning to main menu...")
        self.menu()

    def edit_line(self, edit_this):
        """Edits the line the user is on"""
        split_up = edit_this.split(',')
        part_to_edit = input("What part would you like to edit? Enter: Date, Name, Task, Notes, or Minutes. ").lower()
        change_it_to = input("What would you like to change it to? ")
        if part_to_edit == "date":
            change_it_to = self.date_error_check(change_it_to)
            del split_up[0]
            split_up.insert(0, change_it_to)
        elif "name":
            del split_up[1]
            split_up.insert(1, change_it_to)
        elif "task":
            del split_up[2]
            split_up.insert(2, change_it_to)
        elif "notes":
            del split_up[3]
            split_up.insert(3, change_it_to)
        elif "minutes":
            change_it_to = self.minute_error_check(change_it_to)
            del split_up[4]
            split_up.insert(4, change_it_to)
        else:
            print("Whoops looks like something wasn't entered correctly. Please check spelling and try again.")
            self.edit_line(edit_this)
        new_line = ",".join(split_up)
        print(self.display_entry(new_line))
        with open("work_log.csv", 'a') as file:
            file.write(new_line)
        self.delete_this(edit_this)

    def date_error_check(self, date):
        """Checks the input anytime a date is needed to ensure it's a date and formatted correctly"""
        new_date = date
        running = True
        while running:
            try:
                datetime.datetime.strptime(new_date, '%d/%m/%Y')
                running = False
            except ValueError:
                new_date = input("Looks like that wasn't a valid date. Try again with dd/mm/yyyy format: ")
        return new_date

    def minute_error_check(self, minutes):
        """Checks to make sure the minutes given are in whole number format."""
        new_minutes = minutes
        invalid_minutes = True
        while invalid_minutes:
            try:
                int(new_minutes)
                break
            except ValueError:
                new_minutes = input("Looks like that wasn't a valid input for minutes. Please use numbers. ")
                self.minute_error_check(new_minutes)
        return new_minutes

    def display_entry(self, entry):
        """Displays the csv line in a readable format"""
        empty_list = entry.split(',')
        n = '\n'
        thing_to_return = ("Date: " + empty_list[0] + n + "Name: " + empty_list[1] + n + "Task: " + empty_list[2] + n
                           + "Notes: " + empty_list[3] + n + "Time Spent: " + empty_list[4])
        return thing_to_return

    def query_results(self, results):
        if len(results) >= 1:
            print("Here's the first entry matching your search query. \n")
            print(self.display_entry(results[0]))
            self.what_to_do_next(results)
        while True:
            print("No results matching that criteria found.")
            now_do_this = input("Return to the [M]enu, [S]earch again?").upper()
            if now_do_this == 'M':
                self.menu()
            elif now_do_this == 'S':
                self.search_entry()
            else:
                print("Looks like that wasn't a choice. Try again.")


print("Welcome to ghughes' worklog. Please report any errors to guitarguy13@ymail.com")
WorkLog().menu()
