<div class="start-page__intro" markdown="1">

# Welcome to Extralit

## An advanced platform for scientific literature review and data extraction

If you need support, join the [Extralit Slack community](https://join.slack.com/t/extralit/shared_invite/zt-2kt8t12r7-uFj0bZ5SPAOhRFkxP7ZQaQ)
</div>

<div class="start-page__content" markdown="1">

Get started by setting up your first literature extraction project.

### 1. Install the Extralit SDK
To work with Extralit, you need to use the Extralit SDK. Install it with pip:

```sh
pip install extralit -U
```

### 3. Connect to your Argilla server

Get your `ARGILLA_API_URL`:

- If you are using Docker, it is the URL shown in your browser (by default `http://localhost:6900`)
- If you are using HF Spaces, it should be constructed as follows: `https://[your-owner-name]-[your_space_name].hf.space`

Get your `ARGILLA_API_KEY` you find in ["My settings"](/user-settings) and copy the API key.

Make sure to replace `ARGILLA_API_URL` and `ARGILLA_API_KEY` in the code below. If you are using a private HF Space, you need to specify your `HF_TOKEN` which can be found [here](https://huggingface.co/settings/tokens).

```python
import argilla as rg

rg.init(
    api_url="ARGILLA_API_URL",
    api_key="ARGILLA_API_KEY",
    # extra_headers={"Authorization": f"Bearer {"HF_TOKEN"}"}
)
```

### 4. Create your first dataset

Specify a workspace where the dataset will be created. Check your workspaces in ["My settings"](/user-settings). To create a new workspace, check the [docs](https://docs.argilla.io/en/latest/getting_started/installation/configurations/workspace_management.html).

Create a Dataset with two labels ("sadness" and "joy"). Don't forget to replace "<your-workspace>". Here, we are using a task template, check the docs to [create a fully custom dataset](https://docs.argilla.io/en/latest/practical_guides/create_update_dataset/create_dataset.html).

```python
dataset = rg.FeedbackDataset.for_text_classification(
    labels=["sadness", "joy"],
    multi_label=False,
    use_markdown=True,
    guidelines=None,
    metadata_properties=None,
    vectors_settings=None,
)
dataset.push_to_argilla(name="my-first-dataset", workspace="<your-workspace>")
```

### 5. Add records

Create a list with the records you want to add. Ensure that you match the fields with the ones specified in the previous step.

You can also use `pandas` or `load_dataset` to [read an existing dataset and create records from it](https://docs.argilla.io/en/latest/practical_guides/create_update_dataset/records.html#add-records).

```python
records = [
    rg.FeedbackRecord(
        fields={
            "text": "I am so happy today",
        },
    ),
    rg.FeedbackRecord(
        fields={
            "text": "I feel sad today",
        },
    )
]
dataset.add_records(records)
```

</div>
