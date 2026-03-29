#!/bin/bash
awslocal s3 mb s3://ats-resumes-bucket

sleep 2 # Wait for bucket to be created

awslocal s3 ls
