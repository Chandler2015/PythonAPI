# Coding Challenge: Python, Database

## Background

ComboCurve Sync is a tool for importing well and production data into ComboCurve from a SQL database. To use the tool the user has to create a ComboCurve Sync project, which consist of a few files. Those files are used as input for the tool to determine how the data should be extracted from the user's DB. When the sync tool is executed the data is extracted and sent remotely to ComboCurve using the ComboCurve REST API.

## Objective

You have to implement a simplified version of ComboCurve Sync. It should consist of a python module that can parse a ComboCurve Sync project configuration, use it to query a SQL database and send the result to the ComboCurve REST API.

## Specifications

- A ComboCurve Sync project is a directory consisting of:
  - A [`combocurve.toml`](./example/combocurve.toml) file
  - A [`resources`](./example/resources) sub-directory
- `combocurve.toml` it's a [TOML](https://en.wikipedia.org/wiki/TOML) configuration file.
- It always includes the `connection` section with the attribute `type`, specifying what type of DB the data should be extracted from.
- Possible values for `connection.type` are `mysql`, `sqlserver`, or `postgres`.
- A section with name equal to the connection type will follow, with the required parameters for establishing such database connection.
- Under the `resources` dir there can be multiple `.sql` files, one for each resource (entity) that the user wants to import into ComboCurve, from the ones that the ComboCurve REST API supports of course.

## Requirements

- Your module's entry point should be a function called `start` in `core.main`, but you can split your code into as many function and modules as you like.
- The ComboCurve Sync module should accept the location of the project as a parameter. When not provided it should assume the current working directory.
- If the specified directory is not a valid project, because it does not contain a `combocurve.toml` and at least one `resources/<resource-name>.sql`, it should raise an error saying so.
- The DB connection details should be parsed from `combocurve.toml` in the project directory.
- The data for each one of the resources found under `resources` should be loaded from the DB using the query in the corresponding `.sql` file.
- The loaded data for each resource should be sent as JSON to the ComboCurve API using the corresponding PUT method:
  - [PUT https://test-api.combocurve.com/v1/wells](https://docs.api.combocurve.com/#bcbe26fa-6ae3-4d66-996c-dad9863c580b)
  - [PUT https://test-api.combocurve.com/v1/daily-productions](https://docs.api.combocurve.com/#fc8007de-01b6-46f8-8d3f-b7f92836429a)
- The HTTPS requests to the API must include the following header:
  ```
  x-api-key: AIzaSyCtjb6vep5dWTyrQNvoVBkKYWBH3WeGG2E
  Authorization: Bearer JWT_WE_GAVE_YOU_HERE
  ```
- BONUS: Implement pagination: Load a maximum of 100 records from the DB to be sent to the REST API and repeat until you send up to 1000 records.

## Assumptions

- Only need to implement `connection.type = "mysql"`.
- Only need to implement the `wells` and `daily-production` resources.
- Only need to support importing up to 1000 rows for each resource on one invocation.
- For each resource, only need to support the fields shown in `/example` and `/schema`.
- The ComboCurve REST API documentation shows `api.combocurve.com` as the base URL, but for this project you should use `test-api.combocurve.com`
- If the ComboCurve API respond with errors, that's ok. It will be expected if we don't provide you valid credentials.

## Structure

### [/core](./core)

Where you should write your Python module.

### [/example](./example)

Example ComboCurve project that should be used as input to test your Python module.

### [/schema](./schema)

Example SQL schema that should be used to set up a MySQL database to test your Python module.

## Suggestions

- Reach out for questions if the specifications or requirements are confusing.
- For anything that we not explicitly described in the specifications or requirements feel free to be creative.
- Rely on existing Python packages for the config file parsing and DB connection.
- If you happen to be more familiar with SQL Server or Postgres you can implement any of those instead of MySQL.

## Resources

- [MySQL Connector for Python - Installation](https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html)
- [MySQL Connector for Python - Example](https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html)
- [TOML for Python](https://pypi.org/project/toml/)
- [ComboCurve API Documentation](https://docs.api.combocurve.com/)
