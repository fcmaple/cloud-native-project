#!/bin/bash

# Script: update.sh
# Description: This script could update the user info and trip info
# Usage: ./update.sh -n <item name> -i <id> -k <key> -v <value>

#Default values
NAME=""
ID=""
KEY=""
VALUE=""
VERSION="v0.0.2"

while getopts "n:i:k:v:r:" opt; do 
    case $opt in
        n) NAME=$OPTARG;;
        i) ID=$OPTARG;;
        k) KEY=$OPTARG;;
        v) VALUE=$OPTARG;;
        r) VERSION=$OPTARG;;
        *) echo "Invalid option: -$OPTARG" >&2; exit 1;;
    esac
done
#Check if required options are provided
if [ -z "$VERSION" ] || [ -z "$NAME" ] || [ -z "$ID" ] || [ -z "$KEY" ]||[ -z "$VALUE" ];then
    echo "Usage: ./update.sh -n <item name> -i <id> -k <key> -v <value>"
    echo "Options:"
    # echo " -s <SQL IP>      The update item SQL_IP"
    echo " -n <item name>   update item NAME"
    echo " -i <id>          update item ID"
    echo " -k <key>         update item KEY"
    echo " -v <value>       update item VALUE"
    echo " -r <version>     image version"
    exit 1
fi

docker run --rm --net=cloud-native-project_cloud-native wnlab/uber-api:$VERSION python -m app.tool.tool -n $NAME -i $ID -k $KEY -v $VALUE