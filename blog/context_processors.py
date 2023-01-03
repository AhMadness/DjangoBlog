from .models import BlogPost

def add_variable_to_context(request):
    all_categories = {item[0]:item[1] for item in BlogPost.choices}
    return {"all_categories": all_categories}