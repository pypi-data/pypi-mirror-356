# 🏭 industrial_model_client_generator

A utility for generating client-specific configurations for industrial data models

## 📦 Overview

The `industrial_model_client_generator` package automates the generation of client configurations based on a set of input definitions.

## 🚀 Installation

```bash
pip install industrial-model-client-generator
```

## 🚀 Usage

```python
from industrial_model_client_generator import InstanceSpaceConfig, generate


instance_space_configs = [
        InstanceSpaceConfig(
            view_or_space_external_id="ANY-COR-ALL-DML", instance_spaces_prefix="ANY-"
        ),
        InstanceSpaceConfig(
            view_or_space_external_id="ANOTHER-COR-ALL-DMD",
            instance_spaces=["ANOTHER-COR-ALL-DAT"],
        ),
        InstanceSpaceConfig(
            view_or_space_external_id="CogniteAsset", instance_spaces_prefix="GENERIC-"
        ),
]

generate(
    client_name="TestingClient", # required
    instance_space_configs=instance_space_configs, # optional - map the instance spaces to views to improve perf
    output_path="output" # optional - if not set, it will output to the client_name folder
)

```

# ⚙️ Environment Configuration Guide

Below is a list of all required variables and what each of them does:

| Variable Name                | Description                                            |
| ---------------------------- | ------------------------------------------------------ |
| `CDF_PROJECT`                | The name of the CDF project                            |
| `CDF_CLIENT_NAME`            | A friendly name for the client configuration           |
| `CDF_CLUSTER`                | The Cognite cluster where your project is hosted       |
| `CDF_TOKEN_URL`              | The OAuth2 token URL.                                  |
| `CDF_CLIENT_ID`              | The Client ID of the registered service principal.     |
| `CDF_CLIENT_SECRET`          | The Client Secret of the registered service principal. |
| `CDF_DATA_MODEL_EXTERNAL_ID` | External ID of the data model in CDF.                  |
| `CDF_DATA_MODEL_SPACE`       | Data model space where the model is stored.            |
| `CDF_DATA_MODEL_VERSION`     | The version of the data model to be used.              |

## 🔐 Setting the Variables

### Option: `.env` File (Recommended for Local Development)

Create a file named `.env` in the root of your project:

```env
CDF_PROJECT=cognite-dev
CDF_CLIENT_NAME=testing
CDF_CLUSTER=az-eastus-1
CDF_TOKEN_URL=https://login.microsoftonline.com/xxxx/oauth2/v2.0/token
CDF_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
CDF_CLIENT_SECRET=your-client-secret
CDF_DATA_MODEL_EXTERNAL_ID=CogniteCore
CDF_DATA_MODEL_SPACE=cdf_cdm
CDF_DATA_MODEL_VERSION=v1

```
