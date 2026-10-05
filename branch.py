import json
import os


BRANCH_FILE = "data/branches/branches.json"


class BranchManager:

    def __init__(self):
        os.makedirs("data/branches", exist_ok=True)

        if not os.path.exists(BRANCH_FILE):
            self.branches = {
                "main": None
            }
            self.save()
        else:
            self.load()

    def save(self):
        with open(BRANCH_FILE, "w") as file:
            json.dump(self.branches, file, indent=4)

    def load(self):
        with open(BRANCH_FILE, "r") as file:
            self.branches = json.load(file)

    def create_branch(self, name, current_commit):

        if name in self.branches:
            print("Branch already exists.")
            return

        self.branches[name] = current_commit
        self.save()

        print(f"Branch '{name}' created successfully.")

    def list_branches(self, current_branch):

        print("\n===== BRANCHES =====")

        for branch in self.branches:

            if branch == current_branch:
                print(f"* {branch}")
            else:
                print(f"  {branch}")

        print("====================")

    def switch_branch(self, name):

        if name not in self.branches:
            print("Branch does not exist.")
            return None

        return self.branches[name]