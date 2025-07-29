from logging import DEBUG

import click
import time

from gitlab_evaluate import log
from gitlab_evaluate.migration_readiness.gitlab.report_generator import ReportGenerator as GLReportGenerator
from gitlab_evaluate.migration_readiness.gitlab import evaluate as evaluate_api
from gitlab_evaluate.migration_readiness.jenkins.report_generator import ReportGenerator as JKReportGenerator
from gitlab_evaluate.migration_readiness.bitbucket.report_generator import BitbucketReportGenerator
from gitlab_evaluate.migration_readiness.ado.report_generator import AdoReportGenerator
from gitlab_evaluate.migration_readiness.github_enterprise.report_generator import GithubReportGenerator

@click.command
@click.option("-s", "--source", help="Source URL: REQ'd")
@click.option("-t", "--token", help="Personal Access Token: REQ'd")
@click.option("-o", "--output", is_flag=True, help="Output Per Project Stats to screen")
@click.option("-i", "--insecure", is_flag=True, help="Set to ignore SSL warnings.")
@click.option("-g", "--group", help="Group ID. Evaluate all group projects (including sub-groups)")
@click.option("-f", "--filename", help="XLSX Output File Name. If not set, will default to 'evaluate_output.xlsx'")
@click.option("-p", "--processes", help="Number of processes. Defaults to number of CPU cores")
@click.option("-v", "--verbose", is_flag=True, help="Set logging level to Debug and output everything to the screen and log file")
def evaluate_gitlab(source, token, output, insecure, group, filename, processes, verbose):
    if None not in (token, source):
        if verbose:
            log.setLevel(DEBUG)
        if insecure:
            evaluateApi = evaluate_api.EvaluateApi(ssl_verify=False)
        else:
            evaluateApi = evaluate_api.EvaluateApi()

        rg = GLReportGenerator(source, token, filename=filename,
                               output_to_screen=output, evaluate_api=evaluateApi, processes=processes)
        rg.handle_getting_data(group)
        if rg.using_admin_token:
            log.info("GitLab instance stats and project metadata retrieval")
            rg.get_app_stats(source, token, group)
            log.info("GitLab users metadata retrieval")
            rg.handle_getting_user_data(group)
        else:
            log.info("Using non-admin token. Skipping user retrieval")
        log.info(f"Data retrieval complete. Writing content to file")
        rg.write_workbook()


@click.command
@click.option("-s", "--source", help="Source URL: REQ'd")
@click.option("-u", "--user", help="Username associated with the Jenkins API token: REQ'd")
@click.option("-t", "--token", help="Jenkins API Token: REQ'd")
@click.option("-p", "--processes", help="Number of processes. Defaults to number of CPU cores")
@click.option("-i", "--insecure", is_flag=True, help="Set to ignore SSL warnings.")
def evaluate_jenkins(source, user, token, processes, insecure):
    print("NOTE: Jenkins Evaluation is in a BETA state")
    print(f"Connecting to Jenkins instance at {source}")
    if insecure:
        r = JKReportGenerator(
            source, user, token, filename='evaluate_jenkins', processes=processes, ssl_verify=False)
    else:
        r = JKReportGenerator(source, user, token,
                              filename='evaluate_jenkins', processes=processes)
    print("Retrieving list of Jenkins plugins")
    r.get_plugins()
    print("Retrieving list of Jenkins jobs and performing analysis")
    r.get_raw_data()
    print("Retrieving Jenkins instance statistics")
    stats = r.get_app_stats()
    print("Finalizing report")
    r.get_app_stat_extras(stats)
    r.write_workbook()
    print("Report generated. Please review evaluate_jenkins.xlsx")
    r.jenkins_client.drop_tables()


@click.command
@click.option('-s', '--source', required=True, help='Source URL')
@click.option('-t', '--token', required=True, help='Personal Access Token')
def evaluate_bitbucket(source, token):
    print("NOTE: BitBucket Evaluation is in a BETA state")
    print(f"Connecting to Bitbucket instance at {source}")

    # Record the start time
    start_time = time.time()

    rg = BitbucketReportGenerator(source, token, filename='evaluate_bitbucket')
    print("Retrieving Bitbucket instance statistics")
    rg.get_app_stats()
    rg.handle_getting_data()
    if rg.using_admin_token:
        print("Project data retrieval complete. Moving on to User metadata retrieval")
        rg.handle_getting_user_data()
    else:
        print("Non-admin token used. Skipping user retrieval")
    rg.write_workbook()

    # Record the end time
    end_time = time.time()

    # Calculate the duration in minutes
    duration_minutes = (end_time - start_time) / 60

    print(f"Report generated. Please review evaluate_bitbucket.xlsx")
    print(f"Process completed in {duration_minutes:.2f} minutes.")


@click.command
@click.option('-s', '--source', required=True, help='Source URL')
@click.option('-t', '--token', required=True, help='Personal Access Token')
@click.option("-p", "--processes", help="Number of processes. Defaults to number of CPU cores")
@click.option('--skip-details', is_flag=True, help='Skips details')
# https://learn.microsoft.com/en-us/rest/api/azure/devops/?view=azure-devops-rest-7.2&viewFallbackFrom=azure-devops-rest-4.1#api-and-tfs-version-mapping
@click.option('--api-version', default='7.2-preview', help='API version to use (default: 7.2-preview)')

def evaluate_ado(source, token, skip_details, processes, api_version):
    print("NOTE: Azure DevOps Evaluation is in a BETA state")
    print(f"Connecting to Azure DevOps instance at {source} using API version {api_version}")

    # Record the start time
    start_time = time.time()

    rg = AdoReportGenerator(source, token, filename='evaluate_ado', processes=processes, api_version=api_version)
    print("Retrieving Azure DevOps projects and repository data ... ")
    rg.handle_getting_data(skip_details)
    if "dev.azure.com" in source:
        print("Retrieving Azure DevOps instance users data ... ")
        rg.handle_getting_user_data()
    else:
        print("TFS and Azure DevOps Server do not support user retrieval via API. Skipping user retrieval data ...")
    print("Retrieving Azure DevOps projects pipelines data ... ")
    rg.handle_getting_agent_pool_data()
    print("Retrieving Azure DevOps project variable groups data ... ")
    rg.handle_getting_variable_groups_data()

    print("Retrieving Azure DevOps instance statistics ... ")
    rg.get_app_stats()

    rg.write_workbook()

    # Record the end time
    end_time = time.time()

    # Calculate the duration in minutes
    duration_minutes = (end_time - start_time) / 60

    print("Report generated. Please review evaluate_ado.xlsx")
    print(f"Process completed in {duration_minutes:.2f} minutes.")

@click.command
@click.option('-s', '--source', required=True, help='Source URL')
@click.option('-t', '--token', required=True, help='Personal Access Token')
def evaluate_github_enterprise(source, token):
    print("NOTE: Github Evaluation is in a BETA state")
    print(f"Connecting to Github instance at {source}")

    # Record the start time
    start_time = time.time()

    rg = GithubReportGenerator(source, token, filename='evaluate_github_enterprise')
    print("Retrieving Github instance statistics")
    rg.get_app_stats()
    rg.handle_getting_data()
    if rg.using_admin_token:
        print("Project data retrieval complete. Moving on to User metadata retrieval")
        rg.handle_getting_user_data()
    else:
        print("Non-admin token used. Skipping user retrieval")
    rg.write_workbook()

    # Record the end time
    end_time = time.time()

    # Calculate the duration in minutes
    duration_minutes = (end_time - start_time) / 60

    print(f"Report generated. Please review evaluate_github_enterprise.xlsx")
    print(f"Process completed in {duration_minutes:.2f} minutes.")
