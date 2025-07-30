import os
import subprocess
from datetime import datetime, timedelta


class PySVN:

    def checkout(self, repo_url:str, local_path:str) -> None:
        """
        This function will checkout a directory from SVN to a specified local path
        :param repo_url: Path to directory in SVN
        :param local_path: Path to local destination for checked out directory, if the local path does not exist, it will create it
        """

        checkout_command = f'svn checkout {repo_url} {local_path}'
        os.makedirs(local_path, exist_ok=True)
        try:
            checkout = subprocess.check_call(checkout_command, shell=True)
            print(f"Checked out repository to: {local_path}")
        except subprocess.CalledProcessError as e:
            print(f"Checkout failed with exit status: {e.returncode}")
            print(f"Command output: {e.output}")
        except FileNotFoundError as e:
            print(f"Command not found: {e}")

    def export(self, repo_url:str, local_path:str) -> None:
        """
        This function will export a single file or entire directory from SVN to a specified local path
        :param repo_url: Path to directory in SVN
        :param local_path: Path to local destination for checked out directory, if the local path does not exist, it will create it
        """

        export_command = f'svn export {repo_url} {local_path}'
        os.makedirs(local_path, exist_ok=True)
        try:
            export = subprocess.check_call(export_command, shell=True)
            print(f'Exported out repository to: {local_path}')
        except subprocess.CalledProcessError as e:
            print(f"Checkout failed with exit status: {e.returncode}")
            print(f"Command output: {e.output}")
        except FileNotFoundError as e:
            print(f"Command not found: {e}")

    def commit(self, local_path:str, message:str) -> None:
        """
        This function will commit a single local file or an entire directory to the SVN location that it was checked out from
        :param local_path: Path to local destination for checked out directory. If a single file is desired, ensure that is included in the local_path
        :param message: The log message for SVN
        """

        commit_command = f'svn commit {local_path} -m "{message}"'
        try:
            commit = subprocess.check_call(commit_command, shell=True)
            
            print(f'Files committed back to SVN: {local_path}')
        except subprocess.CalledProcessError as e:
            print(f"Checkout failed with exit status: {e.returncode}")
            print(f"Command output: {e.output}")
        except FileNotFoundError as e:
            print(f"Command not found: {e}")

    def log(self, repo_path:str, username:str, startdate:str=None, enddate:str=None, createdoc:bool=False, file_path:str=None) -> None:
        """
        This function will either display or create a txt file with a list of all files that were modified by a specified user on specified date(s).

        :param repo_path: Path to repository that the logs will be checked in.
        :param username: Username used inside SVN.
        :param startdate: YYYY-MM-DD. The date that the needed revisions occurred on. Defaulted to today's date.
        :param enddate: YYYY-MM-DD. If the dates searched are a range, this is the ending date of a range. If searching a single date, no value is needed. Defaulted to None.
        Please note that if more than one date is needed, one day past the desired end date is required. Example: Dates needed 2024-09-16 - 2024-09-17. The enddate would be 2024-09-18
        :param createdoc: If True, it will write the results to a txt document in the scripts working directory. Defaulted to False.
        :param file_path: The directory where the txt doc will be created. Defaulted to current working directory.
        """

        logs = []
        count = 0

        if startdate == None:
            startdate = datetime.today().date()
        if enddate == None:
            date_format = "%Y-%m-%d"
            start_date = datetime.strptime(startdate, date_format)
            end_date = start_date + timedelta(days=1)
            enddate = end_date.strftime(date_format)
        
        log_command = f'svn log -r {{{startdate}}}:{{{enddate}}} --search {username} -v {repo_path}'

        log = subprocess.run(log_command, capture_output=True, shell=True, text=True)

        if log.returncode != 0:
            print(f"Error executing: {log.stderr}")
        for line in log.stdout.splitlines():
            if line.startswith('   '):
                filepath = line[4:].strip()
                logs.append(filepath)
            elif username in line and 'Rebase' not in line:
                changeDate = line.strip()
                logs.append(changeDate)
        
        if createdoc:
            if file_path == None:
                file_path = os.getcwd()
            file_path = os.path.join(file_path, 'SVN_logs')
            try:
                while os.path.isfile(file_path):
                    file_path = f'{file_path}_{count}'
                    count += 1
                with open(file_path, 'w') as outputfile:
                    for line in logs:
                        if username in line:
                            outputfile.write(f'{line}\n')
                        else:
                            outputfile.write(f'{line}\n')
            except FileNotFoundError:
                print(f"Invalid file path: {file_path}")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            for line in logs:
                if username in line:
                    print(line)
                else:
                    print(line)
        
        if createdoc:
            if os.path.isfile(file_path):
                print(f'File was created at: {file_path}')
        