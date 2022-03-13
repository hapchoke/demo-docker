from .models import Category

def common(request):
    category=Category.objects.all()
    context={
    'category':category
    }
    return context