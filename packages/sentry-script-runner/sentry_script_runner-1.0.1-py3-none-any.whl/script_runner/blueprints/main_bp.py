import functools
import logging
from typing import Any

import requests
from flask import Blueprint, Response, jsonify, make_response, request

from script_runner.approval_policy import ApprovalStatus
from script_runner.config import Config
from script_runner.decorators import authenticate_request, cache_autocomplete
from script_runner.utils import CombinedConfig, MainConfig, RegionConfig


def create_main_bp(app_config: Config) -> Blueprint:
    config = app_config.config
    approval_policy = app_config.approvals_policy

    assert not isinstance(config, RegionConfig)

    main_config_bp: Blueprint = Blueprint("main_config", __name__)

    @main_config_bp.route("/run", methods=["POST"])
    @authenticate_request(app_config)
    def run_all() -> Response:
        """
        Run a script for all regions
        """
        data = request.get_json()

        results = {}
        errors = {}

        group_name = data["group"]
        group = config.groups[group_name]
        requested_function = data["function"]
        function = next(
            (f for f in group.functions if f.name == requested_function), None
        )
        assert function is not None, "Invalid function"
        params = data["parameters"]

        # Check if the function requires approval
        approval_status = approval_policy.requires_approval(
            group_name, function, data["regions"]
        )

        if approval_status != ApprovalStatus.ALLOW:
            raise RuntimeError("Function requires approval.")

        for requested_region in data["regions"]:
            region = next(
                (r for r in config.main.regions if r.name == requested_region), None
            )
            if region is None:
                err_response = make_response(jsonify({"error": "Invalid region"}), 400)
                return err_response

            for audit_logger in config.audit_loggers:
                audit_logger.log(
                    user=config.auth.get_user_email(request) or "unknown",
                    group=group_name,
                    function=requested_function,
                    region=region.name,
                )

            scheme = request.scheme if isinstance(config, CombinedConfig) else "http"
            try:
                res = requests.post(
                    f"{scheme}://{region.url}/run_region",
                    json={
                        "group": group_name,
                        "function": function.name,
                        "function_checksum": function.checksum,
                        "parameters": params,
                        "region": region.name,
                    },
                )
                res.raise_for_status()
                results[region.name] = res.json()

            except requests.exceptions.RequestException as e:
                logging.error(
                    f"Request failed for region {region.name}: {e}", exc_info=True
                )
                error_type = (
                    "TimeoutError"
                    if isinstance(e, requests.exceptions.Timeout)
                    else "ConnectionError"
                )
                errors[region.name] = {
                    "type": error_type,
                    "message": f"Network or connection error contacting region {region.name}",
                    "details": str(e),
                }
            except Exception as e:
                logging.error(
                    f"Unexpected error processing region {region.name}: {e}",
                    exc_info=True,
                )
                errors[region.name] = {
                    "type": "GenericError",
                    "message": f"An unexpected error occurred processing region {region.name}",
                    "details": str(e),
                }

        return make_response(jsonify({"results": results, "errors": errors}), 200)

    @main_config_bp.route("/autocomplete", methods=["GET"])
    @cache_autocomplete
    def autocomplete() -> Response:
        """
        Get autocomplete options for a function parameter
        """
        group_name = request.args["group"]
        group = config.groups[group_name]
        requested_function = request.args["function"]
        regions = request.args["regions"].split(",")
        function = next(
            (f for f in group.functions if f.name == requested_function), None
        )
        assert function is not None, "Invalid function"

        results = {}

        for requested_region in regions:
            region = next(
                (r for r in config.main.regions if r.name == requested_region), None
            )
            if region is None:
                err_response = make_response(jsonify({"error": "Invalid region"}), 400)
                return err_response

            scheme = request.scheme if isinstance(config, CombinedConfig) else "http"

            res = requests.get(
                f"{scheme}://{region.url}/autocomplete_region",
                params={
                    "group": group_name,
                    "function": function.name,
                    "region": region.name,
                },
            )
            results[region.name] = res.json()

        return make_response(jsonify(results), 200)

    @functools.lru_cache(maxsize=1)
    def get_config() -> dict[str, Any]:
        assert isinstance(config, (MainConfig, CombinedConfig))

        regions = config.main.regions
        groups = config.groups

        group_data = [
            {
                "group": g,
                "functions": [
                    {
                        "name": f.name,
                        "docstring": f.docstring,
                        "source": f.source,
                        "parameters": [
                            {
                                "name": p.name,
                                "type": p.type.value,
                                "default": p.default,
                                "enumValues": p.enum_values,
                            }
                            for p in f.parameters
                        ],
                        "isReadonly": f.is_readonly,
                    }
                    for f in function_group.functions
                ],
                "docstring": function_group.docstring,
                "markdownFiles": [
                    {"name": file.filename, "content": file.content}
                    for file in function_group.markdown_files
                ],
            }
            for (g, function_group) in groups.items()
        ]

        return {
            "title": config.main.title,
            "regions": [r.name for r in regions],
            "groups": group_data,
        }

    @main_config_bp.route("/config")
    def fetch_config() -> Response:
        res = get_config()

        groups_without_access = []

        user_groups = set()
        for group in config.groups:
            if config.auth.has_group_access(request, group):
                user_groups.add(group)
            else:
                groups_without_access.append(group)

        filtered_groups = [g for g in res["groups"] if g["group"] in user_groups]
        res["groups"] = filtered_groups
        res["groupsWithoutAccess"] = groups_without_access

        # Map of approval requirements for every group function and region combination
        res["accessMap"] = {
            g["group"]: {
                f["name"]: {
                    r: app_config.approvals_policy.requires_approval(
                        g["group"], f, [r]
                    ).value
                    for r in res["regions"]
                }
                for f in g["functions"]
            }
            for g in filtered_groups
        }

        return make_response(jsonify(res), 200)

    @main_config_bp.route("/requests", methods=["GET"])
    def fetch_approval_requests() -> Response:
        """
        Fetch execution requests for the user's groups which
        are approved or pending approval.
        """
        raise NotImplementedError

    @main_config_bp.route("/requests", methods=["POST"])
    @authenticate_request(app_config)
    def request_approval() -> Response:
        raise NotImplementedError

    @main_config_bp.route("/requests/{request_id}/approve", methods=["POST"])
    @authenticate_request(app_config)
    def approve_request() -> Response:
        raise NotImplementedError

    @main_config_bp.route("/requests/{request_id}/cancel", methods=["POST"])
    @authenticate_request(app_config)
    def cancel_request() -> Response:
        raise NotImplementedError

    @main_config_bp.route("/requests/{request_id}/run", methods=["POST"])
    @authenticate_request(app_config)
    def execute_request() -> Response:
        """
        execute an approved request.
        """
        raise NotImplementedError

    return main_config_bp
