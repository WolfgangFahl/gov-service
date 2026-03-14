"""
Created on 2026-03-14

@author: wf
"""

import os
from dataclasses import dataclass, field
from typing import List, Optional

from basemkit.yamlable import lod_storable
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response
from lodstorage.multilang_querymanager import MultiLanguageQueryManager
from lodstorage.query import EndpointManager, PrefixConfigs
from lodstorage.sparql import SPARQL


class ContentNegotiator:
    """
    Resolve the desired response format from request Accept header or explicit format parameter.
    Priority: format param > Accept header > default.
    Supported formats: html, json, yaml.
    """

    MIME_MAP = {
        "text/html": "html",
        "application/json": "json",
        "application/x-yaml": "yaml",
        "text/yaml": "yaml",
    }

    def __init__(
        self,
        request: Request,
        format_param: Optional[str] = None,
        default: str = "html",
    ):
        self.format = self._resolve(request, format_param, default)

    def _resolve(self, request: Request, format_param: Optional[str], default: str) -> str:
        if format_param:
            return format_param.lower()
        accept = request.headers.get("accept", "")
        for mime, fmt in self.MIME_MAP.items():
            if mime in accept:
                return fmt
        return default

    def respond(self, item: "GOVItem") -> Response:
        """
        Return the appropriate Response for the resolved format.
        """
        if self.format == "json":
            return JSONResponse(content=item.to_dict())
        if self.format == "yaml":
            return PlainTextResponse(content=item.to_yaml(), media_type="application/x-yaml")
        return HTMLResponse(content=item.as_html())


@lod_storable
class GOVItem:
    """
    A single GOV item with its identifier and resolved names.
    State only — no HTML here.
    """

    gov_id: str
    names: List[str] = field(default_factory=list)

    def of_service(self, service: "GovService") -> None:
        """
        Populate names by querying the given GovService.
        """
        sparql_query = service.get_query("NameByGovId", {"gov_id": self.gov_id})
        if not sparql_query:
            return
        results = service.sparql.queryAsListOfDicts(sparql_query)
        for row in results:
            name = row.get("name", "")
            try:
                name = name.encode("latin-1").decode("utf-8")
            except (UnicodeEncodeError, UnicodeDecodeError):
                pass
            if name:
                self.names.append(name)

    def as_html(self) -> str:
        """
        Render this GOVItem as an HTML table fragment.
        All HTML generation is confined to this method.

        Returns:
            str: HTML table rows for GOV-Kennung and Name.
        """
        if self.names:
            items_html = "".join(f"<li><span>{name}</span></li>" for name in self.names)
        else:
            items_html = "<li><span>Unknown</span></li>"
        html = f"""<tr>
<td>GOV-Kennung</td>
<td><a href="https://gov.genealogy.net/item/show/{self.gov_id}">{self.gov_id}</a></td>
</tr>
<tr>
  <td>Name</td>
  <td><ul>{items_html}</ul></td>
</tr>"""
        return html


class GovService:
    """
    GOV-Service backend application
    """

    def __init__(self, debug: bool = False):
        self.debug = debug
        self.app = FastAPI(title="GOV-Service")
        self.setup_config(debug=self.debug)
        self.setup_routes()

    def setup_config(self, debug: bool = False):
        """
        Setup the configuration from the config directory using lodstorage managers.
        """
        base_dir = os.path.join(os.path.dirname(__file__), "config")

        endpoints_path = os.path.join(base_dir, "endpoints.yaml")
        endpoints = EndpointManager.getEndpoints(endpoints_path)
        self.endpoint = endpoints.get("govb")
        self.govb_endpoint_url = getattr(self.endpoint, "endpoint", None)

        prefixes_path = os.path.join(base_dir, "prefixes.yaml")
        self.prefix_configs = PrefixConfigs.preload(prefixes_path)

        queries_path = os.path.join(base_dir, "gov_queries.yaml")
        self.qm = MultiLanguageQueryManager(
            yaml_path=queries_path,
            languages=["sparql"],
            debug=debug,
        )
        self.sparql = SPARQL(self.govb_endpoint_url)

    def get_query(self, query_name: str, param_dict: Optional[dict] = None) -> Optional[str]:
        """
        Get a SPARQL query with parameters applied.
        """
        query = self.qm.query4Name(query_name)
        if query is None:
            return None

        if self.endpoint is not None:
            query.add_endpoint_prefixes(self.endpoint, self.prefix_configs)

        param_dict = param_dict or {}
        sparql_query = query.params.apply_parameters_with_check(param_dict, param_list=query.param_list)

        if query.prefixes:
            prefix_str = "".join(query.prefixes)
            sparql_query = f"{prefix_str}\n{sparql_query}"

        return sparql_query

    def setup_routes(self):
        """
        Setup the FastAPI routes.
        """

        @self.app.get("/item/show/{gov_id}")
        @self.app.get("/item/wikihtml/{gov_id}")
        async def item_show(gov_id: str, request: Request, format: Optional[str] = None):
            """
            Return GOV item in the negotiated format (html, json, yaml).
            Format resolved by: ?format= param > Accept header > html default.
            """
            gov_item = GOVItem(gov_id=gov_id)
            gov_item.of_service(service=self)
            negotiator = ContentNegotiator(request=request, format_param=format)
            return negotiator.respond(gov_item)
