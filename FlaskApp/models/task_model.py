class Task:
    def __init__(self, createdByUid="", assignedToUid="",  description=""):
        # Constructor for the Task model.
        # Initialize the attributes with default values.
        self.createdByUid = createdByUid
        self.assignedToUid = assignedToUid
        self.description = description
        self.done = False  # The constructor initializes the "done" attribute as False

    def to_dict(self):
        # Convert the Task object to a dictionary representation.
        return {
            "createdByUid": self.createdByUid,
            "assignedToUid": self.assignedToUid,
            "description": self.description,
            "done": self.done,
        }

    @classmethod
    def from_dict(cls, data):
        # Create a new Task object from a dictionary.
        task = cls()
        task.createdByUid = data.get("createdByUid", "")
        task.assignedToUid = data.get("assignedToUid", "")
        task.description = data.get("description", "")
        task.done = data.get("done", False)
        return task
