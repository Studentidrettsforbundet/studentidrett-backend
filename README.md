# studentidrett-backend

# Run for the first time

Make sure to have a .env-file in `app/app/` with `DJANGO_SECRET_KEY` set.

To run migrations, navigate to `/app` and run `python manage.py migrate`. This will create a database in the local virtual environment.

If this goes without errors, run `python manage.py runserver`. This will start the server at `localhost:8000`.

### Dependencies

Dependencies are stored in `requirements.txt`, and is installed by running `pip install -r requirements.txt`.

After adding a new dependency, run `pip freeze > requirements.txt` to update.

This makes sure that everyone uses the same dependencies and versions during development.

# Git-conventions

Branches:

- main: update only for deployment (merge from dev)
- dev: development branch, update continuously
- feat/feature-name: a branch that creates/improves a new feature into dev
- task/task-name: a branch that creates/improves a new task into feat. Is used when multiple developers work on a feature
- design/area-name: a branch that creates/improves GUI/UX into dev
- fix/bug-name: a branch that fix a bug or security issue for dev

Pull requests:

- At least one collaborator have to review and approve a pull request before it is merged into dev-branch
- Always use "Squash and merge" as merge-options