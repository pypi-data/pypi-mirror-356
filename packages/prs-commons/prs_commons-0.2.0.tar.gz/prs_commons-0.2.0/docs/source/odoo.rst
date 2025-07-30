Odoo RPC Client
===============

A high-level client for interacting with Odoo's XML-RPC/JSON-RPC API.

Configuration
------------

The OdooRPClient can be configured using environment variables for convenience. All parameters are optional and can be overridden when initializing the client.

.. list-table::
   :header-rows: 1
   :widths: 20 10 10 60

   * - Variable
     - Type
     - Default
     - Description
   * - ODOO_HOST
     - string
     - None
     - Odoo server hostname or IP address
   * - ODOO_PORT
     - int
     - 8069
     - Odoo server port number
   * - ODOO_PROTOCOL
     - string
     - jsonrpc
     - Protocol to use (jsonrpc or xmlrpc)
   * - ODOO_DB
     - string
     - None
     - Database name to connect to
   * - ODOO_USER
     - string
     - None
     - Username for authentication
   * - ODOO_PASSWORD
     - string
     - None
     - Password for authentication

Example ``.env`` file:

.. code-block:: bash

   ODOO_HOST=localhost
   ODOO_PORT=8069
   ODOO_PROTOCOL=jsonrpc
   ODOO_DB=my_database
   ODOO_USER=admin
   ODOO_PASSWORD=admin_password

When using environment variables, you can initialize the client without any parameters:

.. code-block:: python

   from prs_commons.odoo.rpc_client import OdooRPClient

   # Uses environment variables for configuration
   client = OdooRPClient()

   # You can still override specific parameters
   client = OdooRPClient(
       host='custom-host',  # Overrides ODOO_HOST
       database='other_db'  # Overrides ODOO_DB
   )


API Reference
------------

.. py:class:: OdooRPClient(host=None, database=None, username=None, password=None, protocol='jsonrpc', port=8069, **kwargs)

   Initialize the Odoo RPC client.

   :param str host: Odoo server hostname or IP (default: from environment)
   :param str database: Database name (default: from environment)
   :param str username: Login username (default: from environment)
   :param str password: Login password (default: from environment)
   :param str protocol: Protocol to use ('jsonrpc' or 'xmlrpc')
   :param int port: Port number (default: 8069)
   :param kwargs: Additional connection parameters

   .. note::
      This is a singleton class. Multiple instantiations will return the same instance.

   .. py:method:: ensure_connection()

      Ensure connection to the Odoo server is established.

      :raises ConnectionError: If connection cannot be established
      :raises ValueError: If required credentials are missing

   .. py:method:: search_read(model, domain=None, fields=None, offset=0, limit=None, order=None, **kwargs)

      Search and read records matching the criteria.

      :param str model: Name of the Odoo model (e.g., 'res.partner')
      :param list domain: Search domain (list of tuples)
      :param list fields: List of fields to return
      :param int offset: Number of records to skip
      :param int limit: Maximum number of records to return
      :param str order: Sort order (e.g., 'name asc, id desc')
      :return: List of dictionaries containing record data

   .. py:method:: create_record(model, values, **kwargs)

      Create a new record in the specified model.

      :param str model: Name of the Odoo model
      :param dict values: Field values for the new record
      :return: ID of the created record

   .. py:method:: write_record(model, ids, values, **kwargs)

      Update existing record(s).

      :param str model: Name of the Odoo model
      :param list ids: List of record IDs to update
      :param dict values: Field values to update
      :return: True if successful

   .. py:method:: execute_method(model, method, *args, **kwargs)

      Execute a method on the Odoo model.

      :param str model: Name of the Odoo model
      :param str method: Method name to call
      :param args: Positional arguments for the method
      :param kwargs: Keyword arguments for the method
      :return: Result of the method call

Example Usage
-------------

.. code-block:: python
   :emphasize-lines: 3,6,9,14,21,26,29

   from prs_commons.odoo.rpc_client import OdooRPClient

   # Initialize the client (singleton pattern)
   client = OdooRPClient()

   # Ensure connection
   client.ensure_connection()

   # Search for partner records
   domain = [('is_company', '=', True)]
   fields = ['id', 'name', 'email']
   partners = client.search_read('res.partner', domain, fields=fields)

   # Create a new partner
   new_id = client.create_record('res.partner', {
       'name': 'Acme Inc.',
       'is_company': True,
       'email': 'info@acme.com'
   })

   # Update the partner
   client.write_record('res.partner', [new_id], {
       'email': 'contact@acme.com'
   })

   # Execute a method
   result = client.execute_method('res.partner', 'search_read', domain, fields=fields)

   # Close the connection
   client.close_connection()

Error Handling
--------------

The client raises appropriate exceptions for different error conditions:

- :class:`ConnectionError`: When unable to connect to Odoo server
- :class:`ValueError`: For invalid input parameters
- :class:`Exception`: For other Odoo-specific errors

See Also
----------

- `Odoo's External API Documentation <https://www.odoo.com/documentation/16.0/developer/misc/api/odoo.html>`_
- `OdooRPC Library <https://pythonhosted.org/OdooRPC/>`_
