# Study Hours Logger

total_hours = 0.0
session_count = 0
log = ""

print("=== Study Hours Logger ===")

while True:
    print("\n1. Log study session")
    print("2. View summary")
    print("3. Quit")
    choice = input("Choose an option (1-3): ").strip()

    if choice == "1":
        subject = input("Subject: ").strip()
        hours_text = input("Hours studied: ").strip()

        # Check the input is a positive number like 2 or 1.5
        if subject == "":
            print("Subject can't be empty.")
        elif not hours_text.replace(".", "", 1).isdigit():
            print("Please enter hours as a number, e.g. 1.5")
        elif float(hours_text) <= 0:
            print("Hours must be greater than 0.")
        elif float(hours_text) > 24:
            print("That's more than 24 hours in a day!")
        else:
            hours = float(hours_text)
            total_hours = total_hours + hours
            session_count = session_count + 1
            log = log + f"  {session_count}. {subject}: {hours} hrs\n"
            print(f"Logged {hours} hrs of {subject}.")

    elif choice == "2":
        if session_count == 0:
            print("No sessions logged yet.")
        else:
            average = total_hours / session_count
            print("\n--- Summary ---")
            print(log, end="")
            print(f"Sessions: {session_count}")
            print(f"Total hours: {total_hours}")
            print(f"Average per session: {average:.2f} hrs")

    elif choice == "3":
        print("Keep it up. Goodbye!")
        break

    else:
        print("Invalid choice, please enter 1, 2, or 3.")