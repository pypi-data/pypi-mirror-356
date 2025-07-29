from traceback import print_exc
from copy import deepcopy as copy
from json import dumps as json_dumps
from dacite import from_dict
from httpx import Client
from gitlab_ps_utils.misc_utils import safe_json_response
from gitlab_ps_utils.dict_utils import dig
from gitlab_evaluate import log
from gitlab_evaluate.lib import utils
from gitlab_evaluate.migration_readiness.gitlab.flag_remediation import FlagRemediationMessages
from gitlab_evaluate.lib.api_models.user import User
from gitlab_evaluate.migration_readiness.gitlab import limits
from gitlab_evaluate.migration_readiness.gitlab.queries import *
from gitlab_evaluate.migration_readiness.gitlab import glapi

class EvaluateApi():
    gitlab_api = glapi
    app_api_url = "/application/statistics"
    app_ver_url = "/version"

    supported_package_types = ['generic', 'npm', 'pypi', 'maven', 'helm']

    def __init__(self, ssl_verify=False):
        if ssl_verify:
            self.gitlab_api.client = Client(ssl_verify=ssl_verify)

    # Functions - Return API Data
    # Gets the X-Total from the statistics page with the -I on a curl
    def check_x_total_value_update_dict(self, check_func, p, host, token, api=None, value_column_name="DEFAULT_VALUE", over_column_name="DEFAULT_COLUMN_NAME", results={}):
        flag = False
        full_path = p.get('fullPath')
        pid = p.get('id')
        if api:
            count = self.get_total_count(
                host, token, api, full_path, value_column_name, pid)
        else:
            count = self.get_result_value(results, value_column_name)
        log.info(f"{full_path} - {value_column_name} retrieved count: {count}")
        if count is not None:
            num_over = check_func(count)
            if num_over:
                flag = True
            results[value_column_name] = count
            results[over_column_name] = num_over
        else:
            log.debug(
                f"No '{value_column_name}' retrieved for project '{full_path}' (ID: {pid})")
        return flag

    def get_total_count(self, host, token, api, full_path, entity, project_id=None):
        formatted_entity = utils.to_camel_case(entity)
        query = {
            "query": """
                query {
                    project(fullPath: "%s") {
                        name,
                        %s {
                            count
                        }
                    }
                }
            """ % (full_path, formatted_entity)
        }

        if gql_resp := safe_json_response(self.gitlab_api.generate_post_request(host, token, None, json_dumps(query), graphql_query=True)):
            return dig(gql_resp, 'data', 'project', formatted_entity, 'count')

        log.debug(
            f"Could not retrieve total '{api}' count via GraphQL, using API instead")
        return self.gitlab_api.get_count(host, token, api)

    def get_all_projects_by_graphql(self, source, token, full_path=None):
        after = ""
        levels = []
        try:
            while True:
                if full_path:
                    query = generate_group_project_query(full_path, after)
                    levels = ['data', 'group', 'projects', 'nodes']
                else:
                    query = generate_all_projects_query(after)
                    levels = ['data', 'projects', 'nodes']
                if resp := safe_json_response(
                        self.gitlab_api.generate_post_request(source, token, None, data=json_dumps(query), graphql_query=True)):
                    yield from dig(resp, *levels, default=[])
                    page_info = dig(resp, *levels[:-1], 'pageInfo', default={})
                    if cursor := page_info.get('endCursor'):
                        after = cursor
                    if not page_info.get('hasNextPage', False):
                        break
        except Exception as e:
            log.error(f"Failed to get all projects: {e}\n{print_exc()}")

    def genericGet(self, host, token, api):
        return safe_json_response(self.gitlab_api.generate_get_request(host=host, token=token, api=api))

    def getApplicationInfo(self, host, token):
        return self.genericGet(host, token, self.app_api_url)

    def getVersion(self, host, token):
        return self.genericGet(host, token, self.app_ver_url)

    def getArchivedProjectCount(self, host, token):
        if resp := self.gitlab_api.generate_get_request(host=host, token=token, api='projects?archived=True'):
            result = resp.headers.get('X-Total')
            return result

    def get_total_project_count(self, host, token, group_id):
        if resp := self.gitlab_api.generate_get_request(host=host, token=token, api=f'/groups/{group_id}/projects'):
            result = resp.headers.get('X-Total')
            return result

    def build_initial_results(self, project):
        return {
            'Project': project.get('name'),
            'ID': project.get('id'),
            'archived': project.get('archived'),
            'last_activity_at': project.get('lastActivityAt'),
            'URL': project.get('webUrl'),
            'namespace': dig(project, 'namespace', 'fullPath'),
        }

    def get_all_project_data(self, host, token, p):
        results = {}
        flags = []
        messages = ''
        if isinstance(p, dict) and p:
            results = self.build_initial_results(p)
            pid = int(p.get('id', '').split('/')[-1])
            p['id'] = pid

            try:
                # Get project REST stats
                self.get_project_rest_stats(host, token, p, results)
                messages = FlagRemediationMessages(p.get('name'))

                if stats := p.get('statistics'):
                    results['Packages'] = stats.get(
                        "packagesSize", 0)
                    results['Containers'] = stats.get(
                        "containerRegistrySize", 0)
                    self.get_extra_stats(stats, results)

                # Get number of pipelines per project
                pipeline_endpoint = f"projects/{pid}/pipelines"
                flags.append(self.handle_check(
                    messages,
                    self.check_x_total_value_update_dict(
                        utils.check_num_pl, p, host, token, pipeline_endpoint, "Pipelines", "Pipelines_over", results),
                    "pipelines",
                    limits.PIPELINES_COUNT))

                # Get number of issues per project
                issues_endpoint = f"projects/{pid}/issues"
                flags.append(self.handle_check(
                    messages,
                    self.check_x_total_value_update_dict(
                        utils.check_num_issues, p, host, token, issues_endpoint, "Issues", "Issues_over", results),
                    "issues",
                    limits.ISSUES_COUNT))

                # Get number of branches per project
                branches_endpoint = f"projects/{pid}/repository/branches"
                flags.append(self.handle_check(
                    messages,
                    self.check_x_total_value_update_dict(
                        utils.check_num_br, p, host, token, branches_endpoint, "Branches", "Branches_over", results),
                    "branches",
                    limits.BRANCHES_COUNT))

                # Get number of commits per project
                flags.append(self.handle_check(
                    messages,
                    self.check_x_total_value_update_dict(
                        utils.check_num_commits, p, host, token, None, "Commits", "Commits_over", results),
                    "commits",
                    limits.COMMITS_COUNT))

                # Get number of merge requests per project
                mrs_endpoint = f"projects/{pid}/merge_requests"
                flags.append(self.handle_check(
                    messages,
                    self.check_x_total_value_update_dict(
                        utils.check_num_mr, p, host, token, mrs_endpoint, "Merge Requests", "Merge Requests_over", results),
                    "merge_requests",
                    limits.MERGE_REQUESTS_COUNT))

                # Get number of tags per project
                tags_endpoint = f"projects/{pid}/repository/tags"
                flags.append(self.handle_check(
                    messages,
                    self.check_x_total_value_update_dict(
                        utils.check_num_tags, p, host, token, tags_endpoint, "Tags", "Tags_over", results),
                    "tags",
                    limits.TAGS_COUNT))

                # Get list of package types
                self.handle_packages(p, pid,
                                     messages, flags, results)

                # Check repository size
                flags.append(self.handle_check(
                    messages,
                    self.check_x_total_value_update_dict(
                        utils.check_repository_size, p, host, token, None, "Repository", "repository_size_over", results),
                    "repository_size",
                    limits.REPOSITORY_SIZE))

                # Check storage size
                flags.append(self.handle_check(
                    messages,
                    self.check_x_total_value_update_dict(
                        utils.check_storage_size, p, host, token, None, "Storage", "storage_size_over", results),
                    "storage_size",
                    limits.STORAGE_SIZE))

                # Get total packages size
                flags.append(self.handle_check(
                    messages,
                    self.check_x_total_value_update_dict(
                        utils.check_packages_size, p, host, token, None, "Packages", "packages_size_over", results),
                    "packages_size",
                    limits.PACKAGES_SIZE))

                # Get total containers size
                flags.append(self.handle_check(
                    messages,
                    self.check_x_total_value_update_dict(
                        utils.check_registry_size, p, host, token, None, "Containers", "containers_size_over", results),
                    "containers_size",
                    limits.CONTAINERS_SIZE))
            except Exception:
                log.error(
                    f"Failed to get all project {pid} data: {print_exc()}")
            finally:
                return flags, messages, results
        else:
            return flags, messages, results

    def get_project_rest_stats(self, host, token, project, my_dict):
        project_path = project.get('fullPath')
        pid = project.get('id')
        try:
            if result := safe_json_response(self.gitlab_api.generate_get_request(host=host, api="", token=token, url=f"{host}/api/v4/projects/{pid}")):
                if kind := result.get("namespace"):
                    my_dict.update({"kind": kind.get("kind")})

                # Get Mirrors
                my_dict['mirror'] = result.get('mirror', False)
            else:
                log.warning(
                    f"Could not retrieve project '{project_path}' (ID: {pid}) REST stats: {result}")
        except Exception:
            log.error(
                f"Failed to retrieve project '{project_path}' (ID: {pid}) REST stats: {print_exc()}")

    # Get extra project stats
    def get_extra_stats(self, stats, results):
        export_total = 0
        for k, v in stats.items():
            updated_dict_entry = {
                k: v, k + "_over": utils.check_size(k, v)}
            results.update(updated_dict_entry)

            # If 'k' is an item that would be part of the export, add to running total
            if k in [
                "repositorySize",
                "wikiSize",
                "lfsObjectsSize",
                "snippetsSize",
                "uploadsSize"
            ]:
                export_total += int(v)

        # Write running total to my_dict
        export_total_key = "Estimated Export Size"
        results.update({f"{export_total_key}": export_total})

        # 5Gb
        results.update({f"{export_total_key} Over": utils.check_size(
            export_total_key, export_total)})

        # 10Gb
        results.update({f"{export_total_key} S3 Over": utils.check_size(
            f"{export_total_key} S3", export_total)})

    def get_token_owner(self, host, token):
        return self.genericGet(host, token, "user")

    def handle_check(self, messages, flagged_asset, asset_type, flag_condition):
        if flagged_asset == True:
            messages.add_flag_message(asset_type, flag_condition)
        return flagged_asset

    def get_user_data(self, u):
        return from_dict(data_class=User, data=u)

    def get_result_value(self, results, value_column_name):
        key_mapping = {
            'Storage': 'storageSize',
            'Repository': 'repositorySize',
            'Packages': 'packagesSize',
            'Commits': 'commitCount',
            'Containers': 'containerRegistrySize'
        }

        # Get the actual key to use in results
        actual_key = key_mapping.get(value_column_name, value_column_name)

        # Return the value from results or 0 if not found
        return results.get(actual_key, 0)

    def handle_packages(self, project, pid, messages, flags, results):
        # Extract packages from the GraphQL response:
        packages_data = project.get('packages', {}).get('nodes', [])
        if not packages_data:
            # No packages found, so report "N/A"
            results['Package Types In Use'] = "N/A"
            return

        # If packages are present, collect their types
        packages_in_use = set()
        for package in packages_data:
            pkg_type = package.get("packageType", "")
            if pkg_type:
                packages_in_use.add(pkg_type)
            else:
                log.error(
                    f"Project {pid} package missing 'packageType' field: {package}")

            results['Package Types In Use'] = ", ".join(
                packages_in_use) if packages_in_use else "N/A"
            # If a package type is found that doesn't match the constant in the class, raise a flag
            any_unsupported_packages = any(
                p not in self.supported_package_types for p in packages_in_use)
            if packages_in_use and any_unsupported_packages:
                flags.append(True)
                self.handle_check(messages, True, "packages",
                                  copy(results['Package Types In Use']))
