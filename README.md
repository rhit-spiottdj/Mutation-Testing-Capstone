# Mutation-Testing-Capstone
Senior Capstone Project for Mutation Testing Team

## Setup
Run the following command:
pip install pyyaml miniauth progressbar progressbar2 libcst fastmcp

## To Run Tester in Terminal
cd into the PythonTester folder and run "python Main.py" with any desired arguments

## To Run Tester on MCP server
Run serve.py in mutation_mcp_server. 
Then run the mcp.json file to start the MCP server. 
Open VSCode Agent Mode, and run #run_mutation_tests args="--files <file directory> --tests<test directory>" 