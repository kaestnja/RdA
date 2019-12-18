#!/bin/bash

USERNAME=INSERT_USERNAME_HERE
PASSWORD=INSERT_PASSWORD_HERE

# Generate auth header
AUTH=$(echo -n $USERNAME:$PASSWORD | base64)

# Get repository URLs
curl -iH "Authorization: Basic "$AUTH https://api.github.com/user/repos | grep -w clone_url > repos.txt

# Clean URLs (remove " and ,) and print only the second column
cat repos.txt | tr -d \"\, | awk '{print $2}'  > repos_clean.txt

# Insert username:password after protocol:// to generate clone URLs
cat repos_clean.txt |  sed "s/:\/\/git/:\/\/$USERNAME\:$PASSWORD\@git/g" > repos_clone.txt

while read FILE; do
    git clone $FILE
done <repos_clone.txt

rm repos.txt & rm repos_clone.txt