class ProjectRepository:

    def __init__(self):

        self.projects = {}

    def create(self, project):

        self.projects[
            project.id
        ] = project

        return project

    def get(self, project_id):

        return self.projects.get(
            project_id
        )

    def list_by_owner(
        self,
        owner_id,
    ):

        return [
            project
            for project
            in self.projects.values()
            if project.owner_id == owner_id
        ]