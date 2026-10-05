import os

from commit import Commit

from storage import (
    save_commit,
    load_commit,
    save_head,
    load_head,
    save_object,
    load_object
)

from branch import BranchManager


class Repository:

    def __init__(self):

        self.current_commit = load_head()

        self.branch_manager = BranchManager()

        self.current_branch = self.load_current_branch()

    # -----------------------------
    # CURRENT BRANCH
    # -----------------------------

    def load_current_branch(self):

        branch_file = "data/branches/current_branch"

        if os.path.exists(branch_file):

            with open(
                branch_file,
                "r"
            ) as file:

                return file.read().strip()

        return "main"

    def save_current_branch(self):

        os.makedirs(
            "data/branches",
            exist_ok=True
        )

        with open(
            "data/branches/current_branch",
            "w"
        ) as file:

            file.write(self.current_branch)

    # -----------------------------
    # INITIALIZE
    # -----------------------------

    def init(self):

        os.makedirs(
            "data/commits",
            exist_ok=True
        )

        os.makedirs(
            "data/branches",
            exist_ok=True
        )

        os.makedirs(
            "data/objects",
            exist_ok=True
        )

        os.makedirs(
            "workspace",
            exist_ok=True
        )

        if self.branch_manager.branches["main"] is None:

            self.branch_manager.branches["main"] = (
                self.current_commit
            )

            self.branch_manager.save()

        print("\nGit-Lite repository initialized.")

        print(
            "Current branch:",
            self.current_branch
        )

        if self.current_commit:

            print(
                "Current HEAD:",
                self.current_commit
            )

    # -----------------------------
    # TRACK FILES
    # -----------------------------

    def track_files(self):

        files = {}

        workspace = "workspace"

        for root, dirs, filenames in os.walk(workspace):

            for filename in filenames:

                file_path = os.path.join(
                    root,
                    filename
                )

                relative_path = os.path.relpath(
                    file_path,
                    workspace
                )

                try:

                    with open(
                        file_path,
                        "r",
                        encoding="utf-8"
                    ) as file:

                        content = file.read()

                    object_id = save_object(content)

                    files[relative_path] = object_id

                except UnicodeDecodeError:

                    print(
                        f"Skipping binary file: {relative_path}"
                    )

        return files

    # -----------------------------
    # COMMIT
    # -----------------------------

    def commit(self, message):

        file_snapshot = self.track_files()

        new_commit = Commit(
            message=message,
            parent=self.current_commit,
            files=file_snapshot
        )

        save_commit(new_commit)

        self.current_commit = new_commit.commit_id

        self.branch_manager.branches[
            self.current_branch
        ] = self.current_commit

        self.branch_manager.save()

        save_head(self.current_commit)

        print("\nCommit created successfully!")

        print(
            "Commit ID:",
            new_commit.commit_id
        )

        print(
            "Message:",
            new_commit.message
        )

        print(
            "Branch:",
            self.current_branch
        )

    # -----------------------------
    # LOG
    # -----------------------------

    def log(self):

        if not self.current_commit:

            print("No commits yet.")

            return

        current = self.current_commit

        print(
            "\n===== COMMIT HISTORY ====="
        )

        while current:

            commit = load_commit(current)

            if not commit:

                break

            print(
                "\nCommit:",
                commit["commit_id"]
            )

            print(
                "Message:",
                commit["message"]
            )

            print(
                "Time:",
                commit["timestamp"]
            )

            current = commit["parent"]

        print(
            "\n=========================="
        )

    # -----------------------------
    # CREATE BRANCH
    # -----------------------------

    def create_branch(self, name):

        self.branch_manager.create_branch(
            name,
            self.current_commit
        )

    # -----------------------------
    # LIST BRANCHES
    # -----------------------------

    def list_branches(self):

        self.branch_manager.list_branches(
            self.current_branch
        )

    # -----------------------------
    # SWITCH BRANCH
    # -----------------------------

    def switch_branch(self, name):

        commit = self.branch_manager.switch_branch(name)

        if commit is None:

            return

        self.current_branch = name

        self.current_commit = commit

        save_head(
            self.current_commit
        )

        self.save_current_branch()

        print(
            f"\nSwitched to branch '{name}'."
        )

        print(
            "HEAD:",
            self.current_commit
        )

    # -----------------------------
    # RESTORE WORKSPACE
    # -----------------------------

    def restore_workspace(self, files):

        workspace = "workspace"

        os.makedirs(
            workspace,
            exist_ok=True
        )

        restored_files = {}

        # Load all files from the commit
        for relative_path, object_id in files.items():

            relative_path = os.path.normpath(
                relative_path
            )

            # Security check
            if (
                os.path.isabs(relative_path)
                or relative_path == ".."
                or relative_path.startswith(
                    ".." + os.sep
                )
            ):

                print(
                    "Invalid file path in commit."
                )

                return False

            content = load_object(
                object_id
            )

            if content is None:

                print(
                    f"Saved file object missing: {object_id}"
                )

                return False

            restored_files[
                relative_path
            ] = content

        # Remove files that do not
        # exist in selected commit
        for root, dirs, filenames in os.walk(workspace):

            for filename in filenames:

                full_path = os.path.join(
                    root,
                    filename
                )

                relative_path = os.path.relpath(
                    full_path,
                    workspace
                )

                if relative_path not in restored_files:

                    os.remove(full_path)

        # Restore files
        for relative_path, content in restored_files.items():

            file_path = os.path.join(
                workspace,
                relative_path
            )

            parent_directory = os.path.dirname(
                file_path
            )

            if parent_directory:

                os.makedirs(
                    parent_directory,
                    exist_ok=True
                )

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(content)

        print(
            "Workspace files restored successfully."
        )

        return True

    # -----------------------------
    # ROLLBACK
    # -----------------------------

    def rollback(self, commit_id):

        commit = load_commit(
            commit_id
        )

        if commit is None:

            print(
                "Commit not found."
            )

            return

        files = commit.get(
            "files",
            {}
        )

        if not self.restore_workspace(files):

            print(
                "Rollback cancelled."
            )

            return

        self.current_commit = commit_id

        self.branch_manager.branches[
            self.current_branch
        ] = commit_id

        self.branch_manager.save()

        save_head(
            commit_id
        )

        self.save_current_branch()

        print(
            "\nRollback successful."
        )

        print(
            "Current branch:",
            self.current_branch
        )

        print(
            "HEAD:",
            self.current_commit
        )