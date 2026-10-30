from database import Database


def main():
    db = Database()
    task_id = db.add_task("Test task", "This is a database test.", "high")
    print("Tasks:", db.get_tasks())
    db.set_task_status(task_id, "completed")

    note_id = db.add_note("Test note", "SQLite is working.")
    print("Notes:", db.get_notes())

    db.add_focus_session(25)
    db.set_setting("theme", "dark")
    print("Theme:", db.get_setting("theme"))

    # Clean up test records
    db.delete_task(task_id)
    db.delete_note(note_id)
    print("Database test completed successfully.")


if __name__ == "__main__":
    main()
