from repository import Repository


def main():

    repo = Repository()

    while True:

        print("\n========== GIT-LITE ==========")

        print("1. Initialize Repository")
        print("2. Create Commit")
        print("3. View Commit History")
        print("4. Create Branch")
        print("5. List Branches")
        print("6. Switch Branch")
        print("7. Rollback")
        print("8. Exit")

        print("==============================")

        choice = input("Enter choice: ")

        # -------------------------
        # INITIALIZE
        # -------------------------

        if choice == "1":

            repo.init()

        # -------------------------
        # COMMIT
        # -------------------------

        elif choice == "2":

            message = input(
                "Enter commit message: "
            )

            repo.commit(message)

        # -------------------------
        # LOG
        # -------------------------

        elif choice == "3":

            repo.log()

        # -------------------------
        # CREATE BRANCH
        # -------------------------

        elif choice == "4":

            name = input(
                "Enter new branch name: "
            )

            repo.create_branch(name)

        # -------------------------
        # LIST BRANCHES
        # -------------------------

        elif choice == "5":

            repo.list_branches()

        # -------------------------
        # SWITCH BRANCH
        # -------------------------

        elif choice == "6":

            name = input(
                "Enter branch name: "
            )

            repo.switch_branch(name)

        # -------------------------
        # ROLLBACK
        # -------------------------

        elif choice == "7":

            commit_id = input(
                "Enter commit ID to rollback to: "
            )

            repo.rollback(commit_id)

        # -------------------------
        # EXIT
        # -------------------------

        elif choice == "8":

            print("Exiting Git-Lite...")

            break

        else:

            print("Invalid choice.")


if __name__ == "__main__":

    main()