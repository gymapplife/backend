from rest_framework.serializers import ValidationError


def get_query_switches(
    query_params,
    switches,
    raise_on_none=False,
    all_true_on_none=False,
):
    active_switches = set()

    if query_params:
        for switch in switches:
            if switch in query_params:
                value = query_params[switch]
                if value == '' or value == '1':
                    active_switches.add(switch)

    if not active_switches:
        if raise_on_none:
            msg = f'Need at least one active query parameter: {switches}'
            raise ValidationError({'detail': msg})
        if all_true_on_none:
            return set(switches)

    return active_switches
