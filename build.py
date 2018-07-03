#!/usr/bin/env python

import os
import sys
import time
import boto3
from argparse import ArgumentParser

ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_KEY = os.environ['SECRET_KEY']
REGION = os.environ['REGION']


def argument_parser():
    parser = ArgumentParser(description='AWS CodeBuild Manager - starts project builds and captures the output')
    parser.add_argument('-p', '--project', help='the name of the CodeBuild project', required=True)
    parser.add_argument('-i', '--buildid', help='unique id / build reference', required=True)
    parser.add_argument('-b', '--bucket', help='S3 bucket for CodeBuild artifacts', required=True)
    return vars(parser.parse_args())


class CodeBuildManager:
    def __init__(self):
        self.client = boto3.client('codebuild',
                                   aws_access_key_id=ACCESS_KEY,
                                   aws_secret_access_key=SECRET_KEY,
                                   region_name=REGION)

    def get_projects(self):
        response = self.client.list_projects(sortBy='NAME', sortOrder='DESCENDING')
        return response

    def get_project_builds(self, project_name):
        response = self.client.list_builds_for_project(projectName=project_name, sortOrder='DESCENDING')
        return response

    def get_build_details(self, build_id):
        response = self.client.batch_get_builds(ids=[build_id])
        return response

    def start_build(self, project_name, s3_source_location):
        response = self.client.start_build(projectName=project_name,
                                           sourceLocationOverride=s3_source_location)
        return response


class CloudWatchLogsManager:
    def __init__(self):
        self.client = boto3.client('logs',
                                   aws_access_key_id=ACCESS_KEY,
                                   aws_secret_access_key=SECRET_KEY,
                                   region_name=REGION)

    def get_event_logs(self, log_group_name, log_stream_name):
        response = self.client.get_log_events(logGroupName=log_group_name,
                                              logStreamName=log_stream_name,
                                              startFromHead=True)
        return response


class S3BucketManager:
    def __init__(self):
        self.client = boto3.client('s3',
                                   aws_access_key_id=ACCESS_KEY,
                                   aws_secret_access_key=SECRET_KEY,
                                   region_name=REGION)

    def upload_file(self, bucket, filename, key):
        response = self.client.upload_file(Bucket=bucket,
                                           Filename=filename,
                                           Key=key)
        return response


class Build:
    '''
    Example: Capsule-123
    arn:aws:s3:::assetto/Capsule-123.zip
    '''
    def __init__(self, project_name, build_id, bucket):
        self.project_name = project_name
        self.build_id = build_id
        self.bucket = bucket
        self.artifact_location = 'arn:aws:s3:::%s/%s-%s.zip' % (self.bucket, self.project_name, self.build_id)
        self.cbm = CodeBuildManager()
        self.cwlm = CloudWatchLogsManager()
        self.s3bm = S3BucketManager()
        self.codebuild_build_id = None
        self.codebuild_build_details = None
        self.codebuild_build_status = None
        self.log_group_name = None
        self.log_stream_name = None

    def upload_artifacts(self):
        artifact_zipfile = self.project_name + '-' + self.build_id + '.zip'
        if not os.path.isfile(artifact_zipfile):
            print('codebuild artifact zipfile not found: %s' % artifact_zipfile)
            sys.exit(1)
        else:
            self.s3bm.upload_file(bucket=self.bucket, filename=artifact_zipfile, key=artifact_zipfile)

    def create(self):
        project_list = self.cbm.get_projects()['projects']
        if self.project_name not in project_list:
            print('no such project: %s' % self.project_name)
            sys.exit(1)

        # TODO: check the s3 build source exists

        response = self.cbm.start_build(project_name=self.project_name, s3_source_location=self.artifact_location)
        self.codebuild_build_id = response['build']['id']

    def get_details(self):
        self.codebuild_build_details = self.cbm.get_build_details(self.codebuild_build_id)['builds'][0]
        self.codebuild_build_status = self.codebuild_build_details['buildStatus']
        self.log_group_name = self.codebuild_build_details['logs']['groupName']
        self.log_stream_name = self.codebuild_build_details['logs']['streamName']
        return self.codebuild_build_status

    @property
    def current_phase(self):
        if 'phaseStatus' in self.codebuild_build_details['phases'][-1]:
            phase_status = self.codebuild_build_details['phases'][-1]
        else:
            phase_status = 'N/A'

        return self.codebuild_build_details['phases'][-1]['phaseType'], phase_status

    def get_build_logs(self):
        results = []
        if self.log_group_name and self.log_stream_name:
            response = self.cwlm.get_event_logs(self.log_group_name, self.log_stream_name)
            if len(response['events']) > 0:
                for e in response['events']:
                    results.append(e['message'].strip())

        return results


if __name__ == "__main__":
    args = argument_parser()
    b = Build(project_name=args['project'], build_id=args['buildid'], bucket=args['bucket'])
    b.upload_artifacts()
    b.create()
    time.sleep(10)
    while b.get_details() == 'IN_PROGRESS':
        phase_details = b.current_phase
        phase_status = phase_details[0]
        phase_type = phase_details[1]
        print 'Phase: {0} - {1}'.format(b.current_phase[0], b.current_phase[1])
        time.sleep(10)

    logs = b.get_build_logs()
    for log in logs:
        print log