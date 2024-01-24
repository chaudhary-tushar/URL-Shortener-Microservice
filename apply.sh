#!/bin/bash

# Initialize variables with default values
flag_a=false
flag_g=false
flag_p=false
flag_r=false

# Function to display usage
usage() {
    echo "Usage: $0 [-a] [-g] [-p] [-r]"
    exit 1
}

if [ "$#" -eq 0 ]; then
    flag_a=true
    flag_g=true
    flag_p=true
    flag_r=true
fi
# Parse command line options
while getopts "agpr" opt; do
    case $opt in
        a) flag_a=true ;;
        g) flag_g=true ;;
        p) flag_p=true ;;
        r) flag_r=true ;;
        \?) usage ;;
    esac
done

# Perform actions based on options
if $flag_a; then
	kubectl apply -f ./Auth/manifests/
    echo "Option -a selected Auth YAML applied ,Results = $?"
fi

if $flag_g; then
    kubectl apply -f ./Gateway/manifests/
    echo "Option -g selected Gate YAML applied ,Results = $?"
fi

if $flag_p; then
    kubectl apply -f ./Profile/manifests/
    echo "Option -p selected Profile YAML applied ,Results = $?"
fi

if $flag_r; then
    kubectl apply -f ./Redirects/manifests/
    echo "Option -r selected Redirects YAML applied ,Results = $?"
fi

# Additional logic or actions based on selected options can be added here
