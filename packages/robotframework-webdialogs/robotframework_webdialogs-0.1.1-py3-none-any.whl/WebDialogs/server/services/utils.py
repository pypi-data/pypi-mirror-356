def __get_all_values_from_form(request):
    data = {}

    for key in request.form:
        values = request.form.getlist(key)
        data[key] = values if len(values) > 1 else values[0]

    return data
