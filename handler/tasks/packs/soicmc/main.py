def init(celery_app, **global_decorators):
    authorized_task = global_decorators['authorized_task']

    #@authorized_task
    @celery_app.task
    def run_checkpoint1(x: int, y: int):
        program_output = None
        try:
            import os
            import sys
            from tasks.packs.soicmc.resources import sys_utils
            bin_name = 'checkpoint1'
            bin_path = sys_utils.default_bin_dir + "/" + bin_name
            
            program_stdout, program_stderr = sys_utils.run_command(f"./{bin_name}", cwd=bin_path, log_stdout=False, log_stderr=False)
            program_output = program_stdout
        except Exception as exc:
            program_output = f"Failed to execute task. Error: {str(exc)}"
        
        return program_output
    
    #@authorized_task
    @celery_app.task
    def run_checkpoint2(x: int, y: int):
        program_output = None
        try:
            import os
            import sys
            from tasks.packs.soicmc.resources import sys_utils
            bin_name = 'checkpoint2'
            bin_path = sys_utils.default_bin_dir + "/" + bin_name
            
            program_stdout, program_stderr = sys_utils.run_command(f"./{bin_name}", cwd=bin_path, log_stdout=False, log_stderr=False)
            program_output = program_stdout
        except Exception as exc:
            program_output = f"Failed to execute task. Error: {str(exc)}"
            
        return program_output
    
    #@authorized_task
    @celery_app.task
    def run_checkpoint3(x: float, y: float):
        program_output = None
        try:
            import os
            import sys
            from tasks.packs.soicmc.resources import sys_utils
            bin_name = 'checkpoint3'
            bin_path = sys_utils.default_bin_dir + "/" + bin_name
            
            program_stdout, program_stderr = sys_utils.run_command(f"./{bin_name}", cwd=bin_path, log_stdout=False, log_stderr=False)
            program_output = program_stdout
        except Exception as exc:
            program_output = f"Failed to execute task. Error: {str(exc)}"
        
        return program_output