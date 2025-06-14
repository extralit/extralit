---
description: These are the how-to guides for the deployment, configuration, and management of the Extralit server. They provide step-by-step instructions for common scenarios, including detailed explanations and code samples.
hide: toc
---

# How-to guides

>:warning: This page is currently under construction. Please check back later for updates.


## Deployment and configuration
<div class="grid cards" markdown>

-   __Deploy with Docker__

    ---

    Learn how to deploy Extralit using Docker containers for a quick and easy setup.

    [:octicons-arrow-right-24: How-to guide](docker_deployment.md)

-   __Deploy with Kubernetes__

    ---

    Discover how to deploy Extralit on a Kubernetes cluster for scalable and managed environments.

    [:octicons-arrow-right-24: How-to guide](k8s_deployment.md)

-   __Configure Deployments__

    ---

    Learn how to configure various deployment options and customize Extralit for your specific needs.

    [:octicons-arrow-right-24: How-to guide](../reference/argilla-server/configuration.md)

-   __Upgrade Extralit__

    ---

    Find out how to safely upgrade your Extralit installation to the latest version.

    [:octicons-arrow-right-24: How-to guide](upgrading.md)

</div>


## Server management

<div class="grid cards" markdown>

-   __Manage users and credentials__

    ---

    Learn what they are and how to manage (create, read and delete) `Users` in Argilla.

    [:octicons-arrow-right-24: How-to guide](user.md)

-   __Manage workspaces__

    ---

    Learn what they are and how to manage (create, read and delete) `Workspaces` in Argilla.

    [:octicons-arrow-right-24: How-to guide](workspace.md)

-   __Create, update, and delete datasets__

    ---

    Learn what they are and how to manage (create, read and delete) `Datasets` and customize them using the `Settings` for `Fields`, `Questions`,  `Metadata` and `Vectors`.

    [:octicons-arrow-right-24: How-to guide](dataset.md)

-   __Add, update, and delete records__

    ---

    Learn what they are and how to add, update and delete the values for a `Record`, which are made up of `Metadata`, `Vectors`, `Suggestions` and `Responses`.

    [:octicons-arrow-right-24: How-to guide](record.md)

-   __Distribute the annotation__

    ---

    Learn how to use Argilla's automatic `TaskDistribution` to annotate as a team efficiently.

    [:octicons-arrow-right-24: How-to guide](distribution.md)

-   __Annotate a dataset__

    ---

    Learn how to use the Argilla UI to navigate `Datasets` and submit `Responses`.

    [:octicons-arrow-right-24: How-to guide](annotate.md)

-   __Query and filter a dataset__

    ---

    Learn how to query and filter a `Dataset`.

    [:octicons-arrow-right-24: How-to guide](query.md)

-   __Import and export datasets and records__

    ---

    Learn how to export your `Dataset` or its `Records` to Python, your local disk, or the Hugging Face Hub.

    [:octicons-arrow-right-24: How-to guide](import_export.md)


</div>

## Advanced guides

<div class="grid cards" markdown>

-   __Custom fields with layout templates__

    ---

    Learn how to create `CustomFields` with HTML, CSS and JavaScript templates.

    [:octicons-arrow-right-24: How-to guide](custom_fields.md)

-   __Use webhooks to respond to server events__

    ---

    Learn how to use Argilla webhooks to receive notifications about events in your Argilla Server.

    [:octicons-arrow-right-24: How-to guide](webhooks.md)

-   __Webhooks internals__

    ---

    Learn how Argilla webhooks are implented under the hood and the structure of the different events.

    [:octicons-arrow-right-24: How-to guide](webhooks_internals.md)


-   __Use Markdown to format rich content__

    ---

    Learn how to use Markdown and HTML in `TextField` to format chat conversations and allow for basic multi-modal support for images, audio, video and PDFs.

    [:octicons-arrow-right-24: How-to guide](use_markdown_to_format_rich_content.md)

-   __Migrate to Argilla V2__

    ---

    Learn how to migrate `Users`, `Workspaces` and `Datasets` from Argilla V1 to V2.

    [:octicons-arrow-right-24: How-to guide](migrate_from_legacy_datasets.md)

</div>
