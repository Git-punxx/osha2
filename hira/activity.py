class Activity:
    def __init__(self, activity_id, description, category):
        self.id = activity_id
        self.description = description
        self.category = category

    def __hash__(self):
        return hash(self.description)

    def __eq__(self, other):
        return self.description == other.description and self.id == other.id


class Project:
    def __init__(self, title):
        self.title = title
        self.activities = {}

    def add(self, activity):
        self.activities[activity] = activity

    def __str__(self):
        return f'{self.title}: #activities: {len(self.activities)}'



class HazardRegistry:
    def __init__(self):
        self.registry = {}
        self.load()

    def load(self):
        print('Loading hazard registry')



if __name__ == '__main__':
    p = Project('CJ 9315');
    p.add(Activity(1, "some activity", 12))
    print(p)
