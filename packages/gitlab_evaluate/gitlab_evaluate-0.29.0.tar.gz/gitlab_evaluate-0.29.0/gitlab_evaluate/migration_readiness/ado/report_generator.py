import re
from sys import exit as sys_exit
import xlsxwriter
from dateutil import parser

from gitlab_evaluate.lib import utils
from gitlab_evaluate.migration_readiness.ado.evaluate import AdoEvaluateClient
from gitlab_ps_utils.processes import MultiProcessing


class AdoReportGenerator:

    def __init__(self, host, token, filename=None, output_to_screen=False, processes=None, api_version=None):

        self.total_repositories = 0
        self.total_disabled_repositories = 0
        self.total_uninitialized_repositories = 0
        self.total_tfvc_repositories = 0
        self.total_projects = 0
        self.total_users = 0
        self.total_agent_pools = 0
        self.total_variables = 0
        self.total_wikis = 0
        self.host = host
        self.ado_client = AdoEvaluateClient(host, token, api_version=api_version)
        self.validate_token()
        if filename:
            self.workbook = xlsxwriter.Workbook(f'{filename}.xlsx')
        else:
            self.workbook = xlsxwriter.Workbook('ado_evaluate_report')
        self.app_stats = self.workbook.add_worksheet('Organization Insights')
        self.align_left = self.workbook.add_format({'align': 'left'})
        self.header_format = self.workbook.add_format({'bg_color': 'black', 'font_color': 'white', 'bold': True, 'font_size': 10})
        self.users = self.workbook.add_worksheet('Users')
        self.agent_pools = self.workbook.add_worksheet('Agent Pools')
        self.variable_groups = self.workbook.add_worksheet('Variable Groups')
        self.projects = self.workbook.add_worksheet('Raw Project Data')
        self.raw_output = self.workbook.add_worksheet('Raw Repository Data')
        self.output_to_screen = output_to_screen
        self.processes = processes
        self.columns = [
            'Project Name',
            'Project ID',
            'Repository Name',
            'Repository ID',
            'Default Branch',
            'Git URL',
            'Last activity',
            'Branches',
            'Commits',
            'Pull Requests',
            'Repository Size in MB',
            'Repository Disabled'
        ]
        self.user_headers = [
            'Object ID',
            'Descriptor',
            'Display Name',
            'Principal Name',
            'Email'
        ]
        self.agent_pool_headers = [
            'Pool ID',
            'Name',
            'Is Hosted',
            'Pool Size',
            'Legacy',
            'Owner'
        ]
        self.variables_groups_headers = [
            'Project ID',
            'Variable Group ID',
            'Variable Group Name',
            'Variable Group Description',
            'Type',
            'Variable Name',
            'Enabled',
            'Is Secret',
            'Created By',
            'Created on',
            'Modified on'
        ]
        self.project_headers = [
            'Project ID',
            'URL',
            'Name',
            'Total Repositories',
            'Total Build Definitions',
            'Total Release Definitions',
            'Total Work Items',
            'Administrators',
            'TFVC',
            'Wiki'
        ]
        utils.write_headers(0, self.raw_output, self.columns, self.header_format)
        utils.write_headers(0, self.users, self.user_headers, self.header_format)
        utils.write_headers(0, self.agent_pools, self.agent_pool_headers, self.header_format)
        utils.write_headers(0, self.variable_groups, self.variables_groups_headers, self.header_format)
        utils.write_headers(0, self.projects, self.project_headers, self.header_format)
        self.multi = MultiProcessing()

    def write_workbook(self):
        self.app_stats.autofit()
        self.raw_output.autofit()
        self.users.autofit()
        self.projects.autofit()
        self.workbook.close()

    def get_app_stats(self):
        '''
            Gets Azure DevOps instance stats
        '''
        report_stats = [
            ('Organization URL', self.host),
            ('Customer', '<CUSTOMERNAME>'),
            ('Date Run', utils.get_date_run()),
            ('Source', self.scrape_source_details()),
            ('Total Projects', self.total_projects),
            ('Total Repositories', self.total_repositories),
            ('Total Disabled Repositories', self.total_disabled_repositories),
            ('Total Uninitialized Repositories', self.total_uninitialized_repositories),
            ('Total TFVC Repositories', self.total_tfvc_repositories),
            ('Total Users', self.total_users),
            ('Total Agent Pools', self.total_agent_pools),
            ('Total Variables', self.total_variables),
            ('Total wikis', self.total_wikis),
        ]
        for row, stat in enumerate(report_stats):
            self.app_stats.write(row, 0, stat[0])
            self.app_stats.write(row, 1, stat[1])
        return report_stats

    def handle_getting_data(self, skip_details=False):

        params = {
            "$top": "100"
        }

        print("Fetching projects data...")
        while True:
            response = self.ado_client.retry_request(self.ado_client.get_projects, params)
            projects = response.json()
            self.total_projects += len(projects.get('value'))
            print(f"Retrieved {self.total_projects} projects so far...")
            
            for project in projects['value']:
                try:
                    properties_response = self.ado_client.get_project_properties(project['id'])
                    properties = properties_response.json().get("value", [])
                    for prop in properties:
                        if prop.get("name") == "System.SourceControlTfvcEnabled" and prop.get("value") == "True":
                            self.total_tfvc_repositories += 1
                            break
                except Exception as e:
                    print(f"Failed to get project properties for TFVC check: {e}")
                
                try:
                    wikis_response = self.ado_client.get_wikis(project['id'])
                    if wikis_response and wikis_response.status_code == 200:
                        wiki_count = len(wikis_response.json().get('value', []))
                        self.total_wikis += wiki_count
                    else:
                        print(f"Failed to get wiki count for project {project['name']}")
                except Exception as e:
                    print(f"Failed to get wikis for project {project['name']}: {e}")

            for result in list(self.multi.start_multi_process(self.ado_client.handle_getting_project_data, projects['value'], processes=self.processes)):
                utils.append_to_workbook(self.projects, [result], self.project_headers)

            for repo_list in list(self.multi.start_multi_process(self.ado_client.handle_getting_repo_data, projects['value'], processes=self.processes)):
                for repo in repo_list:
                    self.write_output_to_files(repo, skip_details)
                    if repo.get('isDisabled') is True:
                        self.total_disabled_repositories += 1
                    else:
                        self.total_repositories += 1
                    if repo.get('size') is None or repo.get('size') == 0:
                        self.total_uninitialized_repositories += 1

            # Check if there's a next page
            if not any(key.lower() == "x-ms-continuationtoken" for key in response.headers):
                break  # No more pages
            # There is page, so get the continuation token for the next page
            params["continuationToken"] = response.headers["X-MS-ContinuationToken"]

    def handle_getting_project_data(self, project):
        params = {}
        print("Fetching project data...")
        project_id = project["id"]
        project_name = project["name"]
        if "dev.azure.com" in self.host:
            print(f"Retriving project administrators in {project_name}...")
            project_admins = self.ado_client.get_project_administrators(project_id)
            if project_admins and isinstance(project_admins, list):
                project_admins_str = ', '.join(project_admins)
            else:
                project_admins_str = str(project_admins) if project_admins is not None else "No administrators found"
        else:
            print("Project administrators retrieval is not supported for this URL. Skipping ... ")
            project_admins_str = "N/A"

        print(f"Retriving total repositories, yaml definitions, classic releases and work items in {project_name}...")

        get_repos_response = self.ado_client.get_repos(project_id, params=params)
        try:
            total_repos = len(get_repos_response.json().get("value", []))
        except get_repos_response.exceptions.JSONDecodeError:
            print(f"Failed to decode JSON for repositories. Raw response: {get_repos_response.text}")
            total_repos = 0

        get_build_definitions_response = self.ado_client.get_build_definitions(project_id, params=params)
        try:
            total_build_definitions = len(get_build_definitions_response.json().get("value", []))
        except get_build_definitions_response.exceptions.JSONDecodeError:
            print(f"Failed to decode JSON for repositories. Raw response: {get_build_definitions_response.text}")
            total_build_definitions = 0

        get_release_definitions_response = self.ado_client.get_release_definitions(project_id, params=params)
        try:
            total_release_definitions = len(get_release_definitions_response.json().get("value", []))
        except get_release_definitions_response.exceptions.JSONDecodeError:
            print(f"Failed to decode JSON for repositories. Raw response: {get_release_definitions_response.text}")
            total_release_definitions = 0

        get_work_items_response = self.ado_client.get_work_items(project_id, project_name, params=params)
        try:
            total_work_items = len(get_work_items_response.json().get("workItems", []))
        except get_work_items_response.exceptions.JSONDecodeError:
            print(f"Failed to decode JSON for work items. Raw response: {get_work_items_response.text}")
            total_work_items = 0

        project_data = {
            'Project ID': project.get('id', 'N/A'),
            'URL': project.get('url', 'N/A'),
            'Name': project.get('name', 'N/A'),
            'Total Repositories': total_repos,
            'Total Build Definitions': total_build_definitions,
            'Total Release Definitions': total_release_definitions,
            'Total Work Items': total_work_items,
            'Administrators': project_admins_str
        }

        return project_data

    def handle_getting_user_data(self):
        params = {
            "subjectTypes": "aad,msa"
        }
        print("Fetching user data...")
        while True:
            response = self.ado_client.retry_request(self.ado_client.get_users, params)
            users = response.json()
            for user in users["value"]:
                user_data = {
                    'Object ID': user.get('originId', 'N/A'),
                    'Descriptor': user.get('descriptor', 'N/A'),
                    'Display Name': user.get('displayName', 'N/A'),
                    'Principal Name': user.get('principalName', 'N/A'),
                    'Email': user.get('mailAddress', 'N/A')
                }
                utils.append_to_workbook(self.users, [user_data], self.user_headers)
            self.total_users += len(users['value'] if 'value' in users else [])
            print(f"Retrieved {self.total_users} users so far...")

            # Check if there's a next page
            if not any(key.lower() == "x-ms-continuationtoken" for key in response.headers):
                print(f"Retrieved a total of {self.total_users} users.")
                break  # No more pages
            # There is page, so get the continuation token for the next page
            params["continuationToken"] = response.headers["X-MS-ContinuationToken"]
            # print(response.request.url)

    def handle_getting_agent_pool_data(self):
        params = {
            "$top": "100"
        }
        print("Fetching agent pool data...")
        while True:
            response = self.ado_client.retry_request(self.ado_client.get_agent_pools, params)
            agent_pools = response.json()
            for pool in agent_pools["value"]:
                agent_pool_data = {
                    'Pool ID': pool.get('id', 'N/A'),
                    'Name': pool.get('name', 'N/A'),
                    'Is Hosted': pool.get('isHosted', 'N/A'),
                    'Pool Size': pool.get('size', 'N/A'),
                    'Legacy': pool.get('isLegacy', 'N/A'),
                    'Owner': pool.get('owner', {}).get('displayName', 'N/A')
                }
                utils.append_to_workbook(self.agent_pools, [agent_pool_data], self.agent_pool_headers)
            self.total_agent_pools += len(agent_pools['value'])
            print(f"Retrieved {len(agent_pools['value'])} agent pools so far...")

            # Check if there's a next page
            if not any(key.lower() == "x-ms-continuationtoken" for key in response.headers):
                break  # No more pages
            # There is page, so get the continuation token for the next page
            params["continuationToken"] = response.headers["X-MS-ContinuationToken"]

    def handle_getting_variable_groups_data(self):
        for project in self.ado_client.get_projects(params={}).json()['value']:
            project_id = project.get('id')
            variable_groups = self.ado_client.get_variable_groups(project_id, params={}).json()
            for group in variable_groups["value"]:
                print(f"Fetching variable groups for project {project['name']}...")
                variables = group.get('variables', {})
                for variable_name, variable_info in variables.items():
                    variable_data = {
                        'Project ID': project_id,
                        'Variable Group ID': group['id'],
                        'Variable Group Name': group['name'],
                        'Variable Group Description': group.get('description', 'N/A'),
                        'Type': group.get('type'),
                        'Variable Name': variable_name,
                        'Enabled': variable_info.get('enabled'),
                        'Is Secret': variable_info.get('isSecret'),
                        'Created By': group.get('createdBy', {}).get('uniqueName', 'N/A'),
                        'Created on': self.convert_utc_to_local(group.get('createdOn', 'N/A')),
                        'Modified on': self.convert_utc_to_local(group.get('modifiedOn', 'N/A'))
                    }
                    utils.append_to_workbook(self.variable_groups, [variable_data], self.variables_groups_headers)
                self.total_variables += len(variables)

    def write_output_to_files(self, repo, skip_details=False):
        project_id = repo['project']['id']
        repository_id = repo['id']
        last_activity = "N/A"
        default_branch = repo['defaultBranch'] if 'defaultBranch' in repo else 'N/A'

        if repo.get('isDisabled', False) is False:

            if skip_details is False:
                branches = []
                params = {'$top': 1000}
                print(f"Fetching branches for repo {repository_id}...")
                while True:
                    branches_response = self.ado_client.retry_request(self.ado_client.get_branches, params, project_id, repository_id)
                    if branches_response:
                        branches.extend(branches_response.json()['value'])
                        print(f"Retrieved {len(branches)} branches so far...")

                        # Check if there's a next page
                        if not any(key.lower() == "x-ms-continuationtoken" for key in branches_response.headers):
                            break  # No more pages
                        # There is page, so get the continuation token for the next page
                        params["continuationToken"] = branches_response.headers["X-MS-ContinuationToken"]
                    else:
                        break
            else:
                print("Skipping branch details retrieval since `--skip-details` flag was passed")
                branches = "N/A"

            if skip_details is False:
                pull_requests = []
                print(f"Fetching pull requests for repo {repository_id}...")
                while True:
                    prs_response = self.ado_client.retry_request(self.ado_client.get_prs, params, project_id, repository_id)
                    if prs_response:
                        if len(prs_response.json()['value']) > 0:
                            pull_requests.extend(prs_response.json()['value'])
                            print(f"Retrieved {len(pull_requests)} pull requests so far...")
                            if "dev.azure.com" in self.host:
                                # Check if there's a next page
                                if not any(key.lower() == "x-ms-continuationtoken" for key in prs_response.headers):
                                    break  # No more pages
                                # There is page, so get the continuation token for the next page
                                params["continuationToken"] = prs_response.headers["X-MS-ContinuationToken"]
                            else:
                                params['$skip'] = len(pull_requests)

                        else:
                            break
                    else:
                        break
            else:
                print("Skipping PR details retrieval since `--skip-details` flag was passed")
                pull_requests = "N/A"

            if skip_details is False:
                commits = []
                print(f"Fetching commits for repo {repository_id}...")
                while True:
                    commits_response = self.ado_client.retry_request(self.ado_client.get_commits, params, project_id, repository_id)
                    if commits_response:
                        if len(commits_response.json()['value']) > 0:
                            commits.extend(commits_response.json()['value'])
                            print(f"Retrieved {len(commits)} commits so far...")
                            params['$skip'] = len(commits)
                        else:
                            break
                last_activity = commits[0]['committer']['date'] if commits else 'N/A'
                commit_count = len(commits)
            else:
                print("Skipping commits details retrieval since `--skip-details` flag was passed")
                commit_count = "N/A"

        repo_size_mb = "N/A"
        if repo.get('size') is not None and repo.get("isDisabled", False) is False:
            repo_size_mb = round(repo.get('size') / 1024 / 1024, 2)

        repo_data = {
            'Project Name': repo.get('project', {}).get('name', 'N/A'),
            'Project ID': repo.get('project', {}).get('id', 'N/A'),
            'Repository Name': repo.get('name', 'N/A'),
            'Repository ID': repo.get('id', 'N/A'),
            'Default Branch': default_branch,
            'Git URL': repo.get('remoteUrl', 'N/A'),
            'Last activity': last_activity,
            'Branches': len(branches) if repo.get("isDisabled", False) is False and skip_details is False else "N/A",
            'Commits': commit_count if repo.get("isDisabled", False) is False and skip_details is False else "N/A",
            'Pull Requests': len(pull_requests) if repo.get("isDisabled", False) is False and skip_details is False else "N/A",
            'Repository Size in MB': repo_size_mb,
            'Repository Disabled': repo.get('isDisabled', False)
        }
        utils.append_to_workbook(self.raw_output, [repo_data], self.columns)
        if self.output_to_screen:
            print(f"Repository Data: {repo_data}")

    def validate_token(self):
        params = {}
        response = self.ado_client.test_connection(params=params)
        if response.status_code != 200:
            print("Invalid URL or PAT. Exiting...")
            print(f"Response: {response.url} - {response.text}")
            sys_exit(1)

    def convert_utc_to_local(self, date_str, fmt="%Y-%m-%d %H:%M:%S"):
        if not date_str or date_str == "N/A":
            return "N/A"
        try:
            utc_dt = parser.isoparse(date_str)
            local_dt = utc_dt.astimezone()
            return local_dt.strftime(fmt)
        except Exception:
            return date_str

    def scrape_source_details(self):
        request = self.ado_client.get_source_details()
        if request.status_code == 200:
            source = self.extract_ado_version(request.text)
        else:
            source = "Unknown server version"
        return source

    def extract_ado_version(self, text):
        match = re.search(r'"serviceVersion"\s*:\s*"([^"]+)"', text)
        if match:
            return match.group(1)
        else:
            if "tfs" in self.host:
                return "Team Foundation Server"
            else:
                return "Unknown server version"