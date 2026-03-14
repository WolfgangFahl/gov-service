"""
Created on 2026-03-14

@author: wf
"""
import os
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from lodstorage.multilang_querymanager import MultiLanguageQueryManager
from lodstorage.query import Endpoint, EndpointManager, PrefixConfigs
from lodstorage.sparql import SPARQL


class GovService:
    """
    GOV-Service backend application
    """

    def __init__(self, debug: bool = False):
        """
        Constructor
        """
        self.debug = debug
        self.app = FastAPI(title="GOV-Service")
        self.setup_config(debug=self.debug)
        self.setup_routes()

    def setup_config(self, debug: bool = False):
        """
        Setup the configuration from the config directory using lodstorage managers.
        """
        base_dir = os.path.join(os.path.dirname(__file__), "config")

        # Load Endpoints
        endpoints_path = os.path.join(base_dir, "endpoints.yaml")
        endpoints = EndpointManager.getEndpoints(endpoints_path)
        self.endpoint = endpoints.get("govb")
        self.govb_endpoint_url = getattr(self.endpoint, "endpoint", None)

        # Load Prefixes
        prefixes_path = os.path.join(base_dir, "prefixes.yaml")
        self.prefix_configs = PrefixConfigs.preload(prefixes_path)

        # Load Queries
        queries_path = os.path.join(base_dir, "gov_queries.yaml")
        self.qm = MultiLanguageQueryManager(
            yaml_path=queries_path,
            languages=["sparql"],
            debug=debug,
        )

    def get_query(self, query_name: str, param_dict: Optional[dict] = None) -> Optional[str]:
        """
        Get a SPARQL query with parameters applied
        """
        query = self.qm.query4Name(query_name)
        if query is None:
            return None

        # Apply endpoint prefixes
        if self.endpoint is not None:
            query.add_endpoint_prefixes(self.endpoint, self.prefix_configs)

        # Apply parameters
        param_dict = param_dict or {}
        sparql_query = query.params.apply_parameters_with_check(param_dict, param_list=query.param_list)

        # Prepend prefixes
        if query.prefixes:
            prefix_str = "".join(query.prefixes)
            sparql_query = f"{prefix_str}\n{sparql_query}"

        return sparql_query

    def setup_routes(self):
        """
        Setup the FastAPI routes
        """

        @self.app.get("/item/show/{gov_id}", response_class=HTMLResponse)
        async def item_show(gov_id: str):
            """
            Return HTML table fragment with GOV-Kennung and Name.
            """
            sparql_query = self.get_query("NameByGovId", {"gov_id": gov_id})

            if not sparql_query:
                return "<tr><td>Error</td><td>Query not found</td></tr>"

            sparql = SPARQL(self.govb_endpoint_url)
            results = sparql.queryAsListOfDicts(sparql_query)

            names_html = ""
            for row in results:
                name = row.get("name", "")
                try:
                    name = name.encode("latin-1").decode("utf-8")
                except (UnicodeEncodeError, UnicodeDecodeError):
                    pass

                names_html += f"""
        <li>
          <span>{name}</span>
        <span style="color:gray"></span>
          </li>"""

            if not results:
                names_html = """
        <li>
          <span>Unknown</span>
        <span style="color:gray"></span>
          </li>"""

            html = f"""<tr>
<td>GOV-Kennung</td>
<td><a href="https://gov.genealogy.net/item/show/{gov_id}">{gov_id}</a></td>
</tr>
<tr>
  <td>Name</td>
  <td>
    <ul>{names_html}
    </ul>
  </td>
</tr>"""

            return html
