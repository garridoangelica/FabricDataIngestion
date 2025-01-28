# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "139b0f9e-ea6d-4d39-9077-d906a2723906",
# META       "default_lakehouse_name": "bronze",
# META       "default_lakehouse_workspace_id": "1c55b68a-6a98-4dcd-9d0b-5d034ab70e0c"
# META     },
# META     "environment": {
# META       "environmentId": "30bbce7a-995f-9715-4e2f-62f0676c8b77",
# META       "workspaceId": "00000000-0000-0000-0000-000000000000"
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!
print('Hello World')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

## Create a new file in module1 in built-in directory
# mssparkutils.fs.put("file:///synfs/nb_resource/builtin/pythonTemplate/src/packagename/module1/_helloworld.py", "", True)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

## import the package
import builtin.pythonTemplate.src.packagename.module1 as m1


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

## Reimport if you have made updates to the module
import importlib
importlib.reload(m1)

m1.print_hello('Angelica')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import samplepackage.module1 as m1
m1.print_hello("Angelica")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
