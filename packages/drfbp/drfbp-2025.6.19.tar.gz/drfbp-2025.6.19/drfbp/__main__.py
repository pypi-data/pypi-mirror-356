import os
import sys

from .permissions import PERMISSIONS
from .serializers import SERIALIZERS
from .urls import URLS
from .views import VIEWS


def main():
    if len(sys.argv) != 4:
        print("[!] Invalid usage")
        print("Usage\t: drfbp <app> <model> <directory>")
        print("Example\t: drfbp core User .")
        sys.exit(1)

    app = sys.argv[1]
    model = sys.argv[2]

    path = os.path.abspath(sys.argv[3]).split(os.sep)
    path = os.path.join(*path[path.index(app) :]).replace(os.sep, ".")

    abspath = os.path.abspath(sys.argv[3])

    if os.path.exists(abspath) and os.listdir(abspath):
        print(f"Error: Target directory '{abspath}' already exists and is not empty.")
        print("Please provide an empty or non-existing directory.")
        sys.exit(1)

    os.makedirs(abspath, exist_ok=True)

    with open(f"{os.path.join(abspath, '__init__.py')}", "w") as file:
        file.write("")

    with open(f"{os.path.join(abspath, 'permissions.py')}", "w") as file:
        file.write(PERMISSIONS.format(model=model))

    with open(f"{os.path.join(abspath, 'serializers.py')}", "w") as file:
        file.write(SERIALIZERS.format(app=app, model=model))

    with open(f"{os.path.join(abspath, 'views.py')}", "w") as file:
        file.write(VIEWS.format(app=app, path=path, model=model))

    with open(f"{os.path.join(abspath, 'urls.py')}", "w") as file:
        file.write(URLS.format(path=path, model=model, appname=model.lower()))


if __name__ == "__main__":
    main()
