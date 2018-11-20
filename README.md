# crowdea
An open-source idea-management website with crowd-sourcing, crowd-funding and market-testing capabilities.

## Dependencies & Installation
Make sure to have django version 1.11.16  and Python 2.7.5 Installed. 

Once you have Python & pip installed, you can quickly download all dependencies by:

```pip install requirements.txt -r```

## Database Configuration

Run ```python manage.py migrate``` to have your database file created. Make sure to have the correct username and password for your MySQL in crowdea/settings.py file.

## Admin Panel
Once you have everything ready, you can create a super user account for the admin panel by the command: ```python manage.py createsuperuser```

## Running 
The website can be runned by the command ```python manage.py runserver PORT_NUMBER``` executed in the base directory. If PORT_NUMBER is not provided, the default port will be 8000. Assuming you are using the default port, open the browser and navigate to ```localhost:8000```.

## Contribution & Commit Guidlines
### Important
please use the develop branch for all the development purposes and issue a merge request.

For newly developed features, use gitflow (default naming style is feature/branch_name)

Learn more about gitflow commands here: https://danielkummer.github.io/git-flow-cheatsheet/

gitflow commands have comparable commands in git, i.e. if you use are on develop branch and use:
git branch -b feature/branch_name
git push origin feature/branch_name

but after merging with the develop branch, feature_branch needs to be deleted manually this way.

