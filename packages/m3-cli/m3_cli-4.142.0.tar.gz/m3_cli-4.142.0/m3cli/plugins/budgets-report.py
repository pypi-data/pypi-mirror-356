"""
The custom logic for the command m3 budgets-report
This logic is created to convert parameters from the Human readable format to
appropriate for M3 SDK API request.
"""
import json
import datetime

from m3cli.services.request_service import BaseRequest


def compute_month_epoch_ms(year, month):
    return int(
        datetime.datetime(
            year, month, 1, tzinfo=datetime.timezone.utc).timestamp()
    ) * 1000


def create_custom_request(request: BaseRequest) -> BaseRequest:
    params = request.parameters
    if not params.get('criteria'):
        params['criteria'] = 'ALL'
    params['tenantNames'] = [params.pop('tenantGroup')]
    if 'region' in params:
        params['regionName'] = params.pop('region')
    return request


def create_custom_response(
        request: BaseRequest,
        response,
        view_type: str,
):
    try:
        response = json.loads(response)
    except json.decoder.JSONDecodeError:
        return response
    if isinstance(response, dict) and response.get('message') \
            and response.get('s3ReportLink'):
        return f"{response.get('message')} Link: `{response.get('s3ReportLink')}`"

    if view_type == 'table':
        params = getattr(request, 'parameters', None)
        year = \
            int(params.get('year')) if params and params.get('year') else None
        month = \
            int(params.get('month')) if params and params.get('month') else None
        month_epoch_ms = \
            compute_month_epoch_ms(year, month) if year and month else None

        table_rows = []
        for item in response:
            # Find the usage for the requested month
            month_usages = item.get('monthUsages', [])
            month_usage = None
            if month_epoch_ms:
                for usage in month_usages:
                    if int(usage.get("month", 0)) == month_epoch_ms:
                        month_usage = usage
                        break

            # If nothing found, set fields to 'No data to show'
            if month_usage:
                percent_used = month_usage.get('percentUsed')
                utilization = ""
                if percent_used is not None:
                    utilization = \
                        "less than 1%" if percent_used < 1 else f"{percent_used}"
                monthly_budget = month_usage.get("value")
                current_chargeback = month_usage.get("used")
            else:
                utilization = monthly_budget = current_chargeback = ''

            thresholds = item.get('thresholds', [])
            actions = item.get('actions', [])
            threshold_strs = [
                f"{int(th['value'])} %" for th in thresholds if 'value' in th
            ]
            action_plan = None
            if thresholds:
                action_plan = f"Notify on ({', '.join(threshold_strs)})"
                show_action_plan = [a for a in actions if a != 'NOTHING']
                if show_action_plan:
                    action_plan += ", " + ", ".join(show_action_plan)

            row = {
                "tenant": item.get("tenantDisplayName", ""),
                "type": item.get("type", ""),
                "monthlyBudget": monthly_budget,
                "currentChargeback": current_chargeback,
                "utilization": utilization,
                "status": "enabled" if item.get("active") else "disabled",
                "tag": item.get("tag", ""),
                "affectedRegions": item.get("regionName", "")
            }
            if action_plan:
                row["actionPlan"] = action_plan
            table_rows.append(row)
        return sorted(table_rows, key=lambda row: str(row.get('type', '')).upper())

    return response
