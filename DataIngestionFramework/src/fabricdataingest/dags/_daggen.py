import json

class DagGenerator:
    def __init__(self, customer, notebookPath, timeoutInSeconds, concurrency, timoutPerCellInSeconds=90):
        self.customer = customer
        self.notebookPath = notebookPath
        self.timeoutInSeconds = timeoutInSeconds
        self.concurrency = concurrency
        self.timoutPerCellInSeconds = timoutPerCellInSeconds

    def parse_string_to_list(self, input_string):
        return input_string.split(',')

    def generate_json(self, tables, dependencies=None):
        activities = []

        # Add an additional activity for each customer
        for i, table in enumerate(tables):
            ##if customer invoice line , then  generate dependcies 
            activity = {
                "name": f"Notebook{self.customer}_{table}",
                "path": self.notebookPath,
                "timeoutPerCellInSeconds": self.timoutPerCellInSeconds,
                "args": {"customer": self.customer, "tableName": table}
            }
            
            # Add dependencies if they exist for this table
            if dependencies and table in dependencies:
                activity["dependsOn"] = dependencies[table]
                
            activities.append(activity)

        job = {
            "activities": activities,
            "timeoutInSeconds": self.timeoutInSeconds,
            "concurrency": self.concurrency
        }

        return str(json.dumps(job, indent=4))

    def generate_json_from_array(self, notebook_configs):
        """
        Generate a DAG from an array of notebook configurations.
        
        Each element in notebook_configs should be a dictionary with at least:
        - 'table': the table name
        - 'dependencies': (optional) list of activity names this table depends on
        - 'notebook_path': (optional) override the default notebook path
        - 'args': (optional) additional arguments for this specific notebook
        """
        activities = []

        for config in notebook_configs:
            table = config['table']
            
            # Get notebook path (use override if provided, otherwise default)
            notebook_path = config.get('notebook_path', self.notebookPath)
            
            # Create base activity definition
            activity_name = f"Notebook{self.customer}_{table}"
            
            # Prepare args - start with defaults and update with any custom args
            args = {
                "customer": self.customer,  
                "tableName": table
            }
            if 'args' in config:
                args.update(config['args'])
                
            activity = {
                "name": activity_name,
                "path": notebook_path,
                "timeoutPerCellInSeconds": self.timoutPerCellInSeconds,
                "args": args
            }
            
            # Add dependencies if they exist
            if 'dependencies' in config and config['dependencies']:
                activity["dependsOn"] = config['dependencies']
                
            activities.append(activity)

        job = {
            "activities": activities,
            "timeoutInSeconds": self.timeoutInSeconds,
            "concurrency": self.concurrency
        }

        return str(json.dumps(job, indent=4))

