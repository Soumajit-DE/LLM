from dopplersdk import DopplerSDK
import os

# set Doppler token
import os
import sys

# set Doppler token
doppler_token = os.getenv("DOPPLER_AIGUILD_TOKEN")
if not doppler_token:
    print("Error: The DOPPLER_AIGUILD_TOKEN environment variable is not set. Please set it before running this script.", file=sys.stderr)
    sys.exit(1)
doppler_client = DopplerSDK()
doppler_client.set_access_token(doppler_token)


def get_api_key():

    results = doppler_client.secrets.get(
        project="dep-training",
        config="prod_ai_guild_genai_practicum",
        name="AZURE_OPENAI_API_KEY",
    )
    api_key = results.value["raw"]
    return api_key


def get_endpoint():

    results = doppler_client.secrets.get(
        project="dep-training",
        config="prod_ai_guild_genai_practicum",
        name="AZURE_OPENAI_API_BASE",
    )
    endpoint = results.value["raw"]
    return endpoint


def main():
    api_key = get_api_key()
    endpoint = get_endpoint()

    # set the OpenAI API key for the user in environment variable
    with open(os.path.expanduser("~/.bashrc"), "a") as outfile:
        # 'a' stands for "append"
        outfile.writelines("export AZURE_OPENAI_API_KEY=" + api_key + "\n")

    # set the OpenAI API key for the user in environment variable
    with open(os.path.expanduser("~/.bashrc"), "a") as outfile:
        # 'a' stands for "append"
    # Set the OpenAI API key and endpoint for the current process
        os.environ["AZURE_OPENAI_API_KEY"] = api_key
        os.environ["AZURE_OPENAI_API_BASE"] = endpoint

    # Warn the user about the risks of storing secrets in plain text files
    print("WARNING: Storing API keys in ~/.bashrc or other plain text files poses a security risk.")
    print("The credentials have been set for this process only.")
    print("If you need to use these credentials in other shells, consider using a secure secrets manager.")
    print("If you must persist them, you can manually add the following lines to your ~/.bashrc (NOT RECOMMENDED):")
    print(f'    export AZURE_OPENAI_API_KEY="{api_key}"')
    print(f'    export AZURE_OPENAI_API_BASE="{endpoint}"')


if __name__ == "__main__":
    main()
