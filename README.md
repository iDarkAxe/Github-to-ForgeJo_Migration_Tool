# Github-to-ForgeJo_Migration_Tool

Using gh tool to have full github access to migrate properly to Forgejo.


## Usage ##
Mass_Migrate script migrate public and private repos AS public now, as an immediate workaround, patch is making them back as private.
You need to define the variables in the demo files to be able to use the tool.
```sh
python ./mass_migrate.py
python ./patch.py
```
