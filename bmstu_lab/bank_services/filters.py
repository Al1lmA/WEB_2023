def StatusFilter(objects, request):
    if request.query_params.get('status'):
        return objects.filter(request_status=request.query_params.get('status'))
    return objects

def DateFilter(objects, request):
    highest_date = "3000-01-01"
    lowest_date = "2000-01-01"
    if request.query_params.get('lowest_date'):
        lowest_date = request.query_params.get('lowest_date')
    if request.query_params.get('highest_date'):
        highest_date = request.query_params.get('highest_date')
    return objects.filter(creation_date__range=[lowest_date, highest_date])

def RequestsFilter(objects, request):
    return DateFilter(StatusFilter(objects,request),request)

# def FinesFilter(objects, request):
#     if request.query_params.get('title'):
#         return objects.filter(title__icontains=request.query_params.get('title'))
#     return objects